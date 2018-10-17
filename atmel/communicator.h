#include<Arduino.h>
#include "userParams.h"
#include "Adafruit_BLE.h"
#include "Adafruit_BluefruitLE_SPI.h"
#define FACTORYRESET_ENABLE 1
extern Adafruit_BluefruitLE_SPI ble;

#define BUFSIZE                        128   // Size of the read buffer for incoming data
#define VERBOSE_MODE                   true  // If set to 'true' enables debug output
#define BLE_READPACKET_TIMEOUT         500   // Timeout in ms waiting to read a response
//#define BLUEFRUIT_SWUART_RXD_PIN       9    // Required for software serial!
//#define BLUEFRUIT_SWUART_TXD_PIN       10   // Required for software serial!
//#define BLUEFRUIT_UART_CTS_PIN         11   // Required for software serial!
//#define BLUEFRUIT_UART_RTS_PIN         -1   // Optional, set to -1 if unused
#define BLUEFRUIT_SPI_CS               8  
#define BLUEFRUIT_SPI_IRQ              7
#define BLUEFRUIT_SPI_RST              4    // Optional but recommended, set to -1 if unused
#define BLUEFRUIT_SPI_SCK              13
#define BLUEFRUIT_SPI_MISO             12
#define BLUEFRUIT_SPI_MOSI             11
#define FACTORYRESET_ENABLE             1
#define BAUD_RATE                       115200


class communicator {
 public:
   communicator();
   //serial communication functions
   void serialPacketSetup();
   bool checkSerial();
   bool readSerialPacket(byte packet[]);

   //bluetooth functions
   
   uint8_t readBLEPacket(Adafruit_BluefruitLE_SPI *ble, uint16_t timeout,byte packet[]);
   //bool checkBLE(Adafruit_BluefruitLE_SPI *ble) ;//checks if a bluetooth packet is ready, and reads it and parses it
   bool nameChangeBLE(String newName);
   void startBLE(String newName);
   void error(const __FlashStringHelper*err);
};
