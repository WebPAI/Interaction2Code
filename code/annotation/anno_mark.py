import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import json
import os
from pathlib import Path
import shutil

web_number = 105
folder_name = "dataset"
class ImageAnnotationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Annotation Tool")

        # State variables
        self.current_index = 1  # Start with first image pair
        self.drawing = False
        self.start_x = None
        self.start_y = None
        self.rect_src_id = None
        self.rect_dst_id = None
        self.dst_rectangles = []
        self.crop_rect_id = None
        self.current_image_data = None

        self.load_config()
        self.setup_ui()
        self.load_current_images()

    def load_config(self):
        with open(f"{folder_name}/{web_number}/action.json", 'r') as f:
            self.config = json.load(f)

    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=10, pady=10, expand=True, fill='both')

        # Image frames
        self.image_frames = []
        for i, title in enumerate(["Src Path", "Dst Path", "Image3"]):
            frame = ttk.LabelFrame(main_frame, text=title)
            frame.grid(row=0, column=i, padx=5, pady=5)

            canvas = tk.Canvas(frame, width=400, height=300, bg='gray')
            # canvas = tk.Canvas(frame, width=600, height=450, bg='gray')
            canvas.pack(padx=5, pady=5)

            self.image_frames.append(canvas)

            if i == 0:  # Src image
                canvas.bind('<Button-1>', self.start_drawing)
                canvas.bind('<B1-Motion>', self.draw_bbox)
                canvas.bind('<ButtonRelease-1>', self.stop_drawing)
            elif i == 1:  # Dst image
                canvas.bind('<Button-1>', self.start_drawing_dst)
                canvas.bind('<B1-Motion>', self.draw_bbox_dst)
                canvas.bind('<ButtonRelease-1>', self.stop_drawing_dst)
            else:  # Crop image
                canvas.bind('<Button-1>', self.start_crop)
                canvas.bind('<B1-Motion>', self.draw_crop)
                canvas.bind('<ButtonRelease-1>', self.stop_crop)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=3, pady=10)

        ttk.Button(button_frame, text="Save Src Image", command=self.save_src).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Src", command=self.clear_src).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Dst Image", command=self.save_dst).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Dst", command=self.clear_dst).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Interaction", command=self.save_crop).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Crop", command=self.clear_crop).pack(side=tk.LEFT, padx=5)


        ttk.Button(button_frame, text="Last", command=self.last_images).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Next", command=self.next_images).pack(side=tk.LEFT, padx=5)

        # Description
        desc_frame = ttk.LabelFrame(main_frame, text="Description")
        desc_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky='ew')
        self.description_var = tk.StringVar()
        ttk.Label(desc_frame, textvariable=self.description_var).pack(pady=5)


    def get_image_path(self, number):
        return f"./{folder_name}/{web_number}/{number}.png"

    def get_mark_image_path(self, number):
        return f"./{folder_name}/{web_number}/{number}-mark.png"

    def load_current_images(self):
        current_data = self.config[str(self.current_index)]

        src_path = self.get_image_path(current_data['src'])
        dst_path = self.get_image_path(current_data['dst'])
        self.description_var.set(current_data['description'])

        # Load and display images
        for i, path in enumerate([src_path, dst_path, dst_path]):
            try:
                img = Image.open(path)
                # img = img.resize((600, 450))
                img = img.resize((400, 300))
                photo = ImageTk.PhotoImage(img)
                self.image_frames[i].image = photo
                self.image_frames[i].create_image(0, 0, anchor='nw', image=photo)
            except Exception as e:
                print(f"Error loading image {path}: {e}")

    def start_drawing(self, event):
        self.drawing = True
        self.start_x = event.x
        self.start_y = event.y
        # if self.rect_src_id:
        #     self.image_frames[0].delete(self.rect_src_id)

    def draw_bbox(self, event):
        if self.drawing:
            if self.rect_src_id:
                self.image_frames[0].delete(self.rect_src_id)
            self.rect_src_id = self.image_frames[0].create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline='red', width=2
            )

    def stop_drawing(self, event):
        self.drawing = False

    # def start_drawing_dst(self, event):
    #     self.drawing = True
    #     self.start_x = event.x
    #     self.start_y = event.y
        # if self.rect_dst_id:
        #     self.image_frames[1].delete(self.rect_dst_id)

    # def draw_bbox_dst(self, event):
    #     if self.drawing:
    #         if self.rect_dst_id:
    #             self.image_frames[1].delete(self.rect_dst_id)
    #         self.rect_dst_id = self.image_frames[1].create_rectangle(
    #             self.start_x, self.start_y, event.x, event.y,
    #             outline='red', width=2
    #         )


    def start_drawing_dst(self, event):
        self.drawing = True
        self.start_x = event.x
        self.start_y = event.y
        self.current_rect = None

    def draw_bbox_dst(self, event):
        if self.drawing:
            if self.current_rect:
                self.image_frames[1].delete(self.current_rect)
            self.current_rect = self.image_frames[1].create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline='red', width=2
            )
            # print(self.current_rect)

    # def stop_drawing_dst(self, event):
    #     self.drawing = False
    #
    def stop_drawing_dst(self, event):
        if self.drawing and self.current_rect:
            coords = self.image_frames[1].coords(self.current_rect)
            self.dst_rectangles.append(self.current_rect)
        self.drawing = False
        self.current_rect = None
        print(self.dst_rectangles)

    def start_crop(self, event):
        self.drawing = True
        self.start_x = event.x
        self.start_y = event.y
        if self.crop_rect_id:
            self.image_frames[2].delete(self.crop_rect_id)

    def draw_crop(self, event):
        if self.drawing:
            if self.crop_rect_id:
                self.image_frames[2].delete(self.crop_rect_id)
            self.crop_rect_id = self.image_frames[2].create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline='blue', width=2
            )

    def stop_crop(self, event):
        self.drawing = False

    def save_src(self):
        if self.rect_src_id:
            coords = self.image_frames[0].coords(self.rect_src_id)
            img_path = self.get_image_path(self.config[str(self.current_index)]['src'])
            # Save coordinates to file or process as needed

            # save_path = Path(img_path).parent / 'mark'
            save_path = Path(img_path).parent
            save_path.mkdir(exist_ok=True)
            original_img = Image.open(img_path)
            marked_img = original_img.copy()


            draw = ImageDraw.Draw(marked_img)

            # Scale coordinates from canvas size to actual image size
            scale_x = original_img.width / 400
            scale_y = original_img.height / 300
            scaled_coords = [
                coords[0] * scale_x,
                coords[1] * scale_y,
                coords[2] * scale_x,
                coords[3] * scale_y
            ]

            # Draw rectangle on image
            draw.rectangle(scaled_coords, outline='red',
                           width=max(1, int(min(original_img.width, original_img.height) / 250)))
            # Save the marked image
            marked_img.save(save_path / f"{self.config[str(self.current_index)]['src']}_mark.png")

    def save_dst(self):
        # if self.rect_dst_id:
        if self.dst_rectangles:
            # coords = self.image_frames[1].coords(self.rect_dst_id)
            img_path = self.get_image_path(self.config[str(self.current_index)]['dst'])
            # Save coordinates to file or process as needed

            # save_path = Path(img_path).parent / 'mark'
            save_path = Path(img_path).parent
            save_path.mkdir(exist_ok=True)
            original_img = Image.open(img_path)
            marked_img = original_img.copy()

            draw = ImageDraw.Draw(marked_img)

            # Scale coordinates from canvas size to actual image size
            scale_x = original_img.width / 400
            scale_y = original_img.height / 300


            # Draw each rectangle
            for rect_id in self.dst_rectangles:
                coords = self.image_frames[1].coords(rect_id)
                scaled_coords = [
                    coords[0] * scale_x,
                    coords[1] * scale_y,
                    coords[2] * scale_x,
                    coords[3] * scale_y
                ]
                # print(scaled_coords)
                draw.rectangle(scaled_coords, outline='red',
                             width=max(1, int(min(original_img.width, original_img.height) / 250)))

            # scaled_coords = [
            #     coords[0] * scale_x,
            #     coords[1] * scale_y,
            #     coords[2] * scale_x,
            #     coords[3] * scale_y
            # ]
            #
            # # Draw rectangle on image
            # draw.rectangle(scaled_coords, outline='red',
            #                width=max(1, int(min(original_img.width, original_img.height) / 250)))
            # Save the marked image

            marked_img.save(save_path / f"{self.config[str(self.current_index)]['dst']}_mark.png")

    def save_crop(self):
        if self.crop_rect_id:
            coords = self.image_frames[2].coords(self.crop_rect_id)

            img_path = self.get_image_path(self.config[str(self.current_index)]['dst'])

            save_path = Path(img_path).parent
            print(save_path)
            save_path.mkdir(exist_ok=True)
            # Save cropped image
            img = Image.open(img_path)
            crop_coords = [
                int(coords[0] * img.width / 400),
                int(coords[1] * img.height / 300),
                int(coords[2] * img.width / 400),
                int(coords[3] * img.height / 300)
            ]
            cropped_img = img.crop(crop_coords)
            cropped_img.save(save_path / f"interaction_{self.current_index}.png")

    def clear_src(self):
        if self.rect_src_id:
            self.image_frames[0].delete(self.rect_src_id)
            self.rect_src_id = None

    # def clear_dst(self):
    #     if self.rect_dst_id:
    #         self.image_frames[1].delete(self.rect_dst_id)
    #         self.rect_dst_id = None

    def clear_dst(self):
        for rect_id in self.dst_rectangles:
            self.image_frames[1].delete(rect_id)
        self.dst_rectangles = []

    def clear_crop(self):
        if self.crop_rect_id:
            self.image_frames[2].delete(self.crop_rect_id)
            self.crop_rect_id = None

    def next_images(self):
        if str(self.current_index + 1) in self.config:
            self.current_index += 1
            self.clear_src()
            self.clear_dst()
            self.clear_crop()
            self.load_current_images()

    def last_images(self):
        if str(self.current_index - 1) in self.config:
            self.current_index -= 1
            self.clear_src()
            self.clear_dst()
            self.clear_crop()
            self.load_current_images()


if __name__ == '__main__':
    root = tk.Tk()
    app = ImageAnnotationApp(root)
    root.mainloop()