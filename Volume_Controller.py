import cv2
import mediapipe as mp
import time # Pour les fps
import os
from dotenv import load_dotenv
import hand_tracking_module as hd
import math 
import numpy as np


env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path, override=True)
ip_address = os.getenv('WEBCAM_IP')
print(f"Adresse IP chargée : {ip_address}")

# Je travaille sur wsl donc je dois utiliser l'adresse IP de ma machine Windows
# pour accéder à la webcam de ma machine Windows
# Pour cela, j'ai utilisé mjpeg-streamer pour diffuser le flux vidéo de ma webcam
# sur un port spécifique.
# Utilisez l'URL du flux vidéo diffusé par mjpeg-streamer avec l'adresse IP de votre machine Windows
cap = cv2.VideoCapture(f"http://{ip_address}:8000/?action=stream")

if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir le flux vidéo")
    exit()
    
# Pour les fps
previous_time = 0
current_time = 0

detector = hd.handDetector(detectionCon=0.7, maxHands=1)
while True:
    success, img = cap.read()
    
    img = detector.findHands(img)
    findHands = detector.trouverPosition(img, draw=False)
    # On dois trouver le landmark de l'index et du pouce
    # Regardons la documentation https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker?hl=fr
    # 4 Pour le pouce et 8 pour l'index
    if len(findHands) > 0:
        print(findHands[4], findHands[8])
        centre = (findHands[4][1] + findHands[8][1]) // 2, (findHands[4][2] + findHands[8][2]) // 2
        cv2.circle(img, centre, 20, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (findHands[4][1], findHands[4][2]), 20, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (findHands[8][1], findHands[8][2]), 20, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (findHands[4][1], findHands[4][2]), (findHands[8][1], findHands[8][2]), (255, 0, 0), 3)
        
        # Trouver la longeur de la ligne 
        length = math.hypot(findHands[4][1] - findHands[8][1], findHands[4][2] - findHands[8][2])
        print(length)
        
        # On travaille avec python donc il doit bien y'avoir une librairie pour faire le calcul du volume 
        # Trouver pycaw suuuuu
        # Python et WSL c'est pas ouf bon dans la theorie c'est comme ca qu'il faut faire 
        vol = np.interp(length, [50, 300], [0, 1])
        
        # Sur Windows j'ai cree un script pour controler le volume
        # os.system(f"python.exe /mnt/c/*******/volume_control.py {volume_float}")

        
    else:
        print("Aucune main détectée")
        

    
    
    # Pour les fps
    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time
    
    cv2.putText(img, f"FPS : {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
