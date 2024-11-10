import json
import anthropic
from mllm_utils import *
from prompt import *


def all_interaction_prompting(client, image_files, prompt_method):
    images = []
    for image_file in image_files:
        images.append(encode_image(image_file))
    interaction_number = len(images) - 1
    html = claude_call_with_all_images(client, images,
                                       get_prompt_all_interactions(interaction_number=interaction_number,
                                                                   prompt_method=prompt_method))
    return html


def direct_prompting(client, image_file1, image_file2):
    '''
    {original input image, image after interaction + prompt} -> {output html}
    '''

    source_image = encode_image(image_file1)
    interact_image = encode_image(image_file2)
    html = claude_call_with_two_images(client, source_image, interact_image, direct_prompt)
    return html


def mark_prompting(client, image_file1, image_file2):
    '''
    {original input image, image after interaction with marker + prompt} -> {output html}
    '''

    source_image = encode_image(image_file1)
    interact_image = encode_image(image_file2)
    html = claude_call_with_two_images(client, source_image, interact_image, mark_prompt)
    return html


def cot_prompting(client, image_file1, image_file2):
    '''
    {original input image, image after interaction + cot prompt} -> {output html}
    '''

    source_image = encode_image(image_file1)
    interact_image = encode_image(image_file2)
    html = claude_call_with_two_images(client, source_image, interact_image, cot_prompt)

    return html


def generate_page(path, web_number, interact_number, prompt_method):
    save_path = path + f"{web_number}/{interact_number}-{prompt_method}-claude.html"

    if prompt_method == "mark_prompt":
        source_path = path + f"{web_number}/{interact_number}-1-mark.png"
        interact_path = path + f"{web_number}/{interact_number}-2-mark.png"
    else:
        source_path = path + f"{web_number}/{interact_number}-1.png"
        interact_path = path + f"{web_number}/{interact_number}-2.png"

    if prompt_method == "direct_prompt":
        html = direct_prompting(anthropic_client, source_path, interact_path)
    elif prompt_method == "mark_prompt":
        html = mark_prompting(anthropic_client, source_path, interact_path)
    else:
        html = cot_prompting(anthropic_client, source_path, interact_path)

    with open(save_path, "w") as fs:
        fs.write(html)


def generate_page_for_all_interactions(path, web_number, prompt_method):
    save_path = path + f"{web_number}/{prompt_method}-claude.html"

    # interaction_number = get_interact_number(path + f"{web_number}/")
    interaction_number = 3

    if prompt_method == "mark_prompt":
        image_files = [path + f"{web_number}/{1}-1-mark.png"]
    else:
        image_files = [path + f"{web_number}/{1}-1.png"]

    for i in range(1, interaction_number + 1):
        if prompt_method == "mark_prompt":
            image_files.append(path + f"{web_number}/{i}-2-mark.png")
        else:
            image_files.append(path + f"{web_number}/{i}-2.png")

    html = all_interaction_prompting(client=anthropic_client, image_files=image_files, prompt_method=prompt_method)
    with open(save_path, "w") as fs:
        fs.write(html)


if __name__ == "__main__":
    with open("key.json") as fs:
        keys = json.loads((fs.read()))

    anthropic_client = anthropic.Anthropic(
        api_key=keys["claude"]
    )

    # generate_page(path="../../sample/", web_number=1, interact_number=1, prompt_method="direct_prompt")
    # generate_page_for_all_interactions(path="../../sample/", web_number=11,
    #                                    prompt_method="direct_prompt")
    # generate_page_for_all_interactions(path="../../sample/", web_number=1,
    #                                    prompt_method="mark_prompt")
    generate_page_for_all_interactions(path="../../sample/", web_number=0,
                                       prompt_method="mark_prompt")


