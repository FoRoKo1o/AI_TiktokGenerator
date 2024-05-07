import os
import json
import subprocess

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    else:
        return None

def main():
    # Run CombineVideos.py
    subprocess.run(["python", "CombineVideos.py"])
    
    # Read information about used files from temp.json
    temp_file = "temp.json"
    if not os.path.exists(temp_file):
        print("temp.json file not found.")
        return
    
    with open(temp_file, 'r') as temp:
        data = json.load(temp)
    
    # Get file paths from data
    video_file = data.get("video_file")
    mp3_file = data.get("mp3_file")
    
    if not video_file or not mp3_file:
        print("Video or audio file not found in temp.json.")
        return
    
    # Define paths to video and audio files
    video_path = os.path.join("Videos", video_file)
    mp3_path = os.path.join("voiceovers", mp3_file)
    
    # Remove used video and audio files
    if os.path.exists(video_path):
        os.remove(video_path)
        print(f"Removed video file: {video_file}")
    else:
        print(f"Video file not found: {video_file}")
    
    if os.path.exists(mp3_path):
        os.remove(mp3_path)
        print(f"Removed audio file: {mp3_file}")
    else:
        print(f"Audio file not found: {mp3_file}")

if __name__ == "__main__":
    main()
