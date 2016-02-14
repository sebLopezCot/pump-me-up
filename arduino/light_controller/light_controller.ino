#include <Adafruit_NeoPixel.h>

#define PIN 6
#define NUM_PIXELS 166
#define NUM_FIELDS;

// Parameter 1 = number of pixels in strip
// Parameter 2 = pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_PIXELS, PIN, NEO_GRB + NEO_KHZ800);

int motor = 0;
int light = 0;

void setup(){
  Serial.begin(9600);
   strip.begin();
   strip.setBrightness(100);
   strip.show(); // Initialize all pixels to 'off'
   pinMode(3, OUTPUT);
}

void loop() {
  
  if(Serial.available()){
    for(int i=0; i < NUM_FIELDS; i++){
      value[i] = Serial.parseFloat();
      if(i==0) light = value[i];
      if(i==1) motor = value[i];
    }
  }
  
  if(motor == 1){
    digitalWrite(3, HIGH);
  } else {
    digitalWrite(3, LOW);
  }
  
  if(light == 1){
    int i;
    for (i=0; i < strip.numPixels(); i++){
      strip.setPixelColor(i, 255, 255, 255);
    }
    strip.show();
    delay(random(0,100));
    for (i=0; i < strip.numPixels(); i++){
      strip.setPixelColor(i, 0, 0, 0);
    }
    strip.show();
    delay(random(0,100));
  } else {
    for (i=0; i < strip.numPixels(); i++){
      strip.setPixelColor(i, 0, 0, 0);
    }
    strip.show();
    delay(random(0,100));
  }
}
