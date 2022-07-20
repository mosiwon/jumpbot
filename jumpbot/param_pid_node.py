from turtle import delay
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from std_msgs.msg import Float64MultiArray

class MinimalParam(Node):
    
    def __init__(self):
        super().__init__('param_pid_node')
        timer_period = 2  # second
        
        queue_size = 10 
        
        self.declare_parameter('kp', 0.0)   ##default
        self.declare_parameter('ki', 0.0)
        self.declare_parameter('kd', 0.0)
        self.declare_parameter('pitch_desired', 0.0)
        self.declare_parameter('send', False)
        
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.pid_publisher = self.create_publisher(Float64MultiArray, '/demo/pid_protocol', queue_size)
        
    def timer_callback(self):
        kp = self.get_parameter('kp').get_parameter_value().double_value
        ki = self.get_parameter('ki').get_parameter_value().double_value
        kd = self.get_parameter('kd').get_parameter_value().double_value
        pitch_desired = self.get_parameter('pitch_desired').get_parameter_value().double_value
        send = self.get_parameter('send').get_parameter_value().bool_value
        
        value=[kp,ki,kd,pitch_desired]
        
        msg=Float64MultiArray()
        msg.data=value
     
        self.get_logger().info('kp %f   , ki %f  , kd %f   ,pitch_desired %f  ' % (kp,ki,kd,pitch_desired))
        
        if send==True:
            self.get_logger().info('***send value!***')
            self.pid_publisher.publish(msg)
            
            
        my_new_param=rclpy.parameter.Parameter(
            'send',rclpy.Parameter.Type.BOOL,False
        )
        all_new_parameters = [my_new_param]
        self.set_parameters(all_new_parameters)
        
        
    

def main():
    rclpy.init()
    node = MinimalParam()
    rclpy.spin(node)


if __name__ == '__main__':
    main()