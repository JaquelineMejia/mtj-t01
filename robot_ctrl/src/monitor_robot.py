#!/usr/bin/env python3
import rospy as ros
from gazebo_msgs.srv import GetWorldProperties
from gazebo_msgs.srv import GetModelState

class GazeboUtils(object):
    def __init__(self):
        pass
    def getWorldProperties(self):
        #Llamar a servicio siempre entre un try catch
        try:#proxy un camino de conexion de una red (llamada a traves de la red a traves de un servicio)
            get_world_propeties = ros.ServiceProxy('/gazebo/get_world_properties', GetWorldProperties)
            wp = get_world_propeties()
            if wp.success:
                return wp #retorna el objeto
            else:
                ros.logwarn(wp.status_message)
                return None
        except ros.ServiceException as e:
            ros.logerr('Al llamar /gazebo/get_world_properties: %s'%e)

    def getModelState(self, model_name, relative_entity_name= 'world'):
        try:
            get_model_state = ros.ServiceProxy('/gazebo/get_model_state', GetModelState)
            ms = get_model_state(model_name, relative_entity_name)
            if ms.success:
                return ms
            else:
                ros.logerr(ms.status_message)
                return None

        except ros.ServiceException as e:
            ros.logerr("Al llamar /gazebo/get_model_state: %s"%e)

    def get_model_Pose(self, model_name):
        ms = self.getModelState(model_name)
        if ms:
            return ms.pose
        else: 
            return None


def test_services():
    gazebo_utils = GazeboUtils()
    exclude = ['ground_plane', 'turtlebot3_waffle']# NO ME INTERESA CONOCERplano de tierra y la otra de robot
    landmarks = {} #diccionario vacio
    print('Probando GazeboUtils, get_world_properties service:')
    wp = gazebo_utils.getWorldProperties()
    if wp:
        for model in wp.model_names:#va ir cambiando
            if model not in exclude:
                ms = gazebo_utils.get_model_Pose(model)
                if ms:
                    position = (ms.position.x, ms.position.y)
                    landmarks.update({model: position})
                else:
                    print("Fallo la llamada al servicio /gazebo/get_model_state:")
        return landmarks
    else:
         print("Fallo la llamada al servicio /gazebo/get_model_properties")
         return None

if __name__ == '__main__':
    landmarks= test_services()
    if landmarks:
        print(landmarks)
    else:
        print("Fallo al final")