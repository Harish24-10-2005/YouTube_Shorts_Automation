import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

class ImageGenerator:
    def __init__(self, api_key, model="stabilityai/stable-diffusion-xl-base-1.0", width=576, height=1024, output_dir="assets\images"):
        """
        Initializes the ImageGenerator with the given parameters.
        
        :param api_key: Your Hugging Face API key.
        :param model: The model identifier to be used for image generation.
        :param width: The width of the output image (default is 576 for a 9:16 ratio).
        :param height: The height of the output image (default is 1024 for a 9:16 ratio).
        :param output_dir: The directory where images will be saved.
        """
        self.client = InferenceClient(api_key=api_key)
        self.model = model
        self.width = width
        self.height = height
        self.output_dir = output_dir

        # Create the output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_images(self, prompts):
        """
        Generates and saves images for each prompt in the provided list.
        
        :param prompts: A list of strings, each representing a prompt.
        """
        for idx, prompt in enumerate(prompts, start=1):
            print(f"Generating image {idx} for prompt: {prompt}")
            # Generate the image using the text-to-image method
            image = self.client.text_to_image(
                prompt,
                model=self.model,
                width=self.width,
                height=self.height
            )
            # Define the output file path
            output_path = os.path.join(self.output_dir, f"image{idx}.png")
            # Save the image
            image.save(output_path)
            print(f"Saved image {idx} as {output_path} ({image.size[0]}x{image.size[1]})")

# Example usage:
# if __name__ == "__main__":
#     api_key = os.getenv("HUGGING_FACE")  # Replace with your actual API key
#     prompts = [
#         "A distorted view of Times Square, New York, with giant claw marks raking across the billboard screens. The color is dark, a gritty feeling.",
#         # Add more prompts here if needed.
#     ]

#     generator = ImageGenerator(api_key=api_key)
#     generator.generate_images(prompts)
