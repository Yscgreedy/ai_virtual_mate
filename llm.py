# 大语言模型模块
import json
from vlm import *

try:
    from letta import create_client, LLMConfig, EmbeddingConfig
    from letta.schemas.memory import ChatMemory
except:
    pass

lmstudio_history, ollama_history, rwkv_history, custom_history, spark_history, glm_history, lyww_history, ds_history, qwen_history, internlm_history = [], [], [], [], [], [], [], [], [], []
sf_url = "https://api.siliconflow.cn/v1"


def chat_preprocess(msg):  # 预处理
    try:
        content = "图像识别已关闭"
        if (
                "屏幕" in msg or "画面" in msg or "图片" in msg or "看到" in msg or "看见" in msg or "照片" in msg or "摄像头" in msg) and img_menu.get() != "关闭图像识别":
            if "屏幕" in msg or "画面" in msg or "图片" in msg:
                if img_menu.get() == "GLM-4V-Flash":
                    content = glm_4v_screen(msg)
                elif img_menu.get() == "本地Ollama VLM":
                    content = ollama_vlm_screen(msg)
                elif img_menu.get() == "本地QwenVL整合包":
                    content = qwen_vlm_screen(msg)
                elif img_menu.get() == "本地GLM-V整合包":
                    content = glm_v_screen(msg)
                elif img_menu.get() == "本地Janus整合包":
                    content = janus_screen(msg)
                elif img_menu.get() == "自定义API-VLM":
                    content = custom_vlm_screen(msg)
                notice(f"{mate_name}捕获了屏幕，调用[电脑屏幕识别]")
            elif "看到" in msg or "看见" in msg or "照片" in msg or "摄像头" in msg:
                if img_menu.get() == "GLM-4V-Flash":
                    content = glm_4v_cam(msg)
                elif img_menu.get() == "本地Ollama VLM":
                    content = ollama_vlm_cam(msg)
                elif img_menu.get() == "本地QwenVL整合包":
                    content = qwen_vlm_cam(msg)
                elif img_menu.get() == "本地GLM-V整合包":
                    content = glm_v_cam(msg)
                elif img_menu.get() == "本地Janus整合包":
                    content = janus_cam(msg)
                elif img_menu.get() == "自定义API-VLM":
                    content = custom_vlm_cam(msg)
                notice(f"{mate_name}拍了照片，调用[摄像头识别]")
        else:
            content = chat_llm(prompt, msg)
            if think_filter_switch == "开启":
                content = content.split("</think>")[-1].strip()
            notice(f"收到{mate_name}回复")
        return content
    except Exception as e:
        notice(f"图像识别引擎配置错误，错误详情：{e}")
        return "图像识别引擎配置错误"


def chat_llm(tishici, msg):  # 大语言模型聊天
    try:
        if llm_menu.get() == "讯飞星火Lite":
            spark_client = OpenAI(base_url="https://spark-api-open.xf-yun.com/v1", api_key=spark_key)
            spark_history.append({"role": "user", "content": f"{tishici}。我的问题是：{msg}"})
            messages = []
            messages.extend(spark_history)
            completion = spark_client.chat.completions.create(model="general", messages=messages)
            spark_history.append({"role": "assistant", "content": completion.choices[0].message.content})
            return completion.choices[0].message.content
        elif llm_menu.get() == "GLM-4-Flash":
            glm_client = OpenAI(base_url=glm_url, api_key=glm_key)
            glm_history.append({"role": "user", "content": msg})
            messages = [{"role": "system", "content": tishici}]
            messages.extend(glm_history)
            completion = glm_client.chat.completions.create(model="glm-4-flash", messages=messages)
            glm_history.append({"role": "assistant", "content": completion.choices[0].message.content})
            return completion.choices[0].message.content
        elif llm_menu.get() == "DeepSeek-R1-7B":
            ds_client = OpenAI(base_url=sf_url, api_key=sf_key)
            ds_history.append({"role": "user", "content": msg})
            messages = [{"role": "system", "content": tishici}]
            messages.extend(ds_history)
            completion = ds_client.chat.completions.create(model="deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
                                                           messages=messages)
            ds_history.append({"role": "assistant", "content": completion.choices[0].message.content})
            return completion.choices[0].message.content
        elif llm_menu.get() == "思维链Marco-o1":
            marco_client = OpenAI(base_url=sf_url, api_key=sf_key)
            messages = [{"role": "system",
                         "content": f"{tishici}。当你回答问题时，你的思考应该在<think>内完成，<answer>内输出你的结果。<think>应该尽可能是中文"},
                        {"role": "user", "content": msg}]
            completion = marco_client.chat.completions.create(model="AIDC-AI/Marco-o1", messages=messages)
            result = completion.choices[0].message.content
            result = result.replace("<answer>", "").replace("</answer>", "")
            return result
        elif llm_menu.get() == "零一万物1.5-9B":
            lyww_client = OpenAI(base_url=sf_url, api_key=sf_key)
            lyww_history.append({"role": "user", "content": msg})
            messages = [{"role": "system", "content": tishici}]
            messages.extend(lyww_history)
            completion = lyww_client.chat.completions.create(model="01-ai/Yi-1.5-9B-Chat-16K",
                                                             messages=messages)
            lyww_history.append({"role": "assistant", "content": completion.choices[0].message.content})
            return completion.choices[0].message.content
        elif llm_menu.get() == "通义千问2.5-7B":
            qwen_client = OpenAI(base_url=sf_url, api_key=sf_key)
            qwen_history.append({"role": "user", "content": msg})
            messages = [{"role": "system", "content": tishici}]
            messages.extend(qwen_history)
            completion = qwen_client.chat.completions.create(model="Qwen/Qwen2.5-7B-Instruct",
                                                             messages=messages)
            qwen_history.append({"role": "assistant", "content": completion.choices[0].message.content})
            return completion.choices[0].message.content
        elif llm_menu.get() == "InternLM2.5-7B":
            internlm_client = OpenAI(base_url=sf_url, api_key=sf_key)
            internlm_history.append({"role": "user", "content": msg})
            messages = [{"role": "system", "content": tishici}]
            messages.extend(internlm_history)
            completion = internlm_client.chat.completions.create(model="internlm/internlm2_5-7b-chat",
                                                                 messages=messages)
            internlm_history.append({"role": "assistant", "content": completion.choices[0].message.content})
            return completion.choices[0].message.content
        elif llm_menu.get() == "本地Qwen整合包":
            api = f"http://{local_server_ip}:8088/llm/?p={tishici}&q={msg}"
            try:
                res = rq.get(api).json()["answer"]
                return res
            except Exception as e:
                return f"本地Qwen整合包API服务器未开启，错误详情：{str(e)[0:100]}"
        elif llm_menu.get() == "本地LM Studio":
            try:
                lmstudio_client = OpenAI(base_url=f"http://{local_server_ip}:{lmstudio_port}/v1", api_key="lm-studio")
                lmstudio_history.append({"role": "user", "content": msg})
                messages = [{"role": "system", "content": tishici}]
                messages.extend(lmstudio_history)
                completion = lmstudio_client.chat.completions.create(model="", messages=messages)
                lmstudio_history.append({"role": "assistant", "content": completion.choices[0].message.content})
                return completion.choices[0].message.content
            except Exception as e:
                return f"本地LM Studio软件未开启，错误详情：{e}"
        elif llm_menu.get() == "本地Ollama":
            try:
                try:
                    rq.get(f'http://{local_server_ip}:11434')
                except:
                    Popen(f"ollama pull {ollama_model_name}", shell=False)
                ollama_client = Client(host=f'http://{local_server_ip}:11434')
                ollama_history.append({"role": "user", "content": msg})
                messages = [{"role": "system", "content": tishici}]
                messages.extend(ollama_history)
                response = ollama_client.chat(model=ollama_model_name, messages=messages)
                ollama_history.append({"role": "assistant", "content": response['message']['content']})
                return response['message']['content']
            except Exception as e:
                return f"本地Ollama服务未开启，错误详情：{e}"
        elif llm_menu.get() == "本地RWKV运行器":
            try:
                rwkv_client = OpenAI(base_url=f"http://{local_server_ip}:8000/v1", api_key="rwkv")
                rwkv_history.append({"role": "user", "content": msg})
                messages = [{"role": "system", "content": tishici}]
                messages.extend(rwkv_history)
                completion = rwkv_client.chat.completions.create(model="rwkv", messages=messages)
                rwkv_history.append({"role": "assistant", "content": completion.choices[0].message.content})
                return completion.choices[0].message.content
            except Exception as e:
                return f"本地RWKV Runner软件未开启，错误详情：{e}"
        elif llm_menu.get() == "本地OpenVINO":
            api = f"http://{local_server_ip}:8087/openvino/?p={tishici}&q={msg}"
            try:
                res = rq.get(api).json()["answer"]
                return res
            except Exception as e:
                return f"本地OpenVINO整合包API服务器未开启，错误详情：{str(e)[0:100]}"
        elif llm_menu.get() == "本地Dify知识库":
            try:
                res = chat_dify(msg)
                return res
            except Exception as e:
                return f"本地Dify知识库配置错误，错误详情：{e}"
        elif llm_menu.get() == "AnythingLLM":
            try:
                res = chat_anything_llm(msg)
                return res
            except Exception as e:
                return f"本地AnythingLLM知识库配置错误，错误详情：{e}"
        elif llm_menu.get() == "Letta长期记忆":
            res = chat_letta(msg)
            return res
        else:
            try:
                custom_client = OpenAI(base_url=custom_url, api_key=custom_key)
                custom_history.append({"role": "user", "content": msg})
                messages = [{"role": "system", "content": tishici}]
                messages.extend(custom_history)
                completion = custom_client.chat.completions.create(model=custom_model, messages=messages)
                custom_history.append({"role": "assistant", "content": completion.choices[0].message.content})
                return completion.choices[0].message.content
            except Exception as e:
                return f"自定义API配置错误，错误详情：{e}"
    except Exception as e:
        notice(f"{llm_menu.get()}不可用，请前往软件设置正确配置云端AI Key，错误详情：{e}")
        return f"{llm_menu.get()}不可用，请前往软件设置正确配置云端AI Key，错误详情：{e}"


def chat_dify(msg):  # Dify知识库
    headers = {"Authorization": f"Bearer {dify_key}", "Content-Type": "application/json"}
    data = {"query": msg, "inputs": {}, "response_mode": "blocking", "user": username, "conversation_id": None}
    res = rq.post(f"http://{dify_ip}/v1/chat-messages", headers=headers, data=json.dumps(data))
    res = res.json()['answer'].strip()
    return res


def chat_anything_llm(msg):  # AnythingLLM知识库
    url = f"http://{local_server_ip}:3001/api/v1/workspace/{anything_llm_ws}/chat"
    headers = {"Authorization": f"Bearer {anything_llm_key}", "Content-Type": "application/json"}
    data = {"message": msg}
    res = rq.post(url, json=data, headers=headers)
    return res.json().get("textResponse")


def chat_letta(msg):  # Letta长期记忆
    answer = "Letta长期记忆服务拥挤，请一段时间后再试"
    try:
        client = create_client()
        with open('data/db/letta.db', 'r', encoding='utf-8') as f:
            agent_state_id = f.read()
        if len(agent_state_id) < 10:
            agent_state = client.create_agent(
                memory=ChatMemory(persona=prompt, human=f"Name: {username}"),
                llm_config=LLMConfig.default_config(model_name="letta"),
                embedding_config=EmbeddingConfig.default_config(model_name="text-embedding-ada-002"))
            with open('data/db/letta.db', 'w', encoding='utf-8') as f:
                f.write(agent_state.id)
            agent_state_id = agent_state.id
        response = client.send_message(
            agent_id=agent_state_id, role="user", message=f"[{current_time()}]{msg}")
        result = response.messages
        for message in result:
            if message.message_type == 'tool_call_message':
                function_arguments = message.tool_call.arguments
                if function_arguments:
                    arguments_dict = json.loads(function_arguments)
                    answer = arguments_dict.get("message")
                    break
    except:
        answer = "Letta长期记忆出现兼容性问题暂不可用，可更换其他对话模型"
    return answer


def clear_chat():  # 清除对话记录
    global lmstudio_history, ollama_history, rwkv_history, custom_history, spark_history, glm_history, lyww_history, ds_history, qwen_history, internlm_history
    if messagebox.askokcancel(f"清除{mate_name}的记忆和聊天记录",
                              f"您确定要清除{mate_name}的记忆和聊天记录吗？\n如有需要可先点击🔼导出记录再开启新对话"):
        output_box.delete("1.0", "end")
        lmstudio_history, ollama_history, rwkv_history, custom_history, spark_history, glm_history, lyww_history, ds_history, qwen_history, internlm_history = [], [], [], [], [], [], [], [], [], []
        with open('data/db/letta.db', 'w', encoding="utf-8") as f:
            f.write("0")
        notice("记忆和聊天记录已清空")


def clean_chat_web():  # 清除对话记录
    global lmstudio_history, ollama_history, rwkv_history, custom_history, spark_history, glm_history, lyww_history, ds_history, qwen_history, internlm_history
    lmstudio_history, ollama_history, rwkv_history, custom_history, spark_history, glm_history, lyww_history, ds_history, qwen_history, internlm_history = [], [], [], [], [], [], [], [], [], []
