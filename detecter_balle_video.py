import cv2
import numpy as np

# === PARAMÈTRES ===
video_path = r"P:\MEA4\Perception\python\balle.mp4"
tolerance_H = 10
new_color_bgr = [0, 255, 0]  # Vert
teinte_cible = 30  # À ajuster selon la couleur de la balle (jaune ~30, rouge ~179, vert ~60)

# === FONCTIONS ===
def detecter_cercles(img_gray):
    circles = cv2.HoughCircles(
        img_gray,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=80,
        param1=100,
        param2=60,
        minRadius=50,
        maxRadius=300
    )
    return circles


def generer_masque_teinte(img_hsv, h_value, tolerance=10):
    h_channel = img_hsv[:, :, 0]
    s_channel = img_hsv[:, :, 1]
    v_channel = img_hsv[:, :, 2]

    lower_H = (h_value - tolerance) % 180
    upper_H = (h_value + tolerance) % 180

    # Masque sur la teinte uniquement
    if lower_H < upper_H:
        hue_mask = (h_channel >= lower_H) & (h_channel <= upper_H)
    else:
        hue_mask = (h_channel >= lower_H) | (h_channel <= upper_H)

    # Conditions supplémentaires pour éviter zones sombres
    saturation_thresh = s_channel > 50
    value_thresh = v_channel > 50

    hue_mask = hue_mask & saturation_thresh & value_thresh

    # Post-traitement (ouverture morphologique)
    kernel = np.ones((5, 5), np.uint8)
    hue_mask = hue_mask.astype(np.uint8) * 255
    hue_mask = cv2.morphologyEx(hue_mask, cv2.MORPH_OPEN, kernel)

    return hue_mask


# === OUVERTURE VIDÉO ===
capture = cv2.VideoCapture(video_path)

if not capture.isOpened():
    print("Erreur : impossible d'ouvrir le fichier vidéo.")
    exit()

while capture.isOpened():
    ret, frame = capture.read()
    if not ret:
        break

    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hue_mask = generer_masque_teinte(img_hsv, teinte_cible, tolerance_H)

    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.medianBlur(img_gray, 5)

    circles = detecter_cercles(img_blur)

    circle_mask = np.zeros(img_gray.shape, dtype=np.uint8)
    centers = []

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(circle_mask, (i[0], i[1]), i[2], 255, -1)
            centers.append((i[0], i[1], i[2]))

    combined_mask = (hue_mask > 0) & (circle_mask > 0)

    # Coloration des pixels détectés
    frame[combined_mask] = new_color_bgr

    # Affichage des cercles
    for cx, cy, r in centers:
        cv2.circle(frame, (cx, cy), r, (0, 0, 255), 2)
        cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

    # Affichage
    cv2.imshow('Détection balle dans vidéo', frame)

    if cv2.waitKey(25) == 27:  # ESC
        break

capture.release()
cv2.destroyAllWindows()
