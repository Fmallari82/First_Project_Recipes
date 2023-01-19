import base64
import os
from flask import redirect, session, json, request
import requests

def upload_photo(file):
    base64_file = base64.b64encode(file.read())
    url = "https://api.imgbb.com/1/upload"
    payload = {
        'key': os.environ.get("IMGBB_KEY"),
        'image': base64_file
    }
    resp = requests.post(url, payload)
    resp = resp.json()
    return resp

def photo_create():

    data = {
        "description": request.form['url']
    }
    if request.files['file']:
        data['url'] = upload_photo(request.files['file'])
    else:
        data['url'] = request.form['url'],
        
    album_id = request.form['album_id']
    photo_id = {model_image.Image.create}
    data = {
        'photo_id': photo_id,
        'album_id': album_id
    }
    model_album_has_photos.AlbumHasPhotos.create(**data)


import base64
import requests

apiKey = 'xxx' # insert your API key

print("imgBB API Uploader")
print("API Key: " + apiKey)
fileLocation = input("Enter file location: ")

with open(fileLocation, "rb") as file:
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": apiKey,
        "image": base64.b64encode(file.read()),
    }
    res = requests.post(url, payload)

if res.status_code == 200:
    print("Server Response: " + str(res.status_code))
    print("Image Successfully Uploaded")
else:
    print("ERROR")
    print("Server Response: " + str(res.status_code))


                    # <form action="/upload" method="post" enctype="multipart/form-data">
                        
                    #     <div class="flex flex-col" >
                    #         <input type="checkbox" class="h-5 w-5" name="photo_url" id="url_checkbox_photo">
                    #         <label for="photo_url" class="text-xs text-center"> Photo URL</label>
                    #     </div>
                    #     <div class="flex flex-col" id="file_upload_photo">
                    #         <label for="photo_upload" class="text-xs text-center"> Photo Upload</label>
                    #         <input type="file" name="file" id="photo_upload">
                    #     </div>
                    #     <div class="flex flex-col hidden" id="url_upload_photo">
                    #         <label for="url" class="text-xs text-center"> Photo URL</label>
                    #         <input class="input" type="text" name="url" id="url">
                    #     </div>
                    #     <div class="flex flex-col">
                    #         <label for="description" class="text-xs text-center"> Description</label>
                    #         <textarea class="input" name="description" id="description" cols="30" rows="10"></textarea>
                    #     </div>
                    #     <button>submit</button>


apiKey = os.environ.get("IMGBB_KEY")
location = input(UPLOAD_FOLDER)

def upload_photo(location):
    with open(location, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": apiKey,
            "image": base64.b64encode(file.read()),
        }
        res = requests.post(url, payload)

    if res.status_code == 200:
        print("Server Response: " + str(res.status_code))
        print("Image Successfully Uploaded")
    else:
        print("ERROR")
        print("Server Response: " + str(res.status_code))