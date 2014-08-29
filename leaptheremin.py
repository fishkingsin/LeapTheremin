#!/usr/bin/python
import sys
import Leap
from Tone import Tone

class ThereminListener(Leap.Listener):
	def __init__(self, tone = None):
		Leap.Listener.__init__(self)
		self.tone = tone

	def on_init(self, controller):
		print "Initialized"

	def on_connect(self, controller):
		print "Connected"

		# Enable gestures
		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_disconnect(self, controller):
		# Note: not dispatched when running in a debugger.
		print "Disconnected"

	def on_exit(self, controller):
		print "Exited"
	def on_frame(self, controller):
		# Get the most recent frame and report some basic information
		frame = controller.frame()
		# print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
			  # frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
		if frame.hands.is_empty:
			self.tone.setAmplitude(0)
		else:
			# Get the first hand
			hand = frame.hands[0]

			amp = hand.sphere_radius / 100 + 0.5
			# amp = 1.5 - abs(hand.palm_position[1]) / 200
			if amp > 1.0:
				amp = 1.0
			if amp < 0:
				amp = 0
			freq = 220 * (2 ** (abs(hand.palm_position[0] + 200) / 200)) 
			self.tone.setAmplitude(amp)
			self.tone.setFrequency(freq)
	def state_string(self, state):
		if state == Leap.Gesture.STATE_START:
			return "STATE_START"

		if state == Leap.Gesture.STATE_UPDATE:
			return "STATE_UPDATE"

		if state == Leap.Gesture.STATE_STOP:
			return "STATE_STOP"

		if state == Leap.Gesture.STATE_INVALID:
			return "STATE_INVALID"
def main():
	t = Tone()
	t.open()
	t.setAmplitude(0)
	t.start()

	# Create a sample listener and controller
	listener = ThereminListener(t)
	controller = Leap.Controller()

	# Have the sample listener receive events from the controller
	controller.add_listener(listener)

	# Keep this process running until Enter is pressed
	print "Press Enter to quit..."
	sys.stdin.readline()

	# Remove the sample listener when done
	controller.remove_listener(listener)

	t.stop()
	t.close()

if __name__ == "__main__":
	main()
