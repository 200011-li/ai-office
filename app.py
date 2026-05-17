# -*- coding: utf-8 -*-
import streamlit as st
from openai import OpenAI

# ===================== 【你的配置 100% 精准填写】 =====================
API_KEY = "ark-4aaa9335-e5ba-4f88-ae37-b0a0ca396ca1-9cee4"
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
MODEL_NAME = "Doubao-Seed-2.0-lite"
# ====================================================================

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# ===================== 你要的 12 个功能 =====================
FUNCTIONS = {
    "1. 职场日报/周报/月报自动生成":
        "生成标准日报/周报/月报，包含完成工作、问题、计划。",

    "2. 企业内部通知公告撰写":
        "写正式企业通知、公告、人事通知、简洁规范。",

    "3. 商务正式邮件自动撰写":
        "写正式商务邮件，得体、专业、可直接发送。",

    "4. 会议录音文字转结构化纪要":
        "把录音文字整理成标准纪要：主题、内容、决议、待办。",

    "5. 杂乱Excel数据清洗":
        "分析Excel问题，给出清洗、去重、规整方案。",

    "6. PDF长文档提炼核心要点":
        "精简PDF内容，提炼重点、观点、数据。",

    "7. 小红书/短视频爆款文案生成":
        "生成吸睛标题+正文，适合短视频、小红书。",

    "8. 批量数据分析+透视表制作指导":
        "给出数据分析思路 + Excel透视表制作方法。",

    "9. 文档内容一键转PPT文案":
        "把长文转PPT大纲+每页文案，可直接制作PPT。",

    "10. 表格数据分析+数据结论输出":
        "分析表格数据，给出趋势、问题、建议。",

    "11. 专业短视频/宣传片脚本撰写":
        "写专业拍摄脚本：镜头、台词、时长、画面。",

    "12. 公众号爆款推文文章生成":
        "写公众号文章，标题吸睛、结构清晰、易传播。"
}


# ===================== 生成函数（绝对稳定） =====================
def generate_content(selected_func, user_input):
    if not user_input or user_input.strip() == "":
        return "⚠️ 请输入内容后再生成！"

    prompt = FUNCTIONS[selected_func]

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.6,
            max_tokens=3000
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ 错误：{str(e)}"


# ===================== 网页界面 =====================
st.set_page_config(page_title="12合1办公AI工具", layout="wide")
st.title("🧰 12合1全能办公AI工具")
st.markdown("### ✅ 手机/电脑通用 | 无需同一WiFi | 永久在线")

# 功能选择
selected = st.selectbox("请选择功能", list(FUNCTIONS.keys()))

# 输入框
content = st.text_area("请输入你的内容/需求", height=220)

# 生成按钮
if st.button("🚀 一键生成", type="primary"):
    with st.spinner("正在生成..."):
        result = generate_content(selected, content)
        st.success("✅ 生成完成！")
        st.markdown("---")
        st.markdown("## 📝 生成结果")
        st.write(result)