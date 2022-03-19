import common
import rospy  # Main ROS stuff
import math  # Math
import random  # Uniform distributions
from signal import signal, SIGINT  # Control-C handler
from geometry_msgs.msg import Pose, PoseStamped, Quaternion, Point  # Movement
import actionlib
from actionlib_msgs.msg import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Header
from nav_msgs.msg import Odometry  # Odometry
from kobuki_msgs.msg import BumperEvent  # Bumper
from sensor_msgs.msg import LaserScan  # Laser/Ranging info
import numpy as np


class VoiceHandler:

    def handle(self, pocket_sphinx_command):
        commands = {"stop": Pose(), "take me to dumpster": Pose(Point(3.5, -4, 0), Quaternion(0, 0, 0, 1)),
                    "take me to cylinder": Pose(Point(-0.5, -2, 0), Quaternion(0, 0, 0, 1)),
                    "take me to cube": Pose(Point(6.5, 0, 0), Quaternion(0, 0, 0, 1)),
                    "take me to bookshelf": Pose(Point(1.5, 2.2, 0), Quaternion(0, 0, 0, 1))}  # commands should be lower case
        command = pocket_sphinx_command.data.strip()
        rospy.loginfo("Beginning voice processing. Priority is %s" % common.priorityLevel)
        if len(command) > 0 and command in commands and common.priorityLevel == 7:  # The command should always have a value but it never hurts to be safe
            rospy.loginfo("Voice command received: %s" % command)

            common.priorityLevel = 6
            ps = MoveBaseGoal()
            ps.target_pose.header = Header()
            ps.target_pose.header.stamp = rospy.Time.now()
            ps.target_pose.header.frame_id = "map"
            ps.target_pose.pose = commands[command]

            if common.priorityLevel == 6:
                rospy.loginfo("Sending goal pose to publisher")
                common.goalPub.send_goal(ps)
                success = common.goalPub.wait_for_result(rospy.Duration(60))
                state = common.goalPub.get_state()
                if not success or state != GoalStatus.SUCCEEDED:
                    rospy.loginfo("Navigation error!")
                    common.goalPub.cancel_goal()
                common.priorityLevel = 7


