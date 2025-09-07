#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
from std_msgs.msg import Bool
import sys, select, termios, tty
import time

msg = """
Control Your WLKATA!
--------------------------------------
Wait until WLKATA Homing finished, 
and control the WLKATA!

Moving around:
        w         e
   a         d         h
        x         c         ./ 

w/x : increase/decrease X position
a/d : increase/decrease Y position
e/c : increase/decrease Z position(height)

h   : Homing

.,/ : open/close the gripper
 
CTRL-C to quit
"""

def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class PoseNode(Node):
    def __init__(self):
        super().__init__('pose_node')

        self.pub_pose = self.create_publisher(Pose, 'pose', 10)
        self.pub_gripper = self.create_publisher(Bool, 'gripper', 10)
        self.pub_homing = self.create_publisher(Bool, 'homing', 10)

        self.pose = Pose()
        self.pose.position.x = 198.6
        self.pose.position.y = 0.0
        self.pose.position.z = 230.4

        self.gripper = Bool()
        self.homing = Bool()

        self.timer = self.create_timer(0.1, self.timer_callback)
        self.settings = termios.tcgetattr(sys.stdin)
        self.get_logger().info(msg)
        time.sleep(1.0)
        self.homing.data = True
        self.pub_homing.publish(self.homing)

    def timer_callback(self):
        try:
            key = get_key(self.settings)
            if key == 'w':
                self.pose.position.x += 5.0
                self.pub_pose.publish(self.pose)
            elif key == 'x':
                self.pose.position.x -= 5.0
                self.pub_pose.publish(self.pose)
            elif key == 'a':
                self.pose.position.y += 5.0
                self.pub_pose.publish(self.pose)
            elif key == 'd':
                self.pose.position.y -= 5.0
                self.pub_pose.publish(self.pose)
            elif key == 'e':
                self.pose.position.z += 5.0
                self.pub_pose.publish(self.pose)
            elif key == 'c':
                self.pose.position.z -= 5.0
                self.pub_pose.publish(self.pose)
            elif key == 'h':
                self.homing.data = True
                self.pub_homing.publish(self.homing)
            elif key == '.':
                self.gripper.data = True
                self.pub_gripper.publish(self.gripper)
            elif key == '/':
                self.gripper.data = False
                self.pub_gripper.publish(self.gripper)
            elif key == '\x03':  # CTRL-C
                rclpy.shutdown()
        except Exception as e:
            self.get_logger().error(f"Exception in timer_callback: {e}")
            rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = PoseNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
