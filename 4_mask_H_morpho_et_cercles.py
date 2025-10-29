import cv2
import numpy as np

# Charger l'image
img_bgr = cv2.imread("P:\\MEA4\\Perception\\python\\balle_small.jpg")
# Convertir l'image en HSV
img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

# Copies originales
original_bgr = img_bgr.copy()
original_hsv = img_hsv.copy()

# Paramètres
tolerance_H = 10
new_color_bgr = [0, 255, 0]  # Vert

# Détection de cercles (HoughCircles)
def detecter_cercles(img_gray):
    circles = cv2.HoughCircles(
        img_gray,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=80,
        param1=100,
        param2=60,
        minRadius=50,
        maxRadius=150
    )
    return circles


def afficher_image_redim(name, img, scale=0.6):
    h, w = img.shape[:2]
    img_resized = cv2.resize(img, (int(w * scale), int(h * scale)))
    cv2.imshow(name, img_resized)

# Callback souris
def changer_couleur(event, x, y, flags, param):
    global img_bgr, img_hsv

    if event == cv2.EVENT_LBUTTONDOWN:
        h_value = int(img_hsv[y, x, 0])
        print(f"Teinte cliquée : {h_value}")

        h_channel = img_hsv[:, :, 0]
        lower_H = (h_value - tolerance_H) % 180
        upper_H = (h_value + tolerance_H) % 180

        if lower_H < upper_H:
            hue_mask = (h_channel >= lower_H) & (h_channel <= upper_H)
        else:
            hue_mask = (h_channel >= lower_H) | (h_channel <= upper_H)

        afficher_image_redim("Hue Mask - Brut", hue_mask.astype(np.uint8) * 255)

        kernel = np.ones((5, 5), np.uint8)
        hue_mask = hue_mask.astype(np.uint8) * 255
        hue_mask = cv2.morphologyEx(hue_mask, cv2.MORPH_OPEN, kernel)

        afficher_image_redim("Hue Mask - Apres ouverture", hue_mask)


        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        afficher_image_redim("Image Grise", img_gray)

        img_blur = cv2.medianBlur(img_gray, 5)
        afficher_image_redim("Image Floutee", img_blur)

        circles = detecter_cercles(img_blur)

        circle_mask = np.zeros(h_channel.shape, dtype=np.uint8)
        centers = []

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                cv2.circle(circle_mask, (i[0], i[1]), i[2], 255, -1)
                centers.append((i[0], i[1], i[2]))

        afficher_image_redim("Masque Cercles", circle_mask)

        combined_mask = (hue_mask > 0) & (circle_mask > 0)

        afficher_image_redim("Masque Combine", combined_mask.astype(np.uint8) * 255)

        img_bgr[combined_mask] = new_color_bgr

        for cx, cy, r in centers:
            cv2.circle(img_bgr, (cx, cy), r, (0, 0, 255), 2)
            cv2.circle(img_bgr, (cx, cy), 5, (255, 0, 0), -1)





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
        cv2.imwrite("P:\\MEA4\\Perception\\python\\screen_tp1_ex3bis.jpg", img_bgr)
        print("Image sauvegardée sous 'screen_tp1_ex3bis.jpg'")

cv2.destroyAllWindows()
