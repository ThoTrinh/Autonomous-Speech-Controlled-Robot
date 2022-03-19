#!/usr/bin/env python

import rospy  # Main ROS stuff
from signal import signal, SIGINT  # Control-C handler
from geometry_msgs.msg import Twist, Vector3  # Movement
from nav_msgs.msg import Odometry  # Odometry
from kobuki_msgs.msg import BumperEvent  # Bumper
from sensor_msgs.msg import LaserScan  # Laser/Ranging info
from std_msgs.msg import String

rospy.init_node('major-project', anonymous=True)  # One big node for everything. Probably not the best.
import common
import TeleHandler
import BumpHandler
import ObstacleHandler
import OdometryHandler
import ForwardHandler
import VoiceHandler

# Listeners
odoListen = rospy.Subscriber("/odom", Odometry, OdometryHandler.OdometryHandler().handle)  # Odometry
scanListen = rospy.Subscriber("/scan", LaserScan, ObstacleHandler.ObstacleHandler().handle, queue_size=1)  # Laser scanner
teleListen = rospy.Subscriber("/cmd_vel_mux/input/teleop", Twist, TeleHandler.TeleHandler().handle)
bumpListen = rospy.Subscriber("/mobile_base/events/bumper", BumperEvent, BumpHandler.BumpHandler().handle)  # The bumper
voiceListen = rospy.Subscriber("voice_input", String, VoiceHandler.VoiceHandler().handle)  # The bumper


# Detect control-c. This lets us break infinite loops more easily
def exitHandler(signal, frame):
    common.priorityLevel = -1  # This should stop most everything within a few ticks
    print("Control-C!")
    rospy.signal_shutdown("Control-C")
    exit(0)  # Kill the program


forwardsHandler = ForwardHandler.ForwardHandler()

if __name__ == '__main__':
    try:
        signal(SIGINT, exitHandler)
        common.initial_pos_pub()
        common.priorityLevel = 7
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
