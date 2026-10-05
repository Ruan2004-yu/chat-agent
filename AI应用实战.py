import streamlit as st
import os
from openai import OpenAI
from datetime import  datetime
import json

st.set_page_config(
    page_title="AI 语音助手",
    page_icon="👽",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={},
)
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

system_prompt="""
   你的名字是%s
   你是%s，请根据用户输入的提问，给出一个最合适的答案。
"""
#保存会话信息
def save_session():
    # 构建对话对象
    session_data = {
        "nick_name": st.session_state.nick_name,
        "nature": st.session_state.nature,
        "current_session":st.session_state.current_session,
        "messages": st.session_state.messages
    }
    #如果没有文件则创建文件
    if not os.path.exists("../sessions"):
            os.makedirs("../sessions")

    #保存对话数据
    with open("sessions/%s.json" % st.session_state.current_session, "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=4)

def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")
# 加载所有的会话列表信息
def load_sessions():
    session_list = []
    # 加载sessions目录下的文件
    if os.path.exists("../sessions"):
        file_list = os.listdir("../sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    return session_list
# 加载指定的会话信息
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            # 读取会话数据
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
            st.session_state.messages = session_data["messages"]
            st.session_state.nick_name = session_data["nick_name"]
            st.session_state.nature = session_data["nature"]
            st.session_state.current_session = session_name
    except Exception:
        st.error("加载会话失败!")
#删除会话
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")  # 删除文件
            # 如果删除的是当前会话，则需要更新消息列表
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_name()
    except Exception:
        st.error("删除会话失败！")
st.title("AI 语音助手")
#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []
#昵称
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "小美"

#性格
if "nature" not in st.session_state:
    st.session_state.nature = "一个高冷御姐"

#对话标识
if "current_session" not in st.session_state:
   now = generate_session_name()
   st.session_state.current_session = now

#聊天记录
st.text(f"会话名称: {st.session_state.current_session}")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])
#侧边栏
with st.sidebar:
    #会话信息
    st.subheader("AI控制面板")
    #新建对话
    if st.button("新建对话", width="stretch", icon="➕"):
        if st.session_state.messages:
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
            save_session()
            st.rerun()  #重新运行该页面
    #保存对话
    # if st.button("保存对话", width="stretch", icon="💾"):
    #     save_session()

    #会话历史
    st.text("会话历史")
    session_list = load_sessions()
    for session in session_list:
        col1, col2 = st.columns([5, 1])
        with col1:
            # 加载会话信息
            if st.button(session, key=f"load_{session}", width="stretch",type="primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            # 删除会话信息
            if st.button("",width="stretch",icon="❌", key=f"del_{session}"):
                delete_session(session)
                st.rerun()







    st.subheader("伴侣")
    nick_name=st.text_input("昵称", placeholder="请输入昵称", value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name=nick_name

    nature=st.text_area("性格",  placeholder="请输入性格", value=st.session_state.nature)
    if nature:
        st.session_state.nature=nature

#输入框
prompt = st.chat_input("请输入要提问的问题")
if prompt:
    st.chat_message("user").write( prompt)
    print("--------->调用AI大模型，提示词: ", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})


    #调用AI大模型
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.nature)},
            *st.session_state.messages,
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
    # print("--------->AI大模型返回结果: ", response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)

    #流式输出
    response_message=st.empty()
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            response_message.write(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_session()
