

#include <driver/dac.h>
#include <soc/rtc.h>
#include <soc/sens_reg.h>
#include "DataTable.h"
#include "Heart.h"


//Variables
int lastx, lasty;
unsigned long currentMillis = 0;
unsigned long previousMillis = 0;
int Timeout = 20;
const long interval = 990;  //milliseconds, you should twick this
                            //to get a better accuracy
const int ledPin = 2;

//*****************************************************************************
// PlotTable 
//*****************************************************************************

void PlotTable(byte *SubTable, int SubTableSize, int skip, int opt, int offset)
{
  int i=offset;
  while (i<SubTableSize){
    if (SubTable[i+2]==skip){
      i=i+3;
      if (opt==1) if (SubTable[i]==skip) i++;
    }
    Line(SubTable[i],SubTable[i+1],SubTable[i+2],SubTable[i+3]);  
    if (opt==2){
      Line(SubTable[i+2],SubTable[i+3],SubTable[i],SubTable[i+1]); 
    }
    i=i+2;
    if (SubTable[i+2]==0xFF) break;
  }
}

void PlotXYtable(uint16_t *SubTable1, uint16_t *SubTable2, int SubTableSize, int scale) {
  int i = 0;
  while (i < SubTableSize) {
    Line(SubTable1[i] * scale, SubTable1[i + 1] * scale, SubTable2[i] * scale, SubTable2[i + 1] * scale);
    i = i + 1; // Move to the next pair of values
  }
}


//*****************************************************************************
// Dot
//*****************************************************************************

inline void Dot(int x, int y) {
  if (lastx != x) {
    lastx = x;
    dac_output_voltage(DAC_CHANNEL_1, x);
  }
#if defined EXCEL
  Serial.print("0x");
  if (x <= 0xF) Serial.print("0");
  Serial.print(x, HEX);
  Serial.print(",");
#endif
#if defined EXCEL
  Serial.print("0x");
  if (lasty <= 0xF) Serial.print("0");
  Serial.print(lasty, HEX);
  Serial.println(",");
#endif
  if (lasty != y) {
    lasty = y;
    dac_output_voltage(DAC_CHANNEL_2, y);
  }
#if defined EXCEL
  Serial.print("0x");
  if (x <= 0xF) Serial.print("0");
  Serial.print(x, HEX);
  Serial.print(",");
#endif
#if defined EXCEL
  Serial.print("0x");
  if (y <= 0xF) Serial.print("0");
  Serial.print(y, HEX);
  Serial.println(",");
#endif
}

// End Dot
//*****************************************************************************



//*****************************************************************************
// Line
//*****************************************************************************
// Bresenham's Algorithm implementation optimized
// also known as a DDA - digital differential analyzer

void Line(byte x1, byte y1, byte x2, byte y2) {
  int acc;
  // for speed, there are 8 DDA's, one for each octant
  if (y1 < y2) {  // quadrant 1 or 2
    byte dy = y2 - y1;
    if (x1 < x2) {  // quadrant 1
      byte dx = x2 - x1;
      if (dx > dy) {  // < 45
        acc = (dx >> 1);
        for (; x1 <= x2; x1++) {
          Dot(x1, y1);
          acc -= dy;
          if (acc < 0) {
            y1++;
            acc += dx;
          }
        }
      } else {  // > 45
        acc = dy >> 1;
        for (; y1 <= y2; y1++) {
          Dot(x1, y1);
          acc -= dx;
          if (acc < 0) {
            x1++;
            acc += dy;
          }
        }
      }
    } else {  // quadrant 2
      byte dx = x1 - x2;
      if (dx > dy) {  // < 45
        acc = dx >> 1;
        for (; x1 >= x2; x1--) {
          Dot(x1, y1);
          acc -= dy;
          if (acc < 0) {
            y1++;
            acc += dx;
          }
        }
      } else {  // > 45
        acc = dy >> 1;
        for (; y1 <= y2; y1++) {
          Dot(x1, y1);
          acc -= dx;
          if (acc < 0) {
            x1--;
            acc += dy;
          }
        }
      }
    }
  } else {  // quadrant 3 or 4
    byte dy = y1 - y2;
    if (x1 < x2) {  // quadrant 4
      byte dx = x2 - x1;
      if (dx > dy) {  // < 45
        acc = dx >> 1;
        for (; x1 <= x2; x1++) {
          Dot(x1, y1);
          acc -= dy;
          if (acc < 0) {
            y1--;
            acc += dx;
          }
        }

      } else {  // > 45
        acc = dy >> 1;
        for (; y1 >= y2; y1--) {
          Dot(x1, y1);
          acc -= dx;
          if (acc < 0) {
            x1++;
            acc += dy;
          }
        }
      }
    } else {  // quadrant 3
      byte dx = x1 - x2;
      if (dx > dy) {  // < 45
        acc = dx >> 1;
        for (; x1 >= x2; x1--) {
          Dot(x1, y1);
          acc -= dy;
          if (acc < 0) {
            y1--;
            acc += dx;
          }
        }

      } else {  // > 45
        acc = dy >> 1;
        for (; y1 >= y2; y1--) {
          Dot(x1, y1);
          acc -= dx;
          if (acc < 0) {
            x1--;
            acc += dy;
          }
        }
      }
    }
  }
}

// End Line
//*****************************************************************************




//*****************************************************************************
// Circle
//*****************************************************************************



// End Circle
//*****************************************************************************

//*****************************************************************************
// setup
//*****************************************************************************

void setup() {
  Serial.begin(9600);
  Serial.println("\nESP32 Oscilloscope Clock v1.0");
  Serial.println("Mauro Pintus 2018\nwww.mauroh.com");
  //rtc_clk_cpu_freq_set(RTC_CPU_FREQ_240M);
  Serial.println("CPU Clockspeed: ");
  // Serial.println(rtc_clk_cpu_freq_value(rtc_clk_cpu_freq_get()));

  dac_output_enable(DAC_CHANNEL_1);
  dac_output_enable(DAC_CHANNEL_2);
  pinMode(ledPin, OUTPUT);
  delay(1000);
}
// End setup
//*****************************************************************************

void circle(int centerX, int centerY, int radius) {
  digitalWrite(ledPin, LOW);  // turn on the LED
  int lastx_loc = centerX + (radius * cos(0));
  int lasty_loc = centerY + (radius * sin(0));

  for (int angle = 1; angle < 358; angle++) {
    float radians = angle * 0.0174533;          // Convert degrees to radians
    int x = centerX + (radius * cos(radians));  // X coordinate of the point on the circle
    int y = centerY + (radius * sin(radians));  // Y coordinate of the point on the circle

    // Draw a line from the previous point to the current point
    Line(lastx_loc, lasty_loc, x, y);

    // Update the last coordinates
    lastx_loc = x;
    lasty_loc = y;
  }
  digitalWrite(ledPin, HIGH);  // turn off the LED
}

void triangle(int centerX, int centerY, int radius) {
  digitalWrite(ledPin, LOW);  // turn on the LED
  float angleIncrement = 120.0;  // Angle increment for each vertex of the triangle

  // Calculate the coordinates of the three vertices of the triangle
  float radians1 = 0 * 0.0174533;               // Convert degrees to radians for the first vertex
  int x1 = centerX + (radius * cos(radians1));  // X coordinate of the first vertex
  int y1 = centerY + (radius * sin(radians1));  // Y coordinate of the first vertex

  float radians2 = angleIncrement * 0.0174533;  // Convert degrees to radians for the second vertex
  int x2 = centerX + (radius * cos(radians2));  // X coordinate of the second vertex
  int y2 = centerY + (radius * sin(radians2));  // Y coordinate of the second vertex

  float radians3 = (angleIncrement * 2) * 0.0174533;  // Convert degrees to radians for the third vertex
  int x3 = centerX + (radius * cos(radians3));        // X coordinate of the third vertex
  int y3 = centerY + (radius * sin(radians3));        // Y coordinate of the third vertex

  // Draw lines connecting the vertices to form the triangle
  Line(x1, y1, x2, y2);
  Line(x2, y2, x3, y3);
  Line(x3, y3, x1, y1);
  Line(x1, y1, x2, y2);
  Line(x2, y2, x3, y3);
  Line(x3, y3, x1, y1);
  digitalWrite(ledPin, HIGH);  // turn on the LED
}

void square(int centerX, int centerY, int radius) {
  digitalWrite(ledPin, LOW);  // turn on the LED

  int x_left = centerX - radius/2;
  int x_right = centerX + radius/2;
  int y_top = centerY - radius/2;
  int y_bot = centerY + radius/2;
  
  // Draw lines connecting the vertices to form the triangle
  Line(x_left, y_bot, x_right, y_bot); // bottom line
  Line(x_right, y_bot, x_right, y_top); // right line
  Line(x_right, y_top, x_left, y_top); // top line
  Line(x_left, y_top, x_left, y_bot); // left line

  Line(x_left, y_bot, x_right, y_bot); // bottom line
  Line(x_right, y_bot, x_right, y_top); // right line
  Line(x_right, y_top, x_left, y_top); // top line
  Line(x_left, y_top, x_left, y_bot); // left line

  digitalWrite(ledPin, HIGH);  // turn on the LED

}

//*****************************************************************************
// loop
//*****************************************************************************

void loop() {
  // Define the center and radius of the circle

  int dir_x1 = 2;   // movement direction x
  int dir_y1 = 1;   // movement direction x
  int dir_x2 = -2;  // movement direction x
  int dir_y2 = -3;  // movement direction x  
  int dir_x3 = -3;  // movement direction x
  int dir_y3 = 5;  // movement direction x  
  
  int radius1 = 20  ;
  int radius2 = 20  ;
  int radius3 = 20  ;

  int center_x = 128;   // out of 256
  int center_y = 128;   // out of 256
  int center_x2 = 128;  // out of 256
  int center_y2 = 128;  // out of 256
  int center_x3 = 128;  // out of 256
  int center_y3 = 128;  // out of 256


  int center_x_box = 128;  // out of 256
  int center_y_box = 128;  // out of 256
  
  int bound_up = 253;
  int bound_down = 3;

  

  while (true) {

    if (center_x + radius1 >= bound_up || center_x - radius1 <= bound_down) {

      dir_x1 = -dir_x1;
    }
    if (center_y + radius1 >= bound_up || center_y - radius1 <= bound_down) {
      dir_y1 = -dir_y1;
    }
    if (center_x2 + radius2 >= bound_up || center_x2 - radius2 <= bound_down) {

      dir_x2 = -dir_x2;
    }
    if (center_y2 + radius2 >= bound_up || center_y2 - radius2 <= bound_down) {
      dir_y2 = -dir_y2;
    }

    if (center_x3 + radius3 >= bound_up || center_x3 - radius3 <= bound_down) {
      dir_x3 = -dir_x3;
    }
    if (center_y3 + radius3 >= bound_up || center_y3 - radius3 <= bound_down) {
      dir_y3 = -dir_y3;
    }

    center_x = center_x + dir_x1;
    center_y = center_y + dir_y1;
    center_x2 = center_x2 + dir_x2;
    center_y2 = center_y2 + dir_y2;
    center_x3 = center_x3 + dir_x3;
    center_y3 = center_y3 + dir_y3;

    // circle(center_x, center_y, radius1);
    // // triangle(center_x2, center_y2, radius2);
    // square(center_x3, center_y3, radius3);
    // square(center_x_box, center_y_box, 253); // bounding square
    // // heart(center_x2, center_y2, radius2)
    delay(10); // set to time the speed of the objects drawing. Speed of direction is met earlier by dir_x and dir_y params 
    PlotXYtable(Column1Data, Column2Data, sizeof(Column2Data) / sizeof(Column2Data[0]), 1);
  }

}
