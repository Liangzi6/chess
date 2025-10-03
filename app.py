import streamlit as st
from PIL import Image
import zipfile
import os

# -------------------------
# 配置页面
# -------------------------
st.set_page_config(page_title="炮的走法练习题", layout="centered")

# -------------------------
# 解压题库
# -------------------------
zip_path = "汇总题目.zip"
extract_dir = "汇总题目"

if not os.path.exists(extract_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

# -------------------------
# 加载题目列表
# -------------------------
question_dirs = sorted([os.path.join(extract_dir, d) for d in os.listdir(extract_dir)
                        if os.path.isdir(os.path.join(extract_dir, d))])

# -------------------------
# 初始化题目索引
# -------------------------
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0

def show_question(idx):
    st.title("炮的走法练习题")
    st.write("以下是炮的走法学习题目，轮到红方走，哪个选项是正确的？")

    q_dir = question_dirs[idx]
    # 显示题面图
    question_img_path = os.path.join(q_dir, "题面.png")
    if os.path.exists(question_img_path):
        img = Image.open(question_img_path)
        st.image(img, width=400)  # 题目图略微缩小

    # 读取选项图片
    options = []
    for opt in ["A.png", "B.png", "C.png"]:
        opt_path = os.path.join(q_dir, opt)
        if os.path.exists(opt_path):
            options.append((opt[0], opt_path))

    # 读取答案
    answer_path = os.path.join(q_dir, "answer.txt")
    correct_answer = None
    if os.path.exists(answer_path):
        with open(answer_path, "r", encoding="utf-8") as f:
            correct_answer = f.read().strip()

    # 显示选项按钮
    st.write("选择你的答案：")
    cols = st.columns(len(options))
    for i, (label, path) in enumerate(options):
        with cols[i]:
            img = Image.open(path)
            if st.button(f"{label}", key=f"{idx}_{label}"):
                if label == correct_answer:
                    st.success(f"第 {idx+1} 题回答正确！答案是 {correct_answer}")
                else:
                    st.error(f"第 {idx+1} 题回答错误！正确答案是 {correct_answer}")

                # 显示下一题按钮
                if st.session_state.current_idx < len(question_dirs) - 1:
                    if st.button("下一题", key=f"next_{idx}"):
                        st.session_state.current_idx += 1
                        st.experimental_rerun()
                else:
                    st.info("已经是最后一题了！")

# -------------------------
# 显示当前题目
# -------------------------
show_question(st.session_state.current_idx)

