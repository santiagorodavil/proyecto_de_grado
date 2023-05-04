#include <Servo.h>
Servo servo_der;
Servo servo_izq;
int pins[] = {5, 6, 7, 8, 9, 10}; //Pines de los leds arduino
bool encendido[] = {0,0,0,0,0,0}; //Variables bool de cada led (1, encendido, 0, apagado)
bool prev_encendido[] = {0,0,0,0,0,0};
char info; //Informacion que se lee del serial (uno por uno)

void setup()
{
  Serial.begin(9600);
  servo_der.attach(3);
  servo_izq.attach(11);
  for (int i = 0; i < 6; i++)
    pinMode(pins[i], OUTPUT);
}

// Variables que cuentan los espacios y revisan si las acciones cambian de estado
int cont =0;
bool izq, der = false;


void loop()
{
  // Lee el serial y añade en su respectiva posicion el valor de encendido o apagado de cada pin
  if(Serial.available()!=0){
    char info = Serial.read();
    bool led = false;
    if (info == '1')
      led = true;
    encendido[cont] = led;
    cont +=1;    
  }

  // Banderas que revisan si el movimiento ha cambiado
  if(encendido[0] != prev_encendido[0])
    der= true;
  else
    der= false;
    
  if(encendido[1] != prev_encendido[1])
    izq= true;
  else
    izq= false;

  // Enciende los leds y asigna los valores actuales como previos (para verificar si se repiten las acciones)
  if (cont >6){
      cont = 0;
      for(int i = 0; i < 6; i++){
        if (encendido[i] == true)
          digitalWrite(pins[i], HIGH);                   

        else
          digitalWrite(pins[i], LOW);
        prev_encendido[i] = encendido[i];
      }
  }

  // Cambia de dirección los servos dependiendo de si la accion cambio de estado
  if (der==true){
    if(encendido[0] == true){
      servo_der.write(40);
      servo_der.write(150);
    }
    else
      servo_der.write(0);
  }
  if(izq==true){
    if(encendido[1] == true){
      servo_izq.write(40);
      servo_izq.write(150);
    }
    else
      servo_izq.write(0);    
  }

}
