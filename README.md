Video Downloader with Streamlit and yt-dlp
This is a Streamlit web application that allows users to download videos from a URL (e.g., YouTube). The app provides options to select the desired video quality and tracks the download progress.

Features
Fetch available video qualities (with or without audio) for the provided URL.
Select a specific format for downloading.
Progress tracking for the download process with speed and ETA display.
Preview the downloaded video.
Download button to save the video to your local device.
Requirements
Python 3.7+
yt-dlp for video downloading
streamlit for the web interface
Installation
Clone the repository or download the source code.

bash
Copy code
git clone https://github.com/your-repo/video-downloader.git
cd video-downloader
Install the required dependencies using pip.

bash
Copy code
pip install -r requirements.txt
Run the Streamlit app.

bash
Copy code
streamlit run app.py
How to Use
Enter a video URL in the input field (e.g., a YouTube video link).

Click the "Fetch Available Qualities" button to retrieve the list of available formats. The formats will display video and audio options with details on whether it is:

Video with Audio
Video without Audio
Audio only
Select the desired quality from the dropdown menu based on the format information, which includes the size and type (audio or video).

Click "Download Video" to start downloading the selected format. The download progress, including the speed and estimated time remaining (ETA), will be shown during the process.

Once downloaded, you can preview the video within the app and use the "Save Video to Your Computer" button to download the file.

Code Overview
Fetching Formats: The app uses yt-dlp to extract available formats for the video URL and displays the quality options for the user.
Progress Tracking: A progress bar and ETA information are displayed during the download.
Video Preview: After downloading, users can preview the video directly in the Streamlit interface.
Download Options: Users can save the video to their local machine after it has been downloaded.
Example
python
Copy code
# Streamlit interface for video download
st.title("Video Downloader")

# Initialize session state for tracking button click and formats
if "download_clicked" not in st.session_state:
    st.session_state.download_clicked = False
if "formats" not in st.session_state:
    st.session_state.formats = []

# Ask user for the video URL
video_url = st.text_input("Enter the video URL (e.g., https://www.youtube.com/watch?v):")

# Fetch available formats (video qualities)
if st.button("Fetch Available Qualities"):
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(video_url, download=False)
        formats = info.get('formats', [])
    st.session_state.formats = [
        {
            "format_id": f['format_id'],
            "format_note": f.get('format_note', 'Unknown Quality'),
            "filesize": f.get('filesize', 0),
            "acodec": f.get('acodec', 'none'),
            "vcodec": f.get('vcodec', 'none')
        }
        for f in formats if f.get('format_note')
    ]

# Download video based on selected format
if st.button("Download Video"):
    selected_format_id = st.session_state.formats[selected_format_index]['format_id']
    ydl_opts = {
        'format': selected_format_id,
        'outtmpl': 'downloaded_video.mp4'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    st.success("Download complete!")
    st.video('downloaded_video.mp4')
License
This project is licensed under the MIT License.
