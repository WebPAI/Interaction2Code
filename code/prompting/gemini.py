from mllm_utils import *
from prompt import *
import os
import json

os.environ['http_proxy'] = 'http://127.0.0.1:33210'
os.environ['https_proxy'] = 'http://127.0.0.1:33210'
os.environ['all_proxy'] = 'socks://127.0.0.1:33211'


def all_interaction_prompting(client, image_files, prompt_method):
    images = []
    for image_file in image_files:
        images.append(encode_image(image_file))
    interaction_number = len(images) - 1
    html = gemini_call_with_all_images(client, images,
                                       get_prompt_all_interactions(interaction_number=interaction_number,
                                                                   prompt_method=prompt_method))
    return html


def direct_prompting(gemini_client, image_file1, image_file2):
    '''
    {original input image, image after interaction + prompt} -> {output html}
    '''

    source_image = gemini_encode_image(image_file1)
    interact_image = gemini_encode_image(image_file2)
    html = gemini_call_with_two_images(gemini_client, source_image, interact_image, direct_prompt)

    return html


def mark_prompting(client, image_file1, image_file2):
    '''
    {original input image, image after interaction with marker + prompt} -> {output html}
    '''

    source_image = gemini_encode_image(image_file1)
    interact_image = gemini_encode_image(image_file2)
    html = gemini_call_with_two_images(client, source_image, interact_image, mark_prompt)

    return html


def cot_prompting(client, image_file1, image_file2):
    '''
    {original input image, image after interaction + cot prompt} -> {output html}
    '''

    source_image = gemini_encode_image(image_file1)
    interact_image = gemini_encode_image(image_file2)
    html = gemini_call_with_two_images(client, source_image, interact_image, cot_prompt)

    return html


def generate_page(gemini_client, path, web_number, interact_number, prompt_method):
    save_path = path + f"{web_number}/{interact_number}-{prompt_method}-gemini.html"

    if prompt_method == "mark_prompt":
        source_path = path + f"{web_number}/{interact_number}-1-mark.png"
        interact_path = path + f"{web_number}/{interact_number}-2-mark.png"
    else:
        source_path = path + f"{web_number}/{interact_number}-1.png"
        interact_path = path + f"{web_number}/{interact_number}-2.png"

    if prompt_method == "direct_prompt":
        html = direct_prompting(gemini_client, source_path, interact_path)
    elif prompt_method == "mark_prompt":
        html = mark_prompting(gemini_client, source_path, interact_path)
    else:
        html = cot_prompting(gemini_client, source_path, interact_path)

    with open(save_path, "w") as fs:
        fs.write(html)


def generate_page_for_all_interactions(path, web_number, prompt_method):
    save_path = path + f"{web_number}/{prompt_method}-gemini.html"

    interaction_number = get_interact_number(path + f"{web_number}/")

    if prompt_method == "mark_prompt":
        image_files = [path + f"{web_number}/{1}-1-mark.png"]
    else:
        image_files = [path + f"{web_number}/{1}-1.png"]

    for i in range(1, interaction_number + 1):
        if prompt_method == "mark_prompt":
            image_files.append(path + f"{web_number}/{i}-2-mark.png")
        else:
            image_files.append(path + f"{web_number}/{i}-2.png")

    html = all_interaction_prompting(client=gemini_client, image_files=image_files, prompt_method=prompt_method)
    with open(save_path, "w") as fs:
        fs.write(html)


if __name__ == "__main__":
    with open("key.json") as fs:
        keys = json.loads((fs.read()))

    genai.configure(api_key=keys["gemini"])
    gemini_client = genai.GenerativeModel('gemini-1.5-flash-latest')

    # generate_page(gemini_client=gemini_client, path="../../sample/", web_number=2, interact_number=1,
    #               prompt_method="direct_prompt")

    generate_page_for_all_interactions(path="../../sample/", web_number=1,
                  prompt_method="direct_prompt")
