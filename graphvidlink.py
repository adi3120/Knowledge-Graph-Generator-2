from pytube import YouTube

import streamlit as st

def draw_graph_from_link(linkid):
# Replace 'VIDEO_URL' with the URL of the YouTube video you want to download
	video_url = 'https://www.youtube.com/watch?v='+linkid

	try:
		# Create a YouTube object
		yt = YouTube(video_url)

		# Get a list of all available streams for the video
		streams = yt.streams.filter(progressive=True, file_extension='mp4')

		# Choose a stream with 360p resolution
		stream_360p = streams.filter(res='360p').first()

		# Specify the directory where you want to save the downloaded video
		save_path = ''

		# Specify the desired filename (without the extension)
		filename = 'video.mp4'

		# Download the video with the custom filename
		stream_360p.download(output_path=save_path, filename=filename)

		st.success(f"360p video '{yt.title}' downloaded successfully to {save_path}/{filename}.mp4")
	except Exception as e:
		st.error(f"An error occurred: {e}")