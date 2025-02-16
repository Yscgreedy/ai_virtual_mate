# 功能函数模块
import time
from datetime import datetime
from gui import *


def current_time():  # 获取当前时间
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def on_closing():  # 退出程序
    if messagebox.askokcancel("确认退出", "您确定要退出枫云AI虚拟伙伴Web版吗？"):
        root.destroy()


def notice(info):  # 通知
    state_box.delete("1.0", "end")
    state_box.insert("end", info)


def stream_insert(text):  # 流式输出
    def insert_char(char):
        output_box.insert("end", char)
        output_box.see("end")

    def threaded_insert():
        for char in text:
            insert_char(char)
            time.sleep(0.01)

    Thread(target=threaded_insert).start()


def open_ch(e):  # 打开角色
    wb.open(f"http://{server_ip}:{live2d_port}")


def export_chat():  # 导出对话
    chat_records = output_box.get("1.0", "end")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = fd.asksaveasfilename(defaultextension='.txt', filetypes=[('Text Files', '*.txt')],
                                     initialfile=f'枫云AI虚拟伙伴Web版{mate_name}对话记录{timestamp}')
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as chat_file:
            chat_file.write(chat_records)
            notice(f"{mate_name}对话记录导出成功")


def open_chatweb():  # 打开对话网页
    if chat_web_switch == "关闭":
        messagebox.showinfo("提示", "请前往软件设置打开对话网页开关")
        return
    wb.open(f"http://127.0.0.1:{chatweb_port}")
