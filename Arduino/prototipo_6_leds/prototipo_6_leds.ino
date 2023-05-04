int pins[] = {5, 6, 7, 8, 9, 10}; //Pines de los leds arduino
bool encendido[] = {0,0,0,0,0,0}; //Variables bool de cada led (1, encendido, 0, apagado)
char info; //Informacion que se lee del serial (uno por uno)

// estructura de los pines en la camara
/****************
 *  0    1    2 *
 *  5    4    3 *
 ****************
 */
 
void setup()
{
  Serial.begin(9600);
  // Inicializar leds como outputs
  for (int i = 0; i < 6; i++)
    pinMode(pins[i], OUTPUT);
  
}

int cont = 0; //Contador de la posicion actual del vector que se va a analizar
void loop()
{
  //  Lee el serial y añade en su respectiva posicion el valor de encendido o apagado de cada pin
  if(Serial.available()!=0){
    char info = Serial.read();
    bool led = false;
    if (info == '1')
      led = true;
    encendido[cont] = led;
    cont +=1;    
  }
  //Cuando el contador llega a la posicion final del vector, se reinicia y se encienden y apagan los leds correspondientes
  if (cont >6){
    cont = 0;
    //Serial.println("-----");
    for(int i = 0; i < 6; i++){
      if (encendido[i] == true)
        digitalWrite(pins[i], HIGH);
      else
        digitalWrite(pins[i], LOW);
      //Serial.print(encendido[i]);   
    }
    //Serial.println("acabo");
  }

  
}
