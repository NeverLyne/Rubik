import tkinter as tk
from tkinter import simpledialog

# Mapa kolorów dla GUI
color_map = {0: 'white', 1: 'red', 2: 'orange', 3: 'yellow', 4: 'green', 5: 'blue', -1: 'gray'}
reverse_color_map = {'white': 0, 'red': 1, 'orange': 2, 'yellow': 3, 'green': 4, 'blue': 5, 'gray': -1}
face_names = ["Front", "Left", "Back", "Right", "Up", "Down"]


class CubeEditor:
    def __init__(self, root, cube_faces):
        self.root = root
        self.cube_faces = cube_faces
        self.current_face = 0

        # Tworzenie głównego okna
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        self.face_label = tk.Label(self.main_frame, text=f"Editing {face_names[self.current_face]} Face",
                                   font=("Arial", 16))
        self.face_label.pack()

        self.grid_frame = tk.Frame(self.main_frame)
        self.grid_frame.pack()

        self.buttons = []
        self.create_grid()

        self.controls_frame = tk.Frame(self.main_frame)
        self.controls_frame.pack()

        self.prev_button = tk.Button(self.controls_frame, text="Previous", command=self.previous_face)
        self.prev_button.grid(row=0, column=0)

        self.next_button = tk.Button(self.controls_frame, text="Next", command=self.next_face)
        self.next_button.grid(row=0, column=1)

        self.save_button = tk.Button(self.controls_frame, text="Save and Exit", command=self.save_and_exit)
        self.save_button.grid(row=0, column=2)

    def create_grid(self):
        """Tworzy siatkę przycisków dla bieżącej ściany"""
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.buttons = []
        face = self.cube_faces[self.current_face]

        for row_idx, row in enumerate(face):
            button_row = []
            for col_idx, color_code in enumerate(row):
                btn = tk.Button(self.grid_frame, bg=color_map[color_code], width=5, height=2,
                                command=lambda r=row_idx, c=col_idx: self.edit_color(r, c))
                btn.grid(row=row_idx, column=col_idx)
                button_row.append(btn)
            self.buttons.append(button_row)

    def edit_color(self, row, col):
        """Zmienia kolor wybranej komórki"""
        current_color = self.buttons[row][col].cget("bg")
        new_color = simpledialog.askstring("Edit Color",
                                           f"Current color is {current_color}. Enter new color (white/red/orange/yellow/green/blue/gray):")

        if new_color in reverse_color_map:
            new_color_code = reverse_color_map[new_color]
            self.cube_faces[self.current_face][row][col] = new_color_code
            self.buttons[row][col].config(bg=new_color)
        else:
            tk.messagebox.showerror("Invalid Color", "Please enter a valid color.")

    def previous_face(self):
        """Przełącza na poprzednią ścianę"""
        if self.current_face > 0:
            self.current_face -= 1
            self.face_label.config(text=f"Editing {face_names[self.current_face]} Face")
            self.create_grid()

    def next_face(self):
        """Przełącza na następną ścianę"""
        if self.current_face < len(self.cube_faces) - 1:
            self.current_face += 1
            self.face_label.config(text=f"Editing {face_names[self.current_face]} Face")
            self.create_grid()

    def save_and_exit(self):
        """Zamyka okno i zapisuje zmiany"""
        self.root.destroy()
