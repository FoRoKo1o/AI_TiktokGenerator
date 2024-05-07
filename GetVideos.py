import requests
import os
import json

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    else:
        return []

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def download_videos(api_key, query, orientation, num_videos, output_path, downloaded_videos):
    url = f"https://api.pexels.com/videos/search?query={query}&orientation={orientation}&per_page={num_videos}"
    headers = {"Authorization": api_key}
    
    has_more = True
    page = 1
    videos_downloaded = 0
    
    while has_more and videos_downloaded < num_videos:
        response = requests.get(url + f"&page={page}", headers=headers)
        if response.status_code == 200:
            videos_data = response.json().get("videos", [])
            
            if not videos_data:
                has_more = False
                break
            
            for video_data in videos_data:
                video_id = video_data.get("id")
                
                if video_id not in downloaded_videos and videos_downloaded < num_videos:
                    video_files = video_data.get("video_files")
                    hd_video = next((vf for vf in video_files if vf.get("height") >= 1080), None)
                    
                    if hd_video:
                        video_url = hd_video.get("link")
                        
                        response = requests.get(video_url)
                        if response.status_code == 200:
                            video_content = response.content
                            video_name = f"{video_id}.mp4"
                            video_path = os.path.join(output_path, video_name)
                            
                            with open(video_path, 'wb') as video_file:
                                video_file.write(video_content)
                            
                            downloaded_videos.append(video_id)
                            videos_downloaded += 1
            
            page += 1
        else:
            print("Failed to fetch videos from Pexels API.")
            break
    
    save_json(downloaded_videos, "downloaded_videos.json")

if __name__ == "__main__":
    config = load_json("config.json")
    secrets = load_json("secrets.json")
    downloaded_videos = load_json("downloaded_videos.json")
    
    pexels_api_key = secrets.get("pexels_api_key")
    query = secrets.get("query")
    orientation = secrets.get("orientation")
    
    num_videos = config.get("num_videos")
    output_path = config.get("output_path")
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    download_videos(pexels_api_key, query, orientation, num_videos, output_path, downloaded_videos)
