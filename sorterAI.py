import cv2
import serial
import time
from ultralytics import YOLO

PORT_ARDUINO = 'COM5' 
WIRTUALNA_LINIA_Y = 320
STREFA_DETEKCJI = 50      
OPOZNIENIE_ZAPOBIEGAJACE_SPAMOWI = 2.0 

try:
    print(f"Łączenie z Arduino na porcie {PORT_ARDUINO}...")
    arduino = serial.Serial(PORT_ARDUINO, 9600, timeout=1)
    time.sleep(2) 
    print("Połączono z Arduino!")
except:
    print("BŁĄD: Nie można połączyć z Arduino. Czy na pewno dobry port?")
    exit()

model = YOLO('best.pt') 
cap = cv2.VideoCapture(1)

ostatni_czas_wyslania = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    results = model(frame, conf=0.5) 
    
    cv2.line(frame, (0, WIRTUALNA_LINIA_Y), (1000, WIRTUALNA_LINIA_Y), (255, 0, 0), 3)
    cv2.line(frame, (0, WIRTUALNA_LINIA_Y - STREFA_DETEKCJI), (1000, WIRTUALNA_LINIA_Y - STREFA_DETEKCJI), (0, 255, 0), 2)
    cv2.line(frame, (0, WIRTUALNA_LINIA_Y + STREFA_DETEKCJI), (1000, WIRTUALNA_LINIA_Y + STREFA_DETEKCJI), (0, 255, 0), 2)

    for box in results[0].boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        
        x_center, y_center, w, h = map(int, box.xywh[0])
        
        print(f"Widzę: {class_name} na Y = {y_center} (Linia jest na: {WIRTUALNA_LINIA_Y})")
        
        aktualny_czas = time.time()
        
        if abs(y_center - WIRTUALNA_LINIA_Y) < STREFA_DETEKCJI:
            
            if (aktualny_czas - ostatni_czas_wyslania) > OPOZNIENIE_ZAPOBIEGAJACE_SPAMOWI:
                print(f"\n(^)(^)(^) [{time.strftime('%H:%M:%S')}] WYKRYTO: {class_name} przecina linię na Y={y_center}! WYSYŁAM SYGNAŁ!\n")
                
                if class_name == "sruba":
                    arduino.write(b'1')
                elif class_name == "wkret":
                    arduino.write(b'2')
                    
                ostatni_czas_wyslania = aktualny_czas

    annotated_frame = results[0].plot(img=frame)
    cv2.imshow("Sorter AI - Podgląd na żywo", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()