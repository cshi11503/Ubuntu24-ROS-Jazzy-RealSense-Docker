# Qwen3-VL-4B-Instruct with Hugging Face Transformers.
import argparse
import time
from pathlib import Path

import torch
from PIL import Image
from transformers import Qwen3VLForConditionalGeneration, AutoProcessor


MODEL_ID = "Qwen/Qwen3-VL-4B-Instruct"


def load_model():
    """
    Load Qwen3-VL onto the GPU.
    """

    print(f"[INFO] Loading model: {MODEL_ID}")

    processor = AutoProcessor.from_pretrained(MODEL_ID)

    model = Qwen3VLForConditionalGeneration.from_pretrained(
        MODEL_ID,
        dtype=torch.bfloat16,
        device_map="auto",
    )

    model.eval()

    print("[INFO] Model loaded successfully!")

    return model, processor


def run_inference(model, processor, image_path, prompt):
    """
    Run VLM inference on a saved RGB image.
    """

    image_path = Path(image_path)

    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = Image.open(image_path).convert("RGB")

    print(f"[INFO] Image size: {image.width} x {image.height}")

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": image,
                },
                {
                    "type": "text",
                    "text": prompt,
                },
            ],
        }
    ]

    inputs = processor.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt",
    )

    inputs = inputs.to(model.device)

    print("[INFO] Running inference...")

    torch.cuda.synchronize()
    start_time = time.perf_counter()

    with torch.inference_mode():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=False,
        )

    torch.cuda.synchronize()
    inference_time = time.perf_counter() - start_time

    # Remove input tokens from generated output
    generated_ids_trimmed = [
        output_ids[len(input_ids):]
        for input_ids, output_ids in zip(
            inputs.input_ids, generated_ids
        )
    ]

    output_text = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )

    return output_text[0], inference_time


def main():

    parser = argparse.ArgumentParser(
        description="Local Qwen3-VL inference on RealSense RGB images"
    )

    parser.add_argument(
        "--image",
        type=str,
        required=True,
        help="Path to RGB image",
    )

    parser.add_argument(
        "--prompt",
        type=str,
        default="Describe what you see in this image.",
        help="Text prompt for VLM",
    )

    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU is not available")

    print(f"[INFO] GPU: {torch.cuda.get_device_name(0)}")

    model, processor = load_model()

    response, inference_time = run_inference(
        model,
        processor,
        args.image,
        args.prompt,
    )

    print("\n===== VLM RESPONSE =====")
    print(response)

    print(f"\n[INFO] Inference time: {inference_time:.2f} seconds")


if __name__ == "__main__":
    main()