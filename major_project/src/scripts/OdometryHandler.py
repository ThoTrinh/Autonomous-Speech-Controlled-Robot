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


class OdometryHandler():
    # Class Vars
    previousPos = None  # Store this here to keep it persistent
    distanceTraveled = 0  # Also here for persistence

    # Handle odometry data
    def handle(self, data):
        curPos = data.pose.pose.position  # Our position

        if common.priorityLevel != 5:  # Allow higher priorities to override
            return

        if not self.previousPos:  # Do we have a previous position?
            self.previousPos = curPos  # Seems like we just started. Set initial previous pos
            return  # No movement yet

        x2 = curPos.x
        x1 = self.previousPos.x

        dist = math.sqrt(abs(x2 * x2 - x1 * x1))  # Distance traveled in meters
        dist *= 3.28084  # convert to feet

        rospy.loginfo('Distance traveled = %s' % self.distanceTraveled)
        rospy.loginfo("new dist: %f" % dist)
        self.distanceTraveled += dist

        if self.distanceTraveled >= 1:  # Every foot of movement, we:
            common.priorityLevel = 4

            common.uniformTurn(-15, 15, bool(random.getrandbits(1)))
            # This would be a uniform turn, but we want to keep moving while doing this
            # theta = random.uniform(-15, 15)
            # xVelAng = math.cos(theta * (math.pi / 180)) #Some questionable trig to get x and z velocities
            # zVelAng = math.sin(theta * (math.pi / 180))
            #
            # for i in range(10) : #Based on our usual turn speeds, this should be enough time at 10Hz
            # if common.priorityLevel < 4: # More important stuff can stop this turn though!
            # return
            # rospy.loginfo("Priority level %s" % common.priorityLevel)
            # turnTwist = Twist()
            # turnTwist.linear.x = 0.2 # We want to keep moving forward a little during this
            # turnTwist.linear.y = 0
            # turnTwist.linear.z = 0
            # turnTwist.angular.x = xVelAng
            # turnTwist.angular.y = 0
            # turnTwist.angular.z = zVelAng
            #
            # velPub.publish(turnTwist)
            #
            common.rate.sleep()  # Maintain 10Hz command common.rate

            self.distanceTraveled = 0  # Reset distance
            if common.priorityLevel == 4:  # If we weren't interrupted by something, restore to previous level
                common.priorityLevel = 5
        self.previousPos = curPos  # Update the previousPosition
