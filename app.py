import cv2
import serial
import time

# Inisialisasi komunikasi serial dengan Arduino
arduino = serial.Serial('COM3', 9600, timeout=1)  # Sesuaikan 'COM3' dengan port Arduino
time.sleep(2)  # Tunggu beberapa detik agar komunikasi serial siap

# Inisialisasi deteksi wajah dan hidung
faceCascade = cv2.CascadeClassifier("asset/haarcascade_frontalface_default.xml")
noseCascade = cv2.CascadeClassifier("asset/Nariz.xml")
 
video_capture = cv2.VideoCapture(0)
mask_on = False

while True:
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    wajah = faceCascade.detectMultiScale(gray, 1.1, 5)

    for (x, y, w, h) in wajah:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Komunikasi dengan Arduino
        if mask_on:
            arduino.write(b'1')  # Kirim sinyal '1' jika masker terdeteksi (LED hijau ON, LED merah OFF, buzzer OFF)
            cv2.rectangle(frame, (x, y - 50), (x + w, y), (0, 255, 0), -1)
            text = 'Mask On'
        else:
            arduino.write(b'0')  # Kirim sinyal '0' jika tidak ada masker (LED hijau OFF, LED merah ON, buzzer ON)
            cv2.rectangle(frame, (x, y - 50), (x + w, y), (0, 0, 255), -1)
            text = 'Mask Off'

        size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 3)[0]
        f = x + (w - size[0]) // 2
        c = y - 15
        cv2.putText(frame, text, (f, c), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0) if mask_on else (0, 0, 255), 3)


        # Pendeteksian hidung
        hidung = noseCascade.detectMultiScale(roi_gray, 1.18, 35)
        for (sx, sy, sw, sh) in hidung:
            cv2.rectangle(roi_color, (sx, sy), (sx + sw, sy + sh), (255, 0, 0), 2)
            cv2.putText(frame, 'Hidung', (x + sx, y + sy), 1, 1, (0, 255, 0), 1)

        mask_on = len(hidung) == 0  # Jika tidak ada hidung terdeteksi, berarti masker sedang dipakai

    # Jumlah wajah terdeteksi
    wajah_text = 'Jumlah Wajah : ' + str(len(wajah))
    size = cv2.getTextSize(wajah_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    cv2.rectangle(frame, (20, 10), (20 + size[0] + 20, 40 + size[1]), (0, 0, 0), -1)
    cv2.putText(frame, wajah_text, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Tekan tombol 'q' untuk keluar
        break

video_capture.release()
cv2.destroyAllWindows()
arduino.close()  # Tutup komunikasi serial
