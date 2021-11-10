#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

distancia_obstaculo = 1

def callback(msg):
    rospy.loginfo(rospy.get_caller_id() + "distancia para el obstaculo %s", msg.ranges[300])

    if msg.ranges[300] >= distancia_obstaculo:
        move.linear.x = 0.5
        move.angular.z = 0.0

    if msg.ranges[300] <= distancia_obstaculo:
        move.linear.x = 0.0
        move.angular.z = 1

    pub.publish(move)

rospy.init_node('node')
sub = rospy.Subscriber('/scan', LaserScan, callback)
pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=2)
rate = rospy.Rate(2)
move = Twist()

rospy.spin()
