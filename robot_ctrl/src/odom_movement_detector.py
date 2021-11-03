#!/usr/bin/env python3
import rospy as ros
import math
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point

class MovementDetector(object):
    def __init__(self) :
        """Inicializamos los valores de la clase"""
        self._moved_distance = Float64()
        self._moved_distance.data = 0.0
        self._current_position = Point()
        self.get_init_position()
        self.distance_moved_pub = ros.Publisher('/moved_distance', Float64, queue_size=1) #no deja espacio pa publicar
        self.distance_moved_sub = ros.Subscriber('/odom', Odometry, self.odom_callback)

    def get_init_position(self):
        data_odom = None
        while data_odom is None:
            try:
                data_odom = ros.wait_for_message('/odom',Odometry, timeout=1)#encierra en un ciclo de espera 
            except Exception as e:
                ros.logerr(e)
                #ros.loginfo("El topic odom no se encuentra activo, esperando.")
        self._current_position.x = data_odom.pose.pose.position.x
        self._current_position.y = data_odom.pose.pose.position.y
        self._current_position.z = data_odom.pose.pose.position.z

    def odom_callback(self, msg):
        newPosition = msg.pose.pose.position
        self._moved_distance.data += self.calculate_distance(newPosition, self._current_position)
        self.update_curpos(newPosition)
        if self._moved_distance.data < 0.000001:
            aux = Float64()
            aux.data = 0.0
            self.distance_moved_pub.publish(aux)
        else:
            self.distance_moved_pub.publish(self._moved_distance)

    def update_curpos(self, newPosition):
        self._current_position.x = newPosition.x
        self._current_position.y = newPosition.y
        self._current_position.z = newPosition.z
    
    def calculate_distance (self, newPosition, old_position):
        x2 = newPosition.x
        x1 = old_position.x
        y2 = newPosition.y  
        y1 = old_position.y
    #Esta fuincion nos ayuda para calcular la distancia
        dist = math.hypot(x2-x1, y2-y1)
        return dist
    
    def publish_moved_distance(self):
        #
        ros.spin()

if __name__ == '__main__':
    ros.init_node('movement_detector_node')
    mov_dec = MovementDetector()
    mov_dec.publish_moved_distance()