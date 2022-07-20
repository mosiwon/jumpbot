from turtle import delay
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from std_msgs.msg import Float64MultiArray

class Self_balancing(Node):
    
    def __init__(self):
        super().__init__('Self_balancing')
        queue_size = 10 
        self.subsriber=self.create_subscription(
            Float64MultiArray,'/demo/pid_protocol',self.pid_topic_callback,queue_size)
        
    def pid_topic_callback(self,msg):
        self.get_logger().info('***OK set value!***')
        
        
        pid_state=msg.data    ##pid subs
        self.get_logger().info('kp %f   , ki %f  , kd %f   ,pitch_desired %f  ' % (pid_state[0],pid_state[1],pid_state[2],pid_state[3]))
    

def main():
    rclpy.init()
    node = Self_balancing()
    rclpy.spin(node)


if __name__ == '__main__':
    main()