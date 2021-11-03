#!/usr/bin/env python3
import rospy
from pubsub.msg import Status

def publisher():
    pub = rospy.Publisher('pubtopic', Status, queue_size=10)
    rospy.init_node('pubnode', anonymous=False)
    r = rospy.Rate(10)
    valor=0
    msg = Status()
    msg.estado ='Ok'
    msg.codigo = 0

    while not rospy.is_shutdown():
        msg.codigo = msg.codigo+1
        rospy.loginfo(msg)
        pub.publish(msg)
        r.sleep()

if __name__ == "__main__":
    publisher()