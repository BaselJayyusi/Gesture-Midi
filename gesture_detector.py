from typing import List
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmark
FINGER_NAMES = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']

def is_fist(finger_states: list[bool]) -> bool:

    return not any(finger_states)

def is_ok(finger_states: list[bool], landmarks: list[NormalizedLandmark]) -> bool:

    thumbX=landmarks[4].x
    indexX=landmarks[8].x
    thumbY=landmarks[4].y
    indexY=landmarks[8].y
    dist=((thumbX-indexX)**2+(thumbY-indexY)**2)**0.5

    return all(finger_states[2:]) and dist<0.05

def is_point_up(finger_states: list[bool]) -> bool:

    return finger_states[1] and not finger_states[0] and not any(finger_states[2:])
    



def is_palm(finger_states: list[bool]) -> bool:

    return all(finger_states)
