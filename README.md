# TAICA AIGC 作業 Demo：AIGC 課程小助教（文字摘要＋測驗＋封面圖）

這個專題示範一個「AIGC 課程小助教 Agent」：把你貼上的課堂筆記/講義，自動生成：
1) 300 字內摘要（可作為 report 的摘要素材）  
2) 10 題小測驗（含答案）  
3) 1 張封面/縮圖（可選擇風格，使用圖像生成 API）

## 你要交的三樣東西（作業清單）
- report 摘要（300 字 ABSTRACT）
- agent 開發過程對話紀錄
- GitHub repo ＋ Streamlit.app 線上 demo

## 快速開始（本機）
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 部署到 Streamlit Community Cloud
1. 把整個資料夾 push 到 GitHub
2. 到 https://share.streamlit.io/ 連結 GitHub repo → Deploy
3. 在 Streamlit 的 **Secrets** 加上：
```toml
OPENAI_API_KEY="你的key"
```

> 沒有 key 也能開啟介面，但會進入「示範模式」不呼叫 API。

## 檔案結構
- `app.py`：Streamlit 介面與流程
- `agent.py`：Agent（提示詞、流程與工具呼叫）
- `prompts.py`：集中管理提示詞
- `sample_dialogue.md`：可直接當作「agent 開發過程對話紀錄」範本（你可再微調）
- `ABSTRACT_300chars.md`：300字摘要範本（你可換成自己結果）
