#!/usr/bin/env python3
import rospy
from pubsub.msg import Status


def subscriber():
    rospy.init_node('subscriber')
    sub = rospy.Subscriber('pubtopic', Status, func_callback)
    rospy.spin() #bloquea el nodo escuchando indef  

def func_callback(msg):
    rospy.loginfo('La informacion recibida fue codigo:{}-{}'.format(msg.codigo, msg.estado))

if __name__ == '__main__':
    subscriber()