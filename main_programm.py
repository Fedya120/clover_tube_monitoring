import rospy
from clover import srv
from std_srvs.srv import Trigger
import math
from sensor_msgs.msg import Range
from std_msgs.msg import String

rospy.init_node('flight')

#set_effect = rospy.ServiceProxy('led/set_effect', SetLEDEffect)
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

pub = rospy.Publisher("tubes", String, queue_size=10)

cords = []

dist_z = 0
def range_callback(msg):
    global dist_z
    dist_z = msg.range


rospy.Subscriber('rangefinder/range', Range, range_callback)

def navigate_wait(x=0, y=0, z=0, speed=0.5, frame_id='', auto_arm=False, tolerance=0.2, sl = 0):
    navigate(x=x, y=y, z=z, speed=speed, frame_id=frame_id, auto_arm=auto_arm)
    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            rospy.sleep(sl)
            break
        rospy.sleep(0.2)


def navigate_wait_range1(x=0, y=0, z=0, speed=0.5, frame_id='', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, speed=speed, frame_id=frame_id, auto_arm=auto_arm)
    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            rospy.sleep(3)
            break
        if dist_z < 0.94:
            navigate_wait(x=0, y=0, z=0, speed = 0.3, frame_id='body', sl=3)
            telem_now = get_telemetry(frame_id = 'aruco_map')
            x_pipe = telem_now.x
            y_pipe = telem_now.y
            z_pipe = (telem_now.z - dist_z) / 1.5
            s = String()
            s.data = f'x = {x_pipe}, y = {y_pipe}, z = {z_pipe}'
            pub.publish(s)
            print(x_pipe, y_pipe, z_pipe,'- coordinates of pipe')
            navigate_wait(x=0.3, y=0, z=0, speed = 0.3, frame_id='body', sl = 1.5)
            navigate_wait_range1(x=x, y=y, z=z, speed = speed, frame_id=frame_id)
            break
        rospy.sleep(0.2)
    

def navigate_wait_range2(x=0, y=0, z=0, speed=0.5, frame_id='', auto_arm=False, tolerance=0.1):
    navigate(x=x, y=y, z=z, speed=speed, frame_id=frame_id, auto_arm=auto_arm)
    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            rospy.sleep(3)
            break
        if dist_z < 0.94:
            navigate_wait(x=0, y=0, z=0, speed = 0.3, frame_id='body', sl=3)
            telem_now = get_telemetry(frame_id = 'aruco_map')
            x_pipe = telem_now.x
            y_pipe = telem_now.y
            z_pipe = (telem_now.z - dist_z) / 1.5
            s = String()
            s.data = f'x = {x_pipe}, y = {y_pipe}, z = {z_pipe}'
            pub.publish(s)
            print(x_pipe, y_pipe, z_pipe,'- coordinates of pipe')
            navigate_wait(x=0.2, y= 0.3 * math.tan(0.2), z=0, speed = 0.3, frame_id='body', sl = 1.5)
            navigate_wait_range2(x=x, y=y, z=z, speed = speed, frame_id=frame_id)
            break
        rospy.sleep(0.2)
  

def main():
    navigate_wait(z=1.5,frame_id='body',auto_arm=True, sl=3)
    navigate_wait(x=1,y=0.97,z=1.5, frame_id='aruco_map', sl=3)
    navigate_wait_range1(x=7.4,y=0.97,z=1.5,speed = 0.1,frame_id='aruco_map')
    navigate_wait(x=7.2,y=1 + math.tan(0.2) * 0.2,z=1.5, speed = 0.15, frame_id='aruco_map', sl=3)
    navigate_wait_range2(x=9.5,y=1.0 + 2.5 * math.tan(0.2), z=1.5,speed = 0.1,frame_id='aruco_map')
    navigate_wait(z=1.5,frame_id='aruco_map')
    land()

if __name__ == "__main__":
    main()
 
