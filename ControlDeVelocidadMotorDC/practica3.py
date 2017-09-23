#!/usr/bin/python
import RPi.GPIO as GPIO
import time

#Entradas.
pinVB = 18
pinVA = 15
pinH = 23
pinSS = 24

#Salidas.
pinM1 = 20
pinM2 = 21
d1 = 0
d2 = 0
d3 = 0 

#Parametros de la modulacion de ancho de pulso.
frec = 50 #Frecuencia del PWM.
dc = 50 #Valor inicial de Duty Cycle
stop = True #Variable Bandera de Stop
giro = True #Variable Bandera de sentio de giro

#Configuraciones de puertos generales de entrada y salida.
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pinVB,GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Se configuran las entradas para que esten 
GPIO.setup(pinVA,GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #en pulldown por defecto a nivel de software.
GPIO.setup(pinH,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pinSS,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pinM1,GPIO.OUT)
GPIO.setup(pinM2,GPIO.OUT)

p = GPIO.PWM(pinM1, frec) #Creacion de un objeto de la clase PWM.

#Programacion de Eventos.

#Subprograma que enciende o apaga el motor.
def startStop(channel):
	global stop
	if (stop):
		p.start(dc)
		print("El motor esta encendido")
	else:
		p.stop()
		print("El motor esta detenido")
	
	stop = not stop

#Subprograma que aumenta la velocidad del motor
def subirVelocidad(channel):
	global dc
	global p
	if (dc < 100):
		dc = dc + 5
		p.ChangeDutyCycle(dc)
		print("Duty Cycle: " + str(dc))
	else:
		print("No se puede aumentar mas la velocidad")

#Subprograma que disminuye la velocidad del motor
def bajarVelocidad(channel):
	global dc
	global p
	if (dc > 0):
		dc = dc - 5
		p.ChangeDutyCycle(dc)
		print("Duty Cycle: " + str(dc))
	else:
		print("No se puede disminuir mas la velocidad")


#Subprograma que cambia el sentido de giro del motor
def ghah(channel):
	global dc
	global p
	global stop
	global giro
	p.stop()
	if giro == True:
		p = GPIO.PWM(pinM2, frec)
		print("Sentido Antihorario")
	else:
        	p = GPIO.PWM(pinM1, frec)
        	print("Sentido Horario")
	
	giro = not giro
	time.sleep(3)
	if stop == False:
		p.start(dc)
	


#Configuracion Hardware/Evento
#GPIO.add_event_detect(puerto que produce la interrupcion, flanco a detectar, subprograma a llamar, tiempo de rebote)
GPIO.add_event_detect(pinVB, GPIO.RISING, callback = bajarVelocidad, bouncetime=200)
GPIO.add_event_detect(pinVA, GPIO.RISING, callback = subirVelocidad, bouncetime=200)
GPIO.add_event_detect(pinH, GPIO.RISING, callback = ghah, bouncetime=200)
GPIO.add_event_detect(pinSS, GPIO.RISING, callback = startStop, bouncetime=200) 


#Programa Principal
try:
	print("Practica 3")
	while True:
				
		pass

except KeyboardInterrupt:
	pass
p.stop()
GPIO.cleanup()
	

