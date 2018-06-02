#include <SoftwareSerial.h>
SoftwareSerial BluetoothSerial(10, 11); // RX, TX

char recv_char, sent_char;
String sent_data = "";
String recv_data = "";

void setup() {
    Serial.begin(115200);
    while (!Serial) {}
    Serial.println("Serial Connected!");
    BluetoothSerial.begin(9600);
}

void loop() {
    if (Serial.available()) {
        while (Serial.available()) {
            sent_char = Serial.read();
            sent_data += String(sent_char);
            BluetoothSerial.write(sent_char);
            Serial.println("=> send: " + String(sent_char));
            /*
            if (sent_char == '\n') {
                Serial.println("=> send: " + String(sent_data));
                sent_data = "";
            }
            */
        }
    }

    if (BluetoothSerial.available()) {
        while (BluetoothSerial.available()) {
            recv_char = BluetoothSerial.read();
            recv_data += String(recv_char);
            if (recv_char == '\n') {
                Serial.println("=> received: " + String(recv_data));
                recv_data = "";
                BluetoothSerial.flush();
                break;
            }
        }
    }
}