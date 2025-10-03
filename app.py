import os
import json
import streamlit as st

# === 题目路径 ===
quiz_base = "./汇总题目/汇总题目"  # 注意：部署前请把题目文件夹放到同级目录

# 找到所有题目文件夹
quiz_folders = sorted(
    [os.path.join(quiz_base, d) for d in os.listdir(quiz_base) if os.path.isdir(os.path.join(quiz_base, d))],
    key=lambda x: int(''.join(filter(str.isdigit, os.path.basename(x))))
)

# 会话状态保存分数
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0
    st.session_state.score = 0

st.title("象棋走法测验系统")
st.markdown("以下是 **炮的走法学习题目**，轮到红方走，哪个选项是正确的？")

idx = st.session_state.current_idx
qpath = quiz_folders[idx]

st.subheader(f"第 {idx+1} 题")
st.image(os.path.join(qpath, "题面.png"), use_column_width=True)

# 加载meta.json
with open(os.path.join(qpath, "meta.json"), "r", encoding="utf-8") as f:
    meta = json.load(f)

cols = st.columns(len(meta["options"]))

for i, opt in enumerate(meta["options"]):
    with cols[i]:
        st.image(os.path.join(qpath, opt["file"]), use_column_width=True)
        if st.button(f"选择 {opt['label']}", key=f"btn{idx}{i}"):
            if opt["is_correct"]:
                st.success("✅ 回答正确！")
                st.session_state.score += 1
            else:
                st.error(f"❌ 回答错误，正确答案是 {meta['correct_label']}")

            st.session_state.current_idx += 1
            if st.session_state.current_idx >= len(quiz_folders):
                st.balloons()
                st.info(f"测验结束，总分：{st.session_state.score}/{len(quiz_folders)}")
            st.experimental_rerun()
