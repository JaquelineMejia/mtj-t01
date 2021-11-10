#!/usr/bin/env python3

from numpy.lib.arraysetops import isin
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2
import numpy

def newOdom(msg):
    global x
    global y
    global theta

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

rospy.init_node("speed_controller")

sub = rospy.Subscriber("/odom", Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)

speed = Twist()

r = rospy.Rate(4)
x = 0.0
y = 0.0

theta = 0.0

goal = Point()

paso = 1
goal.x = float(input("Escribe la coordenada en x --> "))
goal.y = float(input("Escribe la coordenada en y --> "))

while not rospy.is_shutdown():
    inc_x = goal.x -x
    inc_y = goal.y -y
   
    angle_to_goal = atan2(inc_y, inc_x)

    if abs(angle_to_goal - theta) > 0.1:
        speed.linear.x = 0.0
        speed.angular.z = 0.3
    else:
        speed.linear.x = 0.1
        speed.angular.z = 0.0

    tol_x = abs(goal.x - inc_x)
    tol_y = abs(goal.y - inc_y)
    rango_x = numpy.arange(3-0.4,3+0.4,0.1)
    rango_y = numpy.arange(3-0.4,3+0.4,0.1)
    if inc_x in rango_x or inc_y in rango_y:
        speed.linear.x = 0.0
        speed.angular.z = 0.0
        print("Hemos llegado a las coordenadas x = %s, y = %s",goal.x,goal.y)
        aux = input("¿Quieres coordenadas nuevas? [S/s][N/n]")
        if aux == 'n' or aux == 'N':
            exit()
        else:
            goal.x = int(input("Escribe la coordenada en x --> "))
            goal.y = int(input("Escribe la coordenada en y --> "))

    pub.publish(speed)
    r.sleep()