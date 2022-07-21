#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 18:08:40 2017

@author: sezan92
"""
import sys,time
import rclpy
from rclpy.node import Node
## import pidcontrol as pid

from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32



class PID_Controller(object):
    '''
    General PID control class. 
    '''

    def __init__(self, Kp, Ki, Kd):
        '''
        Constructs a new PID_Controller object.
        '''
        
        # Parameters
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        
        # State variables
        self.Eprev = 0
        self.Stdt = 0
        self.t = 0
    def tune(self,KpNew,KiNew,KdNew):
        self.Kp = KpNew
        self.Ki = KiNew
        self.Kd = KdNew
    def getCorrection(self, target, actual, dt=1):
        '''
        Returns current PID correction based on target value and actual value.
        '''
              
        E = target - actual
    
        # dE / dt
        dEdt = (E - self.Eprev) / dt if self.t > 0 else 0
        
        #if abs(dEdt) > 1: # XXX Why?
        #    dEdt = 0 # XXX Why?
        
        # Integral E / dt XXX not how you actually integrate
        self.Stdt += E*dt if self.t > 0 else 0# (E + self.Eprev)*dt if self.t > 0 else 0
   
        # Correcting

        correction = self.Kp*E + self.Ki*self.Stdt + self.Kd*dEdt
    
        # Update
        self.t += 1
        self.Eprev = E

        return correction
    


Kp =25
Ki =0.8
Kd =0.1


pubx = PID_Controller(Kp,Ki,Kd)
Yaw_Topic = "/demo/yaw"
cmd_vel = "/demo/cmd_vel"
Imu_topic = "/demo/imu"
Kp_topic = "/demo/Kp"
Ki_topic ="/demo/Ki"
Kd_topic = "/demo/Kd"
    
class SelfBalance(Node):
    def __init__(self):
        super().__init__('Selfbalancing')
        
        self.pub = self.create_publisher(Twist, cmd_vel, 1)
        
        self.subscriber = self.create_subscription(Imu, Imu_topic,self.callback, 100)
        
        self.subscriber2 = self.create_subscription(Float32, Kp_topic,self.callback_Kp, 10)
        
        self.subscriber3 = self.create_subscription(Float32, Ki_topic,self.callback_Ki, 10)
        
        self.subscriber4 = self.create_subscription(Float32, Kd_topic,self.callback_Kd, 10)
        
        self.pub1 = self.create_publisher(Float32, Yaw_Topic, 1)
        
        self.xvelMin=-.01
        self.xvelMax =0
        
        self.yMin = -0.01
        self.yMax = -0.001
        
        self.yPrev =0
        self.delY = 0
        
        self.Kp = 1
        self.Ki = 0.008
        self.Kd = 0.001
        
        self.pubx = PID_Controller(self.Kp,self.Ki,self.Kd)
        
        
    def callback(self,data):
        setPoint = 0
        y = -data.orientation.y
        self.delY = y-self.yPrev
        if self.delY>self.yMax:
            self.yMax = self.delY
        elif self.delY<self.yMin:
            self.yMin = self.delY
        vel = Twist()
        xvel = -self.pubx.getCorrection(setPoint,y)
        
        if xvel>self.xvelMax:
            self.xvelMax=xvel
        elif xvel<self.xvelMin:
            self.xvelMin = xvel
            
        if xvel >26:
            xvel =26.0
        elif xvel<-26:
            xvel =-26.0
            
        vel.linear.x = xvel
        vel.linear.y = 0.0
        vel.linear.z = 0.0
        vel.angular.x =0.0
        vel.angular.y = 0.0
        vel.angular.z = 0.0


        self.pub.publish(vel)
        self.yPrev = y
    def callback_Kp(self,data):
        self.Kp = data.data
        self.pubx = PID_Controller(self.Kp,self.Ki,self.Kd)
    def callback_Ki(self,data):
        self.Ki = data.data
        self.pubx = PID_Controller(self.Kp,self.Ki,self.Kd)
    
    def callback_Kd(self,data):
        self.Kd = data.data
        self.pubx = PID_Controller(self.Kp,self.Ki,self.Kd)
        
        
 

def main():
    rclpy.init()
    node = SelfBalance()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    

if __name__ == '__main__':
    main()
