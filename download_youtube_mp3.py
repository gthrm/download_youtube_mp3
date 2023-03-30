import os
import sys
import subprocess
from pytube import YouTube


def download_youtube_video(url, output_directory):
    try:
        # Fetch video metadata
        yt = YouTube(url)

        # Download the best audio quality available
        audio_stream = yt.streams.filter(only_audio=True).first()
        temp_video_name = "temp_video.mp4"
        temp_video_path = os.path.join(output_directory, temp_video_name)
        audio_stream.download(output_path=output_directory,
                              filename=temp_video_name)

        # Convert the downloaded video to MP3 format using ffmpeg
        output_file = os.path.join(output_directory, f"{yt.title}.mp3")
        cmd = f'ffmpeg -i "{temp_video_path}" -vn -b:a 128k -c:a libmp3lame -y "{output_file}"'
        subprocess.call(cmd, shell=True)

        # Remove the temporary video file
        os.remove(temp_video_path)

        print(f'Video downloaded and converted to MP3 in {output_directory}')
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python download_youtube_mp3.py <youtube_url> <output_directory>"
        )
        sys.exit(1)

    youtube_url = sys.argv[1]
    output_directory = sys.argv[2]

    # Check if output directory exists, if not, create it
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    download_youtube_video(youtube_url, output_directory)
