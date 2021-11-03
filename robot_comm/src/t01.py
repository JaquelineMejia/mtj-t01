#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios

vel_lin_max = 1
vel_ang_max = 2

LIN_VEL_STEP_SIZE = 0.5
ANG_VEL_STEP_SIZE = 0.5

msg = """
Control Your TurtleBot3!
---------------------------
Moving around:
            avanza
    gira    detente    d
               x
space key, s : force stop
CTRL-C to quit
"""

e = """
Fallo la comunicacion
"""

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
      vel = constrain(vel, -vel_lin_max, vel_lin_max)
    return vel

def checkAngularLimitVelocity(vel):
    if turtlebot3_model == "waffle" or turtlebot3_model == "waffle_pi":
      vel = constrain(vel, -vel_ang_max, vel_ang_max)
    return vel

if __name__=="__main__":

    try:
        #inicializamos el nodo
        rospy.init_node('turtlebot3_teleop') 
        #declaracion del publicador 
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=10) 

        # Obtenemos el modelo de turtlebot (waffle)
        turtlebot3_model = rospy.get_param("model", "burger")

        # Inicializamos nuestras variables para no tener errores
        status = 0
        target_linear_vel   = 0.0
        target_angular_vel  = 0.0
        control_linear_vel  = 0.0
        control_angular_vel = 0.0

        try:
            print(msg)
            print("Hola, por favor ingres la accion que deseas:\n\n")
            while(1):
                key = input() #Cachamos la variable para la instruccion

                # Preguntamos la accion y dependiendo de eso hacemos lo que nos indica
                if key == 'Avanza' or key == "avanza" :
                    target_linear_vel = checkLinearLimitVelocity(target_linear_vel + LIN_VEL_STEP_SIZE)
                    status = status + 1
                    print("Estamos avanzando")
                elif key == 'Gira' or key == "gira" :
                    target_angular_vel = checkAngularLimitVelocity(target_angular_vel + ANG_VEL_STEP_SIZE)
                    status = status + 1
                    print("Estamos girando")
                elif key == 'Detente' or key == 'detente' :
                    target_linear_vel   = 0.0
                    control_linear_vel  = 0.0
                    target_angular_vel  = 0.0
                    control_angular_vel = 0.0
                    print("Estamos detenidos, nos tiro la ley")
                else:
                    exit()

                twist = Twist()

                control_linear_vel = makeSimpleProfile(control_linear_vel, target_linear_vel, (LIN_VEL_STEP_SIZE/2.0))
                twist.linear.x = control_linear_vel; twist.linear.y = 0.0; twist.linear.z = 0.0

                control_angular_vel = makeSimpleProfile(control_angular_vel, target_angular_vel, (ANG_VEL_STEP_SIZE/2.0))
                twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = control_angular_vel

                pub.publish(twist)

        except:
            print(e)

        finally:
            twist = Twist()
            twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
            pub.publish(twist)
    
    except rospy.ROSInterruptException:
        pass