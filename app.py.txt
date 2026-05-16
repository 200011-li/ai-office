import streamlit as st
from openai import OpenAI
from docx import Document
import io

# 页面基础配置
st.set_page_config(
    page_title="职场AI办公助手",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.title("💼 职场AI办公助手")
st.divider()

# 功能列表
func_list = [
    "1. 职场日报/周报/月报自动生成",
    "2. 岗位JD拆解+面试题生成",
    "3. 商务正式邮件自动撰写",
    "4. 会议录音→结构化纪要",
    "5. 杂乱Excel数据清洗整理",
    "6. PDF文档提炼核心要点",
    "7. 小红书/短视频文案生成",
    "8. 批量数据分析+透视表",
    "9. 文档一键转PPT",
    "10. 表格数据分析+结论",
    "11. 专业视频脚本撰写",
    "12. 公众号爆款文章生成"
]

# 提示词库
prompt_map = {
    1: "请根据我提供的内容，按需求类型（日报/周报/月报），生成一篇专业、简洁、正式的职场报告，尽量口语化，分点描述，突出工作成果与进度。",
    2: "请拆解这个岗位JD，输出：核心要求、胜任力、高频面试题（含回答思路以及具体回答示例）。",
    3: "请根据我提供的对象以及场景帮我写一封正式、得体、专业的商务邮件。",
    4: "请把这段会议录音转文字，整理成结构化、精简、重点清晰的会议纪要。",
    5: "请帮我清洗整理Excel数据，去重、补全、规范格式。",
    6: "请帮我提炼这份PDF的核心要点，分点输出。",
    7: "请根据我提供的主题生成一篇爆款小红书/短视频文案，吸引人、有网感、易传播，突出风格。",
    8: "请帮我分析这批数据，生成数据透视表思路与可视化建议。",
    9: "请把这段文档内容转换成PPT大纲（适合直接复制到PPT）。",
    10: "请分析表格数据，输出结论、洞察、建议。",
    11: "请生成一个完整的短视频脚本范例：镜头、台词、画面、时长。",
    12: """你是资深公众号主编，擅长写1500字左右爆款文章，风格多变。
请按用户要求生成：
- 吸引人标题
- 开头痛点/故事引入
- 3-5个核心小标题模块
- 每段简短、手机友好
- 结尾引导关注/互动
- 风格：专业/亲切/干货/网感（按用户内容调整）
全文结构完整、无AI腔、可直接发布。"""
}

# 输入API密钥
api_key = st.text_input("🔑 填写火山方舟API Key(ak开头)", type="password")
client = None
if api_key:
    client = OpenAI(api_key=api_key, base_url="https://ark.cn-beijing.volces.com/api/v3")
    st.success("✅ 密钥连接成功，可正常使用")

# 选择功能
choose_func = st.selectbox("📌 选择使用功能", func_list)
now_num = func_list.index(choose_func) + 1

# 输入内容
user_text = st.text_area("✍️ 输入你的需求/素材内容", height=180)

# 生成按钮
if st.button("🚀 一键AI生成", type="primary"):
    if not client:
        st.warning("请先填写正确API密钥")
    elif not user_text.strip():
        st.warning("请输入需要处理的内容")
    else:
        with st.spinner("正在快速生成内容，请稍等..."):
            full_prompt = prompt_map[now_num] + "\n用户内容：\n" + user_text
            res = client.chat.completions.create(
                model="doubao-pro-256k",
                messages=[{"role":"user","content":full_prompt}]
            )
            result_data = res.choices[0].message.content
            st.session_state["ai_result"] = result_data

# 展示结果+下载
if "ai_result" in st.session_state:
    st.divider()
    st.subheader("📄 生成完成内容")
    st.write(st.session_state["ai_result"])

    # TXT下载
    st.download_button(
        label="💾 下载保存为TXT文档",
        data=st.session_state["ai_result"],
        file_name="AI办公结果.txt",
        mime="text/plain"
    )

    # Word下载
    doc_file = Document()
    doc_file.add_paragraph(st.session_state["ai_result"])
    buf = io.BytesIO()
    doc_file.save(buf)
    buf.seek(0)
    st.download_button(
        label="📝 下载保存为Word文档",
        data=buf,
        file_name="AI办公结果.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )