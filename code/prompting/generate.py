import os
from prompt import *
from mllm_utils import *
from openai import OpenAI
import anthropic
import json
from tqdm import tqdm

# os.environ['http_proxy'] = 'http://127.0.0.1:33210'
# os.environ['https_proxy'] = 'http://127.0.0.1:33210'
# os.environ['all_proxy'] = 'socks://127.0.0.1:33211'

api_function_dic = {
    "gemini": gemini_call_with_two_images,
    "gpt": gpt4v_call_with_two_images,
    # "qwen": qwen_call_with_two_images,
    "qwen-vl-72B": qwen_call_with_two_images,
    "qwen-vl-7B": qwen_call_with_two_images,
    "qwen-vl-3B": qwen_call_with_two_images,
    "claude": claude_call_with_two_images
}

encode_function_dic = {
    "gemini": gemini_encode_image,
    "gpt": encode_image,
    "qwen-vl-72B": encode_image,
    "qwen-vl-7B": encode_image,
    "qwen-vl-3B": encode_image,
    "claude": encode_image
}


def critic_prompting(client, image_file1, image_file2):
    '''
    {original input image, image after interaction + prompt} -> {output html}
    '''

    source_image = encode_function_dic[model_name](image_file1)
    interact_image = encode_function_dic[model_name](image_file2)
    html = api_function_dic[model_name](client, source_image, interact_image, self_critic_prompt)

    return html



def direct_prompting(client, image_file1, image_file2):
    '''
    {original input image, image after interaction + prompt} -> {output html}
    '''

    source_image = encode_function_dic[model_name](image_file1)
    interact_image = encode_function_dic[model_name](image_file2)
    html = api_function_dic[model_name](client, source_image, interact_image, direct_prompt)

    return html


def mark_prompting(client, image_file1, image_file2):
    '''
    {original input image, image after interaction with marker + prompt} -> {output html}
    '''

    source_image = encode_function_dic[model_name](image_file1)
    interact_image = encode_function_dic[model_name](image_file2)
    html = api_function_dic[model_name](client, source_image, interact_image, mark_prompt)
    return html


def cot_prompting(client, image_file1, image_file2):
    '''
    {original input image, image after interaction + cot prompt} -> {output html}
    '''

    source_image = encode_function_dic[model_name](image_file1)
    interact_image = encode_function_dic[model_name](image_file2)
    html = api_function_dic[model_name](client, source_image, interact_image, cot_prompt)

    return html


def generate_page(path, web_number, interact_number, prompt_method):
    config_path = path + f"{web_number}/action.json"

    with open(config_path, "r") as f_config:
        config = json.loads(f_config.read())

    # save_path = path + f"{web_number}/result/{interact_number}-{prompt_method}-qwen.html"

    # save_path = path + f"{web_number}/result/{interact_number}-{prompt_method}-qwen-vl-3B.html"
    save_path = path + f"{web_number}/result/{interact_number}-{prompt_method}-{model_name}.html"

    if not os.path.exists(path + f"{web_number}/result/"):
        os.mkdir(path + f"{web_number}/result/")

    # if os.path.exists(save_path):
    #     return
    # else:
    #     print(web_number, interact_number)

    if prompt_method == "mark_prompt":
        source_path = path + f"{web_number}/{config[str(interact_number)]['src']}_mark.png"
        interact_path = path + f"{web_number}/{config[str(interact_number)]['dst']}_mark.png"
        # interact_path = path + f"{web_number}/{interact_number}-2-mark.png"
    else:
        source_path = path + f"{web_number}/{config[str(interact_number)]['src']}.png"
        interact_path = path + f"{web_number}/{config[str(interact_number)]['dst']}.png"

    if prompt_method == "direct_prompt":
        html = direct_prompting(client, source_path, interact_path)
    elif prompt_method == "mark_prompt":
        html = mark_prompting(client, source_path, interact_path)
    elif prompt_method == "cot_prompt":
        html = cot_prompting(client, source_path, interact_path)
    else:
        html = critic_prompting(client, source_path, interact_path)
    # print(html)
    with open(save_path, "w") as fs:
        fs.write(html)


if __name__ == "__main__":
    # model_name = "gemini"
    # model_name = "claude"
    # model_name = "claude"
    # model_name = "qwen-vl-72B"
    # model_name = "gpt"
    model_name = "claude"
    # model_name = "qwen-vl-7B"
    # folder = "../annotation/dataset/"
    folder = "../annotation/dataset/"
    model_name = "claude"

    with open("key.json") as fs:
        keys = json.loads((fs.read()))

    if model_name == "gemini":
        genai.configure(api_key=keys["gemini"])
        client = genai.GenerativeModel('gemini-1.5-flash-latest')
    elif model_name == "gpt":
        client = OpenAI(
            api_key=keys["gpt"],
            base_url="https://openkey.cloud/v1"
        )
    elif model_name == "claude":
        client = anthropic.Anthropic(
            api_key=keys["claude"]
        )
    elif "qwen" in model_name:
        client = OpenAI(
            api_key=keys["qwen"],
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

    # prompt_names = ["mark_prompt"]
    # prompt_names = ["direct_prompt", "cot_prompt", "mark_prompt"]
    prompt_names = ["critic_prompt"]

    generate_page(path=folder, web_number="1",
                     interact_number="1", prompt_method="direct_prompt")

    # for prompt_name in prompt_names:
    #     for i in tqdm(range(111, 128)):
    #         with open(f"{folder}{i}/action.json", "r") as fs:
    #             config_dic = json.loads(fs.read())
    #             for interaction_number in range(1, 10):
    #                 if str(interaction_number) in config_dic:
    #                     # print(i, interaction_number)
    #                     generate_page_v1(path=folder, web_number=str(i),
    #                                      interact_number=str(interaction_number), prompt_method=prompt_name)

    # for i in tqdm(range(101, 119)):
    #     with open(f"{folder}{i}/action.json", "r") as fs:
    #         config_dic = json.loads(fs.read())
    #         for interaction_number in range(1, 10):
    #             if str(interaction_number) in config_dic:
    #                 # print(i, interaction_number)
    #                 generate_page_v1(path=folder, web_number=str(i),
    #                                  interact_number=str(interaction_number), prompt_method="cot_prompt")
    #
    # for i in tqdm(range(101, 119)):
    #     with open(f"{folder}{i}/action.json", "r") as fs:
    #         config_dic = json.loads(fs.read())
    #         for interaction_number in range(1, 10):
    #             if str(interaction_number) in config_dic:
    #                 print(i, interaction_number)
    #                 generate_page_v1(path=folder, web_number=str(i),
    #                                  interact_number=str(interaction_number), prompt_method="mark_prompt")
