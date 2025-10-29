import cv2
import numpy as np

# Charger et convertir l'image
img_bgr = cv2.imread("P:\\MEA4\\Perception\\python\\balle_small.jpg")
img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

# Sauvegarde pour réinitialisation
original_bgr = img_bgr.copy()
original_hsv = img_hsv.copy()

# Paramètres
tolerance_H = 5
new_color_bgr = [0, 255, 0]  # Vert

# Callback souris
def changer_couleur(event, x, y, flags, param):
    global img_bgr, img_hsv

    if event == cv2.EVENT_LBUTTONDOWN:
        # Récupérer la teinte H
        h_value = int(img_hsv[y, x, 0])
        print(f"Teinte sélectionnée : {h_value}")

        # Extraire uniquement le canal H
        h_channel = img_hsv[:, :, 0]

        # Créer un masque pour H dans la tolérance
        lower_H = (h_value - tolerance_H) % 180
        upper_H = (h_value + tolerance_H) % 180

        if lower_H < upper_H:
            mask = (h_channel >= lower_H) & (h_channel <= upper_H)
        else:
            # cas où on dépasse 180 et on doit "boucler"
            mask = (h_channel >= lower_H) | (h_channel <= upper_H)

        # Appliquer la nouvelle couleur uniquement aux pixels du masque
        img_bgr[mask] = new_color_bgr

# Fenêtre
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image', changer_couleur)

# Boucle principale
while True:
    cv2.imshow('image', img_bgr)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('s'):
        cv2.imwrite("P:\\MEA4\\Perception\\python\\screen_tp1_ex2.jpg", img_bgr)
        print("Image sauvegardée sous 'screen_tp1_ex2.jpg'")

cv2.destroyAllWindows()
