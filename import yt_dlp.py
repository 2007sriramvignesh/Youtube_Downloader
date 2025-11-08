import yt_dlp

def list_formats(url):
    print("\nFetching available formats...\n")
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])

        print(f"Available formats for: {info.get('title')}\n")
        print("{:<10} {:<8} {:<10} {:<10} {:<10}".format("Format ID", "Type", "Res", "FPS", "Codec"))
        print("-" * 60)

        for f in formats:
            if f.get('vcodec') != 'none' and f.get('acodec') == 'none':
                print("{:<10} {:<8} {:<10} {:<10} {:<10}".format(
                    f['format_id'], 'Video',
                    f.get('height', 'N/A'), f.get('fps', 'N/A'),
                    f.get('vcodec', 'N/A')))
            elif f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                print("{:<10} {:<8} {:<10} {:<10} {:<10}".format(
                    f['format_id'], 'Audio',
                    '—', '—',
                    f.get('acodec', 'N/A')))
    return info.get('title')

def download_and_merge(url, video_id, audio_id, title):
    print(f"\nDownloading and merging video ({video_id}) + audio ({audio_id})...\n")
    ydl_opts = {
        'format': f'{video_id}+{audio_id}',
        'merge_output_format': 'mp4',
        'outtmpl': f'{title}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# === RUN ===
video_url = 'https://youtu.be/7HZrale7Ijw?si=oXjH9GKwUxWxxlE1'  # Replace this

title = list_formats(video_url)

video_format_id = input("\nEnter the VIDEO format ID to download: ").strip()
audio_format_id = input("Enter the AUDIO format ID to download: ").strip()

download_and_merge(video_url, video_format_id, audio_format_id, title)
