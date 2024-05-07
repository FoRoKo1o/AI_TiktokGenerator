import os
import json
import random
from gtts import gTTS

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    else:
        return None

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def generate_voiceover(facts, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    for fact in facts:
        tts = gTTS(text=fact, lang='en')
        audio_path = os.path.join(output_path, f"{fact[:10]}.mp3")  # Generate filename from the first 10 characters of the fact
        tts.save(audio_path)

if __name__ == "__main__":
    config = load_json("config.json")
    facts_data = load_json("facts.json")
    
    if config and facts_data:
        num_videos = config.get("num_videos")
        output_path = config.get("output_path")
        
        facts = facts_data.get("facts", [])  # Get the list of facts from the "facts" key
        selected_facts = random.sample(facts, min(num_videos, len(facts)))
        
        generate_voiceover(selected_facts, "voiceovers")
        
        # Remove selected facts from facts.json
        for fact in selected_facts:
            facts.remove(fact)
        
        save_json(facts_data, "facts.json")
        
        print("Voiceovers generated successfully.")
    else:
        print("Failed to load configuration or facts data.")

