# 语音识别模块
import pyaudio
import wave
import numpy as np
from funasr_onnx import SenseVoiceSmall

with open('data/db/config.db', 'r', encoding='utf-8') as file:
    lines = file.readlines()
asr_sensitivity = lines[67].strip()
if asr_sensitivity == "高":
    SILENCE_DURATION = 2
elif asr_sensitivity == "中":
    SILENCE_DURATION = 3
else:
    SILENCE_DURATION = 4
FORMAT = pyaudio.paInt16
CHANNELS, RATE, CHUNK = 1, 16000, 1024
SILENCE_CHUNKS = SILENCE_DURATION * RATE / CHUNK
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
cache_path = "data/cache/cache_record.wav"
model = SenseVoiceSmall("data/model/sensevoice-small-onnx-quant", batch_size=10, quantize=True)

# 计算rms值
def rms(data):
    return np.sqrt(np.mean(np.frombuffer(data, dtype=np.int16) ** 2))

# 计算dbfs值
def dbfs(rms_value):
    return 20 * np.log10(rms_value / (2 ** 15))

# 录音
def record_audio():
    frames = []
    recording = True
    silence_counter = 0
    while recording:
        data = stream.read(CHUNK)
        frames.append(data)
        current_rms = rms(data)
        current_dbfs = dbfs(current_rms)
        if str(current_dbfs) != "nan":
            silence_counter += 1
            if silence_counter > SILENCE_CHUNKS:
                recording = False
        else:
            silence_counter = 0
    return b''.join(frames)

# 识别
def recognize_audio(audiodata):
    with wave.open(cache_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(audiodata)
    res = model(cache_path, language="zh", use_itn=False)
    info = res[0].split('<|')[1:]
    emotion = info[1].split('|>')[0]
    event = info[2].split('|>')[0]
    text = info[3].split('}')[0].split('|>')[1]
    emotion_dict = {"HAPPY": "[开心]", "SAD": "[伤心]", "ANGRY": "[愤怒]", "DISGUSTED": "[厌恶]",
                    "SURPRISED": "[惊讶]", "NEUTRAL": "", "EMO_UNKNOWN": ""}
    event_dict = {"BGM": "[背景音乐]", "Applause": "[鼓掌]", "Laughter": "[大笑]", "Cry": "[哭]",
                  "Sneeze": "[打喷嚏]", "Cough": "[咳嗽]", "Breath": "[深呼吸]", "Speech": "", "Event_UNK": ""}
    emotion = emotion_dict.get(emotion, emotion)
    event = event_dict.get(event, event)
    result = event + text + emotion
    return result
