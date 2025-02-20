import subprocess
from PIL import Image, ImageDraw
import numpy as np

from selenium.webdriver.firefox.service import Service
import base64
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from selenium.webdriver.firefox.options import Options

class WebDriver:
    def __init__(self, browser_name='firefox', url=None, file=None, string=None, headless=None):
        self.browser_name = browser_name
        self.init_url = None
        self.headless = headless
        self.url = url
        self.file = file
        self.string = string
        self.element_num = 1
        self.main_window = None
        self.driver = self.create_driver()

    def create_driver(self):
        service = Service()
        options = Options()
        if self.headless:
            options.add_argument("-headless")
        driver = webdriver.Firefox(options=options, service=service)


        if self.file:
            driver.get("file:///" + os.getcwd() + "/" + self.file)
            self.init_url = "file:///" + os.getcwd() + "/" + self.file
        elif self.string:
            string = base64.b64encode(self.string.encode('utf-8')).decode()
            driver.get("data:text/html;base64," + string)
        elif self.url:
            driver.get(self.url)
            self.init_url = self.url

        driver.maximize_window()
        self.main_window = driver.current_window_handle
        return driver


    def click_interact(self, element, path):
        """click the element"""
        # folder_path = f"web_images/{file_name}/"
        if not os.path.exists(path):
            os.makedirs(path)

        stop_second = 0.1
        try:
            if self.browser_name != "chrome":
                self.driver.execute_script("arguments[0].scrollIntoView();", element)

            hover = ActionChains(self.driver).click(element)
            hover.perform()
            location = element.location
            x = location['x']
            y = location['y']
            # time.sleep(stop_second)
            time.sleep(stop_second)
            # self.take_screenshot(f"web_images/{file_name}/{self.element_num}_{x}_{y}_click.png")
            self.take_screenshot(path + f"/{self.element_num}_{x}_{y}_click.png")
            self.element_num += 1
            #
            time.sleep(stop_second)
            hover = ActionChains(self.driver).click(element)
            hover.perform()
        except Exception as e:
            print(e)

        # try:
        #     if self.browser_name != "chrome":
        #         self.driver.execute_script("arguments[0].scrollIntoView();", element)
        #
        #     hover = ActionChains(self.driver).move_to_element(element)
        #     hover.perform()
        #     location = element.location
        #     x = location['x']
        #     y = location['y']
        #     # time.sleep(stop_second)
        #     time.sleep(stop_second)
        #     # self.take_screenshot(f"web_images/{file_name}/{self.element_num}_{x}_{y}_click.png")
        #     self.take_screenshot(path + f"/{self.element_num}_{x}_{y}_move.png")
        #     self.element_num += 1
        #     #
        #     time.sleep(stop_second)
        #     hover = ActionChains(self.driver).click(element)
        #     hover.perform()
        # except Exception as e:
        #     print(e)

        # self.close_new_page()

    def take_screenshot(self, filename):
        if self.browser_name == "chrome":
            self.driver.save_screenshot(filename)
        else:
            self.driver.save_full_page_screenshot(filename)

    def quit(self):
        self.driver.quit()



def convert_image_to_code(image_path, output_file, rotation):
    # Open the image using PIL
    image = Image.open(image_path)
    # Convert the image to RGB (or you can use other modes like grayscale if needed)
    image = image.convert("RGB")
    image_array = np.array(image)
    if rotation:
        image_array = np.rot90(image_array, -1)
    x, y, z = image_array.shape
    np.savetxt(output_file, image_array.reshape(x, y * z), fmt='%d', delimiter=',')

    return image_array.reshape(x, y * z)


def read_file(file_path):
    """读取文件并返回每一行的列表"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()


def draw_rectangle(image_path, top_left, bottom_right):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    # draw the rectangle
    draw.rectangle([top_left, bottom_right], outline="red", width=5)
    return img
    # Display the image
    # img.show()


def get_pix(image_path1, image_path2, rotation):
    # git_command = "git" + " diff " + source_file + " " + interaction_file

    output_path1 = "output1.csv"
    output_path2 = "output2.csv"

    # diff_path = "diff.csv"

    print(image_path1, image_path2)

    img_array1 = convert_image_to_code(image_path1, output_file=output_path1, rotation=rotation)
    img_array2 = convert_image_to_code(image_path2, output_file=output_path2, rotation=rotation)


    row_number1, column_number1 = img_array1.shape[0], img_array1.shape[1]
    row_number2, column_number2 = img_array2.shape[0], img_array2.shape[1]

    if column_number1 != column_number2:
        return 0, row_number2

    if row_number1 == row_number2 and column_number1 == column_number2:
        diff_array = img_array1 - img_array2

        # 判断哪些行的非零元素数量不为零
        non_zero_rows = np.any(diff_array != 0, axis=1)

        # 获取这些行的索引
        non_zero_indices = np.where(non_zero_rows)[0]

        return np.min(non_zero_indices), np.max(non_zero_indices)



    git_command = "./git-diff-lines"

    result = subprocess.run(git_command, shell=True, capture_output=True, text=True)
    diff_output = result.stdout
    # Save the diff output to a new file

    diff_output = diff_output.split("\n")
    line_number = []
    for line in diff_output:
        line = line.split(":")
        if len(line) < 2:
            continue
        # file_name = line[0]
        line_number.append(int(line[1]))

    return min(line_number), max(line_number)
    # draw_rectangle(image_path1, line_number)
    # draw_rectangle(image_path2, line_number)


def mark_difference(image_path1, image_path2):
    y_min, y_max = get_pix(image_path1, image_path2, rotation=False)
    x_min, x_max = get_pix(image_path1, image_path2, rotation=True)

    top_left = (x_min, y_min)
    bottom_right = (x_max, y_max)

    interact_name = image_path2.split("/")[-1].split(".")[0]
    base_name2 = image_path2.split(".")[1]
    base_name1 = image_path1.split(".")[1]
    # print(interact_name)
    img1 = draw_rectangle(image_path1, top_left, bottom_right)
    img1.save("./" + base_name1 + "_" + interact_name + "_mark.png")
    img2 = draw_rectangle(image_path2, top_left, bottom_right)
    img2.save("./" + base_name2 + "_mark.png")


def get_interact_part(image_path1, image_path2, save_path):
    y_min, y_max = get_pix(image_path1, image_path2, rotation=False)
    x_min, x_max = get_pix(image_path1, image_path2, rotation=True)

    img = Image.open(image_path2)
    cropped_image = img.crop((x_min, y_min, x_max, y_max))
    cropped_image.save(save_path)

    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2

    return center_x, center_y


def compare_images(image1_path, image2_path):
    # 打开图片并转换为数组
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)

    # 将图片转换为相同的模式
    if img1.mode != img2.mode:
        return False

    # 将图片转换为数组
    img1_array = np.array(img1)
    img2_array = np.array(img2)

    # 比较数组
    return np.array_equal(img1_array, img2_array)


def preprocess_for_evaluation(folder_path):
    html_file = folder_path+".html"
    print(html_file)
    with open(html_file, "r") as fs:
        html_file = fs.read()
    message = {
        "flag": True,
        folder_path: "Good"
    }
    if "</html>" not in html_file:
        message["flag"] = False
        message[folder_path] = "No html tag: [Page generate fail]"
        return message

    files = os.listdir(folder_path)
    images = []
    for file in files:
        if "interact" in file:
            continue
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            images.append(os.path.join(folder_path, file))

    if len(images) != 2:
        if len(images) == 1:
            # print(folder_path, "Only one image:[No interaction]")
            message[folder_path] = "Only one image:[No interaction]"
        else:
            # print(folder_path, "{} images".format(len(images)))
            message[folder_path] = "{} images".format(len(images))
        message["flag"] = False
        return message

    if compare_images(images[0], images[1]):
        # print(folder_path, "Same image:[No interaction or Interaction Fail]")

        message[folder_path] = "Same image:[No interaction or Interaction Fail]"
        message["flag"] = False

    return message