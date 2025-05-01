import cv2
import mediapipe as mp
from gesture_detector import is_fist, is_ok, is_palm, is_point_up
import mido

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
outport = mido.open_output('GestureMidi 2')    ## Replace GestureMidi 2 with your virtual midi out port made in loopmidi
                                               ## use print(mido.get_output_names()) to find the name of your port

FINGER_TIPS = [4, 8, 12, 16, 20]
FINGER_NAMES = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8) as hands:

    prev_finger_states = None
    prev_hand_states = None
    last_cc_value = 0
    lastz = 0
    cc_val1 = 0
    cc_val2 = 0
    cc_val3=0

    while True:
        success, frame = cap.read()
        if not success:
            print("Warning: empty frame")
            continue

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                landmarks = hand_landmarks.landmark
                finger_states = []
                for i, tip_id in enumerate(FINGER_TIPS):
                    tip = landmarks[tip_id]
                    lower = landmarks[tip_id - 2]

                    if i == 0:  # Thumb case
                        wrist = landmarks[0]
                        thumb_tucked = abs(tip.x - wrist.x) < 0.1
                        finger_states.append(not thumb_tucked)
                    else:
                        is_up = tip.y < lower.y
                        finger_states.append(is_up)

                fist = is_fist(finger_states)
                OK = is_ok(finger_states, landmarks)
                palm = is_palm(finger_states)
                pointup=is_point_up(finger_states)

                hand_states = [fist, OK, palm]
                z = landmarks[4].z

                # Print state if changed
                if finger_states != prev_finger_states or hand_states != prev_hand_states or z != lastz:
                    """print("\nFinger states:")
                    for name, state in zip(FINGER_NAMES, finger_states):
                        if name == "Thumb":
                            print(f"Thumb: {'Up' if state else 'Tucked'}")
                        else:
                            print(f"{name}: {'UP' if state else 'DOWN'}")
                    if fist:
                        print("\nFist detected")
                    if OK:
                        print("\nOK detected")
                    if palm:
                        print("\nPalm detected") """

                    prev_finger_states = finger_states
                    prev_hand_states = hand_states
                    lastz = z

                if OK:
                    z = landmarks[4].z
                    NEAR_LIMIT = -0.05
                    FAR_LIMIT = 0.05
                    if z < NEAR_LIMIT:
                        cc_val1 = 127
                    elif z > FAR_LIMIT:
                        cc_val1 = 0
                    else:
                        norm = (z - FAR_LIMIT) / (NEAR_LIMIT - FAR_LIMIT)
                        cc_val1 = int(norm * 127)
                    cc_val1 = max(0, min(127, cc_val1))
                    outport.send(mido.Message('control_change', control=1, value=cc_val1))
                    print(f"👌 CC val1: {cc_val1}")

                elif palm:
                    zpalm = landmarks[12].z
                    PALM_NEAR_LIMIT = -0.1
                    PALM_FAR_LIMIT = 0
                    if zpalm < PALM_NEAR_LIMIT:
                        cc_val2 = 127
                    elif zpalm > PALM_FAR_LIMIT:
                        cc_val2 = 0
                    else:
                        norm = (zpalm - PALM_FAR_LIMIT) / (PALM_NEAR_LIMIT - PALM_FAR_LIMIT)
                        cc_val2 = int(norm * 127)
                    cc_val2 = max(0, min(127, cc_val2))
                    outport.send(mido.Message('control_change', control=2, value=cc_val2))
                    print(f"✋CC value: {cc_val2}")
                elif pointup:
                    z = landmarks[8].z
                    NEAR_LIMIT = -0.1
                    FAR_LIMIT = 0
                    if z < NEAR_LIMIT:
                        cc_val3 = 127
                    elif z > FAR_LIMIT:
                        cc_val3 = 0
                    else:
                        norm = (z - FAR_LIMIT) / (NEAR_LIMIT - FAR_LIMIT)
                        cc_val3 = int(norm * 127)
                    cc_val3 = max(0, min(127, cc_val3))
                    outport.send(mido.Message('control_change', control=3, value=cc_val3))
                    print(f"☝️ CC val3: {cc_val3}")


                elif fist:
                    cc_val1=0
                    cc_val2=0
                    cc_val3=0
                    outport.send(mido.Message('control_change', control=1, value=cc_val1))
                    outport.send(mido.Message('control_change', control=2, value=cc_val2))
                    outport.send(mido.Message('control_change', control=3, value=cc_val3))
                    print("👊")
                

        cv2.imshow('Gesture MIDI - Webcam Feed', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
