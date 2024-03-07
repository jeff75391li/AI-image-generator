from openai import OpenAI


def generate_image(image_desc, image_style, image_size, refinement_enabled, api_key):
    """Generates an image based on the description, style, and size by calling OpenAI APIs.

                Parameters
                ----------
                image_desc : str
                    The image description
                image_style : str
                    The image style
                image_size : str
                    DALL-E 3 supports 1024x1024, 1024x1792, and 1792x1024
                refinement_enabled: bool
                    Whether GPT should help refine the original description.
                    If true, DALL-E will use the refined prompt generated by GPT.
                api_key : str
                    OpenAI API key
    """

    client = OpenAI(api_key=api_key)
    if refinement_enabled:
        # Let GPT generate a more detailed version of the image description
        refinement_prompt = (f"Generate a detailed prompt to generate an image within fifty words based on the "
                             f"following description: '{image_desc}'")
        refined_desc = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.7,
            messages=[
                {"role": "user", "content": refinement_prompt}
            ]
        ).choices[0].message.content
    else:
        refined_desc = image_desc

    # Combine the description and the style as a complete prompt
    full_prompt = (
        f"Subject: {refined_desc} "
        f"Style: {image_style}."
    )

    image_params = {
        "model": "dall-e-3",
        "n": 1,
        "size": image_size,
        "prompt": full_prompt
    }

    # Call DALL-E model to generate images based on the parameters
    response = client.images.generate(**image_params)
    return response.data[0].model_dump()["url"], refined_desc