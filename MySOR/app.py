import json
import os
import traceback
import uuid

from flask import Flask, request, jsonify
from deep_sort_pytorch_master.crop_new import process_video

app = Flask(__name__)


def custom_response(data=None, msg='请求成功', code=200):
    return jsonify({
        'code': code,
        'msg': msg,
        'data': data
    }), code


@app.route('/processVideo', methods=['POST'])
def process_video1():
    try:
        data = request.get_data()
        if data is None or data == b'':
            return custom_response(code=400, msg='缺少必传参数')

        json_data = json.loads(data)

        # 前端传的数据
        path = json_data.get('path')

        # 调用算法处理方法
        process_video(path.replace('/app', '/www/mysor/app'))

        base_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
        os.rename(base_dir + '/demo.mp4', base_dir + '/static/' + uuid.uuid4().hex + '.mp4')

    except Exception as e:
        print(traceback.format_exc())
        return custom_response(code=500, msg=str(e))

    else:
        return custom_response(data='/static/demo.mp4')


if __name__ == '__main__':
    app.run()