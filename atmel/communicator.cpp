#include "communicator.h"

communicator::communicator(){}

void communicator::startBLE(String newName){
 if ( !ble.begin(VERBOSE_MODE) )  {
   error(F("Couldn't find Bluefruit, make sure it's in CoMmanD mode & check wiring?"));
 }
 Serial.println( F("Startup OK!") );

 if (FACTORYRESET_ENABLE){
   if (!ble.factoryReset()){ 
     error(F("Couldn't factory reset"));
   }
     Serial.println( F("Factory Reset OK!") );
 }
 
 // Disable command echo from Bluefruit 
 ble.echo(false);
 ble.info();  //print out BLE Info
 ble.verbose(false);  // debug info is a little annoying after this point!

 ble.println("AT+GAPDEVNAME="+newName);
 ble.waitForOK();

 while (! ble.isConnected()) {
     delay(500);  //wait for connection
 }
 ble.setMode(BLUEFRUIT_MODE_DATA);  //data mode
}

bool communicator::nameChangeBLE(String newName){
 ble.println("AT+GAPDEVNAME=" + newName);
 ble.waitForOK();
}
//
//bool communicator::checkBLE(Adafruit_BluefruitLE_SPI *ble) {//checks if a bluetooth packet is ready, and reads it and parses it
//  if (ble->available()){  //means bytes in the buffer
//    uint8_t numBytes = readBLEPacket(ble,BLE_READPACKET_TIMEOUT,packet);
//    if (numBytes){  //means no failure during reading, checksum worked out, and you have this many bytes
//      Serial.print("Success");
//      packetParser(packet);
//    }
//  }
//}

uint8_t communicator::readBLEPacket(Adafruit_BluefruitLE_SPI *ble, uint16_t timeout,byte packet[]){
 uint16_t origtimeout = timeout, byteNum = 0;

 while (timeout--) {
   if (byteNum >= PACKET_SIZE) break;
     if  (ble->read() == '!'){
     while (ble->available()) {
       char c =  ble->read();
       packet[byteNum] = c;
       byteNum++;
       timeout = origtimeout;  //reset the timeout counter
     }
   }
   if (timeout == 0) break;
   delay(1);
 }

 if (!byteNum) return 0; // no data or timeout 
//  if (packet[0] != '!') return 0; // doesn't start with '!' packet beginning
//  if (!calculateChecksum(packet,byteNum)) return 0; //checksum mismatch
 
 return byteNum;   // checksum passed!
}


/*END BLE FUNCTIONS*/



/*BEGIN SERIAL FUNCTIONS*/
void communicator::serialPacketSetup(){
 Serial.begin(BAUD_RATE);
}

//bool chessboard::checkSerial() {//checks if a serial packet is ready, and reads it and parses it
//  if (Serial.available()){  //means bytes in the buffer
//    uint8_t numBytes = readSerialPacket(packet);
//    if (numBytes){  //means no failure during reading, checksum worked out, and you have this many bytes
//      packetParser(packet);
//    }
//  }
//}

bool communicator::readSerialPacket(byte packet[]){
 uint8_t byteNum=0;
 if (Serial.read() == '!'){
    delay(4);
    while (Serial.available()){
       byte byteIn = Serial.read();
       if (byteIn==0x0A){break;}  //new Line character '/n', exit out of listening
       packet[byteNum]= byteIn;
       byteNum++;
       delay(4);  //arduino is too fast usually.  
     }
 }
 if (!byteNum) return 0; // no data or timeout 
//  if (!calculateChecksum(packet,byteNum)) return 0; //checksum mismatch
 
 return byteNum;   // everything passed, return number of bytes read
}
