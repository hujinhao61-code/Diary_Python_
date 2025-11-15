import requests
import time
import os
import hashlib
import pyperclip  # Required: pip install pyperclip
from datetime import datetime
import threading
import json


class DouyinAutoDownloader:
    def __init__(self, download_folder="douyin_videos"):
        self.download_folder = download_folder
        self.last_clipboard = ""
        self.running = False

        # Create download folder if it doesn't exist
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

    def get_video_info_from_headers(self, response_headers):
        """Extract video information from response headers"""
        info = {}
        if 'etag' in response_headers:
            etag = response_headers['etag'].strip('"')
            info['etag_short'] = etag[:8]
        if 'content-length' in response_headers:
            size = int(response_headers['content-length'])
            info['size_mb'] = round(size / 1024 / 1024, 2)
        if 'last-modified' in response_headers:
            info['last_modified'] = response_headers['last-modified']
        return info

    def generate_smart_filename(self, video_url, response_headers=None):
        """Generate smart filename with metadata"""
        base_info = {}

        if response_headers:
            header_info = self.get_video_info_from_headers(response_headers)
            base_info.update(header_info)

        content_hash = hashlib.md5(video_url.encode()).hexdigest()[:8]
        base_info['hash'] = content_hash

        timestamp = datetime.now().strftime("%m%d_%H%M%S")
        base_info['time'] = timestamp

        if 'etag_short' in base_info:
            filename = f"dy_{base_info['etag_short']}_{timestamp}.mp4"
        else:
            filename = f"dy_{content_hash}_{timestamp}.mp4"

        return filename, base_info

    def download_video(self, video_url):
        """Download single video"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0',
            'Referer': 'https://www.douyin.com/',
            'Origin': 'https://www.douyin.com',
            'Range': 'bytes=0-',
        }

        try:
            print(f"\n🎯 New URL detected, starting download...")

            # Get file information
            head_response = requests.head(video_url, headers=headers)

            if head_response.status_code in [200, 206]:
                filename, video_info = self.generate_smart_filename(video_url, head_response.headers)
                filepath = os.path.join(self.download_folder, filename)

                print(f"📁 Video Info:")
                for key, value in video_info.items():
                    print(f"   {key}: {value}")
                print(f"💾 Saving as: {filename}")

                # Download file
                response = requests.get(video_url, headers=headers, stream=True)
                total_size = int(response.headers.get('content-length', 0))

                downloaded_size = 0
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            if total_size > 0:
                                progress = (downloaded_size / total_size) * 100
                                print(f"\r📥 Download Progress: {progress:.1f}%", end='', flush=True)

                print(f"\n✅ Download completed! File location: {filepath}")
                return True
            else:
                print(f"❌ Download failed, status code: {head_response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error during download: {e}")
            return False

    def is_douyin_url(self, text):
        """Check if text is a Douyin video URL"""
        return text.startswith('https://v') and 'douyinvod.com' in text and '/video/tos/' in text

    def monitor_clipboard(self):
        """Monitor clipboard for changes"""
        print("🔄 Starting clipboard monitoring...")
        print("💡 Now you just need to copy URL in F12, program will auto-detect and download!")
        print("⏹️ Press Ctrl+C to stop monitoring")

        self.running = True
        self.last_clipboard = pyperclip.paste()

        while self.running:
            try:
                current_clipboard = pyperclip.paste()

                # If clipboard content changed and is Douyin URL
                if (current_clipboard != self.last_clipboard and
                        self.is_douyin_url(current_clipboard)):
                    print(f"\n{'=' * 50}")
                    print(f"📋 New URL detected: {current_clipboard[:80]}...")

                    # Download video
                    self.download_video(current_clipboard)

                    self.last_clipboard = current_clipboard
                    print(f"{'=' * 50}")

                time.sleep(1)  # Check every second

            except KeyboardInterrupt:
                print("\n🛑 Stopped clipboard monitoring")
                self.running = False
                break
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(1)


# Usage example
if __name__ == "__main__":
    # Install dependencies: pip install pyperclip requests

    downloader = DouyinAutoDownloader("MyDouyinVideoLibrary")

    print("🎯 Douyin Auto Downloader")
    print("Usage:")
    print("1. Keep this program running")
    print("2. Open Douyin webpage, press F12")
    print("3. In Network panel, filter media, find video and copy URL")
    print("4. Program will auto-detect and download!")
    print("5. Press Ctrl+C to exit program")
    print("\nStarting monitoring...")

    # Start clipboard monitoring
    downloader.monitor_clipboard()