# Gesture-Midi
A real-time, Python-based gesture recognition system that maps hand movements to MIDI output. Built with OpenCV and MediaPipe, it enables expressive musical control through different hand gestures.


## Features

- OK gesture → CC1, controlled by thumb Z-depth
- Palm gesture → CC2, controlled by middle fingertip Z-depth
- Point-up gesture → CC3, controlled by index fingertip Z-depth
- Fist gesture → Resets all CC values to 0
- Real-time feedback via webcam overlay



## Requirements

- Python 3.9+
- [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) — used to create a virtual MIDI output port

Install dependencies:

```bash
pip install -r requirements.txt
```


## Getting Started

1. **Install loopMIDI**

   * Download and install from [here](https://www.tobias-erichsen.de/software/loopmidi.html)
   * Create a virtual MIDI port and name it (e.g., `GestureMidi`)
   * Ensure your DAW (e.g., Ableton Live) is set to receive MIDI from this port

2. **Run the program**

```bash
python main.py
```

3. **Test your gestures**

   * Use hand gestures in front of your webcam (you should see the midi cc values in your terminal)
   * You can verify port names using `print(mido.get_output_names())` in the script


## Notes

* MediaPipe depth values (`landmark.z`) may vary depending on your webcam and lighting conditions. You can adjust `NEAR_LIMIT` and `FAR_LIMIT` values in `main.py` for better responsiveness.
* The program is optimized for one hand at a time (for now), visible clearly in the camera frame.


## Future Plans

* Add gesture-based MIDI note triggering
* Implement GUI controls for selecting CC assignments
* Implement better smoothing for all CC values
* VST or standalone app packaging


## Developed On

* Windows 10
* Python 3.9
* loopMIDI and Ableton Live
* OpenCV and MediaPipe
