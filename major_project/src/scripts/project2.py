#!/usr/bin/env python

import rospy  # Main ROS stuff
from signal import signal, SIGINT  # Control-C handler
from geometry_msgs.msg import Twist, Vector3  # Movement
from nav_msgs.msg import Odometry  # Odometry
from kobuki_msgs.msg import BumperEvent  # Bumper
from sensor_msgs.msg import LaserScan  # Laser/Ranging info

rospy.init_node('project2', anonymous=True)  # One big node for everything. Probably not the best.
import common
import TeleHandler
import BumpHandler
import ObstacleHandler
import OdometryHandler
import ForwardHandler

# Listeners
odoListen = rospy.Subscriber("/odom", Odometry, OdometryHandler.OdometryHandler().handle)  # Odometry
scanListen = rospy.Subscriber("/scan", LaserScan, ObstacleHandler.ObstacleHandler().handle, queue_size=1)  # Laser scanner
teleListen = rospy.Subscriber("/cmd_vel_mux/input/teleop", Twist, TeleHandler.TeleHandler().handle)
bumpListen = rospy.Subscriber("/mobile_base/events/bumper", BumperEvent, BumpHandler.BumpHandler().handle)  # The bumper


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
        while not rospy.is_shutdown() and common.priorityLevel >= 0:  # Negative priority indicates we've stopped. Zero priority is a collision - so we shutdown for safety
            forwardsHandler.handle()  # Attempt to move forwards
    except rospy.ROSInterruptException:
        pass
