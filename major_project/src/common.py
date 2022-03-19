import rospy  # Main ROS stuff
import math  # Math
import random  # Uniform distributions
from signal import signal, SIGINT  # Control-C handler
from geometry_msgs.msg import Twist, Vector3, PoseStamped, PoseWithCovarianceStamped  # Movement
from nav_msgs.msg import Odometry  # Odometry
from kobuki_msgs.msg import BumperEvent  # Bumper
from sensor_msgs.msg import LaserScan  # Laser/Ranging info
import numpy as np
import actionlib
from actionlib_msgs.msg import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

priorityLevel = 7
rate = rospy.Rate(10)  # 10 Hz

# Publishers
velPub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)  # Allow us to send velocity commands
goalPub = actionlib.SimpleActionClient("move_base", MoveBaseAction)
#goalPub.wait_for_server(rospy.Duration(5))
initPub = rospy.Publisher('initialpose', PoseWithCovarianceStamped, queue_size=1)


def initial_pos_pub():
    #Creating the message with the type PoseWithCovarianceStamped
    initial_pos = PoseWithCovarianceStamped()
    #filling header with relevant information
    initial_pos.header.frame_id = "map"
    #filling payload with relevant information gathered from subscribing
    # to initialpose topic published by RVIZ via rostopic echo initialpose
    initial_pos.pose.pose.position.x = 0.0
    initial_pos.pose.pose.position.y = 0.0
    initial_pos.pose.pose.position.z = 0.0

    initial_pos.pose.pose.orientation.x = 0.0
    initial_pos.pose.pose.orientation.y = 0.0
    initial_pos.pose.pose.orientation.z = 0.0
    initial_pos.pose.pose.orientation.w = 0.0

    rospy.loginfo(initial_pos)
    initPub.publish(initial_pos)
    return


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
