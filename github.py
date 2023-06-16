import requests
import urllib.request
import os


class Github:
    def __init__(self):
        self.owner = "OpenStickCommunity"
        self.repo = "GP2040-CE"
        self.firmware_dir = "firmware"

    def get_latest_release_info(self):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/releases"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for non-2xx status codes

            releases = response.json()
            for release in releases:
                if not release.get("prerelease"):
                    version = release["tag_name"]
                    release_date = release["published_at"]
                    assets = release["assets"]
                    # Remove asset with name "flash_nuke.uf2"
                    assets = [
                        asset for asset in assets if asset["name"] != "flash_nuke.uf2"]

                    return version, release_date, assets
        except requests.exceptions.RequestException as e:
            print("Failed to fetch release info:", e)

        return None, None, None

    def download_file(self, url):
        # Extract the filename from the URL
        filename = url.split("/")[-1]

        # Set the path to save the file in the temporary directory
        save_path = os.path.join(self.firmware_dir, filename)

        # Check if the file already exists
        if os.path.exists(save_path):
            return save_path

        try:
            # Download the file and save it to the temporary directory
            urllib.request.urlretrieve(url, save_path)
            print("File downloaded successfully to:", save_path)
            return save_path
        except urllib.error.URLError as e:
            print("Failed to download the file:", e)
            return None
