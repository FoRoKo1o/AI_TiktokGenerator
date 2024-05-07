import os
import json
import subprocess
import time

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    else:
        return None

def main():
    config = load_json("config.json")
    if not config:
        print("Failed to load configuration from config.json")
        return
    
    num_videos = config.get("num_videos")
    
    # Step 1: Run GetVideos.py
    print("Running GetVideos.py...")
    subprocess.run(["python", "GetVideos.py"])
    print("GetVideos.py completed.")
    
    # Step 2: Run GenerateVoiceover.py
    print("Running GenerateVoiceover.py...")
    subprocess.run(["python", "GenerateVoiceover.py"])
    print("GenerateVoiceover.py completed.")
    
    # Step 3: Run RunCombineVideos.py num_videos times
    print(f"Running RunCombineVideos.py {num_videos} times...")
    for _ in range(num_videos):
        print(f"Running RunCombineVideos.py - Iteration {_ + 1}...")
        subprocess.run(["python", "RunCombineVideos.py"])
        print(f"RunCombineVideos.py - Iteration {_ + 1} completed.")
    
    print("All scripts completed.")

if __name__ == "__main__":
    main()
