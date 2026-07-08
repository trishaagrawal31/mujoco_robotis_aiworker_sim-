import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import mujoco
import mujoco.viewer
import time

class RobotisMujocoBridge(Node):
    def __init__(self):
        super().__init__('robotis_mujoco_bridge')

        # Load the ROBOTIS model directly from your cloned directory
        self.model = mujoco.MjModel.from_xml_path('/home/trisha/Desktop/MuJoCo/robotis_mujoco_menagerie/robotis_ffw/scene_ffw_sg2.xml')
        self.data = mujoco.MjData(self.model)

        # ROS 2 Publisher for Joint States
        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)

        # Launch the interactive native MuJoCo viewer in a non-blocking mode
        self.viewer = mujoco.viewer.launch_passive(self.model, self.data)

        # Create a simulation step timer (e.g., 100Hz)
        self.timer = self.create_timer(0.01, self.sim_step)

    def sim_step(self):
        if self.viewer.is_running():
            # Step the physics engine
            mujoco.mj_step(self.model, self.data)

            # Sync physics data with the visualizer window
            self.viewer.sync()

            # Example: Publish the joint states to ROS
            msg = JointState()
            msg.header.stamp = self.get_clock().now().to_msg()
            # Fill msg.name, msg.position, etc. using self.data.qpos
            self.joint_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = RobotisMujocoBridge()
    rclpy.spin(node)
    node.viewer.close()
    rclpy.shutdown()

if __name__ == '__main__':
    main()