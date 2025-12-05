import xml.etree.ElementTree as ET

from string import Template

from random import uniform

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
for num in range(1, 6):
    world = add_model(world, 'mini_pipe' + str(num), x = x_zero + period, y = 1.0, z = 0.3, roll = 0, pitch = 0, yaw = 0)
    period += uniform(0.75, 0.9)
with open(r'/home/clover/catkin_ws/src/clover/clover_simulation/resources/worlds/clover_aruco.world', 'w') as f:
    save_world(world, f)
print('gotovo')