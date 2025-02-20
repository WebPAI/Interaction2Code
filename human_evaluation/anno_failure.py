import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk
import json
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def initialize_firefox():
    service = Service("geckodriver")
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

        if os.path.exists(f"failure/failure_{prompt}_{model}.json"):
            with open(f"failure/failure_{prompt}_{model}.json", "r") as fs:
                self.results = json.loads(fs.read())

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

        # Create a webview window
        # self.window = webview.create_window('Webview Example', 'https://www.example.com')
        # self.window = None
        # self.window = webview.create_window('webpage', "https://wwww.baidu.com", width=1600, height=1200)
        # webview.start()
        # Start the webview window

        # Load saved results if exist
        if os.path.exists(f'failure_{self.prompt}_{self.model}.json'):
            with open(f'failure_{self.prompt}_{self.model}.json', 'r') as f:
                self.results = json.load(f)

        # Load initial data
        self.load_data()

        self.driver = initialize_firefox()

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
        ttk.Label(options_frame, text="Failure Type").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        self.selected_option = tk.IntVar()

        # options_frame2 = ttk.Frame(self.main_frame)
        # options_frame2.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E), padx=10)
        ttk.Label(options_frame, text="Usability").grid(row=30, column=0, sticky=tk.W, pady=(0, 10))
        self.selected_option2 = tk.IntVar()

        # ttk.Label(options_frame, text="Choose").grid(row=50, column=0, sticky=tk.W, pady=(0, 10))
        # self.selected_option3 = tk.IntVar()

        # options = [
        #     "0. No Failure",
        #     "1. Interactive element missing",
        #     "2. No interaction",
        #     "3. Wrong interactive element",
        #     "4. Wrong position after interaction",
        #     "5. Wrong type of interactive element",
        #     "6. Effect on wrong element",
        #     "7. Partial Implementation",
        #     "8. Wrong function",
        # ]

        # options = [
        #     "0. No Failure",
        #     "1. Interactive element missing",
        #     "2. No interaction",
        #     "3. Wrong types of interactive element",
        #     "4. Wrong interactive element",
        #     "5. Wrong position of interactive element",
        #     "6. Wrong position after interaction",
        #     "7. Wrong type of interactive element",
        #     "8. Effect on wrong element",
        #     "9. Partial Implementation",
        #     "10. Wrong function",
        # ]

        options = [
            "0. No Failure",
            "1. Interactive element missing",
            "2. No interaction",
            "3. Wrong types of interactive element",
            "4. Wrong interactive element",
            "5. Wrong position of interactive element",
            "6. Wrong position after interaction",
            "7. Wrong type of interactive element",
            "8. Effect on wrong element",
            "9. Partial Implementation",
            "10. Wrong function",
        ]

        options2 = [
            "0. usable",
            "1. not usable"
        ]

        options3 = [
            "0. choose",
            "1. not choose"
        ]

        for i, option in enumerate(options):
            ttk.Radiobutton(options_frame, text=option, variable=self.selected_option,
                            value=i, command=self.save_selection).grid(row=i + 1, column=0, sticky=tk.W)

        for i, option in enumerate(options2):
            ttk.Radiobutton(options_frame, text=option, variable=self.selected_option2,
                            value=i, command=self.save_selection).grid(row=len(options) + i + 20, column=0, sticky=tk.W)

        # for i, option in enumerate(options3):
        #     ttk.Radiobutton(options_frame, text=option, variable=self.selected_option3,
        #                     value=i, command=self.save_selection).grid(row=len(options) + len(options2) + i + 50,
        #                                                                column=0, sticky=tk.W)


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
        # path = ""
        # path = "/Users/whalexiao/Downloads/pythonProject/dynamic/codes/results/sample/"
        path = "/Users/whalexiao/Downloads/pythonProject/Tool/Interaction2Code/code/annotation/dataset/"
        html_files = []
        image1_files = []
        image2_files = []

        # cases = get_cases()
        # for case in cases[1:]:
        #     print(case, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        #     image1_files.append(path + f"{case[0]}/{case[1]}-1-mark.png")
        #     image2_files.append(path + f"{case[0]}/{case[1]}-2-mark.png")
        #         # html_files.append(path + f"{web_number}/{i}-{self.prompt}-{self.model}.html")
        #     html_files.append(path + f"{case[0]}/{case[1]}-{self.prompt}-only-{self.model}.html")
        #
        # print(self.data_list)

        for web_number in web_numbers:
            config_file = path+f"{web_number}/action.json"
            with open(config_file, "r") as fs:
                config = json.loads(fs.read())
                for interact_number in range(1, 10):
                    if str(interact_number) in config.keys():
                        image1_files.append(path + f"{web_number}/{config[str(interact_number)]['src']}_mark.png")
                        image2_files.append(path + f"{web_number}/{config[str(interact_number)]['dst']}_mark.png")
                        html_files.append(path + f"{web_number}/result/{interact_number}-{self.prompt}-{self.model}.html")


            # try:
            #     interact_number = int(get_interact_number(path + "{}".format(web_number)) / 5)
            # except:
            #     continue
            # for i in range(1, interact_number + 1):
            #     print(web_number, i, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            #     image1_files.append(path + f"{web_number}/{i}_mark.png")
            #     image2_files.append(path + f"{web_number}/{i}_mark.png")
            #     html_files.append(path + f"{web_number}/result/{i}-{self.prompt}-{self.model}.html")
        #
        # print(self.data_list)
        # # 直接读取当前目录下的文件
        # image_files = sorted(glob.glob("*.jpg") + glob.glob("*.png") + glob.glob("*.jpeg"))
        # html_files = sorted(glob.glob("*.html"))
        #
        # self.data_list = []
        #
        # # Group files into sets

        for i in range(0, len(image1_files)):
            self.data_list.append({
                'image1': image1_files[i],
                'image2': image2_files[i],
                'html': html_files[i]
            })

        if self.data_list:
            self.update_display()

    def update_display(self):
        if not self.data_list:
            return

        current_set = self.data_list[self.current_index]

        # Update path display
        self.path_label.config(
            text=f"当前文件：\n图片1: {current_set['image1']}\n图片2: {current_set['image2']}\nHTML: {current_set['html']}")

        # Update images
        for image_key, label in [('image1', self.image1_label), ('image2', self.image2_label)]:
            image_path = current_set[image_key]
            try:
                image = Image.open(image_path)
                # image.thumbnail((200, 200))
                image.thumbnail((1000, 1000))
                photo = ImageTk.PhotoImage(image)
                label.configure(image=photo)
                label.image = photo  # Keep a reference
            except Exception as e:
                label.configure(text=f"Error loading image: {str(e)}")

        # Update HTML display
        # try:
        #     with open(current_set['html'], 'r', encoding='utf-8') as f:
        #         html_content = f.read()
        #     self.html_display.delete(1.0, tk.END)
        #     self.html_display.insert(tk.END, html_content)
        # except Exception as e:
        #     self.html_display.delete(1.0, tk.END)
        #     self.html_display.insert(tk.END, f"Error loading HTML: {str(e)}")

        # webview.start(load_url, self.window, args=(current_set['html'], ))
        # webview.start(lambda: load_url(self.window, current_set['html']))

        # Update selected option if previously saved
        set_id = f"{self.current_index}"
        if set_id in self.results:
            self.selected_option.set(self.results[set_id])
        else:
            self.selected_option.set(-1)

    def save_selection(self):
        if self.data_list:
            # set_id = f"{self.current_index}"

            path_list = self.data_list[self.current_index]["html"].split("/")
            set_id = path_list[-3] + "/" + path_list[-1]
            self.results[set_id] = str(self.selected_option.get()) + "/" + str(self.selected_option2.get())
            # self.results[set_id] = str(self.selected_option.get()) + "/" + str(self.selected_option2.get()) + "/" + str(
            #     self.selected_option3.get())

            # Save to file
            with open(f'failure/failure_{self.prompt}_{self.model}.json', 'w') as f:
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
        # try:
        #     driver.quit()
        # except:
        #     print("xx")
        # self.window = webview.create_window('webpage', self.data_list[self.current_index]['html'], width=1600, height=1200)
        # webview.start()
        # driver = initialize_chrome(headless=headless)
        # driver.get(self.data_list[self.current_index]['html'])

        self.driver.get("file:///" + self.data_list[self.current_index]['html'])

        pass


# def main():
#     root = tk.Tk()
#     app = ImageViewerApp(root, model="gpt", prompt="mark_prompt", begin=1, end=101)
#     root.mainloop()
#     app.driver.quit()

def main():
    root = tk.Tk()
    # app = ImageViewerApp(root, model="gemini", prompt="mark_prompt", begin=40, end=41)
    # app = ImageViewerApp(root, model="gpt", prompt="cot_prompt", begin=1, end=101)
    # app = ImageViewerApp(root, model="claude", prompt="direct_prompt", begin=47, end=101)
    # app = ImageViewerApp(root, model="claude", prompt="mark_prompt", begin=1, end=101)
    # app = ImageViewerApp(root, model="gemini", prompt="direct_prompt", begin=35, end=101)
    # app = ImageViewerApp(root, model="claude", prompt="direct_prompt", begin=1, end=128)
    # gemini
    app = ImageViewerApp(root, model="qwen-vl-3B", prompt="direct_prompt", begin=1, end=128)
    root.mainloop()
    app.driver.quit()


if __name__ == "__main__":
    main()
