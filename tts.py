# 语音合成模块
import asyncio
import edge_tts
import librosa
import pyttsx3
import pygame as pg
import numpy as np
from function import *
import math

voice_path = 'data/cache/cache_voice'
try:
    engine = pyttsx3.init()
except:
    pass
lang_mapping = {"中文": "zh", "英语": "uk", "日语": "jp"}
select_lang = lang_mapping.get(paddle_lang, "kor")
edge_speaker_mapping = {"晓艺-年轻女声": "zh-CN-XiaoyiNeural", "晓晓-成稳女声": "zh-CN-XiaoxiaoNeural",
                        "云健-大型纪录片男声": "zh-CN-YunjianNeural", "云希-短视频热门男声": "zh-CN-YunxiNeural",
                        "云夏-年轻男声": "zh-CN-YunxiaNeural", "云扬-成稳男声": "zh-CN-YunyangNeural",
                        "晓北-辽宁话女声": "zh-CN-liaoning-XiaobeiNeural",
                        "晓妮-陕西话女声": "zh-CN-shaanxi-XiaoniNeural", "晓佳-粤语成稳女声": "zh-HK-HiuGaaiNeural",
                        "晓满-粤语年轻女声": "zh-HK-HiuMaanNeural", "云龙-粤语男声": "zh-HK-WanLungNeural",
                        "晓辰-台湾话年轻女声": "zh-TW-HsiaoChenNeural", "晓宇-台湾话成稳女声": "zh-TW-HsiaoYuNeural",
                        "云哲-台湾话男声": "zh-TW-YunJheNeural", "佳太-日语男声": "ja-JP-KeitaNeural"}
edge_select_speaker = edge_speaker_mapping.get(edge_speaker, "ja-JP-NanamiNeural")

# 播放语音
def play_voice():
    def play_mp3_th():
        pg.init()
        try:
            pg.mixer.music.load(voice_path)
            pg.mixer.music.play()
            while pg.mixer.music.get_busy():
                pg.time.Clock().tick(1)
            pg.mixer.music.stop()
        except:
            pass
        pg.quit()

    Thread(target=play_mp3_th).start()

# 获取并播放语音
def get_tts_play_live2d(text):
    async def ms_edge_tts():
        try:
            # 新增参数校验
            #validate_speaker(edge_select_speaker)
            communicate = edge_tts.Communicate(text, edge_select_speaker, rate=f"{edge_rate}%", pitch=f"{edge_pitch}Hz")
            await communicate.save(voice_path)
        except edge_tts.ErrorCode.INVALID喉音:
            raise ValueError("无效的发音人配置")
    
    def fetch_and_save_audio(url, error_message):
        try:
            response = rq.get(url)
            response.raise_for_status()  # 检查HTTP错误
            with open(voice_path, 'wb') as f:
                f.write(response.content)
            play_voice()
        except Exception as e:
            notice(f"{error_message}，错误详情：{str(e)}")

    try:
        if tts_menu.get() == "云端edge-tts":
            asyncio.run(ms_edge_tts())
            play_voice()
        elif tts_menu.get() == "云端百度TTS":
            url = f'https://fanyi.baidu.com/gettts?lan={select_lang}&spd={paddle_rate}&text={text}'
            fetch_and_save_audio(url, "云端百度TTS请求失败")
        elif tts_menu.get() == "本地GPT-SoVITS":
            import os
            import random
            import urllib.parse
            text,emotion=text.split("&")
            emotion_folder = os.path.join("data", "momoka", emotion)
            emotion_files = [f for f in os.listdir(emotion_folder) if f.endswith('.wav')]
            if emotion_files:
                selected_file = random.choice(emotion_files)
                refer_wav_path = os.path.abspath(os.path.join(emotion_folder, selected_file))
                prompt_text = os.path.splitext(selected_file)[0]
                # 对文件名进行URL编码，避免特殊字符导致的问题
                refer_wav_path = urllib.parse.quote(refer_wav_path)
                prompt_text = urllib.parse.quote(prompt_text)
            #上面是api.py
            #下面是api_v2.py
            #url = f'http://{local_server_ip}:{gsv_port}/?refer_wav_path={refer_wav_path}&prompt_text={prompt_text}&prompt_language=ja&text={text}&text_language=ja'
            url = f'http://{local_server_ip}:{gsv_port}/tts?ref_audio_path={refer_wav_path}&prompt_text={prompt_text}&prompt_lang=ja&text={text}&text_lang=ja&parallel_infer=False'
            fetch_and_save_audio(url, "本地GPT-SoVITS API请求失败")
        elif tts_menu.get() == "本地CosyVoice":
            url = f'http://{local_server_ip}:{cosy_port}/cosyvoice/?text={text}'
            fetch_and_save_audio(url, "本地CosyVoice API请求失败")
        elif tts_menu.get() == "本地Kokoro-TTS":
            url = f'http://{local_server_ip}:9882/kokoro/?text={text}'
            fetch_and_save_audio(url, "本地Kokoro-TTS API请求失败")
        elif tts_menu.get() == "本地pyttsx3":
            try:
                engine.save_to_file(text, voice_path)
                engine.runAndWait()
                play_voice()
            except Exception as e:
                notice(f"pyttsx3使用失败：{str(e)}")
    except FileNotFoundError as e:
        notice(f"文件未找到：{str(e)}")
    except Exception as e:
        notice(f"错误：{str(e)}", level='error')

    def play_live2d():  # 读取缓存音频播放Live2D对口型动作
        try:
            x, sr = librosa.load(voice_path, sr=8000)
            x = x - min(x)
            x = x / max(x)
            epsilon = np.finfo(float).eps
            x = np.log(x + epsilon) + 1  # 添加epsilon避免log(0)
            x = x / max(x) * 1.2
            s_time = time.time()
            total_samples = len(x)
            loop_count = math.ceil(total_samples / 800)  # 向上取整循环次数
            for _ in range(loop_count):
                current_time = time.time() - s_time
                current_index = min(current_time * 8000, total_samples-1)
                # 新增边界检查
                if current_index < 0 or current_index >= len(x):
                    continue
                it = x[current_index]
                if it < 0:
                    it = 0
                with open("data/cache/cache.txt", "w") as cache_file:
                    cache_file.write(str(float(it)))
                time.sleep(0.1)
        except IndexError:
            notice("音频数据索引越界", level='warning')
        finally:
            time.sleep(0.1)
            with open("data/cache/cache.txt", "w") as cache_file:
                cache_file.write("0")
            pg.mixer.quit()

    Thread(target=play_live2d).start()
