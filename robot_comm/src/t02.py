#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist,Point
import sys, select, os
from nav_msgs.msg import Odometry
from pubsub.msg import Status

from re import sub
from threading import current_thread
from nav_msgs import msg
import rospy
import math

WAFFLE_MAX_LIN_VEL = 1
WAFFLE_MAX_ANG_VEL = 2

LIN_VEL_STEP_SIZE = 0.5
ANG_VEL_STEP_SIZE = 0.5

msg = """
Controla tu robot!
---------------------------
Comandos de movimiento:

Escribe la coordenada en X a la que quieres llegar

Escribe la coordenada en Y a la que quieres llegar

Escribe "Exit" o "exit" para salir del programa
"""

e = """Fallo la comunicacion"""

def makeSimpleProfile(output, input, slop):
    if input > output:
        output = min( input, output + slop)
    elif input < output:
        output = max( input, output - slop)
    else:
        output = input

    return output

def constrain(input, low, high):
    if input < low:
      input = low
    elif input > high:
      input = high
    else:
      input = input

    return input

def checkLinearLimitVelocity(vel):
    if turtlebot3_model == "waffle" or turtlebot3_model == "waffle_pi":
      vel = constrain(vel, -WAFFLE_MAX_LIN_VEL, WAFFLE_MAX_LIN_VEL)
    return vel

def checkAngularLimitVelocity(vel):
    if turtlebot3_model == "waffle" or turtlebot3_model == "waffle_pi":
      vel = constrain(vel, -WAFFLE_MAX_ANG_VEL, WAFFLE_MAX_ANG_VEL)
    return vel

def vel_new(control_linear_vel,control_angular_vel):
    twist = Twist()
    control_linear_vel = makeSimpleProfile(control_linear_vel, target_linear_vel, (LIN_VEL_STEP_SIZE/2.0))
    twist.linear.x = control_linear_vel; twist.linear.y = 0.0; twist.linear.z = 0.0
    control_angular_vel = makeSimpleProfile(control_angular_vel, target_angular_vel, (ANG_VEL_STEP_SIZE/2.0))
    twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = control_angular_vel
    pub.publish(twist)


# .................. Nuevas funciones ..................

def inicio(): # Creamos una funcion para inicializar todo
    odom_msg = None
    current_position = None
    while odom_msg is None:
        try:
            odom_msg = rospy.wait_for_message('/odom',Odometry,timeout=10)
        except Exception as e:
            rospy.logerr(str(e))
            #exit()

    current_position = odom_msg.pose.pose.position #Guardamos el valor de la posicion
    
    return current_position

def callback_llamada(msg):
    current_position = msg.pose.pose.position

def extrae_plano(position):
    return (position.x, position.y)

if __name__=="__main__":
    rospy.init_node('turtlebot3_teleop')
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    #rospy.init_node('monitor')
    sub = rospy.Subscriber('/odom',Odometry,callback_llamada)

    # Obtenemos el modelo de turtlebot (waffle)
    turtlebot3_model = rospy.get_param("model", "waffle")

    # Inicializamos nuestras variables para no tener errores
    status = 0
    target_linear_vel   = 0.0
    target_angular_vel  = 0.0
    control_linear_vel  = 0.0
    control_angular_vel = 0.0


    #Comenzamos a pedir nuetras variables
    try:
        print(msg)
        print("\n\nIngresa las coordenadas (X,Y) que deseas\n\n")
        while(1):
            # Pedimos las coordenadas en X y Y
            keyx=int(input("Coordenada en X --> "))
            keyy=int(input("Coordenada en Y --> "))

            #Obtnemos las coordenadas en las que nos encontramos
            pos = extrae_plano(inicio())
            posx=round(pos[0],4)
            posy=round(pos[1],4)

            # Preguntamos la accion y dependiendo de eso hacemos lo que nos indica
            while (keyx != posx):

                # La variable posx es la que nos dice donde nos encontramos respecto a x
                if posx < keyx: # Si la coordenada en x es negativa vamos hacia delante
                    target_linear_vel = checkLinearLimitVelocity(target_linear_vel + LIN_VEL_STEP_SIZE)
                    status = status + 1
                elif posx > keyx: # Si la coordenada en x es positiva vamos hacia atras
                    target_linear_vel = checkLinearLimitVelocity(target_linear_vel - LIN_VEL_STEP_SIZE)
                    status = status + 1

                if keyx == posx: # Si hemos llegado a la posicion que queremos, nos detenemos
                    print("Hemos llegado a la coordenada en x")
                    target_linear_vel   = 0.0
                    control_linear_vel  = 0.0
                    target_angular_vel  = 0.0
                    control_angular_vel = 0.0

                # Iniciamos la parte donde reasignamos las nuevas velocidades                
                vel_new()

            while (keyy != posy):
                # La variable posy es la que nos dice donde nos encontramos respecto a y
                # La variable posx la podemos encontrar en uno de los programas hechos por el profesor
                
                if posy < keyy: # Si la coordenada en y es negativa vamos hacia la izquierda
                    target_angular_vel = checkAngularLimitVelocity(target_angular_vel + ANG_VEL_STEP_SIZE)
                    status = status + 1

                elif posy > keyy: # Si la coordenada en y es positiva vamos hacia la derecha
                    target_angular_vel = checkAngularLimitVelocity(target_angular_vel - ANG_VEL_STEP_SIZE)
                    status = status + 1

                if keyy == posy: # Si hemos llegado a la posicion que queremos, nos detenemos
                    print("Hemos llegado a la coordenada en y")
                    target_linear_vel   = 0.0
                    control_linear_vel  = 0.0
                    target_angular_vel  = 0.0
                    control_angular_vel = 0.0
                
                # Iniciamos la parte donde reasignamos las nuevas velocidades                
                vel_new()

    except:
        print(e)

    finally:
        twist = Twist()
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)
