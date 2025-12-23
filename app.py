# app.py
import os
import streamlit as st
from dotenv import load_dotenv

from agent import AIGCTeachingAssistantAgent
from openai import OpenAI
from PIL import Image
from io import BytesIO

load_dotenv()

st.set_page_config(page_title="AIGC 課程小助教", page_icon="🤖", layout="wide")
st.title("🤖 AIGC 課程小助教 Agent（摘要 / 測驗 / 封面圖）")

with st.expander("作業繳交提醒（你要交什麼）", expanded=True):
    st.markdown("""- **(1) report 摘要 300 字（ABSTRACT）**
- **(2) agent 開發過程對話紀錄**
- **(3) GitHub repo ＋ Streamlit.app 線上 demo**

你可以把本專案直接當成 demo：貼上課堂內容 → 一鍵生成三種輸出。
""")

api_key = st.secrets.get("OPENAI_API_KEY", None) if hasattr(st, "secrets") else None
api_key = api_key or os.getenv("OPENAI_API_KEY")

colL, colR = st.columns([1.2, 1])

with colL:
    notes = st.text_area("貼上課堂筆記/講義內容（越完整越好）", height=260, placeholder="例如：本週介紹 Transformer、擴散模型、提示詞工程、RAG ...")
    model = st.selectbox("文字模型（可改）", ["gpt-4o-mini", "gpt-4.1-mini", "gpt-4o"], index=0)
    gen_image = st.checkbox("同時生成封面圖（需要圖像 API）", value=True)

run = st.button("🚀 生成（摘要＋測驗＋封面提示詞）", type="primary", use_container_width=True)

if run:
    agent = AIGCTeachingAssistantAgent(api_key=api_key, model=model)
    result = agent.run(notes)

    with colR:
        st.subheader("1) 300 字內摘要")
        st.write(result.summary)
        st.download_button("下載摘要 txt", data=result.summary, file_name="abstract.txt")

        st.subheader("2) 測驗（含答案）")
        st.write(result.quiz)
        st.download_button("下載測驗 txt", data=result.quiz, file_name="quiz.txt")

        st.subheader("3) 封面圖像提示詞（A/B/C 三種風格）")
        st.write(result.cover_prompt)
        st.download_button("下載封面提示詞 txt", data=result.cover_prompt, file_name="cover_prompt.txt")

    if gen_image:
        st.divider()
        st.subheader("封面圖（使用 OpenAI Images API；沒有 key 會略過）")

        if not api_key:
            st.info("尚未設定 OPENAI_API_KEY → 目前不產生圖片（但文字輸出仍可用示範模式）。")
        else:
            # 取 B 風格當預設，讓畫面更吸睛
            prompt_lines = [line.strip() for line in result.cover_prompt.splitlines() if line.strip()]
            img_prompt = None
            for line in prompt_lines:
                if line.startswith("B:"):
                    img_prompt = line.replace("B:", "").strip()
                    break
            img_prompt = img_prompt or prompt_lines[0].split(":",1)[-1].strip()

            client = OpenAI(api_key=api_key)
            with st.spinner("生成圖片中..."):
                img = client.images.generate(
                    model="gpt-image-1",
                    prompt=img_prompt,
                    size="1024x1024",
                )
            b64 = img.data[0].b64_json
            image_bytes = BytesIO(__import__("base64").b64decode(b64))
            image = Image.open(image_bytes)

            st.image(image, caption="Generated cover image", use_container_width=False)
            buf = BytesIO()
            image.save(buf, format="PNG")
            st.download_button("下載封面圖 PNG", data=buf.getvalue(), file_name="cover.png", mime="image/png")

st.caption("提示：你可以把生成的摘要貼進 report；把你與本 app 的互動截圖/貼進 sample_dialogue.md 當作 agent 對話紀錄。")
