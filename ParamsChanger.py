import xml.etree.ElementTree as ET

def modify_arg_value(file_path, arg_name, new_value):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for arg in root.findall('arg'):
        if arg.get('name') == arg_name:
            arg.set('default', new_value)
            break

    tree.write(file_path)

file_path = '/home/clover/catkin_ws/src/clover/clover/launch/clover.launch'
modify_arg_value(file_path, 'aruco', 'true')
modify_arg_value(file_path, 'rangefinder_vl53l1x', 'true')
file_path = '/home/clover/catkin_ws/src/clover/clover/launch/aruco.launch'
modify_arg_value(file_path, 'aruco_map', 'true')
modify_arg_value(file_path, 'aruco_vpe', 'true')

import subprocess
import os

package_name = 'aruco_pose'
node_name = 'genmap.py'
args = ['0.335', '10', '10', '1', '1', '0']
output_file = os.path.expanduser('~/catkin_ws/src/clover/aruco_pose/map/map.txt')
additional_args = ['--top-left']

command = ['rosrun', package_name, node_name] + args + additional_args

with open(output_file, 'w') as f:
    try:
        subprocess.run(command, stdout=f, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(e.stderr.decode())


print("Done")