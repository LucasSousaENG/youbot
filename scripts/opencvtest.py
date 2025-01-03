#codigo teste para conectar a simulacao e testar o opencv na aquisicao das imagens

import rospy

# Initialize the ROS Node named 'opencv_example', allow multiple nodes to be run with this name
rospy.init_node('opencv_example', anonymous=True)

# Print "Hello ROS!" to the Terminal and ROSLOG
rospy.loginfo("Hello ROS!")