import streamlit as st
import yt_dlp
from pathlib import Path
import os

# Streamlit interface for video download
st.title("Video Downloader")

# Initialize session state for tracking button click
if "download_clicked" not in st.session_state:
    st.session_state.download_clicked = False

# Step 1: Ask user for the video URL
video_url = st.text_input("Enter the video URL (e.g., https://www.youtube.com/watch?v):")

# Function to update the progress bar and information
def update_progress(d, progress_bar, progress_info):
    """Update the Streamlit progress bar and info based on download status."""
    if d['status'] == 'downloading':
        if d.get('total_bytes') is not None:
            progress = d['downloaded_bytes'] / d['total_bytes']
            progress_bar.progress(progress)

            # Initialize variables for download info
            downloaded_bytes = d['downloaded_bytes']
            total_bytes = d['total_bytes']
            speed = d.get('speed')  # Use .get() to avoid KeyError
            eta = d.get('eta')  # Use .get() to avoid KeyError

            # Check if speed and eta are not None
            if speed is not None and eta is not None:
                speed_mib = speed / (1024 * 1024)  # Convert to MiB/s
                eta_minutes = eta // 60
                eta_seconds = eta % 60
                
                # Create formatted information string
                progress_info.text(
                    f"{downloaded_bytes / (1024 * 1024):.1f}MB of "
                    f"{total_bytes / (1024 * 1024):.1f}MB at "
                    f"{speed_mib:.2f}MB/s ETA {eta_minutes:02}:{eta_seconds:02}"
                )
            else:
                # If speed or ETA is not available, show partial info
                progress_info.text(
                    f"{downloaded_bytes / (1024 * 1024):.1f}MB of "
                    f"{total_bytes / (1024 * 1024):.1f}MB"
                )

# Step 2: Button to start the download
if not st.session_state.download_clicked:
    if st.button("Download Video"):
        if video_url:
            # Hide the button once clicked
            st.session_state.download_clicked = True

            # Define temporary save location
            temp_video_location = Path(os.getcwd()) / "downloaded_video.mp4"
            
            # Options for yt-dlp
            ydl_opts = {
                'outtmpl': str(temp_video_location),
                'format': 'best',  # Download the best video and audio combined
                'progress_hooks': [lambda d: update_progress(d, progress_bar, progress_info)]
            }

            # Create a progress bar and information text
            progress_bar = st.progress(0)
            progress_info = st.empty()  # Placeholder for progress info

            # Show downloading message and spinner
            with st.spinner('Downloading...'):
                try:
                    # Use yt-dlp for the provided URL
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([video_url])
                    
                    # Preview the downloaded video
                    st.success("Video downloaded successfully!")
                    st.video(str(temp_video_location))  # Display video in the interface

                    # Provide download button
                    with open(temp_video_location, "rb") as video_file:
                        st.download_button(
                            label="Save Video to Your Computer",
                            data=video_file,
                            file_name="downloaded_video.mp4",
                            mime="video/mp4"
                        )
                        
                    # Remove the temporary file after download
                    os.remove(temp_video_location)

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    # Remove the temporary file if it exists and an error occurs
                    if temp_video_location.exists():
                        os.remove(temp_video_location)

                # Reset button state after download
                st.session_state.download_clicked = False
                
            # Reset progress bar
            progress_bar.empty()
            progress_info.empty()
                
        else:
            st.warning("Please enter a valid video URL.")
else:
    st.warning("Download in progress. Please wait...")