import cv2
import numpy as np


# Funkcja do nic nie robienia dla trackbara
def nothing(x):
    pass




# Główna funkcja do przechwytywania obrazu i kalibracji kolorów
def main():
    # Przechwycenie obrazu z kamerki
    cap = cv2.VideoCapture(0)

    # Tworzenie okien z suwakami do kalibracji
    cv2.namedWindow('Kalibracja')
    cv2.createTrackbar('Low H', 'Kalibracja', 0, 179, nothing)
    cv2.createTrackbar('High H', 'Kalibracja', 179, 179, nothing)
    cv2.createTrackbar('Low S', 'Kalibracja', 0, 255, nothing)
    cv2.createTrackbar('High S', 'Kalibracja', 255, 255, nothing)
    cv2.createTrackbar('Low V', 'Kalibracja', 0, 255, nothing)
    cv2.createTrackbar('High V', 'Kalibracja', 255, 255, nothing)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Konwersja obrazu do HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Odczyt wartości z suwaków
        low_h = cv2.getTrackbarPos('Low H', 'Kalibracja')
        high_h = cv2.getTrackbarPos('High H', 'Kalibracja')
        low_s = cv2.getTrackbarPos('Low S', 'Kalibracja')
        high_s = cv2.getTrackbarPos('High S', 'Kalibracja')
        low_v = cv2.getTrackbarPos('Low V', 'Kalibracja')
        high_v = cv2.getTrackbarPos('High V', 'Kalibracja')

        # Definiowanie dolnego i górnego zakresu dla maski HSV
        lower_bound = np.array([low_h, low_s, low_v])
        upper_bound = np.array([high_h, high_s, high_v])

        # Tworzenie maski na podstawie suwaków
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        # Zastosowanie maski na obraz
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # Wyświetlenie oryginalnego obrazu oraz wyniku
        cv2.imshow('Kamera', frame)
        cv2.imshow('Maska', mask)
        cv2.imshow('Wynik', result)

        # Wyjście z programu po wciśnięciu 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
