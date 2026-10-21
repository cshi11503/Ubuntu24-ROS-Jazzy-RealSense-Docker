# using chatgpt with API key
# need to pay for credits
# dont wanna spend money on this

import os
import json
import base64
import argparse
import mimetypes

from pathlib import Path
from openai import OpenAI


def encode_image(image_path):
    """
    Convert an image into a Base64-encoded data URL.
    """

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    mime_type, _ = mimetypes.guess_type(image_path)

    if mime_type not in ("image/png", "image/jpeg", "image/webp"):
        raise ValueError(f"Unsupported image format: {mime_type}")

    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")

    return f"data:{mime_type};base64,{encoded}"


def run_vlm(image_path, prompt, model="gpt-5.5"):
    """
    Send an RGB image and text prompt to an OpenAI vision model.
    """

    client = OpenAI()

    image_data = encode_image(image_path)

    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt
                    },
                    {
                        "type": "input_image",
                        "image_url": image_data
                    }
                ]
            }
        ]
    )

    return response.output_text


def main():

    parser = argparse.ArgumentParser(
        description="Send a RealSense RGB image to a VLM."
    )

    parser.add_argument(
        "--image",
        type=str,
        required=True,
        help="Path to the RGB image."
    )

    parser.add_argument(
        "--prompt",
        type=str,
        default="Describe what you see in this image.",
        help="Text instruction for the VLM."
    )

    parser.add_argument(
        "--model",
        type=str,
        default="gpt-5.5",
        help="OpenAI vision model."
    )

    args = parser.parse_args()

    print("\nSending image to VLM...")
    print(f"Image: {args.image}")
    print(f"Prompt: {args.prompt}")
    print(f"Model: {args.model}")

    result = run_vlm(
        image_path=args.image,
        prompt=args.prompt,
        model=args.model
    )

    print("\n===== VLM RESPONSE =====")
    print(result)


if __name__ == "__main__":
    main()