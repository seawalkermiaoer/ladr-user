import streamlit as st
import pandas as pd
from typing import List, Dict, Any
import os
import sys

# 添加当前目录到路径以导入模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from api_service import make_api_request
from pages.login import show_login_page, check_login, show_logout_button

# 使用 Streamlit secrets 获取 Supabase 配置
try:
    SUPABASE_URL = st.secrets["supabase"]["url"]
    SUPABASE_KEY = st.secrets["supabase"]["key"]
except KeyError:
    SUPABASE_URL = ""
    SUPABASE_KEY = ""

# 页面配置
st.set_page_config(
    page_title="ladr",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 获取数据的辅助函数
@st.cache_data(ttl=30)
def get_questions() -> List[Dict]:
    """获取题目列表"""
    result = make_api_request("GET", "questions")
    return result["data"] if result["success"] else []

@st.cache_data(ttl=30)
def get_exam_papers() -> List[Dict]:
    """获取试卷列表"""
    result = make_api_request("GET", "exam_papers")
    return result["data"] if result["success"] else []

# 主应用逻辑
if not check_login():
    show_login_page()
else:
    # 显示登出按钮
    show_logout_button()
    
    # 自动设置默认学生信息
    if 'selected_student' not in st.session_state:
        st.session_state.selected_student = {
            'id': 1,
            'name': '默认学生',
            'user_id': 1
        }
    
    # 显示当前学生信息
    with st.sidebar:
        st.markdown("### 👤 当前学生")
        selected = st.session_state.selected_student
        
        # 获取当前学生的试卷数量
        all_exam_papers = get_exam_papers()
        student_papers = [paper for paper in all_exam_papers if paper.get('student_id') == selected['id']]
        paper_count = len(student_papers)
        
        st.info(f"**{selected['name']}** (ID: {selected['id']})")
        st.metric("📚 试卷数量", paper_count)
        
        # 调试信息（可选显示）
        if st.checkbox("显示调试信息", key="debug_info"):
            st.write(f"总试卷数: {len(all_exam_papers)}")
            st.write(f"当前学生ID: {selected['id']}")
            if all_exam_papers:
                st.write("试卷数据示例:")
                st.json(all_exam_papers[0] if all_exam_papers else {})
            st.write(f"匹配的试卷: {len(student_papers)}")
            if student_papers:
                st.write("匹配试卷示例:")
                st.json(student_papers[0])
    
    # 定义页面
    exam_paper_detail_page = st.Page(
        "pages/exam_paper_detail.py", 
        title="试卷详情", 
        icon="📋"
    )
    error_analysis_page = st.Page(
        "pages/error_analysis.py", 
        title="错题分析", 
        icon="📊"
    )
    
    # 创建导航
    pg = st.navigation([
        exam_paper_detail_page,
        error_analysis_page
    ])
    
    # 运行页面
    pg.run()