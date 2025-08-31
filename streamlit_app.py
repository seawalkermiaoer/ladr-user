import streamlit as st
import pandas as pd
from typing import List, Dict, Any
import os
import sys

# 添加当前目录到路径以导入模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from api_service import make_api_request, api_service
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
def get_questions_by_student_id(student_id: int) -> List[Dict[str, Any]]:
    """根据学生ID获取题目列表
    
    Args:
        student_id (int): 学生ID
        
    Returns:
        List[Dict[str, Any]]: 题目列表，如果出错则返回空列表
    """
    try:
        # 通过学生试卷获取相关题目，提升性能
        student_papers = api_service.get_exam_papers_by_student_id(student_id)
        if not student_papers:
            return []
        
        # 获取所有相关题目ID
        question_ids = set()
        for paper in student_papers:
            if 'questions' in paper and paper['questions']:
                question_ids.update(paper['questions'])
        
        # 如果没有题目ID，返回空列表
        if not question_ids:
            return []
            
        # 获取所有题目并筛选
        result = make_api_request("GET", "questions")
        if result["success"] and result["data"]:
            return [q for q in result["data"] if q.get('id') in question_ids]
        return []
        
    except Exception as e:
        st.error(f"获取学生题目数据时出错: {str(e)}")
        return []

@st.cache_data(ttl=30)
def get_exam_papers_by_student_id(student_id: int) -> List[Dict[str, Any]]:
    """根据学生ID获取试卷列表
    
    Args:
        student_id (int): 学生ID
        
    Returns:
        List[Dict[str, Any]]: 试卷列表，如果出错则返回空列表
    """
    try:
        return api_service.get_exam_papers_by_student_id(student_id)
    except Exception as e:
        st.error(f"获取学生试卷数据时出错: {str(e)}")
        return []

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
        
        # 获取当前学生的试卷数量（优化版本，包含错误处理）
        try:
            student_papers = get_exam_papers_by_student_id(selected['id'])
            paper_count = len(student_papers) if student_papers else 0
            
            # 显示学生基本信息
            st.info(f"**{selected['name']}** (ID: {selected['id']})")
            st.metric("📚 试卷数量", paper_count)
                        
        except Exception as e:
            st.error(f"加载学生信息时出错: {str(e)}")
            # 提供默认显示
            st.info(f"**{selected['name']}** (ID: {selected['id']})")
            st.metric("📚 试卷数量", "--")
    
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