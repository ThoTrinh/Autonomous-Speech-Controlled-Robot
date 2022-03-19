import rospy  # Main ROS stuff
import math  # Math
import random  # Uniform distributions
from signal import signal, SIGINT  # Control-C handler
from geometry_msgs.msg import Twist, Vector3  # Movement
from nav_msgs.msg import Odometry  # Odometry
from kobuki_msgs.msg import BumperEvent  # Bumper
from sensor_msgs.msg import LaserScan  # Laser/Ranging info
import numpy as np

priorityLevel = 5
rate = rospy.Rate(10)  # 10 Hz

# Publishers
velPub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)  # Allow us to send velocity commands

def uniformTurn(a, b, cw):
    angular_speed = 2 * math.pi / 9  # degrees per second
    theta = random.uniform(a, b) * 2 * math.pi / 360  # uniform sample in degrees, convert to radians

    # Create an initially empty Twist
    turnTwist = Twist()
    turnTwist.linear.x = 0
    turnTwist.linear.y = 0
    turnTwist.linear.z = 0
    turnTwist.angular.x = 0
    turnTwist.angular.y = 0

    # Calculate angular velocity
    if cw:
        turnTwist.angular.z = -abs(angular_speed)
    else:
        turnTwist.angular.z = abs(angular_speed)

    t0 = rospy.Time.now().to_sec()
    current_angle = 0

    # Execute turn
    while current_angle < theta:
        # print("Current angle: %f, Theta: %f" % (current_angle, theta))
        velPub.publish(turnTwist)
        rate.sleep()
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed * (t1 - t0)  # Find completed portion of turn
    return
