from openai import OpenAI
import gradio as gr

# ===================== 【必须填写】你的API配置 =====================
API_KEY = "ark-4aaa9335-e5ba-4f88-ae37-b0a0ca396ca1-9cee4"
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
MODEL_NAME = "doubao-pro-4k"
# ===================================================================

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# 12个职场功能提示词
FUNCTION_PROMPT = {
    "1.职场日报/周报/月报自动生成":
        "你是资深职场文员，根据用户提供工作内容，自动生成标准规范日报、周报、月报，分工作完成、现存问题、后续工作计划，排版工整适合直接上交",
    "2.企业内部通知公告撰写":
        "专业行政文案，撰写正规企业内部通知、公告、放假通知、人事通知、活动通知，格式标准、语言正式简洁、要素齐全",
    "3.商务正式邮件自动撰写":
        "精通职场商务邮件，撰写对外对接、合作、回访、请假、汇报类正式邮件，格式标准、语气得体专业，可直接复制发送",
    "4.会议录音文字转结构化纪要":
        "用户粘贴会议口语化录音文字，帮其梳理提炼成标准结构化会议纪要，区分参会人、会议主题、讨论内容、内容重点、达成决议、待办事项、责任人与时间",
    "5.杂乱Excel数据清洗":
        "用户给出Excel表格，帮忙筛查问题并给出完整的处理结果版本",
    "6.PDF长文档提炼核心要点":
        "用户粘贴PDF全文/段落内容，快速精简提炼全文核心主旨、重点信息、关键结论、核心数据，去除冗余内容",
    "7.小红书/短视频爆款文案生成":
        "擅长新媒体流量文案，根据产品、主题、场景生成吸睛标题+正文，风格贴合小红书、抖音短视频，情绪到位易出圈",
    "8.批量数据分析+透视表制作指导":
        "针对批量业务数据，给出数据分析思路、统计维度、数据分类方法，附带Excel数据透视表详细制作流程与字段搭配技巧",
    "9.文档内容一键转PPT文案（可选风格）":
        "把用户长篇文字内容，拆分梳理成标准PPT每页大纲+每页精简文案，支持简约商务/文艺清新/正式汇报三种风格，直接套用做PPT",
    "10.表格数据分析+数据结论输出":
        "根据用户表格内数据内容，进行理性数据分析，总结数据趋势、好坏表现、存在问题、优化建议，输出完整专业数据结论",
    "11.专业短视频/宣传片视频脚本撰写":
        "按照标准影视脚本格式撰写，包含镜头画面、台词文案、时长安排、背景音乐、场景动作，结构完整可直接拍摄使用",
    "12.公众号爆款推文文章生成":
        "根据用户需求撰写公众号优质原创推文，逻辑流畅、段落分明、标题吸睛、排版舒服，符合大众阅读习惯，自带传播感"
}

# 核心生成函数
def run_office_tool(select_func, user_input):
    if not user_input or len(user_input.strip()) == 0:
        return "⚠️ 请填写对应的内容、素材、需求后再生成！"

    system_prompt = FUNCTION_PROMPT[select_func]
    try:
        res = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.6,
            max_tokens=2500
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"❌ 生成失败：{str(e)}"

# 网页界面
with gr.Blocks(title="全能办公AI工具箱") as web_app:
    gr.Markdown("""
    # 🧰 12合一全能办公AI工具
    手机/电脑通用 | 无需同一WiFi | 永久在线
    """)

    func_choice = gr.Dropdown(
        label="请选择所需办公功能",
        choices=list(FUNCTION_PROMPT.keys()),
        value="1.职场日报/周报/月报自动生成"
    )

    user_input_box = gr.Textbox(
        label="输入素材/内容/需求",
        lines=8,
        placeholder="粘贴文字、会议录音、工作内容、产品信息、文档内容等"
    )

    result_show = gr.Textbox(
        label="AI智能生成结果",
        lines=15
    )

    submit_btn = gr.Button("🚀 一键智能生成", variant="primary")
    submit_btn.click(fn=run_office_tool, inputs=[func_choice, user_input_box], outputs=result_show)

# Hugging Face专用启动方式
if __name__ == "__main__":
    web_app.launch()