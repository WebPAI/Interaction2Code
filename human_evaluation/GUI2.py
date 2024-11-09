import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk
import json
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def get_interact_number(folder_path):
    png_count = 0
    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):
            png_count += 1
    return png_count


def initialize_firefox():
    service = Service()
    options = Options()
    driver = webdriver.Firefox(options=options, service=service)
    driver.maximize_window()
    return driver


class ImageViewerApp:
    def __init__(self, root, model, prompt, begin, end):
        self.root = root
        self.root.title("Image and HTML Viewer")

        # Data storage
        self.current_index = 0
        self.data_list = []
        self.results = {}

        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.create_display_frame()
        self.create_options_frame()
        self.create_navigation_frame()

        self.model = model
        self.prompt = prompt
        self.begin = begin
        self.end = end

        # Load saved results if exist
        if os.path.exists(f'compare_{self.prompt}_{self.model}.json'):
            with open(f'compare_{self.prompt}_{self.model}.json', 'r') as f:
                self.results = json.load(f)

        # Load initial data
        self.load_data()

        self.driver1 = initialize_firefox()

        self.driver2 = initialize_firefox()

    def create_display_frame(self):
        # Frame for images and HTML
        display_frame = ttk.Frame(self.main_frame)
        display_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Current file paths display
        path_frame = ttk.Frame(display_frame)
        path_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.path_label = ttk.Label(path_frame, text="当前文件：", wraplength=400)
        self.path_label.grid(row=0, column=0, sticky=tk.W)

        # Image labels
        image_frame = ttk.Frame(display_frame)
        image_frame.grid(row=1, column=0, columnspan=2)

        self.image1_label = ttk.Label(image_frame)
        self.image1_label.grid(row=0, column=0, padx=5, pady=5)

        self.image2_label = ttk.Label(image_frame)
        self.image2_label.grid(row=0, column=1, padx=5, pady=5)

        # # # HTML display
        # self.html_display = tk.Text(display_frame, height=15, width=60)
        # self.html_display.grid(row=2, column=0, columnspan=2, pady=5)

    def create_options_frame(self):
        # Frame for failure type options
        options_frame = ttk.Frame(self.main_frame)
        options_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E), padx=10)

        # ttk.Label(options_frame,  font=('Arial', 16), text="Compare:\n (Win means experiment group (gpt/claude) \n beat gemini direct prompt)").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        ttk.Label(options_frame,
                  text="Compare:\n (Win means experiment group (gpt/claude) \n beat gemini direct prompt)").grid(row=0,
                                                                                                                 column=0,
                                                                                                                 sticky=tk.W,
                                                                                                                 pady=(
                                                                                                                 0, 10))

        self.selected_option = tk.IntVar()

        options = [
            "0. Win",
            "1. Tie",
            "2. Lose",
        ]

        for i, option in enumerate(options):
            ttk.Radiobutton(options_frame, text=option, variable=self.selected_option,
                            value=i, command=self.save_selection).grid(row=i + 1, column=0, sticky=tk.W)

    def create_navigation_frame(self):
        # Frame for navigation buttons
        nav_frame = ttk.Frame(self.main_frame)
        nav_frame.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(nav_frame, text="Previous", command=self.previous_item).grid(row=0, column=0, padx=10)
        ttk.Button(nav_frame, text="Next", command=self.next_item).grid(row=0, column=1, padx=10)
        ttk.Button(nav_frame, text="Show Page", command=self.show_page).grid(row=0, column=2, padx=10)

    def load_data(self):

        web_numbers = [i for i in range(self.begin, self.end)]
        # 31 left
        # web_numbers = [i for i in range(91, 101)]
        # web_numbers = [12]
        path = "../sample/"
        html1_files = []
        html2_files = []
        image1_files = []
        image2_files = []
        for web_number in web_numbers:
            try:
                interact_number = int(get_interact_number(path + "{}".format(web_number)) / 5)
            except:
                continue
            for i in range(1, interact_number + 1):
                print(web_number, i, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                image1_files.append(path + f"{web_number}/{i}-1-mark.png")
                image2_files.append(path + f"{web_number}/{i}-2-mark.png")
                html1_files.append(path + f"{web_number}/{i}-direct_prompt-gemini.html")
                html2_files.append(path + f"{web_number}/{i}-{self.prompt}-{self.model}.html")

        print(self.data_list)


        for i in range(0, len(image1_files)):
            self.data_list.append({
                'image1': image1_files[i],
                'image2': image2_files[i],
                'html1': html1_files[i],
                'html2': html2_files[i]
            })

        if self.data_list:
            self.update_display()

    def update_display(self):
        if not self.data_list:
            return

        current_set = self.data_list[self.current_index]

        # Update path display
        self.path_label.config(
            text=f"当前文件：\n图片1: {current_set['image1']}\n图片2: {current_set['image2']}\n 对照组HTML: {current_set['html1']}\n控制组HTML:{current_set['html2']}\n 计数器:{self.current_index+1}")

        # Update images
        for image_key, label in [('image1', self.image1_label), ('image2', self.image2_label)]:
            image_path = current_set[image_key]
            try:
                image = Image.open(image_path)
                # 保持原始宽高比例，限制最大尺寸为200x200
                # image.thumbnail((200, 200))
                image.thumbnail((1000, 1000))
                photo = ImageTk.PhotoImage(image)
                label.configure(image=photo)
                label.image = photo  # Keep a reference
            except Exception as e:
                label.configure(text=f"Error loading image: {str(e)}")

        # Update selected option if previously saved
        set_id = f"{self.current_index}"
        if set_id in self.results:
            self.selected_option.set(self.results[set_id])
        else:
            self.selected_option.set(-1)

    def save_selection(self):
        if self.data_list:
            # set_id = f"{self.current_index}"
            set_id = self.data_list[self.current_index]["html2"]
            self.results[set_id] = self.selected_option.get()

            # Save to file
            with open(f'compare_{self.prompt}_{self.model}.json', 'w') as f:
                json.dump(self.results, f)

    def previous_item(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_display()

    def next_item(self):
        if self.current_index < len(self.data_list) - 1:
            self.current_index += 1
            self.update_display()

    def show_page(self):

        self.driver1.get("file:///" + self.data_list[self.current_index]['html1'])
        self.driver2.get("file:///" + self.data_list[self.current_index]['html2'])

        pass


def main():
    root = tk.Tk()
    app = ImageViewerApp(root, model="gemini", prompt="cot_prompt", begin=1, end=101)
    root.mainloop()
    app.driver1.quit()
    app.driver2.quit()


if __name__ == "__main__":
    main()
