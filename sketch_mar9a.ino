#include <KeyboardController.h>
#include <MouseController.h>
#include <Usb.h>
#include <address.h>
#include <adk.h>
#include <confdescparser.h>
#include <hid.h>
#include <hidboot.h>
#include <hidusagestr.h>
#include <parsetools.h>
#include <usb_ch9.h>

#include <USBHost.h>

USBHost myusb;
HIDJoystick joystick(myusb);
typedef struct{
int rightjoyX;
int rightjoyY;
int leftjoyX;
int leftjoyY;
int lefttrigger;
int righttrigger;
bool Ybutton;
bool Xbutton;
bool Bbutton;
bool Abutton;
bool Backbutton;
bool Startbutton;
bool Modebutton;
bool Dpadup;
bool Dpadleft;
bool Dpadright;
bool Dpaddown;
} controller;

controller logi
void setup() {
  Serial.begin(115200);
  myusb.begin();
  Serial.println("Waiting for joystick...");
}

void loop() {
  myusb.Task();

  if (joystick.available()) {
    logi.leftjoyX = joystick.getX();
    logi.leftjoyY = joystick.getY();
    logi.rightjoyX = joystick.getRx();
    logi.rightjoyY = joystick.getRY();
    logi.lefttrigger = joystick.getZ();
    logi.righttrigger = joystick.getRz();
    logi.Ybutton = joystick.getButton(4);
    logi.Xbutton = joystick.getButton(3);
    logi.Bbutton = joystick.getButton(2);
    logi.Abutton = joystick.getButton(1);
    logi.Backbutton = joystick.getButton(7);
    logi.Startbutton = joystick.getButton(8);
    
    // I DONT KNOW WHAT THIS IS, USE getRawData to find what the button is logi.Modebutton = joystick.getButton(8);
    Serial.println(joystick.getRawData());

    logi.Dpadup = joystick.getHat(0);
    logi.Dpaddown = joystick.getHat(4);
    logi.Dpadleft = joystick.getHat(6);
    logi.Dpadright = joystick.getHat(2);
  }


  Serial.println(logi);
}
