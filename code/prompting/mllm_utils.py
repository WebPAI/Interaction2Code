import base64
from PIL import Image
import retry
import google.generativeai as genai
import os


@retry.retry(tries=2, delay=2)
def gemini_call_with_two_images(gemini_client, encoded_image1, encoded_image2, prompt):
    generation_config = genai.GenerationConfig(
        temperature=1,
        candidate_count=1,
        max_output_tokens=4096,
    )

    response = gemini_client.generate_content(
        [prompt, "Original webpage:", encoded_image1, "Webpage after some interaction:",
         encoded_image2],
        generation_config=generation_config)
    print(response)
    response.resolve()
    response = response.text
    response = cleanup_response(response)

    return response


@retry.retry(tries=2, delay=2)
def gemini_call_with_all_images(gemini_client, images, prompt):
    generation_config = genai.GenerationConfig(
        temperature=1,
        candidate_count=1,
        max_output_tokens=4096,
    )
    inputs = [prompt]
    for img in images:
        inputs.append(img)

    response = gemini_client.generate_content(inputs, generation_config=generation_config)
    print(response)
    response.resolve()
    response = response.text
    response = cleanup_response(response)

    return response


@retry.retry(tries=3, delay=2)
def gpt4v_call_with_two_images(openai_client, source_image, interact_image, prompt):
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{source_image}",
                            "detail": "high"
                        },
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{interact_image}",
                            "detail": "high"
                        },
                    },
                ],
            }
        ],
        max_tokens=4096,
        temperature=1,
        seed=42
    )

    print(response)
    response = response.choices[0].message.content.strip()
    response = cleanup_response(response)

    return response


@retry.retry(tries=3, delay=2)
def gpt4v_call_with_all_images(openai_client, images, prompt):
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]

    for img in images:
        img_message = {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{img}",
                "detail": "high"
            }
        }
        messages[0]['content'].append(img_message)

    response = openai_client.chat.completions.create(
        # model="gpt-4-vision-preview",
        model="gpt-4o",
        messages=messages,
        max_tokens=4096,
        temperature=1,
        seed=2024
    )

    response = response.choices[0].message.content.strip()
    response = cleanup_response(response)

    return response


def claude_call_with_two_images(anthropic_client, source_image, interact_image, prompt):
    messages = [
        {"role": "user", "content": [
            {"type": "image", "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": f"{source_image}"
            }},
            {"type": "image", "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": f"{interact_image}"
            }},
            {"type": "text", "text": prompt}
        ]}
    ]

    response = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=4096,
        messages=messages,
        temperature=1
    )
    print(response)
    response = response.content[0].text.strip()
    response = cleanup_response(response)
    return response



def claude_call_with_all_images(anthropic_client, images, prompt):
    messages = [
        {"role": "user", "content":
            [
                {"type": "text", "text": prompt}
            ]
        }
    ]

    for img in images:
        messages[0]["content"].append(
            {"type": "image", "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": f"{img}"
            }}
        )

    response = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=4096,
        messages=messages,
        temperature=1
    )
    print(response)
    response = response.content[0].text.strip()
    response = cleanup_response(response)
    return response


def cleanup_response(response):
    ## simple post-processing
    if response[: 3] == "```":
        response = response[3:].strip()
    if response[-3:] == "```":
        response = response[: -3].strip()
    if response[: 4] == "html":
        response = response[4:].strip()

    ## strip anything before '<!DOCTYPE'
    if '<!DOCTYPE' in response:
        response = response.split('<!DOCTYPE', 1)[1]
        response = '<!DOCTYPE' + response

    ## strip anything after '</html>'
    if '</html>' in response:
        response = response.split('</html>')[0] + '</html>'
    return response


# encoding image for gpt-4o and claude
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# encoding image for gemini
def gemini_encode_image(image_path):
    return Image.open(image_path)


def get_interact_number(folder_path):
    png_count = 0
    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):
            png_count += 1
    return int(png_count / 5)