import common
import rospy  # Main ROS stuff
import math  # Math
import random  # Uniform distributions
from signal import signal, SIGINT  # Control-C handler
from geometry_msgs.msg import Twist, Vector3  # Movement
from nav_msgs.msg import Odometry  # Odometry
from kobuki_msgs.msg import BumperEvent  # Bumper
from sensor_msgs.msg import LaserScan  # Laser/Ranging info
import numpy as np


class ForwardHandler():

    # Move forward. Forever. Unless something important happens
    def handle(self):

        forward_msg = Twist()
        forward_msg.linear.x = 0.2  # Slow forwards velocity
        forward_msg.linear.y = 0
        forward_msg.linear.z = 0
        forward_msg.angular.x = 0
        forward_msg.angular.y = 0
        forward_msg.angular.z = 0

        if common.priorityLevel == 5:  # we're good to go!
            rospy.loginfo("Setting forward velocity. pLevel = %s" % common.priorityLevel)
            common.velPub.publish(forward_msg)
            common.rate.sleep()
