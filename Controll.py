import glob
import os
import sys
import random
import time
import numpy as pie
import cv2
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla



im_width = 1280
im_height = 768	 		


def imagetobeprocessed(captureimage):
    i = pie.array(captureimage.raw_data)
    i2 = i.reshape((im_height, im_width, 4))
    i3 = i2[:, :, :3]
    cv2.imshow("", i3)
    cv2.waitKey(1)
    return i3/255.0


actor_list = []
try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(4.0)

    world = client.get_world()

    blueprint_library = world.get_blueprint_library()

    bp = blueprint_library.filter('model3')[0]
    print(bp)

    spawn_point = random.choice(world.get_map().get_spawn_points())

    vehicle = world.spawn_actor(bp, spawn_point)
    vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
    actor_list.append(vehicle)

    
    cam_bp= blueprint_library.find("sensor.camera.rgb")
    cam_bp.set_attribute("captureimage_size_x", f"{im_width}")
    cam_bp.set_attribute("captureimage_size_y", f"{im_height}")
    cam_bp.set_attribute("fov", "110")

    spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))

    sensor = world.spawn_actor(cam_bp, spawn_point, attach_to =  vehicle)
    actor_list.append(sensor)
    sensor.listen(lambda data: imagetobeprocessed(data))

    time.sleep(7)


