import cv2
import mediapipe as mp
import time # Pour les fps
import os
from dotenv import load_dotenv


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        # Création d'un objet de la classe Hands
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
    
    def findHands(self, img, draw=True):
        # ici c'est pour convertir l'image en RGB pour que Mediapipe puisse la traiter
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # process() est la fonction qui va nous permettre de traiter l'image 
        self.results = self.hands.process(imgRGB)
          # Savoir combien de mains sont détectées
        # ici je teste si une main est détectée
        #print(results.multi_hand_landmarks)
        if(self.results.multi_hand_landmarks):
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def trouverPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            if len(self.results.multi_hand_landmarks) > handNo:
                handLms = self.results.multi_hand_landmarks[handNo]
                # recupérer les coordonnées de chaque landmark
                for id, lm in enumerate(handLms.landmark):
                    #print(id, lm)
                    ih, iw, ic = img.shape
                    x, y = int(lm.x*iw), int(lm.y*ih)
                    #print(id, x, y) # connaître les coordonnées de chaque landmark grace a l'id
                    lmList.append([id, x, y])
                    if draw and id == 0:
                        cv2.circle(img, (x, y), 15, (0, 0, 255), cv2.FILLED)
        return lmList
    
    
def main():
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

    detector = handDetector()
    while True:
        success, img = cap.read()
        
        img = detector.findHands(img)
        detector.trouverPosition(img)
        
        # Pour les fps
        current_time = time.time()
        fps = 1/(current_time - previous_time)
        previous_time = current_time
        
        cv2.putText(img, f"FPS : {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()