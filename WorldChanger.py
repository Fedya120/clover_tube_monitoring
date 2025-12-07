import xml.etree.ElementTree as ET

from string import Template

from random import uniform

import math

WORLD_INCLUDE = Template('''
    <include>
      <uri>model://${model_name}</uri>
      <pose>${x} ${y} ${z} ${roll} ${pitch} ${yaw}</pose>
    </include>
''')

def load_world(world_file):
    '''
    Load Gazebo world as an ElementTree object
    '''
    return ET.parse(world_file)


def add_model(world, model_name, x, y, z, roll, pitch, yaw, index=0):
    '''
    Create and add an element to the world
    '''
    world_elem = world.find('world')
    model_elem = ET.fromstring(WORLD_INCLUDE.substitute(
        model_name=model_name,
        x=x,
        y=y,
        z=z,
        roll=roll,
        pitch=pitch,
        yaw=yaw
    ))
    model_elem.tail = '\n    '
    world_elem.insert(index, model_elem)
    return world


def save_world(world, file):
    '''
    Save the world to file-like object
    '''
    return world.write(file, encoding='unicode')

with open(r'/home/clover/catkin_ws/src/clover/clover_simulation/resources/worlds/clover_aruco.world', 'w') as f:
    pass

x_zero = uniform(1.2, 3.0)
period = 0
world = load_world(r'/home/clover/catkin_ws/src/clover/clover_simulation/resources/worlds/clover_aruco1.world')
world = add_model(world, 'big_tube_with_angle', x = 4.0, y = 1.0, z = 0.1, roll = 0, pitch = 0, yaw = 0)

random_floats = []
current_value = 1
next_value = 0
cnt = 0
while len(random_floats) < 5:
    next_value = current_value + uniform(0.75, (8.5 - current_value))
    cnt += 1
    if next_value <= 9 - (0.95 * (5 - cnt)):
        random_floats.append(next_value)
        current_value = next_value
    else:
        cnt -= 1

cnt = 0
for float in random_floats:
    cnt += 1
    if float <= 7:
        world = add_model(world, 'mini_pipe' + str(cnt), x = float, y = 1.0, z = 0.3, roll = 0, pitch = 0, yaw = 0)
    else:
        world = add_model(world, 'mini_pipe' + str(cnt), x = float, y = 1.0 + math.tan(0.2) * (float - 7), z = 0.3, roll = 0, pitch = 0, yaw = 0)
with open(r'/home/clover/catkin_ws/src/clover/clover_simulation/resources/worlds/clover_aruco.world', 'w') as f:
    save_world(world, f)
print('gotovo')
'''+ math.tan(0.2) * float'''