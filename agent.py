# agent.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Optional

from openai import OpenAI

from prompts import SYSTEM_AGENT, SUMMARY_PROMPT, QUIZ_PROMPT, COVER_PROMPT

@dataclass
class AgentResult:
    summary: str
    quiz: str
    cover_prompt: str
    used_api: bool
    raw: Optional[Dict[str, Any]] = None

class AIGCTeachingAssistantAgent:
    """一個最小可用的 Agent：把筆記 → 摘要/測驗/封面prompt。"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key) if api_key else None

    def _chat(self, user_prompt: str) -> str:
        assert self.client is not None
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_AGENT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
        )
        return resp.choices[0].message.content.strip()

    def run(self, notes: str) -> AgentResult:
        notes = (notes or "").strip()
        if not notes:
            return AgentResult(
                summary="（請先貼上課堂筆記或講義內容）",
                quiz="（請先貼上課堂筆記或講義內容）",
                cover_prompt="（請先貼上課堂筆記或講義內容）",
                used_api=False,
            )

        if not self.client:
            # 無 API Key：示範模式（用固定模板輸出，讓 App 仍可操作）
            demo_summary = """本系統示範以生成式 AI 將課堂筆記轉為可用的學習素材：先抽取主題與關鍵概念，形成 300 字內摘要；再依概念層級產生混合題型測驗以檢核理解；並輸出封面圖像提示詞以利製作簡報或作業展示。此流程可加速內容整理與教學互動，但仍需人類檢查事實正確性、避免機密外洩並留意偏誤與版權。"""
            demo_quiz = """1)【選擇】生成式AI最常用的文本生成架構是？(A)CNN (B)Transformer (C)KNN (D)SVM  Answer: B
2)【選擇】文字生成時常用來控制多樣性的是？(A)temperature (B)learning rate (C)batch size (D)momentum  Answer: A
3)【選擇】圖像生成擴散模型的核心概念最接近？(A)逐步加噪再去噪 (B)一次性重建 (C)只做分類 (D)只做聚類  Answer: A
4)【選擇】提示詞工程的目的較接近？(A)壓縮模型 (B)引導模型輸出 (C)更換GPU (D)只改資料集  Answer: B
5)【是非】生成式模型輸出必然正確。 Answer: 否
6)【是非】RAG 可用外部資料降低幻覺。 Answer: 是
7)【是非】圖像生成可完全不考慮著作權。 Answer: 否
8)【簡答】請描述 temperature 對輸出有何影響。 Answer: 越高越多樣但更不穩定；越低越保守可重現。
9)【簡答】擴散模型為何能生成高品質圖像？ Answer: 透過逐步去噪學習資料分佈，生成時從噪聲逐步還原。
10)【簡答】實務上如何降低生成內容風險？ Answer: 人審、內容過濾、來源註記、避免機密/個資、測試與監控。"""
            demo_cover = """A: 乾淨學術海報風，中央是一張筆記頁面與神經網路示意圖，旁有流程箭頭(摘要→測驗→封面)，白底藍灰配色，資訊圖表構圖
B: 未來科技風，霓虹光的資料流在空中組成Transformer與擴散模型圖示，背景是數位城市與雲端，紫藍霓虹，科幻強對比
C: 溫暖教育插畫風，桌上有課本與平板，螢幕顯示AI生成摘要與小測驗，旁邊有可愛圖示與便利貼，柔和暖色、溫馨教室氛圍"""
            return AgentResult(demo_summary, demo_quiz, demo_cover, used_api=False)

        # 有 API Key：真正呼叫模型
        summary = self._chat(SUMMARY_PROMPT.format(notes=notes))
        quiz = self._chat(QUIZ_PROMPT.format(notes=notes))
        cover_prompt = self._chat(COVER_PROMPT.format(notes=notes))
        return AgentResult(summary=summary, quiz=quiz, cover_prompt=cover_prompt, used_api=True)
