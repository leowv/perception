import cv2
import numpy as np

# Charger l'image
img_bgr = cv2.imread("D:\\polytech mtp\\Prception\\balle_small.jpg")
# Convertir l'image en HSV
img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

# Copies originales
original_bgr = img_bgr.copy()
original_hsv = img_hsv.copy()

# Paramètres
tolerance_H = 10
new_color_bgr = [0, 255, 0]  # Vert

# # Détection de cercles (HoughCircles)
# def detecter_cercles(img_gray):
#     # HoughCircles travaille sur des images en niveaux de gris
#     circles = cv2.HoughCircles(
#         img_gray,
#         cv2.HOUGH_GRADIENT, # Méthode de détection
#         dp=1.2,
#         minDist=100,         # Distance minimale entre les centres des cercles détectés
#         param1=50,           # Seuillage du gradient
#         param2=50,           # Seuillage pour la détection des cercles (plus bas = plus sensible)
#         minRadius=50,
#         maxRadius=150
#     )
#     return circles

# Callback souris
def changer_couleur(event, x, y, flags, param):
    global img_bgr, img_hsv

    if event == cv2.EVENT_LBUTTONDOWN:
        # 1. Récupérer la teinte (H)
        h_value = int(img_hsv[y, x, 0])
        print(f"Teinte cliquée : {h_value}")

        #création mask basé sur H
        h_channel = img_hsv[:, :, 0]
        # Calcul de la plage
        lower_H = (h_value - tolerance_H) % 180
        upper_H = (h_value + tolerance_H) % 180

        # Gestion du cas où la plage H "déborde" autour de 0
        if lower_H < upper_H:
            hue_mask = (h_channel >= lower_H) & (h_channel <= upper_H)
        else:
            hue_mask = (h_channel >= lower_H) | (h_channel <= upper_H)

        # Convertir le masque en uint8 pour l'ouverture
        hue_mask_uint8 = hue_mask.astype(np.uint8) * 255

        # ouverture
        kernel = np.ones((5, 5), np.uint8)
        mask_eroded = cv2.erode(hue_mask_uint8, kernel, iterations=1)
        mask_dilated = cv2.dilate(mask_eroded, kernel, iterations=1)

        # colorier les pixels sélectionnés
        img_bgr[mask_dilated > 0] = new_color_bgr

        # # 2. Détection de cercles
        # img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        # img_blur = cv2.medianBlur(img_gray, 5)
        # circles = detecter_cercles(img_blur)

        # # 3. Créer un masque vide de même taille que l'image pour y dessiner les cercles détectés
        # circle_mask = np.zeros(h_channel.shape, dtype=np.uint8)

        # # Si des cercles sont détectés
        # if circles is not None:
        #     circles = np.uint16(np.around(circles))
        #     for i in circles[0, :]:
        #         center = (i[0], i[1])
        #         radius = i[2]
        #         # Dessiner les cercles sur l'image originale
        #         cv2.circle(img_bgr, center, radius, (0, 0, 255), 3)  # Rouge
        
        # (Optionnel) Affichage pour debug
        cv2.imshow("Masque HSV", hue_mask_uint8)
        cv2.imshow("Après morphologie", mask_dilated)

        # 4. Combiner les deux masques (HUE et cercle)
        # combined_mask = mask_dilated & (circle_mask > 0)

        # 5. convertir masque en uint8


        # 5. Colorier la zone sélectionnée
        #img_bgr[combined_mask] = new_color_bgr



# Fenêtre et boucle
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image', changer_couleur)

while True:
    cv2.imshow('image', img_bgr)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('r'):
        img_bgr = original_bgr.copy()
        img_hsv = original_hsv.copy()
        print("Image réinitialisée.")
    elif key == ord('q'):
        break
    elif key == ord('s'):
        cv2.imwrite("P:\\MEA4\\Perception\\python\\screen_tp1_ex3.jpg", img_bgr)
        print("Image sauvegardée sous 'screen_tp1_ex3.jpg'")


cv2.destroyAllWindows()
