#define ledHijau 2
#define ledMerah 3
#define buzzer 4

void setup() {
  // Inisialisasi pin sebagai OUTPUT
  pinMode(ledHijau, OUTPUT);
  pinMode(ledMerah, OUTPUT);
  pinMode(buzzer, OUTPUT);
  
  // Inisialisasi komunikasi serial
  Serial.begin(9600);
}

void loop() {
  // Jika ada data serial yang diterima
  if (Serial.available() > 0) {
    char data = Serial.read();  // Membaca data yang dikirim dari Python
    
    if (data == '1') {
      // Masker terdeteksi, LED hijau ON, LED merah OFF, buzzer OFF
      digitalWrite(ledHijau, HIGH);
      digitalWrite(ledMerah, LOW);
      digitalWrite(buzzer, LOW);
    } else if (data == '0') {
      // Masker tidak terdeteksi, LED hijau OFF, LED merah ON, buzzer ON
      digitalWrite(ledHijau, LOW);
      digitalWrite(ledMerah, HIGH);
      digitalWrite(buzzer, HIGH);
    }
  }
}


 
