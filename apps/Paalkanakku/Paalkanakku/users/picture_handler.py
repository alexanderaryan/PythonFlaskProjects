import os
from PIL import Image
from flask import url_for, current_app, flash


def add_profile_pic(pic_upload,username):

    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    storage_file = str(username)+'.'+ext_type

    filepath = os.path.join(current_app.root_path, 'static/profile_pics', storage_file)


    output_size = (150, 150)

    try:
        pic = Image.open(pic_upload)
        pic.thumbnail(output_size)
    except:
        flash('Image file seems corrupted. Try with other image!')
    else:
        prev_images = list(
            filter(lambda f: f.startswith(str(username)), os.listdir(current_app.root_path + '/static/profile_pics')))
        for file in prev_images:
            print(current_app.root_path + '/static/profile_pics/' + file)
            os.remove(current_app.root_path + '/static/profile_pics/' + file)
        pic.save(filepath)

    return storage_file
