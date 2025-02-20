import json
import os.path
from selenium.webdriver.common.by import By
import cv2
import torch
from torch.nn.functional import cosine_similarity
import clip
from nltk.translate.bleu_score import sentence_bleu
import easyocr
from skimage.metrics import structural_similarity as ssim
import re
import shutil
from metric_utils import *
from tqdm import tqdm

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)


def interact_by_id(file_name, folder_path):
    # print(file_name)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    # if os.path.exists(folder_path):
    #     return
    # else:
    #     print(file_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    web_driver = WebDriver(browser_name='firefox', url=None, file=file_name, string=None, headless=False)

    time.sleep(1)
    web_driver.take_screenshot(folder_path + "0_source.png")
    all_elements = web_driver.driver.find_elements(By.XPATH, "//*")
    interact_elements = [el for el in all_elements if re.match(r'^interact', el.get_attribute('id'))]
    numbers = len(interact_elements)

    for i in range(1, numbers + 1):
        try:
            selenium_element = web_driver.driver.find_element(By.ID, f"interact{i}")
            print(selenium_element.location, selenium_element.id)
            # print(element.tag, element.attrib, xpath, element.text, selenium_element.location)
            # web_driver.move_interact(selenium_element)
            web_driver.click_interact(selenium_element, path=folder_path)
            # parent_element = selenium_element.
            # web_driver.click_interact(parent_element, path=folder_path)

        except Exception as e:
            print(e)
            continue
    web_driver.quit()
    # (folder_path=folder_path)


def clip_similarity(image_path1, image_path2):
    # Load the CLIP model and processor
    # Load and preprocess the images
    if isinstance(image_path1, str) and isinstance(image_path2, str):
        img1 = Image.open(image_path1)
        img2 = Image.open(image_path2)
    else:
        img1 = image_path1
        img2 = image_path2
    # Load and preprocess the images
    img1 = preprocess(img1).unsqueeze(0).to(device)
    img2 = preprocess(img2).unsqueeze(0).to(device)

    # Extract features using CLIP
    with torch.no_grad():
        features1 = model.encode_image(img1)
        features2 = model.encode_image(img2)

    # Normalize the features
    features1 = features1 / features1.norm(p=2, dim=-1, keepdim=True)
    features2 = features2 / features2.norm(p=2, dim=-1, keepdim=True)

    # Compute cosine similarity
    similarity = cosine_similarity(features1, features2)

    # Output the similarity score
    # print(f"Similarity: {similarity.item()}")
    return similarity


def ssim_similarity(image_path1, image_path2):
    image1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)
    image2_resized = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
    score, diff = ssim(image1, image2_resized, full=True)
    return score


def get_text_from_image(image_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path)
    texts = ""
    for (bbox, text, confidence) in result:
        texts += (" " + text)
        # print(f'Text: {text}, Bbox: {bbox}, Confidence: {confidence}')
    return texts


def get_bleu(reference_image, generated_image):
    text1 = get_text_from_image(np.array(reference_image))
    text2 = get_text_from_image(np.array(generated_image))
    if len(text1) != 0 and len(text2) != 0:
        # print(text1)
        # print(text2)
        # text_similarity = SequenceMatcher(None, text1, text2).ratio()

        reference = [text1]
        candidate = text2
        bleu_score = sentence_bleu(reference, candidate)
        # text_similarity = SequenceMatcher(None, text1, text2).ratio()
        return bleu_score
    elif len(text1) == 0 and len(text2) == 0:
        bleu_score = 1
    else:
        bleu_score = None
    return bleu_score


def find_match_interaction(web_page_folder_path, reference_image_path):
    # Traverse the folder and calculate similarity for each image
    max_similarity = 0
    most_similar_image_path = None
    most_similar_image_name = None
    for filename in os.listdir(web_page_folder_path):
        if "0_source" in filename:
            continue
        if "interact" in filename:
            continue
        image_path = os.path.join(web_page_folder_path, filename)
        # Only process files that are images
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path1 = image_path
            image_path2 = reference_image_path
            similarity = clip_similarity(image_path1=image_path1, image_path2=image_path2)
            if similarity.item() > max_similarity:
                max_similarity = similarity.item()
                most_similar_image_path = image_path
                most_similar_image_name = filename

    print(most_similar_image_path, max_similarity)
    return most_similar_image_name, most_similar_image_path, max_similarity


def convert_image_to_code(image_path, output_file):
    # Open the image using PIL
    image = Image.open(image_path)
    # Convert the image to RGB (or you can use other modes like grayscale if needed)
    image = image.convert("RGB")
    # Convert the image to a NumPy array
    image_array = np.array(image)
    x, y, z = image_array.shape
    np.savetxt(output_file, image_array.reshape(x, y * z), fmt='%d', delimiter=',')
    # Print pixel values row by row
    # with open(output_file, "w") as f:
    #     for row in image_array:
    #         # array_string = np.array2string(row, threshold=np.inf, precision=8, suppress_small=False, separator=',')
    #         array_string = np.array2string(row, threshold=np.inf, precision=8, suppress_small=False, separator=',')
    #         array_string = array_string.replace('\n', '')
    #         f.write(array_string)
    #         f.write("\n")


def git_difference(output_file, source_file, interaction_file):
    # # Define the output file name
    # output_file = "diff_output.py"
    # path = "/Users/whalexiao/Downloads/pythonProject/dynamic/codes/"
    #
    # # Define the git diff command. This can be modified to include specific paths or commit ranges.
    # git_command = "git" + " diff " + path + "output1.py" + " " + path + "output2.py"
    t0 = time.time()
    git_command = "git" + " diff " + source_file + " " + interaction_file
    result = subprocess.run(git_command, shell=True, capture_output=True, text=True)
    diff_output = result.stdout
    # Save the diff output to a new file
    with open(output_file, "w") as file:
        file.write(diff_output)
    # print(f"Diff output has been saved to {output_file}")
    results_add = []
    results_delete = []

    with open(output_file, 'r') as file:
        lines = file.readlines()
        # lines = lines[7].split("\n")
        # print("hello")
        for line in lines:
            if line.startswith("-") and line[1].isdigit():
                results_delete.append(line[1:])
            if line.startswith("+") and line[1].isdigit():
                results_add.append(line[1:])

    print(len(results_add), len(results_delete))

    with open(output_file, "w") as file:
        for item in results_add:
            # item = "[" + item + "]"
            file.write(item)
        # array_list.append(ast.literal_eval(item))

    # Convert the list to a numpy array
    array_list = np.loadtxt(output_file, delimiter=',', dtype=np.uint8)
    # array_list = array_list.reshape((-1, len(array_list)))
    if array_list.ndim == 1:
        array_list = array_list.reshape(1, -1)

    x, y = array_list.shape
    array_list = array_list.reshape((x, int(y / 3), 3)).astype(np.uint8)
    image = Image.fromarray(array_list)
    # Display the image
    image.show()
    return image


def get_image_size(image_path):
    with Image.open(image_path) as img:
        width, height = img.size

    return width, height


def get_interact_position(image_path):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 | mask2

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    norm_center_x = None
    norm_center_y = None
    print(len(contours))
    x_min = 10000000000
    y_min = 10000000000
    x_max = 0
    y_max = 0

    # for cnt in contours:
    for cnt in [contours[0]]:
        x, y, w, h = cv2.boundingRect(cnt)
        # 计算中心点
        center_x = x + w // 2
        center_y = y + h // 2
        # 标准化中心点
        norm_center_x = center_x / width
        norm_center_y = center_y / height

        if norm_center_x < x_min:
            x_min = norm_center_x
        if norm_center_y < y_min:
            y_min = norm_center_y
        if norm_center_x > x_max:
            x_max = norm_center_x
        if norm_center_y > y_max:
            y_max = norm_center_y

        # 输出标准化中心点位置
        print(f"Normalized center position: x={norm_center_x:.2f}, y={norm_center_y:.2f}")

    return norm_center_x, norm_center_y
    # return (x_min + x_max) / 2, (y_min + y_max) / 2




def get_all_score(web_name, interact_name, model_name, prompt_name):
    generated_webpage_folder = prediction_path + f"{web_name}/result/{interact_name}-{prompt_name}-{model_name}"
    config_file = prediction_path + f"{web_name}/action.json"

    with open(config_file, "r") as fs:
        config = json.loads(fs.read())
    print(config)

    message = preprocess_for_evaluation(generated_webpage_folder)

    most_similar_image_name, most_similar_image_path, cp_similarity = find_match_interaction(
        web_page_folder_path=generated_webpage_folder,
        reference_image_path=prediction_path + f"{web_name}/{config[interact_name]['dst']}.png")

    print(most_similar_image_path)

    img1 = Image.open(prediction_path + f"{web_name}/{config[interact_name]['dst']}.png")

    bleu_score = 0
    ssim_score = 0
    if most_similar_image_path is not None and message["flag"]:
        img2 = Image.open(most_similar_image_path)
        bleu_score = get_bleu(reference_image=img1, generated_image=img2)
        ssim_score = ssim_similarity(prediction_path + f"{web_name}/{config[interact_name]['dst']}.png",
                                     most_similar_image_path)

    full_page_results = {
        "clip_similarity": cp_similarity,
        # "size_score": size_score,
        "text_similarity": bleu_score,
        "structure_similarity": ssim_score
        # "position_similarity": position_similarity,
        # "color_similarity": color_similarity
    }

    position_similarity = 0
    bleu_score = 0
    interact_score = 0
    ssim_score = 0
    position_similarity_after = 0

    if most_similar_image_name is not None and message["flag"]:
        # src_position = interact_name.split("_")
        # src_width, src_height = get_image_size(prediction_path+f"{web_name}/0_source.png")
        # src_x = int(src_position[1]) / src_height
        # src_y = int(src_position[2]) / src_width

        src_x, src_y = get_interact_position(
            image_path=prediction_path + f"{web_name}/{config[interact_name]['src']}_mark.png")
        src_x_after, src_y_after = get_interact_position(
            image_path=prediction_path + f"{web_name}/{config[interact_name]['dst']}_mark.png")

        interact_position = most_similar_image_name.split("_")
        interact_width, interact_height = get_image_size(
            prediction_path + f"{web_name}/result/{interact_name}-{prompt_name}-{model_name}/0_source.png")
        # interact_x = int(interact_position[1]) / interact_height
        # interact_y = int(interact_position[2]) / interact_width
        interact_x = int(interact_position[1]) / interact_width
        interact_y = int(interact_position[2]) / interact_height
        print(interact_x, interact_y)

        position_similarity = 1 - max(abs(interact_x - src_x), abs(interact_y - src_y))

        img1 = Image.open(prediction_path + f"{web_name}/interaction_{interact_name}.png")
        # img2 = Image.open(prediction_path + f"{web_name}/{interact_name}-{prompt_name}-{model_name}/interact.png")

        generated_src_path = prediction_path + f"{web_name}/result/{interact_name}-{prompt_name}-{model_name}/0_source.png"
        generated_interact_path = most_similar_image_path
        save_path = prediction_path + f"{web_name}/result/{interact_name}-{prompt_name}-{model_name}/interact.png"

        try:
            t1 = time.time()
            center_x, center_y = get_interact_part(generated_src_path, generated_interact_path, save_path)
            t2 = time.time()
            print("Interaction Difference:", t2 - t1)
            interact_width_after, interact_height_after = get_image_size(generated_interact_path)
            interact_x_after = int(center_x) / interact_width_after
            interact_y_after = int(center_y) / interact_height_after
            position_similarity_after = 1 - max(abs(interact_x_after - src_x_after),
                                                abs(interact_y_after - src_y_after))

            img2 = Image.open(save_path)
            ssim_score = ssim_similarity(prediction_path + f"{web_name}/interaction_{interact_name}.png", save_path)
            interact_score = clip_similarity(img1, img2)
            interact_score = interact_score.item()

            bleu_score = get_bleu(reference_image=img1, generated_image=img2)
        except SystemError:
            message["flag"] = False
            message[generated_webpage_folder] = "Same image:[No interaction or Interaction Fail]"

    else:
        print("[Warning]: No Implemented Interaction")

    interact_results = {
        "clip_similarity": interact_score,
        "text_similarity": bleu_score,
        "structure_similarity": ssim_score,
        "position_similarity": position_similarity,
        "position_similarity_after": position_similarity_after
    }
    return full_page_results, interact_results, message


if __name__ == "__main__":
    # web_name = 1
    # interact_name = 1
    # web_name = 2
    # interact_name = "1"
    # model_name = "gpt"
    # model_name = "qwen-vl-3B"
    # model_name = "qwen"
    # model_name = "claude"
    model_name = "gemini"
    # prompt_name = "mark_prompt"
    prompt_name = "direct_prompt"
    # prompt_name = "mark_prompt"
    # prediction_path = "/Users/whalexiao/Downloads/pythonProject/Tool/tmp/Interaction2Code/sample/"
    prediction_path = "../annotation/dataset/"

#                             interact_by_id(
#                                 file_name=prediction_path + f"{web_name}/result/{interaction_number}-{prompt_name}-{model_name}.html",
#                                 folder_path=prediction_path + f"{web_name}/result/{interaction_number}-{prompt_name}-{model_name}/")
#
# full_page_results, interact_results, message = get_all_score(str(web_name),
#                                                                 str(interaction_number),
#                                                                 model_name,
#                                                                 prompt_name)