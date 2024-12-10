import pyray as pr
import config
from rubik import Rubik


pr.init_window( config.window_w, config.window_w, "Kostka")

rubik_cube = Rubik()

rotation_queue = [config.rubik_moves['U\''],
                  config.rubik_moves['B']]

pr.set_target_fps(config.fps)

while not pr.window_should_close():

    rotation_queue, _ = rubik_cube.handle_rotation(rotation_queue)

    pr.update_camera(config.camera, pr.CameraMode.CAMERA_THIRD_PERSON)

    pr.begin_drawing()
    pr.clear_background(pr.RAYWHITE)





    pr.begin_mode_3d(config.camera)

    pr.draw_grid(20,1.0)

    for i, cube in enumerate(rubik_cube.cubes):
        for cube_part in cube:
            position = pr.Vector3(cube[0].center[0], cube[0].center[1], cube[0].center[2])
            pr.draw_model(cube_part.model,
                          position,
                          2,
                          cube_part.face_color)

    pr.end_mode_3d()
    pr.end_drawing()