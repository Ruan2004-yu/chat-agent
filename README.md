# AI 语音助手 (AI Voice Assistant)

基于 Streamlit + DeepSeek 的 AI 对话助手，可自定义 AI 伴侣的昵称与性格，并支持多会话保存 / 加载 / 删除。

A Streamlit + DeepSeek based AI chat assistant. Customize the AI companion's nickname and personality, with multi-session save / load / delete support.

## 功能 Features

- 自定义昵称与性格 (customizable nickname & personality)
- 多会话管理 (multi-session management)
- 流式输出 (streaming output)

## 安装 Install

```bash
pip install -r requirements.txt
```

## 运行 Run

```bash
# 设置 DeepSeek API 密钥
export DEEPSEEK_API_KEY=你的key

streamlit run AI应用实战.py
```

## 环境变量 Environment Variables

- `DEEPSEEK_API_KEY`：DeepSeek API 密钥 (DeepSeek API key)
