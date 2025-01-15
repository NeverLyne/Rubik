import cv2
import numpy as np
from scipy.stats import mode
import pyray as pr
import config
from rubik import Rubik
import alphacube
from CubeEditor import CubeEditor
import tkinter as tk
from tkinter import simpledialog


# Function to assign numeric codes to colors based on HSV values
def recognize_color(hsv_value):
    h, s, v = hsv_value
    if v > 140:  # Check if the pixel is bright enough
        if s < 30 and h > 40:
            return 0  # White
        elif (h < 5 or h > 150) and s > 160:
            return 1  # Red
        elif h < 20:
            return 2  # Orange
        elif h < 50:
            return 3  # Yellow
        elif 50 < h < 90:
            return 4  # Green
        elif 90 < h < 130:
            return 5  # Blue
        else:
            return -1
    else:
        return -1  # Unknown color (e.g., black, gray, etc.)


# Function to process the central area of the frame for color recognition
def process_rubiks_image(frame, cube_size):
    height, width, _ = frame.shape
    central_size = 150
    x_center = width // 2 - central_size // 2
    y_center = height // 2 - central_size // 2
    step_x = central_size // cube_size
    step_y = central_size // cube_size
    cube_colors = []

    for row in range(cube_size):
        row_colors = []
        for col in range(cube_size):
            x_start = x_center + col * step_x
            y_start = y_center + row * step_y
            roi = frame[y_start:y_start + step_y, x_start:x_start + step_x]
            hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            color_codes = [recognize_color(pixel) for pixel in hsv_roi.reshape(-1, 3) if recognize_color(pixel) != -1]
            row_colors.append(int(mode(color_codes, keepdims=True).mode[0]) if color_codes else -1)
        cube_colors.append(row_colors)
    return cube_colors, frame


# Function to draw the central grid based on cube size
def draw_grid(frame, cube_size):
    height, width, _ = frame.shape
    central_size = 150
    x_center = width // 2 - central_size // 2
    y_center = height // 2 - central_size // 2
    step_x = central_size // cube_size
    step_y = central_size // cube_size

    for i in range(cube_size + 1):
        cv2.line(frame, (x_center, y_center + i * step_y), (x_center + central_size, y_center + i * step_y),
                 (255, 255, 255), 2)
        cv2.line(frame, (x_center + i * step_x, y_center), (x_center + i * step_x, y_center + central_size),
                 (255, 255, 255), 2)
    return frame


def prepare_flat_stickers(cube_faces):
    # Kolejność ścian w cube_faces: [Front, Left, Back, Right, Up, Down]
    face_order = [4, 5, 1, 3, 2, 0]  # Up, Down, Left, Right, Back, Front
    flat_stickers = []
    for index in face_order:
        face = cube_faces[index]
        rotated_face = [
            face[2][0], face[1][0], face[0][0],
            face[2][1], face[1][1], face[0][1],
            face[2][2], face[1][2], face[0][2]
        ]
        flat_stickers.extend(rotated_face)
    print(flat_stickers)
    return flat_stickers


# Main function for capturing and processing the Rubik's cube faces
color_map = {0: 'W', 1: 'R', 2: 'O', 3: 'Y', 4: 'G', 5: 'B', -1: '?'}


def main():
    face_order = ["Front", "Left", "Back", "Right", "Up", "Down"]

    while True:
        try:
            rubik_size = int(input("Enter the Rubik's cube size (2, 3, 4, or 5): "))
            if rubik_size in {2, 3, 4, 5}:
                break
            else:
                print("Invalid input. Please enter 2, 3, 4, or 5.")
        except ValueError:
            print("Invalid input. Please enter an integer value.")

    cap = cv2.VideoCapture(0)
    cube_faces = []

    for face in face_order:
        print(f"Align the {face} face and press 's' to save.")

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (700, 500))
            frame_with_grid = draw_grid(frame.copy(), rubik_size)
            cv2.putText(frame_with_grid, f"Position {face} face, press 's' to save", (150, 480),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.imshow("Rubik's Cube", frame_with_grid)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                colors, processed_frame = process_rubiks_image(frame, rubik_size)
                cube_faces.append(colors)
                print(f"{face} face saved:")
                for row in colors:
                    letter_row = [color_map[color] for color in row]
                    print(' '.join(letter_row))
                break
            elif key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                print("Capture aborted by user.")
                return

    cap.release()
    cv2.destroyAllWindows()

    # Display saved cube data and all faces
    if len(cube_faces) == 6:

        root = tk.Tk()
        root.title("Rubik's Cube Editor")
        editor = CubeEditor(root, cube_faces)
        root.mainloop()

        pr.init_window(config.window_w, config.window_w, "Kostka")

        rubik_cube = Rubik(cube_faces, rubik_size)

        pr.set_target_fps(config.fps)
        alphacube.load(model_id="large")
        stickers = prepare_flat_stickers(cube_faces)

        if rubik_size == 3:
            result = alphacube.solve(scramble=stickers, format='stickers', beam_width=2048)
            print(result)

            solution_string = result['solutions'][0]  # Pobierz pierwsze rozwiązanie
            moves = solution_string.split()  # Podziel string na poszczególne ruchy
            rotation_queue = [config.rubik_moves[move] for move in moves]


        while not pr.window_should_close():

            if rubik_size == 3:
                rotation_queue, _ = rubik_cube.handle_rotation(rotation_queue)
            pr.update_camera(config.camera, pr.CameraMode.CAMERA_THIRD_PERSON)

            pr.begin_drawing()
            pr.clear_background(pr.DARKGRAY)

            pr.begin_mode_3d(config.camera)

            for i, cube in enumerate(rubik_cube.cubes):
                for cube_part in cube:
                    position = pr.Vector3(cube[0].center[0], cube[0].center[1], cube[0].center[2])
                    pr.draw_model(cube_part.model,
                                  position,
                                  2,
                                  cube_part.face_color)

            pr.end_mode_3d()
            pr.end_drawing()











    else:
        print("Program ended before all faces were saved.")


if __name__ == "__main__":
    main()
