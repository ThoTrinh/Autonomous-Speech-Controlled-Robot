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


class ObstacleHandler():
    def handle(self, msg):
        ranges = msg.ranges  # Get ranges from laser scan
        if (min(
                msg.ranges)) <= 0.6 and common.priorityLevel != 2:  # Due to the minimum range + some buffer space, we check for items with 0.7 meters
            rospy.loginfo("Found min range: %f from %d entries" % (min(msg.ranges), len(msg.ranges)))
            right_dists = 0
            left_dists = 0
            for i in range(639, 320, -1):  # Space measured is approximately even, so we iterate over half the array
                l = ranges[i]
                r = ranges[639 - i]
                if np.isnan(l) or math.isnan(r):  # If one side is nan, remove that pair
                    continue
                left_dists += l
                right_dists += r
            asymmetry = left_dists - right_dists  # Are we asymetric?
            # print(ranges)
            print("Right dists is %s" % right_dists)
            print("left dists is %s" % left_dists)
            print("Asymmetry is %s" % asymmetry)
            if abs(asymmetry) < 30:
                self.escape()
            else:
                self.avoid(asymmetry)
        elif common.priorityLevel != 0:
            common.priorityLevel = 5

        return

    def avoid(self, asymmetry):
        if common.priorityLevel < 3:  # Allow lower levels to take over
            return
        common.priorityLevel = 3
        if asymmetry < 0:  # object is to the left
            common.uniformTurn(45, 45, True)
        else:
            common.uniformTurn(45, 45, False)
        common.rate.sleep()
        common.priorityLevel = 5

        return

    # Turn 180 +/- 30 degrees from symmetric obstacles
    def escape(self):
        common.priorityLevel = 2

        common.uniformTurn(150, 210, True)  # Turn 180 +- 30 degrees
        rospy.loginfo("Priority level %s" % common.priorityLevel)
        common.rate.sleep()
        common.priorityLevel = 5

        return
