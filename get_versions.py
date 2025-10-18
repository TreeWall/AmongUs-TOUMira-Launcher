import json
import urllib.request

repo_owner = "AU-Avengers"
repo_name = "TOU-Mira"
url_prefix = f"https://github.com/{repo_owner}/{repo_name}/releases/download/"

url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"

headers = {
    "User-Agent": "Python script"  # GitHub requires a user-agent
}

req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req) as response:
        data = json.load(response)

    # Create dictionary {version: relative .zip path}
    version_zip_dict = {}

    for release in data:
        version = release.get("tag_name")
        assets = release.get("assets", [])

        for asset in assets:
            name = asset.get("name", "")
            if name.endswith("x86-steam-itch.zip"):
                download_url = asset.get("browser_download_url")
                # Remove the prefix to get relative path
                if download_url.startswith(url_prefix):
                    download_url = download_url[len(url_prefix):]
                version_zip_dict[version] = download_url
                break  # Only take the first matching .zip per release

    # Print the resulting dictionary
    print(version_zip_dict)

except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.reason}")
except urllib.error.URLError as e:
    print(f"URL Error: {e.reason}")
