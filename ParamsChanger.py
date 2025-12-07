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
print("Done")