#!/usr/bin/env python3

from numpy.lib.arraysetops import isin
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2
import numpy
from rospy.names import valid_name_validator_resolved
from sensor_msgs.msg import LaserScan
import time

# Generamos una funcion para obtener nuestra posicion en X y Y
def newOdom(msg):

    # Generamos variables globales para usarlas en cualquier lado
    global x
    global y
    global theta

    # Obtenemos la posicion en X y Y y las guardamos en las variables x,y
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    # Obtenemos la orientacioin del robot
    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])


# Generamos una funcion para poder hacer funcionar el sensor
def sensor_callback(msg):
    global wall
    wall = msg.ranges[300]

# Iniciamos el noto
rospy.init_node("speed_controller")

# Nos suscribimos y publicamos
sub = rospy.Subscriber("/odom", Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
sub_2 = rospy.Subscriber('/scan', LaserScan, sensor_callback)

# Ponemos todo en orden para inicializar las variables
speed = Twist()

r = rospy.Rate(4)
x = 0.0
y = 0.0
theta = 0.0
wall = 0.0
count = 0

# Asignamos la funcion Point() a una variable para tener comodidad al escribir
goal = Point()

# Pedimos por primera vez nuestros datos
goal.x = float(input('Escribe la coordenada en x --> '))
goal.y = float(input('Escribe la coordenada en y --> '))
# Preguntamos si queremos visualizar la posicion en la que se encuentra el robot
option = int(input("Deseas saber tus coordenadas? [S = 1][N = 0] --> "))


# Iniciamos el programa principal
while not rospy.is_shutdown():

    # Creamos la condicion donde imprimimos las coordenadas o no
    if option == 1:
        print('Estamos en la coordenada (',round(x,2),' , ',round(y,2),')')

    # Calculamos la distancia que existe entre las coordenadas actuales y las que asignamos
    inc_x = goal.x -x
    inc_y = goal.y -y

    #Calculamos el angulo que existe entre los puntos   
    angle_to_goal = atan2(inc_y, inc_x)

    #print(wall)
    #print(angle_to_goal)
    #print(round(inc_x,2),round(inc_y,2))
    if abs(angle_to_goal - theta) > 1:
        speed.linear.x = 0.0
        speed.angular.z = 0.3
    elif wall <= 1:
        print("Obstaculo")
        speed.linear.x = -0.3
        speed.angular.z = 0.0
        pub.publish(speed)
        time.sleep(2)
        speed.linear.x = 0.0
        speed.angular.z = 0.3
        pub.publish(speed)
        time.sleep(5)
        speed.linear.x = 0.5
        speed.angular.z = 0.0
        pub.publish(speed)
        time.sleep(6)
    else:
        speed.linear.x = 0.2
        speed.angular.z = 0.0

    # Creamos dos rangos que nos serviran como tolerancia para que el robot no se quede girando
    rango_x = numpy.arange(-0.05,0.05,0.01)
    rango_y = numpy.arange(-0.05,0.05,0.01)

    # Creamos la condicion donde preguntaremos si inc_x e inc_y estan dentro de nuestra tolerancia
    if round(inc_x,2) in rango_x and round(inc_y,2) in rango_y:
        # En caso de que si estemos en la tolerancia paramos el robot
        speed.linear.x = 0.0
        speed.angular.z = 0.0
        # Publicamos la velocidad a nuestro robot
        pub.publish(speed)
        r.sleep()
        print('Hemos llegado a las coordenadas [x = ',goal.x,'y = ',goal.y,']')
        
        # Creamos una variable para preguntar si queremos coordenadas nuevas
        aux = input('Quieres coordenadas nuevas? [S = 1][N = 0] --> ')
        if aux == 0 or aux == 0: # En caso de que no, entonces el programa terminara
            exit()
        elif aux == 1 or aux == 1: # En caso de que si, entonces pedimos los mismos datos de nuevo
            print("Va va va va ya estas, entonces vamos de nuevo 7u7r")
            goal.x = int(input('Escribe la coordenada en x --> '))
            goal.y = int(input('Escribe la coordenada en y --> '))
            option = int(input("Deseas saber tus coordenadas? [S = 1][N = 0] --> "))
        else:
            print('Ingresa bien lo que se pide por favor UnU, no seas malito :(')

 
    # Publicamos a nuestro robot la velocidad calculada

    pub.publish(speed)
    r.sleep()