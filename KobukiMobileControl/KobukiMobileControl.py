#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file KobukiMobileControl.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist


import math


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
kobukimobilecontrol_spec = ["implementation_id", "KobukiMobileControl", 
		 "type_name",         "KobukiMobileControl", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "Hiroaki Matsuda", 
		 "category",          "Kobuki", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class KobukiMobileControl
# @brief ModuleDescription
# 
# 
class KobukiMobileControl(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_target_pose = RTC.TimedPose2D(RTC.Time(0,0), RTC.Pose2D(RTC.Point2D(0.0, 0.0), 0.0))
		"""
		"""
		self._target_poseIn = OpenRTM_aist.InPort("target_pose", self._d_target_pose)
		self._d_target_velocity = RTC.TimedVelocity2D(RTC.Time(0,0), RTC.Velocity2D(0.0, 0.0, 0.0))
		"""
		"""
		self._target_velocityIn = OpenRTM_aist.InPort("target_velocity", self._d_target_velocity)
		self._d_kobuki_pose = RTC.TimedPose2D(RTC.Time(0,0), RTC.Pose2D(RTC.Point2D(0.0, 0.0), 0.0))
		"""
		"""
		self._kobuki_poseIn = OpenRTM_aist.InPort("kobuki_pose", self._d_kobuki_pose)
		self._d_flag = RTC.TimedBoolean(RTC.Time(0,0), False)
		"""
		"""
		self._flagOut = OpenRTM_aist.OutPort("flag", self._d_flag)
		self._d_kobuki_velocity = RTC.TimedVelocity2D(RTC.Time(0,0), RTC.Velocity2D(0.0, 0.0, 0.0))
		"""
		"""
		self._kobuki_velocityOut = OpenRTM_aist.OutPort("kobuki_velocity", self._d_kobuki_velocity)


		
	def onInitialize(self):
		# Bind variables and configuration variable
		
		# Set InPort buffers
		self.addInPort("target_pose",self._target_poseIn)
		self.addInPort("target_velocity",self._target_velocityIn)
		self.addInPort("kobuki_pose",self._kobuki_poseIn)
		
		# Set OutPort buffers
		self.addOutPort("flag",self._flagOut)
		self.addOutPort("kobuki_velocity",self._kobuki_velocityOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports

		self.current_x = 0.0
		self.current_y = 0.0
		self.current_heading = 0.0
		
		return RTC.RTC_OK
	
	def onActivated(self, ec_id):
	
		return RTC.RTC_OK
	

	def onDeactivated(self, ec_id):
	
		return RTC.RTC_OK
	

	def onExecute(self, ec_id):
                if self._target_poseIn.isNew():
                        self.move_kobuki(self._target_poseIn.read())
                        self._d_flag.data = True
                        self._flagOut.write()
	
		return RTC.RTC_OK

	def move_kobuki(self, target_pose):

                target_x = target_pose.data.position.x
                target_y = target_pose.data.position.y
                target_heading = target_pose.data.heading

                self._face_target_position(target_x, target_y)
                self._move_target_position(target_x, target_y)


        def _face_target_position(self, target_x, target_y):
                flag = False

                target_heading = math.atan2(target_y - self.current_y, target_x - self.current_x)               
                
		print "target heading: " + str(target_heading * 180.0 / math.pi)
		

                while flag == False:


                        if self._kobuki_poseIn.isNew():
                                self._d_kobuki_pose = self._kobuki_poseIn.read()

				self.current_x = self._d_kobuki_pose.data.position.x
                                self.current_y = self._d_kobuki_pose.data.position.y
                                self.current_heading = self._d_kobuki_pose.data.heading

                                differance_heading = target_heading - self._d_kobuki_pose.data.heading
				print "differance heading: " + str(differance_heading * 180.0 / math.pi)

				if differance_heading >= 0:
					
					self._d_kobuki_velocity.data = RTC.Velocity2D(0.0, 0.0, 0.1)
					self._kobuki_velocityOut.write()
				
				elif differance_heading < 0:
					
					self._d_kobuki_velocity.data = RTC.Velocity2D(0.0, 0.0, -0.1)
					self._kobuki_velocityOut.write()

				if -0.5 * math.pi / 180.0 <= differance_heading <=  0.5 * math.pi / 180.0:
					
					flag = True

		self._d_kobuki_velocity.data = RTC.Velocity2D(0.0, 0.0, 0.0)
                self._kobuki_velocityOut.write()

                return True

        def _move_target_position(self, target_x, target_y):
                flag = False

		self._d_kobuki_pose = self._kobuki_poseIn.read()

		self.current_x = self._d_kobuki_pose.data.position.x
                self.current_y = self._d_kobuki_pose.data.position.y
		self.current_heading = self._d_kobuki_pose.data.heading

		past_differance_distance = math.hypot(target_x - self.current_x, target_y - self.current_y)  
                
                while flag == False:
                        self._d_kobuki_velocity.data = RTC.Velocity2D(0.2, 0.0, 0.0)
                        self._kobuki_velocityOut.write()
                        
                        if self._kobuki_poseIn.isNew():
                                self._d_kobuki_pose = self._kobuki_poseIn.read()
				self.current_x = self._d_kobuki_pose.data.position.x
                                self.current_y = self._d_kobuki_pose.data.position.y
                                self.current_heading = self._d_kobuki_pose.data.heading

                                differance_distance = math.hypot(target_x - self.current_x, target_y - self.current_y)
				print "differance_distance:" + str(differance_distance)
                                if differance_distance <=  0.15:
                                        flag = True

				if past_differance_distance < differance_distance - 0.001:
					flag = True
					print "past_differance_distance:" + str(past_differance_distance)


				past_differance_distance = differance_distance

		self._d_kobuki_velocity.data = RTC.Velocity2D(0.0, 0.0, 0.0)
                self._kobuki_velocityOut.write()

                return True
	

def KobukiMobileControlInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=kobukimobilecontrol_spec)
    manager.registerFactory(profile,
                            KobukiMobileControl,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    KobukiMobileControlInit(manager)

    # Create a component
    comp = manager.createComponent("KobukiMobileControl")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

