#define LED_PIN     5
#define LED_PIN2    6
#define ledDensity  16  // number of LEDs per square
#define NumSquares  32
#define NUM_LEDS    ledDensity*NumSquares
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB
#define NUM_STRANDS  2
#define UPDATES_PER_SECOND 100
#define PACKET_SIZE  195 //equal to 64 squares x 3 color vals per square (rgb) + 

#define maxBrightness  20
#define minBrightness  0
//#define fadeDelay  10
#define testDelayTime  100 
