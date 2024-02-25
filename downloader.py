import yt_dlp
from yt_dlp.utils import download_range_func

link = r"https://www.youtube.com/watch?v=tz8Puc4W5BM"

# Units: seconds
start = 2
end = 7

yt_opts = {

    'verbose': False,
    'download_ranges': download_range_func(None, [(start, end)]),
    'force_keyframes_at_cuts': True  # Test without it

}

with yt_dlp.YoutubeDL(yt_opts) as ydl:

    ydl.download(link)