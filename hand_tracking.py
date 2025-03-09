import cv2
import mediapipe as mp
import time # Pour les fps
import os
from dotenv import load_dotenv

load_dotenv()
ip_address = os.getenv('WEBCAM_IP')

# Je travaille sur wsl donc je dois utiliser l'adresse IP de ma machine Windows
# pour accéder à la webcam de ma machine Windows
# Pour cela, j'ai utilisé mjpeg-streamer pour diffuser le flux vidéo de ma webcam
# sur un port spécifique.
# Utilisez l'URL du flux vidéo diffusé par mjpeg-streamer avec l'adresse IP de votre machine Windows
cap = cv2.VideoCapture(f"http://{ip_address}:8000/?action=stream")

if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir le flux vidéo")
    exit()

# Création d'un objet de la classe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    
    # ici c'est pour convertir l'image en RGB pour que Mediapipe puisse la traiter
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # process() est la fonction qui va nous permettre de traiter l'image 
    results = hands.process(imgRGB)
    
    # Savoir combien de mains sont détectées
    
    # ici je teste si une main est détectée
    #print(results.multi_hand_landmarks)
    if(results.multi_hand_landmarks):
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)