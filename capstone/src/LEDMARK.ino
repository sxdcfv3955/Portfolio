#include <SPI.h>
#include <Adafruit_GFX.h>
#include <TFT_ILI9163C.h>
#include <Wire.h>
#define SLAVE 1

// Color definitions
#define	BLACK   0x0000
#define	BLUE    0x001F
#define	RED     0xF800
#define	GREEN   0x07E0
#define CYAN    0x07FF
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define WHITE   0xFFFF

/*
  Teensy3.x and Arduino's
  You are using 4 wire SPI here, so:
  MOSI:  11//Teensy3.x/Arduino UNO (for MEGA/DUE refere to arduino site)
  MISO:  12//Teensy3.x/Arduino UNO (for MEGA/DUE refere to arduino site)
  SCK:   13//Teensy3.x/Arduino UNO (for MEGA/DUE refere to arduino site)
  the rest of pin below:
*/

/*
  Teensy 3.x can use: 2,6,9,10,15,20,21,22,23
  Arduino's 8 bit: any
  DUE: check arduino site
  If you do not use reset, tie it to +3V3
*/


TFT_ILI9163C lcd1 = TFT_ILI9163C(10, 9);
TFT_ILI9163C lcd2 = TFT_ILI9163C(7, 6);
TFT_ILI9163C lcd3 = TFT_ILI9163C(5, 4);
TFT_ILI9163C lcd4 = TFT_ILI9163C(3, 2);

TFT_ILI9163C lcd[4] = {lcd1, lcd2, lcd3, lcd4};

int w = 128;
int h = 128;
int i = 0;
char temp;

void setup() {
  lcd1.begin();
  lcd2.begin();
  lcd3.begin();
  lcd4.begin();
  Wire.begin(SLAVE);
  Wire.onReceive(receiveFromMaster);
  Serial.begin (9600);
}

void loop() {
  if (count > 3)
    count = 0;

  if (temp == '2')
    UP(lcd[count]);
  else if (temp == '3')
    RIGHT(lcd[count]);
  else if (temp == '4')
    DOWN(lcd[count]);
  else if (temp == '5')
    LEFT(lcd[count]);

  count++;

}

void UP(TFT_ILI9163C t) {
  t.fillScreen(WHITE);
  int j = 0;
  for (int i = 0; i < h / 2; i++) {
    t.drawLine(w / 2 - j, i, w / 2 + j, i, GREEN);
    j++;
  }
  for (int i = h / 2; i < h; i++) {
    t.drawLine(w / 4, i, 3 * w / 4, i, GREEN);
  }
}

void RIGHT(TFT_ILI9163C t) {
  t.fillScreen(WHITE);
  int j = 0;
  for (int i = w / 2; i < w; i++) {
    t.drawLine(i, j, i, h - j, GREEN);
    j++;
  }
  for (int i = 0; i < w / 2; i++) {
    t.drawLine(i, h / 4, i, 3 * h / 4, GREEN);
  }
}

void LEFT(TFT_ILI9163C t) {
  t.fillScreen(WHITE);
  int j = 0;
  for (int i = w / 2; i < w; i++) {
    t.drawLine(i, h / 4, i, 3 * h / 4, GREEN);

  }
  for (int i = 0; i < w / 2; i++) {
    t.drawLine(i, h / 2 - j, i, h / 2 + j, GREEN);
    j++;
  }
}

void DOWN(TFT_ILI9163C t) {
  t.fillScreen(WHITE);
  int j = 0;
  for (int i = 0; i < h / 2; i++) {
    t.drawLine(w / 4, i, 3 * w / 4, i, GREEN);
  }
  for (int i = h / 2; i < h; i++) {
    t.drawLine(j, i, w - j, i, GREEN);
    j++;
  }
}

void DONOTENTER(TFT_ILI9163C t) {
  t.fillScreen(WHITE);
  t.setCursor(0, 0);
  t.setTextColor(RED);
  t.setTextSize(4);
  t.println("DO");
  t.println("NOT");
  t.println("ENTER");
}

void receiveFromMaster(int bytes) {
  char ch[2];
  for (int i = 0 ; i < bytes ; i++) {
    // 수신 버퍼 읽기
    ch[i] = Wire.read();
  }
  temp = ch[0];
}
