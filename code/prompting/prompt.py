def get_prompt_description(description, prompt_method):
    direct_prompt_with_description = f"""
    You are a web developer proficient in HTML, CSS and JavaScript.
    The user provides two screenshots of a webpage. 
    The first screenshot shows the webpage in its original state, while the second shows the webpage after the user has interacted with certain elements. 
    You are tasked with creating a webpage that replicates the layout, design, and content of the original screenshot, while incorporating the interactive changes observed in the second screenshot. 
    The differences should be fully implemented, such as changes in color, size, or visibility when interacting with the elements (e.g., clicking a button, hovering over an element, etc.).
    The original state of the generated webpage needs to be consistent with the first screenshot, and the state after interaction needs to be consistent with the second screenshot.


    Requirements:
    - Accurate Replication: The webpage should look identical to the first screenshot before interaction, with attention to details such as font, layout, color, padding, and margins.
    - Interactive Effects: Implement the visual changes in screenshots. This may involve hover effects, click events, or any other form of interaction.
    - Use the exact text from the screenshot.
    - If it involves any images, use \"placeholder.jpg\" as the placeholder. Please make sure to adjust the height and width in "<img src="placeholder.jpg" height="" width="">" to keep image size consistent with the screenshot.
    - Do not hallucinate any dependencies to external files.
    - Do not add comments in the code such as "<!-- Add other navigation links as needed -->" and "<!-- ... other news items ... -->" in place of writing the full code. WRITE THE FULL CODE.
    - Repeat elements as needed to match the screenshot. For example, if there are 15 items, the code should have 15 items. DO NOT LEAVE comments like "<!-- Repeat for each news item -->" or bad things will happen.
    - You need to set the id of the interactive element (which causes the change shown in the second screenshot) as "interact1".
    For example, if the button is clicked in the second screenshot, the id of the button element is set to interact1: "<button id="interact1">Click Me!</button>"
    - Please ensure the code ends with </html> and all code is embedded between the tags <html> and </html>.
    - The interaction description is \"{description}\", please also pay attention to the description during replicate the interaction.

    Combine HTML, CSS and JavaScript codes into one file and respond the codes only (don't output the text before and after the code):
    """

    mark_prompt_with_description = f"""
    You are a web developer proficient in HTML, CSS and JavaScript.
    The user provides two screenshots of a webpage. 
    The first screenshot shows the webpage in its original state, while the second shows the webpage after the user has interacted with certain elements. 
    In the first screenshot, the interactive elements are highlighted with red bounding boxes. In the second screenshot, the changes (after interaction) are highlighted with red bounding boxes 
    You are tasked with creating a webpage that replicates the layout, design, and content of the original screenshot, while incorporating the interactive changes observed in the second screenshot. 
    The differences should be fully implemented, such as changes in color, size, or visibility when interacting with the highlighted elements (e.g., clicking a button, hovering over an element, etc.).
    The original state of the generated webpage needs to be consistent with the first screenshot, and the state after interaction needs to be consistent with the second screenshot.

    Requirements:
    - Accurate Replication: The webpage should look identical to the first screenshot before interaction, with attention to details such as font, layout, color, position, padding, and margins.
    - Interactive Effects: Implement the visual changes highlighted in screenshots (as indicated by the red bounding boxes). This may involve hover effects, click events, or any other form of interaction.
    - Use the exact text from the screenshot.
    - If it involves any images, use \"placeholder.jpg\" as the placeholder. Please make sure to adjust the height and width in "<img src="placeholder.jpg" height="" width="">" to keep image size consistent with the screenshot.
    - Do not hallucinate any dependencies to external files.
    - Please generate interactive elements based on the content in the red bounding box in the first screenshot, and generate interactive effects based on the content in the red bounding box in the second screenshot.
    - Pay attention to the position of the red bounding box, which mark the position of interaction. But do not generate the red bounding box, which is just used for marking the interaction area.
    - Do not add comments in the code such as "<!-- Add other navigation links as needed -->" and "<!-- ... other news items ... -->" in place of writing the full code. WRITE THE FULL CODE.
    - Repeat elements as needed to match the screenshot. For example, if there are 15 items, the code should have 15 items. DO NOT LEAVE comments like "<!-- Repeat for each news item -->" or bad things will happen.
    - You need to set the id of the interactive element (which causes the change shown in the second screenshot) as "interact1".
    For example, if the button is clicked in the second screenshot, the id of the button element is set to interact1: "<button id="interact1">Click Me!</button>"
    - Please ensure the code ends with </html> and all code is embedded between the tags <html> and </html>.
    - The interaction description is \"{description}\", please also pay attention to the description during replicate the interaction.

    Combine HTML, CSS and JavaScript codes into one file and respond the codes only (don't output the text before and after the code):
    """

    cot_prompt_with_description = f"""
    You are a web developer proficient in HTML, CSS and JavaScript.
    The user provides two screenshots of a webpage. 
    The first screenshot shows the webpage in its original state, while the second shows the webpage after the user has interacted with certain elements. 
    You are tasked with creating a webpage that replicates the layout, design, and content of the original screenshot, while incorporating the interactive changes observed in the second screenshot. 
    The differences should be fully implemented, such as changes in color, size, or visibility when interacting with the highlighted elements (e.g., clicking a button, hovering over an element, etc.).

    Requirements:
    - Accurate Replication: The webpage should look identical to the first screenshot before interaction, with attention to details such as font, layout, color, padding, and margins.
    - Interactive Effects: Implement the visual changes in screenshots. This may involve hover effects, click events, or any other form of interaction.
    - Use the exact text from the screenshot.
    - If it involves any images, use \"placeholder.jpg\" as the placeholder. Please make sure to adjust the height and width in "<img src="placeholder.jpg" height="" width="">" to keep image size consistent with the screenshot.
    - Do not hallucinate any dependencies to external files.
    - Do not add comments in the code such as "<!-- Add other navigation links as needed -->" and "<!-- ... other news items ... -->" in place of writing the full code. WRITE THE FULL CODE.
    - Repeat elements as needed to match the screenshot. For example, if there are 15 items, the code should have 15 items. DO NOT LEAVE comments like "<!-- Repeat for each news item -->" or bad things will happen.
    - You need to set the id of the interactive element as "interact1". 
    For example, if the button is clicked in the second screenshot, the id of the button element is set to interact1: "<button id="interact1">Click Me!</button>"
    - Please ensure the code ends with </html> and all code is embedded between the tags <html> and </html>.    
    - The interaction description is \"{description}\", please also pay attention to the description during replicate the interaction.
    
    You should think step by step:

    Step 1: Analyze the difference between the two screenshots. 
    Carefully compare the original and interactive screenshots of the webpage. 
    Identify any visual, structural, or functional changes that have occurred due to user interaction. 
    These could include changes in color, text, position, layout, animations, popups, new component and so on.

    Step 2: Locate the interactive elements. 
    Once you’ve identified the differences, pinpoint which elements on the webpage were interacted with to cause these changes. 
    This could be buttons, dropdown menus, labels, input, image, link, text etc. 
    Specify the exact components and explain how they contribute to the interaction.

    Step 3: Implement the interaction. 
    Writing codes (HTML, CSS and JavaScript) to implement the interaction.
    The interaction function should cause the difference you analyze in Step 1.
    Implement the interaction function on the interactive element you locate from step 2.
    Ensure the functionality matches what is observed in the second screenshot.

    Combine HTML, CSS and JavaScript codes into one file and respond the codes only (don't output the text before and after the code):
    """

    prompts = {
        "direct_prompt": direct_prompt_with_description,
        "cot_prompt": cot_prompt_with_description,
        "mark_prompt": mark_prompt_with_description
    }
    return prompts[prompt_method]


def get_prompt_only_description(description, prompt_method):
    direct_prompt_with_description = f"""
    You are a web developer proficient in HTML, CSS and JavaScript.
    The user provides a screenshot of a webpage. 
    You are tasked with creating a webpage that replicates the layout, design, and content of the original screenshot, while incorporating the interaction. 


    Requirements:
    - Accurate Replication: The webpage should look identical to the first screenshot before interaction, with attention to details such as font, layout, color, padding, and margins.
    - Interaction Replication: The interaction description is \"{description}\", please generate the interaction effect based on the description. This may involve hover effects, click events, or any other form of interaction.
    - Use the exact text from the screenshot.
    - If it involves any images, use \"placeholder.jpg\" as the placeholder. Please make sure to adjust the height and width in "<img src="placeholder.jpg" height="" width="">" to keep image size consistent with the screenshot.
    - Do not hallucinate any dependencies to external files.
    - Do not add comments in the code such as "<!-- Add other navigation links as needed -->" and "<!-- ... other news items ... -->" in place of writing the full code. WRITE THE FULL CODE.
    - Repeat elements as needed to match the screenshot. For example, if there are 15 items, the code should have 15 items. DO NOT LEAVE comments like "<!-- Repeat for each news item -->" or bad things will happen.
    - You need to set the id of the interactive element (which causes the change shown in the second screenshot) as "interact1".
    For example, if the button is clicked in the second screenshot, the id of the button element is set to interact1: "<button id="interact1">Click Me!</button>"
    - Please ensure the code ends with </html> and all code is embedded between the tags <html> and </html>.


    Combine HTML, CSS and JavaScript codes into one file and respond the codes only (don't output the text before and after the code):
    """

    mark_prompt_with_description = f"""
    
    You are a web developer proficient in HTML, CSS and JavaScript.
    The user provides a screenshot of a webpage. 
    You are tasked with creating a webpage that replicates the layout, design, and content of the original screenshot, while incorporating the interaction. 
    In the screenshot, the interactive elements are highlighted with red bounding boxes.

    Requirements:
    - Accurate Replication: The webpage should look identical to the first screenshot before interaction, with attention to details such as font, layout, color, position, padding, and margins.
    - Interaction Replication: The interaction description is \"{description}\", please generate the interaction effect based on the description. This may involve hover effects, click events, or any other form of interaction.
    - Use the exact text from the screenshot.
    - If it involves any images, use \"placeholder.jpg\" as the placeholder. Please make sure to adjust the height and width in "<img src="placeholder.jpg" height="" width="">" to keep image size consistent with the screenshot.
    - Do not hallucinate any dependencies to external files.
    - Please generate interactive elements based on the content in the red bounding box in the first screenshot.
    - Pay attention to the position of the red bounding box, which mark the position of interaction. But do not generate the red bounding box, which is just used for marking the interaction area.
    - Do not add comments in the code such as "<!-- Add other navigation links as needed -->" and "<!-- ... other news items ... -->" in place of writing the full code. WRITE THE FULL CODE.
    - Repeat elements as needed to match the screenshot. For example, if there are 15 items, the code should have 15 items. DO NOT LEAVE comments like "<!-- Repeat for each news item -->" or bad things will happen.
    - You need to set the id of the interactive element (which causes the change shown in the second screenshot) as "interact1".
    For example, if the button is clicked in the second screenshot, the id of the button element is set to interact1: "<button id="interact1">Click Me!</button>"
    - Please ensure the code ends with </html> and all code is embedded between the tags <html> and </html>.

    Combine HTML, CSS and JavaScript codes into one file and respond the codes only (don't output the text before and after the code):
    """

    cot_prompt_with_description = f"""
    You are a web developer proficient in HTML, CSS and JavaScript.
    The user provides a screenshot of a webpage. 
    You are tasked with creating a webpage that replicates the layout, design, and content of the original screenshot, while incorporating the interaction. 


    Requirements:
    - Accurate Replication: The webpage should look identical to the first screenshot before interaction, with attention to details such as font, layout, color, padding, and margins.
    - Interaction Replication: The interaction description is \"{description}\", please generate the interaction effect based on the description. This may involve hover effects, click events, or any other form of interaction.
    - Use the exact text from the screenshot.
    - If it involves any images, use \"placeholder.jpg\" as the placeholder. Please make sure to adjust the height and width in "<img src="placeholder.jpg" height="" width="">" to keep image size consistent with the screenshot.
    - Do not hallucinate any dependencies to external files.
    - Do not add comments in the code such as "<!-- Add other navigation links as needed -->" and "<!-- ... other news items ... -->" in place of writing the full code. WRITE THE FULL CODE.
    - Repeat elements as needed to match the screenshot. For example, if there are 15 items, the code should have 15 items. DO NOT LEAVE comments like "<!-- Repeat for each news item -->" or bad things will happen.
    - You need to set the id of the interactive element (which causes the change shown in the second screenshot) as "interact1".
    For example, if the button is clicked in the second screenshot, the id of the button element is set to interact1: "<button id="interact1">Click Me!</button>"
    - Please ensure the code ends with </html> and all code is embedded between the tags <html> and </html>.


    You should think step by step:

    Step 1: Analyze the interaction description, translate the description into design.
    Step 2: Based on the design you analyze from Step 1, implement the interaction. 

    Combine HTML, CSS and JavaScript codes into one file and respond the codes only (don't output the text before and after the code):
    """

    prompts = {
        "direct_prompt": direct_prompt_with_description,
        "cot_prompt": cot_prompt_with_description,
        "mark_prompt": mark_prompt_with_description
    }
    return prompts[prompt_method]


direct_prompt = """
You are a web developer proficient in HTML, CSS and JavaScript.
The user provides two screenshots of a webpage. 
The first screenshot shows the webpage in its original state, while the second shows the webpage after the user has interacted with certain elements. 
You are tasked with creating a webpage that replicates the layout, design, and content of the original screenshot, while incorporating the interactive changes observed in the second screenshot. 
The differences should be fully implemented, such as changes in color, size, or visibility when interacting with the elements (e.g., clicking a button, hovering over an element, etc.).
The original state of the generated webpage needs to be consistent with the first screenshot, and the state after interaction needs to be consistent with the second screenshot.


Requirements:
- Accurate Replication: The webpage should look identical to the first screenshot before interaction, with attention to details such as font, layout, color, padding, and margins.
- Interactive Effects: Implement the visual changes in screenshots. This may involve hover effects, click events, or any other form of interaction.
- Use the exact text from the screenshot.
- If it involves any images, use \"placeholder.jpg\" as the placeholder. Please make sure to adjust the height and width in "<img src="placeholder.jpg" height="" width="">" to keep image size consistent with the screenshot.
- Do not hallucinate any dependencies to external files.
- Do not add comments in the code such as "<!-- Add other navigation links as needed -->" and "<!-- ... other news items ... -->" in place of writing the full code. WRITE THE FULL CODE.
- Repeat elements as needed to match the screenshot. For example, if there are 15 items, the code should have 15 items. DO NOT LEAVE comments like "<!-- Repeat for each news item -->" or bad things will happen.
- You need to set the id of the interactive element (which causes the change shown in the second screenshot) as "interact1".
For example, if the button is clicked in the second screenshot, the id of the button element is set to interact1: "<button id="interact1">Click Me!</button>"
- Please ensure the code ends with </html> and all code is embedded between the tags <html> and </html>.

Combine HTML, CSS and JavaScript codes into one file and respond the codes only (don't output the text before and after the code):
"""

mark_prompt = """
You are a web developer proficient in HTML, CSS and JavaScript.
The user provides two screenshots of a webpage. 
The first screenshot shows the webpage in its original state, while the second shows the webpage after the user has interacted with certain elements. 
In the first screenshot, the interactive elements are highlighted with red bounding boxes. In the second screenshot, the changes (after interaction) are highlighted with red bounding boxes 
You are tasked with creating a webpage that replicates the layout, design, and content of the original screenshot, while incorporating the interactive changes observed in the second screenshot. 
The differences should be fully implemented, such as changes in color, size, or visibility when interacting with the highlighted elements (e.g., clicking a button, hovering over an element, etc.).
The original state of the generated webpage needs to be consistent with the first screenshot, and the state after interaction needs to be consistent with the second screenshot.

Requirements:
- Accurate Replication: The webpage should look identical to the first screenshot before interaction, with attention to details such as font, layout, color, position, padding, and margins.
- Interactive Effects: Implement the visual changes highlighted in screenshots (as indicated by the red bounding boxes). This may involve hover effects, click events, or any other form of interaction.
- Use the exact text from the screenshot.
- If it involves any images, use \"placeholder.jpg\" as the placeholder. Please make sure to adjust the height and width in "<img src="placeholder.jpg" height="" width="">" to keep image size consistent with the screenshot.
- Do not hallucinate any dependencies to external files.
- Please generate interactive elements based on the content in the red bounding box in the first screenshot, and generate interactive effects based on the content in the red bounding box in the second screenshot.
- Pay attention to the position of the red bounding box, which mark the position of interaction. But do not generate the red bounding box, which is just used for marking the interaction area.
- Do not add comments in the code such as "<!-- Add other navigation links as needed -->" and "<!-- ... other news items ... -->" in place of writing the full code. WRITE THE FULL CODE.
- Repeat elements as needed to match the screenshot. For example, if there are 15 items, the code should have 15 items. DO NOT LEAVE comments like "<!-- Repeat for each news item -->" or bad things will happen.
- You need to set the id of the interactive element (which causes the change shown in the second screenshot) as "interact1".
For example, if the button is clicked in the second screenshot, the id of the button element is set to interact1: "<button id="interact1">Click Me!</button>"
- Please ensure the code ends with </html> and all code is embedded between the tags <html> and </html>.

Combine HTML, CSS and JavaScript codes into one file and respond the codes only (don't output the text before and after the code):
"""

cot_prompt = """
You are a web developer proficient in HTML, CSS and JavaScript.
The user provides two screenshots of a webpage. 
The first screenshot shows the webpage in its original state, while the second shows the webpage after the user has interacted with certain elements. 
You are tasked with creating a webpage that replicates the layout, design, and content of the original screenshot, while incorporating the interactive changes observed in the second screenshot. 
The differences should be fully implemented, such as changes in color, size, or visibility when interacting with the highlighted elements (e.g., clicking a button, hovering over an element, etc.).

Requirements:
- Accurate Replication: The webpage should look identical to the first screenshot before interaction, with attention to details such as font, layout, color, padding, and margins.
- Interactive Effects: Implement the visual changes in screenshots. This may involve hover effects, click events, or any other form of interaction.
- Use the exact text from the screenshot.
- If it involves any images, use \"placeholder.jpg\" as the placeholder. Please make sure to adjust the height and width in "<img src="placeholder.jpg" height="" width="">" to keep image size consistent with the screenshot.
- Do not hallucinate any dependencies to external files.
- Do not add comments in the code such as "<!-- Add other navigation links as needed -->" and "<!-- ... other news items ... -->" in place of writing the full code. WRITE THE FULL CODE.
- Repeat elements as needed to match the screenshot. For example, if there are 15 items, the code should have 15 items. DO NOT LEAVE comments like "<!-- Repeat for each news item -->" or bad things will happen.
- You need to set the id of the interactive element as "interact1". 
For example, if the button is clicked in the second screenshot, the id of the button element is set to interact1: "<button id="interact1">Click Me!</button>"
- Please ensure the code ends with </html> and all code is embedded between the tags <html> and </html>.

You should think step by step:

Step 1: Analyze the difference between the two screenshots. 
Carefully compare the original and interactive screenshots of the webpage. 
Identify any visual, structural, or functional changes that have occurred due to user interaction. 
These could include changes in color, text, position, layout, animations, popups, new component and so on.

Step 2: Locate the interactive elements. 
Once you’ve identified the differences, pinpoint which elements on the webpage were interacted with to cause these changes. 
This could be buttons, dropdown menus, labels, input, image, link, text etc. 
Specify the exact components and explain how they contribute to the interaction.

Step 3: Implement the interaction. 
Writing codes (HTML, CSS and JavaScript) to implement the interaction.
The interaction function should cause the difference you analyze in Step 1.
Implement the interaction function on the interactive element you locate from step 2.
Ensure the functionality matches what is observed in the second screenshot.

Combine HTML, CSS and JavaScript codes into one file and respond the codes only (don't output the text before and after the code):
"""

direct_prompt_all_image = """
You are a web developer proficient in HTML, CSS and JavaScript.
The user provides some screenshots of a webpage. 
The first screenshot shows the webpage in its original state, while others show the webpage after the user has interacted with certain elements. 
You are tasked with creating a webpage that replicates the layout, design, and content of the original screenshot, while incorporating the interactive changes observed in screenshots. 
The differences should be fully implemented, such as changes in color, size, or visibility when interacting with the elements (e.g., clicking a button, hovering over an element, etc.).

Requirements:
- Accurate Replication: The webpage should look identical to the first screenshot before interaction, with attention to details such as font, layout, color, padding, and margins.
- Interactive Effects: Implement the visual changes in screenshots. This may involve hover effects, click events, or any other form of interaction.
- Use the exact text from the screenshot.
- If it involves any images, use \"placeholder.jpg\" as the placeholder. Please make sure to adjust the height and width in "<img src="placeholder.jpg" height="" width="">" to keep image size consistent with the screenshot.
- Do not hallucinate any dependencies to external files.
- Do not add comments in the code such as "<!-- Add other navigation links as needed -->" and "<!-- ... other news items ... -->" in place of writing the full code. WRITE THE FULL CODE.
- Repeat elements as needed to match the screenshot. For example, if there are 15 items, the code should have 15 items. DO NOT LEAVE comments like "<!-- Repeat for each news item -->" or bad things will happen.

Combine HTML, CSS and JavaScript codes into one file and respond the content:
"""

cot_prompt_all_images = """
You are a web developer proficient in HTML, CSS and JavaScript.
The user provides some screenshots of a webpage. 
The first screenshot shows the webpage in its original state, while others (Second, Third, Fourth....) show the webpage after the user has interacted with certain elements. 
You are tasked with creating a webpage that replicates the layout, design, and content of the original screenshot, while incorporating the interactive changes observed in the second screenshot. 
The differences should be fully implemented, such as changes in color, size, or visibility when interacting with the highlighted elements (e.g., clicking a button, hovering over an element, etc.).

Requirements:
- Accurate Replication: The webpage should look identical to the first screenshot before interaction, with attention to details such as font, layout, color, padding, and margins.
- Interactive Effects: Implement the visual changes in screenshots. This may involve hover effects, click events, or any other form of interaction.
- Use the exact text from the screenshot.
- If it involves any images, use \"placeholder.jpg\" as the placeholder. Please make sure to adjust the height and width in "<img src="placeholder.jpg" height="" width="">" to keep image size consistent with the screenshot.
- Do not hallucinate any dependencies to external files.
- Do not generate the red rectangular bounding box, which is just used for marking the interaction area.
- Do not add comments in the code such as "<!-- Add other navigation links as needed -->" and "<!-- ... other news items ... -->" in place of writing the full code. WRITE THE FULL CODE.
- Repeat elements as needed to match the screenshot. For example, if there are 15 items, the code should have 15 items. DO NOT LEAVE comments like "<!-- Repeat for each news item -->" or bad things will happen.
- There are 3 interactions in the generated web page. You need to number these interactive elements from interact1 to interact3, interact1 corresponds to the interaction presented in the second screenshot, and interact2 corresponds to the interaction presented in the third screenshot, and so on. 
For example, if the button is clicked in the second screenshot, the id of the button element is set to interact1: "<button id="interact1">Click Me!</button>"
You should think step by step:

Step 1: Analyze the difference between the first screenshot and other screenshots (Second, Third, Fourth....). 
Carefully compare the original and interactive versions of the webpage. 
Identify any visual, structural, or functional changes that have occurred due to user interaction. 
These could include changes in buttons, popups, animations, text color, layout and so on.

Step 2: Locate the interactive elements. 
Once you’ve identified the differences, pinpoint which elements on the webpage were interacted with to cause these changes. 
This could be buttons, hover effects, dropdown menus, etc. 
Specify the exact components and explain how they contribute to the interaction.

Step 3: Implement the interaction functionality. 
Using the insights from Steps 1 and 2, detail how you would implement this interaction on the webpage. 
This could include writing code, such as HTML, CSS, or JavaScript, to simulate the interaction. 
Ensure the functionality matches what is observed in other screenshots (Second, Third, Fourth....).

Combine HTML, CSS and JavaScript codes into one file and respond the content:
"""
