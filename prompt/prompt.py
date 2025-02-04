CONTENT_PROMPT = """Act as a Viral Content Engineer specializing in crafting captivating YouTube Short scripts centered around impossible or mind-bending scenarios based on the true conditions . Develop an engaging 60 second script for:
"{title}"
Your response should:

Hook viewers within the first 3 seconds to stop them from scrolling.
Build curiosity and suspense throughout the content.
Be optimized for AI-generated image-based reels.
the content need to linear and continous till the end.
Be structured in a way that can quickly trend and go viral.
the content should be detailled and not to bore the viewers and not also be consice.
make the output a 10 segments 6 seconds each segment.
Maintain a compelling narrative in a 20-line plain paragraph, ensuring viewers are motivated to engage and share and attract the viewers nad hold viwers .
Return the response in that need to make viral shorts in youtube, engaging format."""

SCRIPT_PROMPT = """You are a master script and scene creator specializing in highly engaging, viral short-form content. Your task is to generate a 60-second YouTube Short script based on the user-provided content. The final output must be in JSON format with two separate arrays: one for voice scripts and one for image prompts.
for the content:{content}
Requirements:
1. **Voice Scripts (10 items):**
   - each scripts must need to be 7 to 10 sec long..not more than that and not less
   - only the first voice script  starts with "what if ..."content"..."
   - full voice script need to a linear and understandable format
   - Each voice script should be 6 seconds or less.
   - They must be clear, compelling, and easy to understand.
   - Each script should fully deliver a part of the story, driving curiosity and engagement.
   - Ensure each voice script aligns perfectly with the corresponding visual scene.

2. **Image Prompts (20 items):**
   - Each voice script is paired with 2 image prompts (totaling 20 images).
   - Each image prompt is for a 3-second display and must be detailed and vivid.
   - The prompts should be designed to generate AI images that capture the essence of the scene, enhance the story, and intrigue the viewer.
   - Use rich descriptive language to specify colors, emotions, settings, and key visual elements.

3. **Overall Content:**
   - The script and images should create a seamless narrative arc for the entire 42-second short.
   - Every voice script and image prompt must be interconnected, ensuring continuity and maximum viewer engagement.
   - Focus on building curiosity, encouraging the viewer to stop scrolling, and making the content shareable and trending.
   - The content must be entirely based on the subject matter provided by the user.
   - Output the result as a JSON object with two keys: `"voice_scripts"` (an array of 10 voice script strings) and `"image_prompts"` (an array of 20 detailed image description strings).

Please generate the voice scripts and image prompts as specified, ensuring every prompt is engaging, detailed, and perfectly suitable for creating stunning AI-generated visuals.
"""