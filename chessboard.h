#include<Arduino.h>
//#include "userParams.h"

#include "ledWriter.h"
//#include "packetParser.h"
//#include "textChess.h"
//#include "communicator.h"



class chessboard {
  public:
    chessboard();
    void startup();
    
    //ledWriter ledControl;
    void turnOn(ledWriter* ledControl);




   private:
};
