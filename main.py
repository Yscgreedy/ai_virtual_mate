# 主程序
import keyboard as kb
from chat_web import *
from live2d import *
import os

def refresh_preference():  # 获取用户设置
    global voice_switch, prefer_llm, prefer_tts, prefer_img, history
    while True:
        try:
            voice_switch = voice_option_menu.get()
            prefer_llm = llm_menu.get()
            prefer_tts = tts_menu.get()
            prefer_img = img_menu.get()
            history = output_box.get(1.0, "end").strip() + "\n"
        except:
            pass
        time.sleep(0.1)


def run_chatweb():  # 运行对话网页
    try:
        ft.app(target=web_main, assets_dir="data", view=ft.WEB_BROWSER, port=chatweb_port)
    except:
        pass


def text_chat(event=None):  # 发送消息
    def text_chat_th():
        pg.quit()
        msg = input_box.get("1.0", "end").strip()
        if msg == "":
            messagebox.showinfo("提示", "请输入内容后再发送")
            return
        input_box.delete("1.0", "end")
        common_chat(msg)

    Thread(target=text_chat_th).start()


def common_chat(msg):  # 通用对话
    output_box.insert("end", f"\n{username}:\n    {msg}\n")
    output_box.see("end")
    notice(f"消息已发送，{mate_name}正在思考中...")
    bot_response = chat_preprocess(msg)
    parts = bot_response.split('|', 1)  # 仅分割一次
    if len(parts) == 2:
        chinese_part = parts[0].strip()
        english_part = parts[1].strip()
    else:
        chinese_part = bot_response.strip()
        english_part = ""  # 处理没有英文的情况
    stream_insert(f"{mate_name}:\n    {chinese_part}\n")
    get_tts_play_live2d(english_part)


def sensevoice_th():  # 语音识别(普通模式)
    from asr import recognize_audio, record_audio
    while True:
        try:
            if voice_option_menu.get() == "实时语音识别" or voice_option_menu.get() == "自定义唤醒词":
                pg.init()
                if pg.mixer.music.get_busy():
                    pass
                else:
                    say_text = recognize_audio(record_audio())
                    if len(say_text) > 1 and voice_option_menu.get() == "实时语音识别":
                        common_chat(say_text)
                    elif wake_word in say_text and voice_option_menu.get() == "自定义唤醒词":
                        if len(say_text) > 2:
                            say_text = say_text.replace(wake_word, "")
                        common_chat(say_text)
            else:
                time.sleep(0.1)
        except:
            time.sleep(0.1)


def sensevoice_th_break():  # 语音识别(实时语音打断模式)
    from asr import recognize_audio, record_audio
    while True:
        try:
            if voice_option_menu.get() == "实时语音识别" or voice_option_menu.get() == "自定义唤醒词":
                say_text = recognize_audio(record_audio())
                if len(say_text) > 1 and voice_option_menu.get() == "实时语音识别":
                    pg.quit()
                    common_chat(say_text)
                elif wake_word in say_text and voice_option_menu.get() == "自定义唤醒词":
                    if len(say_text) > 2:
                        say_text = say_text.replace(wake_word, "")
                    pg.quit()
                    common_chat(say_text)
            else:
                time.sleep(0.1)
        except:
            time.sleep(0.1)


def switch_voice(event=None):  # 切换语音识别
    if voice_switch == "实时语音识别":
        voice_var.set("关闭语音识别")
    elif voice_switch == "关闭语音识别":
        voice_var.set("实时语音识别")


if not os.path.exists('data/momoka'):
    os.makedirs('data/momoka', exist_ok=True)
    for label in ["LABEL_0", "LABEL_1", "LABEL_2", "LABEL_3"]:
        dir_path = os.path.join('data/momoka', label)
        os.makedirs(dir_path, exist_ok=True)
Thread(target=run_live2d).start()
if chat_web_switch == "开启":
    Thread(target=run_chatweb).start()
if voice_break == "开启":
    Thread(target=sensevoice_th_break).start()
else:
    Thread(target=sensevoice_th).start()
Thread(target=refresh_preference).start()
input_box.bind('<Return>', text_chat)
kb.add_hotkey('alt+g', pg.quit)
try:
    kb.add_hotkey(f'alt+{voice_key}', switch_voice)
except:
    pass
dkdh_icon = Image.open("data/image/ui/dkdh.png")
dkdh_icon = dkdh_icon.resize((int(150 * scaling_factor), int(35 * scaling_factor)), Image.Resampling.LANCZOS)
dkdh_icon = ImageTk.PhotoImage(dkdh_icon)
Button(root, image=dkdh_icon, command=open_chatweb, borderwidth=0, highlightthickness=0).place(relx=0.87, rely=0.01)
dkjs_icon = Image.open("data/image/ui/dkjs.png")
dkjs_icon = dkjs_icon.resize((int(150 * scaling_factor), int(35 * scaling_factor)), Image.Resampling.LANCZOS)
dkjs_icon = ImageTk.PhotoImage(dkjs_icon)
Button(root, image=dkjs_icon, command=lambda: wb.open(f"http://127.0.0.1:{live2d_port}"), borderwidth=0,
       highlightthickness=0).place(relx=0.87, rely=0.07)
zygl_icon = Image.open("data/image/ui/zygl.png")
zygl_icon = zygl_icon.resize((int(150 * scaling_factor), int(35 * scaling_factor)), Image.Resampling.LANCZOS)
zygl_icon = ImageTk.PhotoImage(zygl_icon)
Button(root, image=zygl_icon, command=open_change_w, borderwidth=0, highlightthickness=0).place(relx=0.03, rely=0.15)
rjsz_icon = Image.open("data/image/ui/rjsz.png")
rjsz_icon = rjsz_icon.resize((int(150 * scaling_factor), int(41 * scaling_factor)), Image.Resampling.LANCZOS)
rjsz_icon = ImageTk.PhotoImage(rjsz_icon)
Button(root, image=rjsz_icon, command=open_setting_w, borderwidth=0, highlightthickness=0).place(relx=0.03, rely=0.235)
tzbf_icon = Image.open("data/image/ui/tzbf.png")
tzbf_icon = tzbf_icon.resize((int(150 * scaling_factor), int(39 * scaling_factor)), Image.Resampling.LANCZOS)
tzbf_icon = ImageTk.PhotoImage(tzbf_icon)
Button(root, image=tzbf_icon, command=pg.quit, borderwidth=0, highlightthickness=0).place(relx=0.03, rely=0.32)
export_icon = Image.open("data/image/ui/export.png")
export_icon = export_icon.resize((int(25 * scaling_factor), int(25 * scaling_factor)), Image.Resampling.LANCZOS)
export_icon = ImageTk.PhotoImage(export_icon)
Button(root, image=export_icon, command=export_chat, borderwidth=0, highlightthickness=0).place(relx=0.97, rely=0.845)
add_icon = Image.open("data/image/ui/add.png")
add_icon = add_icon.resize((int(25 * scaling_factor), int(25 * scaling_factor)), Image.Resampling.LANCZOS)
add_icon = ImageTk.PhotoImage(add_icon)
Button(root, image=add_icon, command=clear_chat, borderwidth=0, highlightthickness=0).place(relx=0.97, rely=0.895)
send_icon = Image.open("data/image/ui/send.png")
send_icon = send_icon.resize((int(25 * scaling_factor), int(25 * scaling_factor)), Image.Resampling.LANCZOS)
send_icon = ImageTk.PhotoImage(send_icon)
Button(root, image=send_icon, command=text_chat, borderwidth=0, highlightthickness=0).place(relx=0.97, rely=0.945)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
with open('data/db/preference.db', 'w', encoding='utf-8') as file2:
    file2.write(f'[语音识别模式]\n{voice_switch}\n\n')
    file2.write(f'[对话语言模型]\n{prefer_llm}\n\n')
    file2.write(f'[语音合成引擎]\n{prefer_tts}\n\n')
    file2.write(f'[图像识别引擎]\n{prefer_img}')
with open(f'data/db/history.db', 'w', encoding='utf-8') as file3:
    file3.write(history)
os.kill(os.getpid(), 15)
