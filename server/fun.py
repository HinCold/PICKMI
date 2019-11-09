import os
from flask import jsonify
import uuid

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
def upphoto(f):

    if not (f and allowed_file(f.filename)):
        return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    # print(basepath)
    src_imgname = str(uuid.uuid1()) + ".jpg"
    upload_path = os.path.join(basepath, 'images/')
    if os.path.exists(upload_path) == False:
        os.makedirs(upload_path)

    src = upload_path + src_imgname
    print(src)
    f.save(src)
    return src
