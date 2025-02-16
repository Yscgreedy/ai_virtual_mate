# 系统初始化模块
import socket
import shutil
from tkinter import filedialog as fd, messagebox

with open('data/db/config.db', 'r', encoding='utf-8') as file:
    lines = file.readlines()
mate_name = lines[1].strip()
prompt = lines[4].strip()
username = lines[7].strip()
password = lines[10].strip()
paddle_rate = lines[13].strip()
paddle_lang = lines[16].strip()
chatweb_port = lines[19].strip()
live2d_port = lines[22].strip()
local_server_ip = lines[25].strip()
anything_llm_ws = lines[28].strip()
lmstudio_port = lines[31].strip()
anything_llm_key = lines[34].strip()
ollama_model_name = lines[37].strip()
gsv_port = lines[40].strip()
custom_url = lines[43].strip()
custom_key = lines[46].strip()
custom_model = lines[49].strip()
voice_key = lines[52].strip()
chat_web_switch = lines[55].strip()
ollama_vlm_name = lines[58].strip()
wake_word = lines[61].strip()
voice_break = lines[64].strip()
asr_sensitivity = lines[67].strip()
dify_ip = lines[70].strip()
dify_key = lines[73].strip()
edge_speaker = lines[76].strip()
edge_rate = lines[79].strip()
edge_pitch = lines[82].strip()
custom_vlm = lines[85].strip()
cosy_port = lines[88].strip()
think_filter_switch = lines[91].strip()
with open('data/db/preference.db', 'r', encoding='utf-8') as file2:
    lines2 = file2.readlines()
voice_switch = lines2[1].strip()
prefer_llm = lines2[4].strip()
prefer_tts = lines2[7].strip()
prefer_img = lines2[10].strip()
with open('data/db/history.db', 'r', encoding='utf-8') as file3:
    history = file3.read()
with open('dist/assets/live2d_core/live2d_js_part1', 'r', encoding='utf-8') as file10:
    live2d_js_part1 = file10.read()
with open('dist/assets/live2d_core/live2d_js_part2', 'r', encoding='utf-8') as file11:
    live2d_js_part2 = file11.read()
with open('dist/assets/live2d_core/live2d_js_part3', 'r', encoding='utf-8') as file12:
    live2d_js_part3 = file12.read()
with open('dist/assets/live2d_core/live2d_js_part4', 'r', encoding='utf-8') as file13:
    live2d_js_part4 = file13.read()
with open('dist/assets/live2d_core/live2d_js_part5', 'r', encoding='utf-8') as file14:
    live2d_js_part5 = file14.read()
with open('data/set/cam_num_set.txt', 'r', encoding='utf-8') as file15:
    cam_num = int(file15.read())
with open('data/set/key_set.txt', 'r', encoding='utf-8') as file16:
    lines16 = file16.readlines()
sf_key = lines16[1].strip()
glm_key = lines16[4].strip()
spark_key = lines16[7].strip()


def get_local_ip():  # 获取本机局域网IP地址
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('223.5.5.5', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    return ip


def upload_image():  # 上传图片
    file_path = fd.askopenfilename(title="选择一张JPG图片", filetypes=[("JPG文件", "*.jpg")])
    if file_path:
        target_path = "dist/assets/image/bg.jpg"
        shutil.copy(file_path, target_path)
        messagebox.showinfo("提示", "更换网页背景成功,请刷新网页")


server_ip = get_local_ip()
edge_speaker_list = ["晓艺-年轻女声", "晓晓-成稳女声", "云健-大型纪录片男声", "云希-短视频热门男声",
                     "云夏-年轻男声", "云扬-成稳男声", "晓北-辽宁话女声", "晓妮-陕西话女声", "晓佳-粤语成稳女声",
                     "晓满-粤语年轻女声", "云龙-粤语男声", "晓辰-台湾话年轻女声", "晓宇-台湾话成稳女声",
                     "云哲-台湾话男声", "佳太-日语男声", "七海-日语女声"]
