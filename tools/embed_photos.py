import os
import ruamel.yaml
import requests

def download_photo(url, name):
    if url.startswith("//"):
        url = "https:" + url
    extension = os.path.splitext(url)[1]
    if not extension:
        extension = ".jpg"  # Add .jpg extension for URLs without an extension
    filename = name.replace(" ", "_") + extension
    filepath = os.path.join("assets/team", filename)

    if not os.path.exists(filepath):  # Check if file exists
        response = requests.get(url)
        with open(filepath, "wb") as file:
            file.write(response.content)

    return "/" + filepath  # Include leading "/"

def process_team_members_yaml(file_path):
    yaml = ruamel.yaml.YAML()
    yaml.width = float("inf")  # Disable line wrapping

    with open(file_path, "r") as file:
        data = yaml.load(file)

    for member in data:
        photo_url = member.get("photo")
        if photo_url:
            member["photo"] = download_photo(photo_url, member["name"])

    with open(file_path, "w") as file:
        yaml.dump(data, file)

data_file = "_data/team_members.yml"
process_team_members_yaml(data_file)
