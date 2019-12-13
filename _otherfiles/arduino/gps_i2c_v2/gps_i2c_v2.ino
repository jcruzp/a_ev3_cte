#include <Wire.h>
#include <string.h>
#include <ctype.h>
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>

// Software serial TX & RX Pins for the gpsSerial module
#define SoftrxPin 3
#define SofttxPin 2

// Initiate the software serial connection
//SoftwareSerial gpsSerialSerial = SoftwareSerial(SoftrxPin, SofttxPin);

SoftwareSerial mySerial(SoftrxPin, SofttxPin);
Adafruit_GPS gpsSerial(&mySerial);

int ledPin = 6; //LED test pin
int ledPin2 = 5; //LED test pin
// Enable/disable debug modes
//boolean debug_gpsSerial = true;
//boolean debug_nxt = true;

#define DEBUG_gpsSerial
#define DEBUG_EV3

// Timer variables
unsigned long lastRequest = 0; //the number of milliseconds from when the program started running
int timePassed = 0; //interval time
// Protocol variables
int transactionNmr = 0; //which data to transfer
boolean alive = false; //variable to check if the connection is alive
boolean confirmed = false; //to check if the datatype is confirmed
boolean transfer = false; //variable to know when to start transfering
boolean dataAvailable = false; //variable that checks if there was already data from the gpsSerial module
// gpsSerial variables
int bytegps = -1; //byte containing current received byte

char gps0; //time in UTC (HhMmSs)
char gps1; //status of the data (A=active, V=invalid)
char gps2; //latitude
char gps3; //latitude Hemisphere (N/S)
char gps4; //longitude
char gps5; //longitude Hemisphere (E/W)
char gps6; //velocity (knots)
char gps7; //bearing (degrees)
char gps8; //checksum

void setup()
{
  pinMode(ledPin, OUTPUT); //initialize LED pins
  pinMode(ledPin2, OUTPUT);
  blinkBothLED(); // blink leds to indicate the program has booted
  Serial.begin(9600); //start serial for output
  gpsSerial.begin(9600); //start serial for communication with gpsSerial

  // uncomment this line to turn on RMC (recommended minimum) and GGA (fix data) including altitude
  gpsSerial.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // uncomment this line to turn on only the "minimum recommended" data
  //gpsSerial.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);
  // For parsing data, we don't suggest using anything but either RMC only or RMC+GGA since
  // the parser doesn't care about other sentences at this time

  // Set the update rate
  gpsSerial.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate
  // For the parsing code to work nicely and have time to sort thru the data, and
  // print it out we don't suggest using anything higher than 1 Hz

  Wire.begin(127); //join i2c bus with address 127
  Wire.onRequest(requestEvent); //request event

  //for (int i = 0; i < 300; i++) { // Initialize a buffer for received data
  //  stringgps[i] = ' ';
  // }

  delay(1000);
  // Ask for firmware version
  mySerial.println(PMTK_Q_RELEASE);

  Serial.println("Arduino booted");
}

void loop()
{
  //check every 100 ms if the connection is still alive
  //if the time passed is more then 100 ms, then kill connection
  if (millis() - lastRequest > 80 && alive)
  {
    killTransaction();
  }
  //poll the gpsSerial module
  checkgps();
}

void requestEvent()
{
  //function that is triggered when the I2C master requests data (in this case the NTX)
  timePassed = millis() - lastRequest; //measure how many timepassed between   this request and last request.
  lastRequest = millis(); // make this request the last request
  //first check if we have an alive connection
  if (!alive)
    //a new transaction starts
  {
    digitalWrite(ledPin2, HIGH); //make the LED pin high to show a transaction starts
    alive = true; //the connection is alive
    transactionNmr = 0; //reset datatype to zero
    transactionNmr++; //start counting
    Wire.write(0); //send a zero back to master
  }
  else if (alive)
    //a transaction is still running, check which operation to perform based on the delay time
  {
    if (timePassed < 30 && !confirmed)
      //the datatype transaction is not yet finished
    {
#ifdef DEBUG_EV3
      Serial.println(timePassed);
#endif
      Wire.write(0);
      transactionNmr++; //increase the datatype
    }
    else if (timePassed >= 40 && timePassed < 60 && !confirmed)
      //the transaction number is received, the NXT wants confirmation
    {
      transactionNmr = transactionNmr - 1;
      Wire.write(transactionNmr); //send the understood datatype to master
      confirmed = true; //confirmed state
#ifdef DEBUG_EV3
      Serial.println("confirm");
#endif
    }
    else if (confirmed && alive && !transfer )
      //the actual transaction starts
    {
      //first send character to indicate the transaction is starting
      Wire.write("#");
      transfer = true;
#ifdef DEBUG_EV3
      Serial.println("start");
#endif
    }
    else if (confirmed && alive && transfer)
      //the actual transaction starts
    {
      //send the correct data, depending on the datatype (the transactionNmr)
      switch (transactionNmr) {
        case 0:
          if (dataAvailable)
          {
            Wire.write(gps0);
          }
          else
          {
            Wire.write("error");
          }
#ifdef DEBUG_EV3
          Serial.println("case 0");
#endif
          break;
        case 1:
          if (dataAvailable)
          {
            Wire.write(gps1);
          }
          else
          {
            Wire.write("error");
          }
#ifdef DEBUG_EV3
          Serial.println("case 1");
          Serial.println(gps1);
#endif
          break;
        case 2:
          if (dataAvailable)
          {
            Wire.write(gps2);
          }
          else
          {
            Wire.write("error");
          }
#ifdef DEBUG_EV3
          Serial.println("case 2");
          Serial.println(gps2);
#endif
          break;
        case 3:
          if (dataAvailable)
          {
            Wire.write(gps3);
          }
          else
          {
            Wire.write("error");
          }
#ifdef DEBUG_EV3
          Serial.println("case 3");
#endif
          break;
        case 4:
          if (dataAvailable)
          {
            Wire.write(gps4);
          }
          else
          {
            Wire.write("error");
          }
#ifdef DEBUG_EV3
          Serial.println("case 4");
          Serial.println(sizeof(gps4));
#endif
          break;
        case 5:
          if (dataAvailable)
          {
            Wire.write(gps5);
          }
          else
          {
            Wire.write("error");
          }
#ifdef DEBUG_EV3
          Serial.println("case 5");
#endif
          break;
        case 6:
          if (dataAvailable)
          {
            Wire.write(gps6);
          }
          else
          {
            Wire.write("error");
          }
#ifdef DEBUG_EV3
          Serial.println("case 6");
#endif
          break;
        case 7:
          if (dataAvailable)
          {
            Wire.write(gps7);
          }
          else
          {
            Wire.write("error");
          }
#ifdef DEBUG_EV3
          Serial.println("case 7");
#endif
          break;
        case 8:
          if (dataAvailable)
          {
            Wire.write(gps8);
          }
          else
          {
            Wire.write("error");
          }
#ifdef DEBUG_EV3
          Serial.println("case 8");
#endif
          break;
        default:
          Wire.write("error");
#ifdef DEBUG_EV3
          Serial.println("else");
#endif
          break;
      }
      killTransaction(); //transaction finished, kill the connection
    }
    else {
      Wire.write(0);
    }
  }
}

uint32_t timer = millis();

void checkgps() {

  //function to receive gpsSerial data from the module
  digitalWrite(ledPin, LOW); //start by making the LED low
  bytegps = gpsSerial.read(); //read a byte from the serial port
  if (bytegps == -1) { //if no data is received, then do nothing
    dataAvailable = false;
    delay(100);

  }
  else {

    // if a sentence is received, we can check the checksum, parse it...
    if (gpsSerial.newNMEAreceived()) {
      // a tricky thing here is if we print the NMEA sentence, or data
      // we end up not listening and catching other sentences!
      // so be very wary if using OUTPUT_ALLDATA and trytng to print out data
      //Serial.println(gpsSerial.lastNMEA());   // this also sets the newNMEAreceived() flag to false

      if (!gpsSerial.parse(gpsSerial.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
        dataAvailable = false;
      return;  // we can fail to parse a sentence in which case we should just wait for another
    }


    // if millis() or timer wraps around, we'll just reset it
    if (timer > millis())  timer = millis();

    // approximately every 2 seconds or so, print out the current stats
    if (millis() - timer > 2000) {
      timer = millis(); // reset the timer

      Serial.print("\nTime: ");
      if (gpsSerial.hour < 10) {
        Serial.print('0');
      }
      Serial.print(gpsSerial.hour, DEC); Serial.print(':');
      if (gpsSerial.minute < 10) {
        Serial.print('0');
      }
      Serial.print(gpsSerial.minute, DEC); Serial.print(':');
      if (gpsSerial.seconds < 10) {
        Serial.print('0');
      }
      Serial.print(gpsSerial.seconds, DEC); Serial.print('.');
      if (gpsSerial.milliseconds < 10) {
        Serial.print("00");
      } else if (gpsSerial.milliseconds > 9 && gpsSerial.milliseconds < 100) {
        Serial.print("0");
      }
      Serial.println(gpsSerial.milliseconds);
      gps0 = gpsSerial.hour + ':' + gpsSerial.minute + ':' + gpsSerial.seconds ;
      Serial.print("Date: ");
      Serial.print(gpsSerial.day, DEC); Serial.print('/');
      Serial.print(gpsSerial.month, DEC); Serial.print("/20");
      Serial.println(gpsSerial.year, DEC);
      Serial.print("Fix: "); Serial.print((int)gpsSerial.fix);
      Serial.print(" quality: "); Serial.println((int)gpsSerial.fixquality);
      if (gpsSerial.fix) {
        Serial.print("Location: ");
        Serial.print(gpsSerial.latitude, 4); Serial.print(gpsSerial.lat);
        gps2 = gpsSerial.latitude;
        gps3 = gpsSerial.lat;
        Serial.print(", ");
        Serial.print(gpsSerial.longitude, 4); Serial.println(gpsSerial.lon);
        gps4 = gpsSerial.longitude;
        gps5 = gpsSerial.lon;

        Serial.print("Speed (knots): "); Serial.println(gpsSerial.speed);
        gps6 = gpsSerial.speed;
        Serial.print("Angle: "); Serial.println(gpsSerial.angle);
        gps7 = gpsSerial.angle;
        Serial.print("Altitude: "); Serial.println(gpsSerial.altitude);
        Serial.print("Satellites: "); Serial.println((int)gpsSerial.satellites);

        dataAvailable = true;
      }
    }


  }
}
/*


  stringgpsSerial[stringgpsSerialPosition] = bytegpsSerial; //if there is serial port data, it is put in the buffer

  stringgpsSerialPosition++; //and the buffer position is increased
  if (bytegpsSerial == 13) { //if the received byte is = to 13, end of transmission
    stringgpsSerial[stringgpsSerialPosition + 1] = '\0'; //character to end the string
    Serial.println(stringgpsSerial);
    seperatorCounter = 0; //reset counters
    stringCheckCounter = 0;
    for (int i = 1; i < 7; i++) { //verifies if the received command starts with $GPRMC (this is the data we would like to process)
      if (stringgpsSerial[i] == stringCheck[i - 1]) {
        stringCheckCounter++;
      }
    }
    if (stringCheckCounter == 6) { //if yes, continue and process the data
      boolean firstChecksum = false;
      for (int i = 0; i < 300; i++) {
        if (stringgpsSerial[i] == ',') { // check for the position of the "," separator
          if (seperatorCounter < 12)
          {
            seperators[seperatorCounter] = i; //and store the location in the               seperators array
            seperatorCounter++;
          }
        }
        if (string[i] == '*' && !firstChecksum) { // ... and the "*"
          seperators[12] = i;
          firstChecksum = true;
        }
      }

        the separators array indicate the position of:
        0 = the time in UTC (HhMmSs)
        1 = Status of the data (A=active, V=invalid)
        2 = Latitude
        3 = Latitude Hemisphere (N/S)
        4 = Longitude
        5 = Longitude Hemisphere (E/W)
        6 = Velocity (knots)
        7 = Bearing (degrees)
        8 = date UTC (DdMmAa)
        9 = Magnetic degrees
        12 = Checksum

      //check if the data is active
      int data = 1;
      for (int j = seperators[data]; j < seperators[data + 1] - 1; j++) {
        gps1 = stringGPS[j + 1];
      }
      if (gps1 == 'A') //the data is good
      {
  #ifdef DEBUG_GPS
        Serial.println("------------------");
  #endif
        dataAvailable = true; //data is availabe, enable this boolean
        digitalWrite(ledPin, HIGH); //enable the LED pin
        emptyStrings(); //empty previous strings
        data = 0; //reset data variables
        int i = 0;
        // Now we will store all the data one by one in seperate variables
        // this makes it possible for the protocol to send the correct variable
        // when requested.
        for (int j = seperators[data]; j < seperators[data + 1] - 1; j++) {
          gps0[i] = stringGPS[j + 1];
          i++;
        }
        gps0[6] = '\0';
        i = 0;
        data = 2;
        for (int j = seperators[data]; j < seperators[data + 1] - 1; j++) {
          gps2[i] = stringGPS[j + 1];
          i++;
        }
        gps2[10] = '\0';
        i = 0;
        data = 3;
        for (int j = seperators[data]; j < seperators[data + 1] - 1; j++) {
          gps3 = stringGPS[j + 1];
          i++;
        }
        i = 0;
        data = 4;
        for (int j = seperators[data]; j < seperators[data + 1] - 1; j++) {
          gps4[i] = stringGPS[j + 1];
          i++;
        }
        gps4[10] = '\0';
        i = 0;
        data = 5;
        for (int j = seperators[data]; j < seperators[data + 1] - 1; j++) {
          gps5 = stringGPS[j + 1];
        }
        i = 0;
        data = 6;
        for (int j = seperators[data]; j < seperators[data + 1] - 1; j++) {
          gps6[i] = stringGPS[j + 1];
          i++;
        }
        gps6[3] = '\0';
        i = 0;
        data = 7;
        for (int j = seperators[data]; j < seperators[data + 1] - 1; j++) {
          gps7[i] = stringGPS[j + 1];
          i++;
        }
        gps7[6] = '\0';
        i = 0;
        data = 12;
        for (int j = seperators[data]; j < seperators[data + 1] - 1; j++) {
          gps8[i] = stringGPS[j + 1];
          i++;
        }
        gps8[3] = '\0';
  #ifdef DEBUG_GPS
        Serial.println(gps0);
        Serial.println(gps1);
        Serial.println(gps2);
        Serial.println(gps3);
        Serial.println(gps4);
        Serial.println(gps5);
        Serial.println(gps6);
        Serial.println(gps7);
        Serial.println(gps8);
  #endif
      }
    }
    stringGPSPosition = 0;
    // Reset the buffer
    for (int i = 0; i < 300; i++) { //
      stringGPS[i] = ' ';
    }
  }
  }
  }

*/
/*
  void emptyStrings()
  {
  //function to clear all the strings
  for (int i = 0; i < 7; i++) { //
    gps0[i] = ' ';
  }
  gps1 = ' ';
  for (int i = 0; i < 11; i++) { //
    gps2[i] = ' ';
  }
  gps3 = ' ';
  for (int i = 0; i < 11; i++) { //
    gps4[i] = ' ';
  }
  gps5 = ' ';
  for (int i = 0; i < 4; i++) { //
    gps6[i] = ' ';
  }
  for (int i = 0; i < 7; i++) { //
    gps7[i] = ' ';
  }
  for (int i = 0; i < 4; i++) { //
    gps8[i] = ' ';
  }
  }
*/

void blinkBothLED()
{
  //function to blink both LEDs
  digitalWrite(ledPin, HIGH);
  digitalWrite(ledPin2, HIGH);
  delay(500);
  digitalWrite(ledPin, LOW);
  digitalWrite(ledPin2, LOW);
  delay(500);
}

void killTransaction()
{
  // Function to kill the transaction, used when a time out occured.
  // or when the data was succesfuly sent.
#ifdef DEBUG_EV3
  Serial.println("transaction stopped");
  Serial.println(" ");
#endif
  digitalWrite(ledPin2, LOW);
  alive = false;
  confirmed = false;
  transfer = false;
  transactionNmr = 0;
}
