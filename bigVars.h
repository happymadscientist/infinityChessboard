static const uint8_t squares[8][8][4] = {
    {{1, 2, 127, 128}, {82, 87, 88, 89}, {27, 28, 29, 30}, {78, 91, 92,93}, {55, 56, 57, 58}, {74, 95, 96, 97}, {83, 84, 85, 86}, {99,  100, 101, 102}},
    {{83, 84, 85, 86}, {3, 4, 5, 126}, {79, 80, 81, 90}, {26, 31, 32, 33}, {75, 76, 77, 94}, {54, 59, 60, 61}, {72, 73,    98, 103}, {82, 87, 88, 89}},
    {{6, 123, 124, 125}, {54, 59, 60, 61}, {23, 24, 25, 34}, {50, 63, 64, 65}, {51, 52, 53, 62}, {46, 67, 68, 69}, {79, 80, 81, 90}, {71, 104, 105, 106}},
    {{55, 56, 57, 58}, {7, 8, 9, 122}, {51, 52, 53, 62}, {22, 35, 36, 37}, {47, 48, 49, 66}, {50, 63, 64, 65}, {44, 45, 70, 107}, {78, 91, 92, 93}},
    {{10, 119, 120, 121}, {26, 31, 32, 33}, {19, 20, 21, 38}, {22, 35, 36, 37}, {47, 48, 49, 66}, {18, 39, 40, 41}, {75, 76, 77, 94}, {43, 108, 109, 110}},
    {{27, 28, 29, 30}, {11, 12, 13, 118}, {23, 24, 25, 34}, {18, 39, 40, 41}, {19, 20, 21, 38}, {46, 67, 68, 69}, {16, 17, 42, 111}, {74, 95, 96, 97}},
    {{14, 115, 116, 117}, {3, 4, 5, 126}, {16, 17, 42, 111}, {7, 8, 9, 122}, {44, 45, 70, 107}, {11, 12, 13, 118}, {72, 73, 98, 103}, {15, 112, 113, 114}},
    {{1, 2, 127, 128}, {15, 112, 113, 114}, {6, 123, 124, 125}, {43, 108, 109, 110}, {10, 119, 120, 121}, {71, 104, 105, 106}, {14, 115, 116, 117}, {99, 100, 101, 102}}
   };


 /*
 static const uint8_t picture[8][8][3] ={
  {{255, 255, 255}, {255, 251, 249}, {251, 250, 246}, {255, 255,   255}, {137, 214, 136}, {125, 212, 125}, {246, 252, 246}, {254, 255, 254}},
  {{255, 255, 255}, {255, 207, 154}, {252, 206, 151}, {255, 255, 255}, {181, 230, 178}, {0, 164, 0}, {4, 171, 4}, {197, 236, 197}},
  {{255, 255, 251}, {253, 137, 62}, {253, 138, 62}, {253, 254, 246}, {255, 255, 255}, {202, 237, 202}, {12, 175, 12}, {140, 215, 140}},
  {{255, 255, 251}, {250, 101, 37}, {253, 103, 41}, {246, 255, 240}, {118, 209, 120}, {116, 209, 115}, {96, 202, 96}, {14, 176, 14}},
  {{255, 255, 251}, {250, 101, 37}, {253, 103, 41}, {246, 255, 240}, {118, 209, 120}, {116, 209, 115}, {96, 202, 96}, {14, 176, 14}},
  {{255, 255, 251}, {253, 137, 62}, {253, 138, 62}, {253, 254, 246}, {255, 255, 255}, {202, 237, 202}, {12, 175, 12}, {140, 215, 140}},
  {{255, 255, 255}, {255, 207, 154}, {252, 206, 151}, {255, 255, 255}, {181, 230, 178}, {0, 164, 0}, {4, 171, 4}, {197, 236, 197}}, 
  {{255, 255, 255}, {255, 251, 249}, {251, 250, 246}, {255, 255, 255}, {137, 214, 136}, {125, 212, 125}, {246, 252, 246}, {254, 255, 254}}
  };*/

  /*
static const uint8_t picture2[8][8][3] = {
  {{26, 0, 0}, {186, 0, 0}, {211, 0, 0}, {56, 0, 0}, {54, 0, 0}, {206, 0, 0}, {187, 0, 0}, {30, 0, 0}}, 
  {{192, 0, 0}, {255, 0, 0}, {255, 0, 0}, {240, 0, 0}, {240, 0, 0}, {255, 0, 0}, {255, 0, 0}, {195, 0, 0}}, 
  {{250, 0, 0}, {252, 0, 0}, {253, 0, 0}, {255, 0, 0}, {255, 0, 0}, {253, 0, 0}, {252, 0, 0}, {248, 0, 0}}, 
  {{213, 0, 0}, {253, 0, 0}, {253, 0, 0}, {254, 0, 0}, {254, 0, 0}, {253, 0, 0}, {253, 0, 0}, {217, 0, 0}}, 
  {{89, 0, 0}, {255, 0, 0}, {250, 0, 0}, {254, 0, 0}, {254, 0, 0}, {250, 0, 0}, {255, 0, 0}, {90, 0, 0}},
  {{0, 0, 0}, {138, 0, 0}, {255, 0, 0}, {252, 0, 0}, {252, 0, 0}, {255, 0, 0}, {137, 0, 0}, {0, 0, 0}},
  {{3, 0, 0}, {0, 0, 0}, {109, 0, 0}, {255, 0, 0}, {255, 0, 0}, {107, 0, 0}, {0, 0, 0}, {3, 0, 0}},
  {{0, 0, 0}, {4, 0, 0}, {0, 0, 0}, {96, 0, 0}, {98, 0, 0}, {0, 0, 0}, {4, 0, 0}, {0, 0, 0}}
  };
  */
  
