import json
import requests

# Load API key from secrets.json file
with open('secrets.json') as f:
    secrets = json.load(f)
yt_api_key = secrets.get("yt_api_key")

# Define the parameters for the request
params = {
    'part': 'snippet,status',
    'key': yt_api_key
}

# Define the video metadata including the YouTube options for shorts
metadata = {
  "snippet": {
    "categoryId": "22",
    "description": "Description of uploaded video.",
    "title": "Test video upload.",
    "tags": [
      "shorts"
    ]
  },
  "status": {
    "privacyStatus": "private"
  }
}

# Define the video file path
video_path = 'Finished/Random Fact_1.mp4'  # Replace 'path/to/your/video.mp4' with the actual path to your video file

# Make the POST request to upload the video
upload_url = 'https://www.googleapis.com/upload/youtube/v3/videos'
files = {'mediaFile': open(video_path, 'rb')}
response = requests.post(upload_url, params=params, json=metadata, files=files)

# Check the response
if response.status_code == 200:
    print('Video uploaded successfully.')
    print('Video ID:', response.json()['id'])
    print('Video URL:', 'https://www.youtube.com/watch?v=' + response.json()['id'])
else:
    print('Error uploading video. Status code:', response.status_code)
    print('Response:', response.text)
