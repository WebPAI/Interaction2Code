from urllib.parse import urlparse

import gradio as gr
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import json
import keyboard

import time
from lxml import etree
from io import StringIO

global image_index
# global screenshots_list
# screenshots_list = []
image_index = [0] * 50
# save_folder_name = "data"
save_folder_name = "dataset"

def load_web_driver():
    chrome_options = Options()
    chrome_driver_path = "./chromedriver"
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # driver.set_window_size(width=1000, height=400)
    driver.maximize_window()
    return driver


# def process_url(driver, target_url, placeholder_image="https://via.placeholder.com/150"):

def process_url(driver, target_url, placeholder_image="https://i.ibb.co/gjkw4Fk/placeholder.jpg"):
    # Initialize WebDriver

    # driver = initialize_firefox(headless=headless, geckodriver_path=geckodriver_path)
    # driver = initialize_chrome(headless=headless)
    driver.get(target_url)

    # t1 = time.time()
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    html_str = str(soup)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html_str), parser)

    # driver.execute_script("window.scrollTo(0, 0)")
    # time.sleep(5)


    # all_elements = driver.find_elements(By.XPATH, "//*")
    # web_driver.take_screenshot(f"web_images/{tmp_name}/0_{tmp_name}.png")
    # web_driver.take_screenshot(f"web_images/{tmp_name}/0_source.png")
    time.sleep(1)

    for element in tree.iter():
        try:
            xpath = tree.getpath(element)
            selenium_element = driver.find_element(By.XPATH, xpath)
            driver.execute_script("arguments[0].scrollIntoView();", selenium_element)
            print(element.tag, element.attrib, xpath, element.text, selenium_element.location)
        except Exception as e:
            print(e)
            continue
    time.sleep(5)
    try:
        # Navigate to the target URL

        # Wait for the page to load completely
        # time.sleep(3)  # Adjust as needed or use WebDriverWait for better control

        # Process the WebDriver to modify the page
        process_webdriver(driver, placeholder_image_url=placeholder_image)
        process_webdriver(driver, placeholder_image_url=placeholder_image)

    except Exception as e:
        # Quit the driver to close the browser
        print(e)
        # driver.quit()


def process_webdriver(driver, placeholder_image_url="https://via.placeholder.com/150"):
    """
    Modifies the current page loaded in the Firefox WebDriver by:
    - Removing all external links.
    - Replacing all images with a placeholder image.

    Args:
        driver: Selenium WebDriver instance (Firefox).
        placeholder_image_url (str): URL of the placeholder image.

    Returns:
        driver: The modified WebDriver instance.
    """
    # Get the current page URL to determine the domain
    current_url = driver.current_url
    parsed_current = urlparse(current_url)
    current_domain = parsed_current.netloc

    # JavaScript to remove external links
    # remove_external_links_js = f"""
    # (function() {{
    #     var links = document.getElementsByTagName('a');
    #     for (var i = 0; i < links.length; i++) {{
    #         var link = links[i];
    #         var href = link.getAttribute('href');
    #         if (href) {{
    #             try {{
    #                 var parsed_href = new URL(href, window.location.href);
    #                 if (parsed_href.hostname !== 'xxx') {{
    #                     // Remove href to disable the link
    #                     link.removeAttribute('href');
    #                 }}
    #             }} catch(e) {{
    #                 // Invalid URL, ignore
    #             }}
    #         }}
    #     }}
    # }})();
    # """

    # Disable lazy loading by removing the 'loading="lazy"' attribute from all images

    remove_lazy_load = """
        let images = document.querySelectorAll('img[loading="lazy"]');
        images.forEach(img => img.removeAttribute('loading'));
    """

    show_all_image = """
        let images = document.querySelectorAll('img');
        images.forEach(img => {
            if (img.dataset.src) {
                img.src = img.dataset.src;
            }
        });
    """

    # Alternatively, force the image source to load immediately

    remove_external_links_js = f"""
    (function() {{
        var links = document.getElementsByTagName('a');
        for (var i = 0; i < links.length; i++) {{
            var link = links[i];
            var href = link.getAttribute('href');
            if (href) {{
                try {{
                    var parsed_href = new URL(href, window.location.href);
                    link.removeAttribute('href');
                }} catch(e) {{
                    // Invalid URL, ignore
                }}
            }}
        }}
    }})();
    """

    # JavaScript to replace all images with the placeholder
    replace_images_js = f"""
    (function() {{
        var placeholder = '{placeholder_image_url}';

        // Function to replace image source
        function replaceSrc(element) {{
            element.src = placeholder;
            element.removeAttribute('srcset');
        }}

        // Replace all <img> elements
        var imgs = document.getElementsByTagName('img');
        for (var i = 0; i < imgs.length; i++) {{
            replaceSrc(imgs[i]);
        }}

        // Replace all <source> elements within <picture>
        var sources = document.getElementsByTagName('source');
        for (var i = 0; i < sources.length; i++) {{
            var source = sources[i];
            source.src = placeholder;
            source.removeAttribute('srcset');
        }}

        // Replace all <input type="image">
        var inputs = document.querySelectorAll('input[type="image"]');
        for (var i = 0; i < inputs.length; i++) {{
            inputs[i].src = placeholder;
        }}

        // Replace CSS background images
        var allElements = document.getElementsByTagName('*');
        for (var i = 0; i < allElements.length; i++) {{
            var elem = allElements[i];
            var style = window.getComputedStyle(elem);
            if (style.backgroundImage && style.backgroundImage !== 'none') {{
                elem.style.backgroundImage = "url('{placeholder_image_url}')";
                // Optionally, adjust background size or other properties
                elem.style.backgroundSize = 'cover';
            }}
        }}

        // Replace inline SVG images that use <image> tags
        var svgImages = document.getElementsByTagName('image');
        for (var i = 0; i < svgImages.length; i++) {{
            svgImages[i].setAttribute('href', '{placeholder_image_url}');
            svgImages[i].setAttributeNS('http://www.w3.org/1999/xlink', 'href', '{placeholder_image_url}');
        }}

        // Optionally, remove srcset from <video> and <audio> if they contain image-like sources
        var mediaSources = document.querySelectorAll('video, audio');
        mediaSources.forEach(function(media) {{
            media.removeAttribute('poster'); // Remove video poster images
        }});

    }})();
    """

    # Scroll down incrementally to load dynamic content (like lazy-loading images)
    # for i in range(10):
    #     driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
    #     time.sleep(1)

    # Adding a delay for each scroll to let content load
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Execute the JavaScript on the current page
    driver.execute_script(remove_lazy_load)
    driver.execute_script(show_all_image)
    driver.execute_script(remove_external_links_js)
    driver.execute_script(replace_images_js)
    # 查找所有外部链接
    external_links = driver.find_elements(By.XPATH, "//a[starts-with(@href, 'https://')]")
    # 删除外部链接
    for link in external_links:
        driver.execute_script("arguments[0].remove();", link)
    return driver


class LinkNavigator:
    def __init__(self, begin_id):
        # self.links = [
        #     "https://salinaka-ecommerce.web.app/shop",
        #     "https://www.invoiceninja.com",
        #     "https://adventar.org",
        #     "https://jitsi.org/jitsi-meet",
        # ]
        self.links = [
            "https://salinaka-ecommerce.web.app/shop",
            "https://www.invoiceninja.com",
        ]
        # self.begin_id = 10
        self.begin_id = begin_id
        # self.current_index = 0
        self.current_index = 1

        self.set_image_index()


    def set_image_index(self):
        screenshot_dir = f"./{save_folder_name}/{self.current_index}"
        index = 0
        for filename in os.listdir(screenshot_dir):
            if filename.endswith('.png') and filename.split(".")[0].isdigit():
                img_id = int(filename.split(".")[0])
                if img_id > index:
                    index = img_id
        image_index[self.current_index] = index + 1
        print(image_index)


    def get_current_link(self):
        if 0 <= self.current_index < len(self.links):
            return self.links[self.current_index]
        return ""

    def get_current_id(self):
        return str(self.begin_id + self.current_index)

    def next_link(self):
        if self.current_index < len(self.links) - 1:
            self.current_index += 1
        return self.get_current_link()

    def last_link(self):
        if self.current_index >= 1:
            self.current_index -= 1
        return self.get_current_link()


def process_open(link):
    try:
        # driver.get(link)
        process_url(driver=driver, target_url=link, placeholder_image="https://i.ibb.co/gjkw4Fk/placeholder.jpg")
        # iframe_html = f'<iframe src="{link}" width="100%" height="800px" frameborder="0"></iframe>'
        # return iframe_html
    except Exception as e:
        # return f"Failed to load link: {str(e)}"
        print("Failed to load link: {str(e)}")


navigator = LinkNavigator(begin_id=0)


def take_screenshot():
    global image_index
    try:
        # body = driver.find_element(By.TAG_NAME, "body")
        # total_height = body.size['height']
        # total_width = body.size['width']
        #
        # driver.set_window_size(total_width, total_height)

        screenshot_dir = f"./{save_folder_name}/{navigator.current_index}"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        filename = f"{screenshot_dir}/{image_index[navigator.current_index]}.png"

        screenshot_data = driver.get_screenshot_as_png()

        with open(filename, "wb") as file:
            file.write(screenshot_data)
            image_index[navigator.current_index] += 1

        return f"Screenshot taken: {filename}"
    except Exception as e:
        return f"Screenshot failed: {str(e)}"


def input_text(img_dir):
    img_paths_list = [os.path.join(img_dir, name) for name in sorted(os.listdir(img_dir)) if
                      name.endswith(('.png', '.jpg', '.webp', '.tif', '.jpeg'))]

    dict_path = []
    for i in range(len(img_paths_list)):
        # dict_path.append((img_paths_list[i], 'img_descrip' + str(i)))
        dict_path.append((img_paths_list[i], img_paths_list[i]))
    print(dict_path)
    return dict_path


# def save(link, topic, framework, src, dst, operation, fdesc, bdesc):
def save(link, topic, framework, src, dst, operation, description, tag_type, visual_type):
    save_path = f"./{save_folder_name}/{navigator.current_index}/action.json"
    if os.path.exists(save_path):
        with open(save_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for i in range(2, 1000):
            key = str(i)
            if key not in data:
                data[key] = {
                    "src": src,
                    "dst": dst,
                    "action": operation,
                    "description": description,
                    "tag type": tag_type,
                    "visual type": visual_type
                }
                print(key)
                with open(save_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                return f"Description Saved:{link}"
    else:
        save_file = {
            "link": link,
            "topic": topic,
            "framework": framework,
            "1": {
                "src": src,
                "dst": dst,
                "action": operation,
                "description": description,
                "tag type": tag_type,
                "visual type": visual_type
            },
        }
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(save_file, f, ensure_ascii=False, indent=4)
        return f"Description Saved:{link}"


def get_demo():
    tag_options = ["button", "input", "link", "iframe", "textarea", "option", "select", "form", "label", "detail",
                   "progress", "datalist",
                   "summary", "output", "image", "video", "dialog", "audio", "template", "text", "area", "span", "table"
                   ]

    visual_options = ["new component", "text", "color", "new window", "position", "size", "switch", "new page"]

    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column(scale=2):
                web_id_input = gr.Textbox(label="Web ID", value=navigator.get_current_id(), interactive=False)
                # link_input = gr.Textbox(label="Link", value=navigator.get_current_link(), interactive=False)
                link_input = gr.Textbox(label="Link", value=navigator.get_current_link(), interactive=True)
                topic_input = gr.Textbox(label="Topic", placeholder="Topic")
                # framework_input = gr.Textbox(label="Framework/Language", placeholder="Framework/Language")
                framework_input = gr.Textbox(label="Framework/Language", placeholder="Framework/Language")
                src_id_input = gr.Textbox(label="src_id", placeholder="Source ID")
                dst_id_input = gr.Textbox(label="dst_id", placeholder="Destination ID")
                operation_input = gr.Textbox(label="Operation", placeholder="Operation")
                description_input = gr.Textbox(label="Interaction Description", placeholder="Interaction Description")

                # tag_type_input = gr.Dropdown(choices=tag_options, label="Tag label")
                # visual_type_input = gr.Dropdown(choices=visual_options, label="Visual label")
                tag_type_input = gr.CheckboxGroup(choices=tag_options, label="Tag label")
                # visual_type_input = gr.Textbox(choices=visual_options, label="Visual label:switch/new component")

                visual_type_input = gr.CheckboxGroup(visual_options, label="Visual label")

                # gr.Dropdown(choices=["Option 1", "Option 2", "Option 3"], label="Tag label", placeholder="Interaction Description")

                # 创建一个Select组件，并设置初始值为"选项1"
                # select_component = gr.Select(options, default="选项1", label="Tag Label")

                # fdescription_input = gr.Textbox(label="FDescription", placeholder="Front End Description")
                # bdescription_input = gr.Textbox(label="BDescription", placeholder="Back End Description")

                with gr.Row():
                    open_btn = gr.Button("Open", variant="primary")
                    save_btn = gr.Button("Save", variant="primary")
                    screenshot_btn = gr.Button("Take Screenshot", variant="primary")

            with gr.Column(scale=4):
                with gr.Row():
                    last_btn = gr.Button("Last", variant="primary")
                    next_btn = gr.Button("Next", variant="primary")
                    output = gr.Textbox(label="Output")
                with gr.Row():
                    # dir_inputs = gr.Textbox(label="Image Directory", placeholder='./data/0')
                    dir_inputs = gr.Textbox(label="Image Directory", placeholder=f'./{save_folder_name}/0',
                                            value="./{}/{}".format(save_folder_name, navigator.get_current_id()))
                    # web_id_input = gr.Textbox(label="Web ID", value=navigator.get_current_id(), interactive=False)
                    show_btn = gr.Button(value="Show", elem_id="generate-btn", variant="primary")
                with gr.Row():
                    imagebox = gr.Gallery(
                        label="Interaction Images",
                        type="filepath",
                        # height=850,
                    )
                # dir_input = gr.Textbox(placeholder='./data/0')
                # website_display = gr.HTML()

                # gr.Interface(
                #     fn=input_text,
                #     inputs=gr.Textbox(placeholder='./data/0'),
                #     # inputs=take_screenshot(),
                #     # inputs=gr.inputs.Image(type="pil"),
                #     # outputs=gr.Gallery(label="最终的结果图片").style(height='auto', columns=4),
                #     outputs=gr.Gallery(label="Screenshots"),
                # )

        def update_link():
            next_link = navigator.next_link()
            next_id = navigator.get_current_id()
            next_dir = f"./{save_folder_name}/{next_id}"
            return next_link, next_id, next_dir, "", "", "", "", "", "", "", ""

        def back_link():
            last_link = navigator.last_link()
            last_id = navigator.get_current_id()
            last_dir = f"./{save_folder_name}/{last_id}"
            return last_link, last_id, last_dir

        show_btn.click(
            input_text,
            inputs=[dir_inputs],
            outputs=[imagebox],  # Update both components on generation
        )

        open_btn.click(
            fn=process_open,
            inputs=[link_input],
            # outputs=[website_display]
        )

        save_btn.click(
            fn=save,
            inputs=[
                link_input, topic_input, framework_input,
                src_id_input, dst_id_input, operation_input,
                description_input, tag_type_input, visual_type_input
            ],
            outputs=[output]
        )

        screenshot_btn.click(
            fn=take_screenshot,
            inputs=[],
            outputs=[output]
        )

        next_btn.click(
            fn=update_link,
            inputs=[],
            outputs=[link_input, web_id_input, dir_inputs,
                     topic_input, framework_input, src_id_input, dst_id_input, operation_input, description_input,
                     tag_type_input, visual_type_input
                     ]
        )

        last_btn.click(
            fn=back_link,
            inputs=[],
            outputs=[link_input, web_id_input, dir_inputs]
        )

        return demo


def handle_exit(e):
    if keyboard.is_pressed('ctrl') and e.name == 'c':
        print("\nExiting...")
        os._exit(0)


if __name__ == "__main__":
    driver = load_web_driver()
    keyboard.add_hotkey('i+p', take_screenshot, suppress=True, trigger_on_release=True)
    print("Press i+p to take a screenshot. Press ctrl+c to exit.")
    # keyboard.wait('ctrl+c')
    keyboard.on_press(handle_exit)

    demo = get_demo()
    demo.launch()
    driver.quit()
