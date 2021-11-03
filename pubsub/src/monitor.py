#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
from pubsub.msg import Status

def process_msg_callback(msg): #round redondea los gigitos a dos
    dx = round(msg.twist.twist.linear.x, 2) #se entra desde el osometry para ver las variables
    # Debido a que nuestro robot es (2,0) no puede moverse sobre el eje Y
    #dy = msg.twist.twist.linear.y #rosmsg info nav_msgs/Odometry
    tetha = round(msg.twist.twist.angular.z, 2)
    rospy.loginfo('Actualmente el robot tiene dx = {:.2f} m/s, tetha = {:.2f} radianes'.format(dx,tetha))
    if dx == 0.0 and tetha == 0.0:
        pubmsg.codigo = 0
        pubmsg.estado = 'Detenido'
    elif dx != 0.0 and tetha == 0.0:
        pubmsg.codigo = 100
        pubmsg.estado = 'Solo velocidad lineal {} m'.format(dx)
    elif dx == 0.0 and tetha != 0.0:
        pubmsg.codigo = 200
        pubmsg.estado = 'Solo velocidad angular {} rad'.format(tetha)
    elif dx != 0.0 and tetha != 0.0:
        pubmsg.codigo = 100
        pubmsg.estado = 'Movimiento angular {} rad y lineal {} m'.format(tetha,dx)
    else:
        pubmsg.codigo= 1000
        pubmsg.estado = 'Error'
    pub.publish(pubmsg)
   # rate.sleep() #ciclo de refresh
    #rospy.spin() #indica al sub volver a girar reiniciar el subscriptor

rospy.init_node('monitor')
sub = rospy.Subscriber('odom', Odometry, process_msg_callback)
pub = rospy.Publisher('status', Status, queue_size=2)
rate = rospy.Rate(2)
pubmsg = Status()
rospy.spin()

#if __name__ == "__main__":
 #   init_monitor()