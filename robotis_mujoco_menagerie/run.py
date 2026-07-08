import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import mujoco
import mujoco.viewer
import time

class RobotisMujocoBridge(Node):
    def __init__(self):
        super().__init__('robotis_mujoco_bridge')

        self.model = mujoco.MjModel.from_xml_path(
            '/home/trisha/Desktop/MuJoCo/robotis_mujoco_menagerie/robotis_ffw/scene_ffw_sg2.xml'
        )
        self.data = mujoco.MjData(self.model)

        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)
        self.viewer = mujoco.viewer.launch_passive(self.model, self.data)
        self.timer = self.create_timer(0.01, self.sim_step)

        self.step_count = 0
        self.target_steps = 800  # increase if it does not reach the table

    def sim_step(self):
        if self.viewer.is_running():
            # reset controls
            self.data.ctrl[:] = 0.0

            # drive straight forward until target steps reached
            if self.step_count < self.target_steps:
                self.data.ctrl[3] = 30.0   # left_wheel_drive
                self.data.ctrl[4] = 30.0   # right_wheel_drive
                self.data.ctrl[5] = 30.0   # rear_wheel_drive
                self.step_count += 1

            mujoco.mj_step(self.model, self.data)
            self.viewer.sync()

            msg = JointState()
            msg.header.stamp = self.get_clock().now().to_msg()
            self.joint_pub.publish(msg)
    

def main(args=None):
    rclpy.init(args=args)
    node = RobotisMujocoBridge()
    rclpy.spin(node)
    node.viewer.close()
    rclpy.shutdown()

if __name__ == '__main__':
    main()