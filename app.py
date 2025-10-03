import streamlit as st
from zipfile import ZipFile
from io import BytesIO
from PIL import Image

# ----------------------
# 读取题目数据
# ----------------------
import os

DATA_ZIP = "汇总题目.zip"
QUESTIONS = []

def load_questions(zip_path):
    questions = []
    with ZipFile(zip_path, 'r') as zf:
        for folder in zf.namelist():
            if folder.endswith('题面.png'):
                q_folder = os.path.dirname(folder) + '/'
                # 题面图片
                question_img = Image.open(BytesIO(zf.read(folder)))
                # 选项
                options = []
                for opt_name in ['A.png', 'B.png', 'C.png']:
                    try:
                        img_path = q_folder + opt_name
                        opt_img = Image.open(BytesIO(zf.read(img_path)))
                        options.append((opt_name[0], opt_img))
                    except KeyError:
                        pass  # 如果某些选项不存在
                questions.append({
                    'question_img': question_img,
                    'options': options
                })
    return questions

QUESTIONS = load_questions(DATA_ZIP)

# ----------------------
# Streamlit app
# ----------------------
st.title("炮的走法练习题")

if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0
if "answers" not in st.session_state:
    st.session_state.answers = []

def show_question(idx):
    if idx >= len(QUESTIONS):
        st.success("你已经完成所有题目！")
        st.write("你的答案：", st.session_state.answers)
        return
    
    question = QUESTIONS[idx]
    
    st.subheader(f"第 {idx+1} 题")
    st.markdown("**以下是炮的走法学习题目，轮到红方走，哪个选项是正确的？**")
    
    # 显示题面图片，稍小一点
    st.image(question['question_img'], width=400)
    
    options = question['options']
    if not options:
        st.error("当前题目没有选项！")
        return
    
    # 显示选项按钮，稍大一点
    cols = st.columns([1.5]*len(options))
    for i, (label, img) in enumerate(options):
        with cols[i]:
            st.image(img, width=120)
            if st.button(label):
                st.session_state.answers.append(label)
                st.session_state.current_idx += 1
                st.experimental_rerun()  # 点击后刷新显示下一题

# 显示当前题
show_question(st.session_state.current_idx)

