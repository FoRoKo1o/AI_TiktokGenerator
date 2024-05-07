import os
import json
import random
from moviepy.editor import VideoFileClip, AudioFileClip

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    else:
        return None

def select_random_file(folder_path, extension):
    files = [file for file in os.listdir(folder_path) if file.endswith(extension)]
    if files:
        return random.choice(files)
    else:
        return None

def generate_unique_filename(folder_path, base_filename):
    index = 1
    while True:
        new_filename = f"{os.path.splitext(base_filename)[0]}_{index}{os.path.splitext(base_filename)[1]}"
        if not os.path.exists(os.path.join(folder_path, new_filename)):
            return new_filename
        index += 1

def main():
    config = load_json("config.json")
    if not config:
        print("Failed to load configuration from config.json")
        return
    
    voiceovers_folder = "voiceovers"
    video_folder = "Videos"
    finished_folder = "Finished"
    temp_file = "temp.json"
    
    if not os.path.exists(finished_folder):
        os.makedirs(finished_folder)
    
    mp3_file = select_random_file(voiceovers_folder, ".mp3")
    if not mp3_file:
        print("No .mp3 files found in the voiceovers folder.")
        return
    
    mp3_path = os.path.join(voiceovers_folder, mp3_file)
    mp3_duration = AudioFileClip(mp3_path).duration
    
    video_file_attempts = 0
    while True:
        video_file = select_random_file(video_folder, ".mp4")
        if not video_file:
            print("No .mp4 files found in the video folder.")
            return
        
        video_path = os.path.join(video_folder, video_file)
        video_duration = VideoFileClip(video_path).duration
        
        if video_duration > mp3_duration + 1:
            # Load video clip and audio clip
            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(mp3_path)
            
            # Trim the video clip to the duration of the audio clip + 1s
            video_clip = video_clip.subclip(0, mp3_duration)
            
            # Add audio clip with offset of 0.5s
            video_clip = video_clip.set_audio(audio_clip.set_start(0.5))
            
            # Generate a unique filename for the output video
            output_filename = generate_unique_filename(finished_folder, "Random Fact.mp4")
            output_path = os.path.join(finished_folder, output_filename)
            
            # Write the final video file
            video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=30)
            print(f"Finished merging {mp3_file} with {video_file}.")
            
            # Close clips
            video_clip.close()
            audio_clip.close()
            
            # Save information about used files to temp.json
            with open(temp_file, 'w') as temp:
                temp.write(json.dumps({"video_file": video_file, "mp3_file": mp3_file, "output_path": output_path}))
            
            return
        
        # If the current video file doesn't meet the requirements, try another one
        print(f"The duration of {video_file} is not at least 1 second longer than {mp3_file}. Trying another video.")
        video_file_attempts += 1
        if video_file_attempts >= 5:
            print("No suitable video file found after 5 attempts. Skipping audio file.")
            return

if __name__ == "__main__":
    main()
