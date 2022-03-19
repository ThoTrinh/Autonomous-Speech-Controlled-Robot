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


class BumpHandler():

    def handle(self, data):
        # https://canvas.harvard.edu/courses/37276/pages/getting-started-2-ros-turtlebot-sensors-and-code
        if data.state == BumperEvent.PRESSED:  # We hit something
            haltTwist = Twist()  # By default, Twist has 0 velocity
            common.priorityLevel = 0  # Most important priority. Will stop all other execution
            common.velPub.publish(haltTwist)  # Stop the bot
            rospy.loginfo("BUMPER HIT!!!")
