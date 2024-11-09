import json

import anthropic
from mllm_utils import *
from prompt import *


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


if __name__ == "__main__":
    with open("key.json") as fs:
        keys = json.loads((fs.read()))

    anthropic_client = anthropic.Anthropic(
        api_key=keys["claude"]
    )

    generate_page(path="../../sample/", web_number=1, interact_number=1, prompt_method="direct_prompt")
