# agent 開發過程對話紀錄（範例，可直接交）

> 你可以把這份檔案當作「開發紀錄」：一方面展示你如何用 Agent 思維拆解需求，
> 一方面也能貼上你在 Streamlit demo 內測試的真實輸入/輸出片段（建議再補 1~2 組你自己的測試）。

---

## Round 0：釐清作業要求

**User**：作業要交什麼？  
**Agent**：需要三項：  
1) 300 字摘要（ABSTRACT）  
2) Agent 開發過程對話紀錄  
3) GitHub repo 與 Streamlit.app 線上 demo（可讓助教實際操作）  

---

## Round 1：決定專題主題（深度學習＋AIGC）

**User**：我想做一個跟課堂內容貼近的 demo。  
**Agent**：建議做「AIGC 課程小助教」：輸入課堂筆記 → 生成摘要＋測驗＋封面圖。  
優點：同時涵蓋文字生成與圖像生成、可快速 demo、也能在報告摘要說明方法與限制。  

---

## Round 2：設計 Agent 流程與工具

**User**：Agent 要怎麼做才像真的？  
**Agent**：把任務拆成 3 個工具呼叫：  
- tool_1：摘要（300 字硬限制）  
- tool_2：測驗（混合題型＋答案）  
- tool_3：封面提示詞（A/B/C 三種風格）  
如果有圖像 API，再加 tool_4：把其中一個風格 prompt 轉成封面圖。  

---

## Round 3：第一次測試（用課堂筆記）

**User**（貼上筆記）：本週介紹 Transformer attention、diffusion model 去噪生成、prompt engineering、以及 RAG…  
**Agent**：  
- 摘要：<貼你在 app 產出的摘要>  
- 測驗：<貼你在 app 產出的 10 題測驗>  
- 封面提示詞：<貼你在 app 產出的 A/B/C prompt>  

---

## Round 4：發現問題並改進

**User**：摘要常常超過 300 字。  
**Agent**：把摘要提示詞改成「嚴格 <= 300 字」且只輸出摘要本體；必要時加上「若超字請自動刪減」。  

**User**：測驗題目太像抄筆記。  
**Agent**：在提示詞加上「要能測出理解，不要抄句子」，並要求題型混合。  

---

## Round 5：第二次測試（更完整內容）

**User**（貼上更完整講義）：…  
**Agent**：輸出品質提升（摘要更精煉、題目更理解導向、封面 prompt 更可視覺化）。  

---

## Round 6：部署與提交

**User**：怎麼交？  
**Agent**：  
- GitHub：上傳本 repo（含 README、requirements、app.py）  
- Streamlit：連 GitHub → Deploy → 設定 Secrets（OPENAI_API_KEY）  
- report：把 abstract 貼上＋用 2~3 句交代你的 demo 做什麼與限制  
- 對話紀錄：提交本檔＋補上你自己的 1~2 次真實測試內容/截圖  
