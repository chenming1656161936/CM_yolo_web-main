import argparse

from flask import Flask, request, render_template
import os
from detect import main

app = Flask(__name__)

def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream

# 定义路由
@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':  #post是一种请求方式
        # 从表单中获取上传的文件
        f = request.files['file']  #request.files 函数作用就是获取前端名为 'file'的文件信息
        global filename  # 定义全局变量，方便其他地方调用filename，如果不定义全局变量，其他地方无法调用
        filename = f.filename  # 获取前端上传图片名字
        global file_path  #同理，定义全局变量
        
        # 将文件保存到服务器本地
        # file_path = file_path + '/runs/image'
        file_path = os.path.join(os.getcwd() + '/runs/images', filename)  #本地路径+图片名字= 文件路径（file-path)

        print(file_path)  # 当时只是为了测试程序
        f.save(file_path)  # 保存上传的图片到本地目录下，方便后续推理，直接找到图片
        # 返回文件路径
        # return file_path

        #进行检测
        opt = parse_opt() 
        main(opt)
        img_path = 'runs/detect/exp/' + str(filename)
        img_stream = return_img_stream(img_path)  # 获取图片流
        return render_template('index.html', img_stream=img_stream)
    return render_template('index.html')




def parse_opt():
    parser = argparse.ArgumentParser()

    parser.add_argument('--weights', nargs='+', type=str, default= 'yolov5x.pt', help='model path or triton URL')
    #parser.add_argument('--source', type=str, default=0, help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--source', type=str, default= file_path, help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--data', type=str, default= 'models/yolov5x.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--project', default= 'runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--vid-stride', type=int, default=1, help='video frame-rate stride')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    #print_args(vars(opt))
    args = parser.parse_args(args=[])
    print(args)
    return opt

# 启动Flask应用
if __name__ == '__main__':
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(host='0.0.0.0', port=5010)
    

