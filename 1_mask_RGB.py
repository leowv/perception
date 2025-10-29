import cv2
import numpy as np

# Charger l'image
img = cv2.imread("P:\\MEA4\\Perception\\python\\balle_small.jpg")
original_img = img.copy()  # Garder une copie originale
target_color = None        # Couleur sélectionnée
new_color = [0, 0, 255]    # Vert
tolerance = 40

# Fonction de callback pour la souris
def changer_couleur(event, x, y, flags, param):
    global target_color, img

    if event == cv2.EVENT_LBUTTONDOWN:
        # Récupérer la couleur du pixel cliqué
        target_color = img[y, x].tolist()
        print(f"Couleur sélectionnée : {target_color}")

        # Définir la plage de tolérance autour de la couleur sélectionnée
        lower = np.array([max(0, c - tolerance) for c in target_color], dtype=np.uint8)
        upper = np.array([min(255, c + tolerance) for c in target_color], dtype=np.uint8)
        # Créer un masque pour tous les pixels dans cette plage de couleurs
        mask = cv2.inRange(img, lower, upper)
        # Appliquer la nouvelle couleur à tous les pixels sélectionnés
        img[mask == 255] = new_color

# Affichage de l'image avec la gestion des clics
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image', changer_couleur)

while True:
    cv2.imshow('image', img)
    key = cv2.waitKey(1) & 0xFF

    # Appuyer sur 'r' pour réinitialiser l'image
    if key == ord('r'):
        img = original_img.copy()
    # Appuyer sur 's' pour sauvegarder l'image
    elif key == ord('s'):
        cv2.imwrite("P:\\MEA4\\Perception\\python\\screen_tp1.jpg", img)
        print("Image sauvegardée sous 'screen_tp1.jpg'")
    # Appuyer sur 'q' pour quitter
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
