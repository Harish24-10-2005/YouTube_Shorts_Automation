# CONTENT_PROMPT = """Act as a Viral Content Engineer specializing in crafting captivating YouTube Short scripts centered around impossible or mind-bending scenarios based on the true conditions . Develop an engaging 60 second script for:
# "{title}"
# Your response should:

# Hook viewers within the first 3 seconds to stop them from scrolling.
# Build curiosity and suspense throughout the content.
# Be optimized for AI-generated image-based reels.
# the content need to linear and continous till the end.
# Be structured in a way that can quickly trend and go viral.
# the content should be detailled and not to bore the viewers and not also be consice.
# make the output a 10 segments 6 seconds each segment.
# Maintain a compelling narrative in a 20-line plain paragraph, ensuring viewers are motivated to engage and share and attract the viewers nad hold viwers .
# Return the response in that need to make viral shorts in youtube, engaging format."""

# SCRIPT_PROMPT = """You are a master script and scene creator specializing in highly engaging, viral short-form content. Your task is to generate a 60-second YouTube Short script based on the user-provided content. The final output must be in JSON format with two separate arrays: one for voice scripts and one for image prompts.
# for the content:{content}
# Requirements:
# 1. **Voice Scripts (10 items):**
#    - each scripts must need to be 7 to 10 sec long..not more than that and not less
#    - only the first voice script  starts with "what if ..."content"..."
#    - full voice script need to a linear and understandable format
#    - Each voice script should be 6 seconds or less.
#    - They must be clear, compelling, and easy to understand.
#    - Each script should fully deliver a part of the story, driving curiosity and engagement.
#    - Ensure each voice script aligns perfectly with the corresponding visual scene.

# 2. **Image Prompts (20 items):**
#    - Each voice script is paired with 2 image prompts (totaling 20 images).
#    - Each image prompt is for a 3-second display and must be detailed and vivid.
#    - The prompts should be designed to generate AI images that capture the essence of the scene, enhance the story, and intrigue the viewer.
#    - Use rich descriptive language to specify colors, emotions, settings, and key visual elements.

# 3. **Overall Content:**
#    - The script and images should create a seamless narrative arc for the entire 42-second short.
#    - Every voice script and image prompt must be interconnected, ensuring continuity and maximum viewer engagement.
#    - Focus on building curiosity, encouraging the viewer to stop scrolling, and making the content shareable and trending.
#    - The content must be entirely based on the subject matter provided by the user.
#    - Output the result as a JSON object with two keys: `"voice_scripts"` (an array of 10 voice script strings) and `"image_prompts"` (an array of 20 detailed image description strings).

# Please generate the voice scripts and image prompts as specified, ensuring every prompt is engaging, detailed, and perfectly suitable for creating stunning AI-generated visuals.
# """

CONTENT_PROMPT = """
Act as a Viral Content Engineer and master viral content creator for YouTube Shorts. Your task is to craft an irresistibly engaging 60-second script based on the mysterious topic titled "{title}" that immediately hooks the viewer with a "What if…" or "Imagine…" opening. The final output must deliver a continuous, suspenseful narrative that compels viewers to stop scrolling, share, and rewatch. Follow these detailed guidelines:
make sure that all content need to based on the title ->"{title}".
Overall Narrative Structure:

Length & Flow: Create a 60-second YouTube Short divided into 10 seamlessly connected segments (approximately 6 seconds each). Present the narrative as one cohesive 20-line paragraph.
Hook: The first 3 seconds must start with a powerful hook beginning with “What if…” (or “Imagine…”), instantly grabbing attention.
Continuity: Each segment must flow naturally into the next, using transitional phrases, cause-and-effect logic, and callbacks to earlier points.
Engagement: Use curiosity gaps, emotional triggers, and sensory language throughout. Build suspense gradually and conclude with a mind-bending, satisfying revelation that ties back to the opening hook.
Tone & Style: Maintain a present-tense, active, conversational tone filled with vivid, sensory details and emotional moments.

Hook viewers within the first 3 seconds to stop them from scrolling.
Build curiosity and suspense throughout the content.
Be optimized for AI-generated image-based reels.
the content need to linear and continous till the end.
Be structured in a way that can quickly trend and go viral.
the content should be detailled and not to bore the viewers and not also be consice.
make the output a 10 segments 6 seconds each segment.
Maintain a compelling narrative in a 20-line plain paragraph, ensuring viewers are motivated to engage and share and attract the viewers nad hold viwers .
Return the response in that need to make viral shorts in youtube, engaging format.
The narrative must:
- Feel like one continuous story rather than separate segments
- Build anticipation naturally between segments
- Use transitional phrases to connect ideas
- Include cause-and-effect relationships
- Reference earlier points in later segments
"""

SCRIPT_PROMPT = """
Act as a Viral Content Engineer and master viral content creator for YouTube Shorts. Your task is to craft an irresistibly engaging 60-second script based on the mysterious topic titled "{content}" that immediately hooks the viewer with a "What if…" or "Imagine…" opening. The final output must deliver a continuous, suspenseful narrative that compels viewers to stop scrolling, share, and rewatch. Follow these detailed guidelines:

Overall Narrative Structure:

Length & Flow: Create a 60-second YouTube Short divided into 10 seamlessly connected segments (approximately 6 seconds each). Present the narrative as one cohesive 20-line paragraph.
Hook: The first 3 seconds must start with a powerful hook beginning with “What if…” (or “Imagine…”), instantly grabbing attention.
Continuity: Each segment must flow naturally into the next, using transitional phrases, cause-and-effect logic, and callbacks to earlier points.
Engagement: Use curiosity gaps, emotional triggers, and sensory language throughout. Build suspense gradually and conclude with a mind-bending, satisfying revelation that ties back to the opening hook.
Tone & Style: Maintain a present-tense, active, conversational tone filled with vivid, sensory details and emotional moments.
Important :
all the voice scripts and image prompts must be for given content.
for the content:{content}
# Requirements:


All voiceScripts and image prompts are only related to the content -> {content}
1. Voice Scripts Array (10 items):
Ensure smooth, logical transitions between scripts so that the entire narrative feels continuous and builds in intensity.
Each script should be clear, engaging, and emotionally charged—planting questions or mysteries that get answered later.
- Length: Exactly 6 seconds each if needed more than 6sec also ok
- First script: Starts with compelling "What if..." hook
- each scripts must need to be  7-10 sec long..not more than that and not less
- only the first voice script  starts with "what if ..."content"..."
- full voice script need to a linear and understandable format
- Each voice script should be 6-10 seconds or less.
- They must be clear, compelling, and easy to understand.
- Each script should fully deliver a part of the story, driving curiosity and engagement.
- Ensure each voice script aligns perfectly with the corresponding visual scene.
- Continuous story:Ensure smooth, logical transitions between scripts so that the entire narrative feels continuous and builds in intensity.
- Language: Clear,simple english emotionally engaging
- Transitions: Use connecting phrases between segments
- References: Call back to earlier points
- Questions: Plant and answer mysteries throughout
- Tone: Maintain consistent narrative voice
- Pacing: Build tension systematically
- Ending: Deliver satisfying conclusion

2. Image Prompts Array (20 items):
- Each voice script is paired with 2 image prompts (totaling 20 images).
  - Each image prompt is for a 3-second display and must be detailed and vivid.
  - The prompts should be designed to generate AI images that capture the essence of the scene, enhance the story, and intrigue the viewer.
  - Use rich descriptive language to specify colors, emotions, settings, and key visual elements.
- prompt must be more detailed 3 to 5 lines
- Two 3-second prompts per voice segment
- Format: [Composition][Subject][Action][Mood][Color Scheme][Style]
- Details: Include camera angles, lighting, expressions
- Continuity: Ensure visual flow between scenes
- Movement: Describe dynamic elements and transitions
- Focus: Highlight key story elements
- Atmosphere: Specify emotional tone and ambiance
- Effects: Include any special visual effects
- Quality: Optimize for AI image generation
- Style: Maintain consistent visual aesthetic
Continuity & Impact: Ensure that the visual prompts not only complement the voice scripts but also build a cohesive, mysterious visual narrative that enhances the overall story and maintains viewer intrigue.

3. **Overall Content:**
maintain proper order of image prompt based on the voice script
   - The script and images should create a seamless narrative arc for the entire 60-second short.
   - Every voice script and image prompt must be interconnected, ensuring continuity and maximum viewer engagement.
   - Focus on building curiosity, encouraging the viewer to stop scrolling, and making the content shareable and trending.
   - The content must be entirely based on the subject matter provided by the user.
   -maintain the order of images prompt realated to voicescripts.
   - Output the result as a JSON object with two keys: `"voice_scripts"` (an array of 10 voice script strings) and `"image_prompts"` (an array of 20 detailed image description strings).

Output Format:
{
  "voice_scripts": [
    
  ],
  "image_prompts": [
    
  ]
}


Ensure perfect alignment between voice and visuals, maintaining suspense while delivering a coherent story that compels sharing.
"""