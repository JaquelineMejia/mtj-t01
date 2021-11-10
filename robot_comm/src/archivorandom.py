#!/usr/bin/env python3

from re import sub
from threading import current_thread
from nav_msgs import msg
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
import math



def inicio(): # Creamos una funcion para inicializar todo
    odom_msg = None
    current_position = None
    while odom_msg is None:
        try:
            odom_msg = rospy.wait_for_message('/odom',Odometry,timeout=10)
        except Exception as e:
            rospy.logerr(str(e))
            exit()

    current_position = odom_msg.pose.pose.position #Guardamos el valor de la posicion
    
    return current_position

def callback_llamada(msg):
    current_position = msg.pose.pose.position

def extrae_plano(position):
    return (position.x, position.y)


sub = rospy.Subscriber('/odom',Odometry,callback_llamada)

while not rospy.is_shutdown():
    rospy.init_node('monitor')
    pos = extrae_plano(inicio())
    print('Estamos en la coordenada x = ',round(pos[0],4),' y = ',round(pos[1],4))

