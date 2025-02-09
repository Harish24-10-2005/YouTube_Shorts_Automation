import os
import time
from queue import Queue
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

class ImageGenerator:
    def __init__(self, api_keys, model="stabilityai/stable-diffusion-xl-base-1.0", 
                 width=576, height=1024, output_dir="assets/images", video_mode: bool = False):
        self.api_keys = api_keys
        self.model = model
        if video_mode:
            self.width = 1920  # YouTube video width
            self.height = 1080  # YouTube video height
        else:
            self.width = 1080  # YouTube Shorts width (portrait)
            self.height = 1920 # YouTube Shorts height
        self.output_dir = output_dir
        self.key_usage = {key: {'count': 0, 'last_used': 0} for key in api_keys}
        os.makedirs(self.output_dir, exist_ok=True)

    def get_available_key(self):
        """Finds a key that hasn't exceeded rate limits"""
        now = time.time()
        for key, usage in self.key_usage.items():
            # Reset counter if more than 60 seconds have passed
            if now - usage['last_used'] > 60:
                usage['count'] = 0
            if usage['count'] < 3:
                return key
        return None

    def generate_image_with_retry(self, prompt, idx, max_retries=5):
        """Generates an image with retry logic and rate limit management"""
        for retry in range(max_retries):
            key = self.get_available_key()
            if not key:
                wait_time = 60 - (time.time() - min([v['last_used'] for v in self.key_usage.values()]))
                print(f"All keys rate limited. Waiting {wait_time:.1f} seconds...")
                time.sleep(max(wait_time, 10))
                continue

            client = InferenceClient(api_key=key)
            try:
                print(f"Generating image {idx} using key ending with {key[-4:]}")
                print(f"Prompt: {prompt}")
                
                start_time = time.time()
                image = client.text_to_image(
                    prompt,
                    model=self.model,
                    width=self.width,
                    height=self.height
                )
                
                output_path = os.path.join(self.output_dir, f"image_{idx}.png")
                image.save(output_path)
                print(f"Saved image {idx} ({image.size[0]}x{image.size[1]}) to {output_path}")
                
                # Update key usage
                self.key_usage[key]['count'] += 1
                self.key_usage[key]['last_used'] = time.time()
                return True

            except Exception as e:
                print(f"Error generating image {idx} (attempt {retry+1}/{max_retries}): {str(e)}")
                if "TooManyRequests" in str(e):
                    self.key_usage[key]['count'] = 3  # Mark key as rate limited
                    time.sleep(30)  # Wait longer after hitting rate limit
                else:
                    time.sleep(10)
        
        print(f"Failed to generate image {idx} after {max_retries} attempts")
        return False

    def generate_all_images(self, prompts):
        """Process all prompts with proper rate limiting"""
        queue = Queue()
        for idx, prompt in enumerate(prompts, 1):
            queue.put((idx, prompt))

        while not queue.empty():
            idx, prompt = queue.get()
            success = self.generate_image_with_retry(prompt, idx)
            if not success:
                queue.put((idx, prompt))  # Re-add failed item to queue
                time.sleep(60)  # Wait before retrying

# if __name__ == "__main__":
#     api_keys = [
#         os.getenv("HUGGING_FACE1"),
#         os.getenv("HUGGING_FACE2")
#     ]
    
#     prompts = [
#         "Blurry phone footage, Triceratops grazing in a suburban backyard, sunny afternoon, slightly out of focus, panicked feeling.",
#         "Ultra-realistic Triceratops peacefully grazing in a meticulously manicured suburban backyard, vibrant green grass, blue sky.",
#         "Quick cuts of scientific articles discussing de-extinction, high-tech laboratory environment with glowing screens, sterile white lighting.",
#         "AI-generated laboratory, scientist in a lab coat examining dinosaur DNA on a holographic display, futuristic equipment, dynamic lighting.",
#         "Animated map showing potential dinosaur habitats overlapping with major cities, red zones indicating high-risk areas, dramatic lighting.",
#         "Detailed map showing dinosaur habitats overlapping with New York City, highlighting Central Park and surrounding areas, chaotic weather effects.",
#         "AI generated images of dinsoaurs invading human settlements, a T-Rex stomping through a suburban neighborhood, destruction and chaos.",
#         "Close-up of a T-Rex foot crushing a car in a suburban street, overturned mailboxes, broken fences, sense of overwhelming power.",
#         "AI images of humans dealing with dinsoaurs in everyday lives, a person dodging a Pterodactyl swooping for their sandwich in a park, humorous.",
#         "A person riding a bike while evading a Pterodactyl trying to snatch their backpack, vibrant park setting, comedic action.",
#         "A computer graphic showing a simplified food chain with humans near the bottom, dinosaurs at the top, stark contrast, informative.",
#         "Food chain graphic, with humans at the bottom, raptors in the middle, and T-Rex at the top, emphasize the change in dominance.",
#         "AI images of a scientist in lab with dinosaur behind glass, concerned expression, high-tech environment, ethical dilemma.",
#         "A concerned scientist peering through reinforced glass at a baby raptor, sterile laboratory setting, dramatic backlighting.",
#         "Mock news footage of military vehicles confronting a dinosaur, stylized for humor, tanks firing at a T-Rex with minimal effect, dry desert.",
#         "Military Humvees firing futilely at a T-Rex, explosions and smoke, comedic overtones, news report style.",
#         "A split screen: one side a pristine, dinosaur-free world, the other a chaotic dinosaur-filled world, stark contrast, thought-provoking.",
#         "Split screen: peaceful, lush forest on one side, dinosaur-infested cityscape on the other, dramatic lighting, clear separation.",
#         "Text overlaid on a vibrant, engaging background, 'Like & Subscribe for more!', dynamic motion graphics, eye-catching colors.",
#         "Animated text 'Like & Subscribe for more!' with a silhouette of a T-Rex roaring in the background, dynamic and energetic, vibrant colors."
#     ]
    
#     generator = ImageGenerator(api_keys, video_mode=True)
#     generator.generate_all_images(prompts)