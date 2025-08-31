import streamlit as st
import pandas as pd
from typing import List, Dict, Any
import os
import sys

# 添加父目录到路径以导入api_service
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_service import make_api_request
from cos_uploader import ExamPaperCOSManager

# 获取数据的辅助函数
@st.cache_data(ttl=30)
def get_exam_papers() -> List[Dict]:
    """获取试卷列表"""
    result = make_api_request("GET", "exam_papers")
    return result["data"] if result["success"] else []

@st.cache_data(ttl=30)
def get_exam_paper_images() -> List[Dict]:
    """获取试卷图片列表"""
    result = make_api_request("GET", "exam_paper_images")
    return result["data"] if result["success"] else []

@st.cache_data(ttl=30)
def get_questions() -> List[Dict]:
    """获取题目列表"""
    result = make_api_request("GET", "questions")
    return result["data"] if result["success"] else []

def show_exam_paper_detail(paper_id: int):
    """显示试卷详情页面"""
    all_exam_papers = get_exam_papers()
    all_questions = get_questions()
    all_exam_paper_images = get_exam_paper_images()
    
    # 获取当前试卷信息
    current_paper = next((p for p in all_exam_papers if p['id'] == paper_id), None)
    if not current_paper:
        st.error("试卷不存在")
        return
    
    # 页面标题
    st.title(f"📄 {current_paper['title']}")
    
    # 显示创建时间和描述
    col1, col2 = st.columns([1, 1])
    with col1:
        st.info(f"📅 创建时间: {current_paper.get('created_time', 'N/A')}")
    with col2:
        # 查看试卷图片按钮
        paper_images = [img for img in all_exam_paper_images if img['exam_paper_id'] == paper_id]
        if paper_images:
            if st.button(f"🖼️ 查看试卷图片 ({len(paper_images)}张)", key="view_images_btn"):
                st.session_state['show_images'] = True
        else:
            st.info("🖼️ 暂无试卷图片")
    
    if current_paper.get('description'):
        st.markdown(f"**描述:** {current_paper['description']}")
    
    # 显示图片（如果用户点击了查看按钮）
    if st.session_state.get('show_images', False) and paper_images:
        st.markdown("---")
        st.subheader("🖼️ 试卷图片")
        
        # 关闭图片显示按钮
        if st.button("❌ 关闭图片显示", key="close_images_btn"):
            st.session_state['show_images'] = False
            st.rerun()
        
        # 按上传顺序排序显示图片
        sorted_images = sorted(paper_images, key=lambda x: x.get('upload_order', 0))
        
        # 使用列布局显示图片，每行3张
        cols_per_row = 3
        for i in range(0, len(sorted_images), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                img_index = i + j
                if img_index < len(sorted_images):
                    img = sorted_images[img_index]
                    with col:
                        try:
                            # 初始化COS管理器
                            cos_manager = ExamPaperCOSManager()
                            
                            # 处理图片URL
                            image_url = img['image_url']
                            if 'cos.ap-guangzhou.myqcloud.com' in image_url:
                                # 从完整URL中提取文件名
                                filename = image_url.split('.myqcloud.com/')[-1]
                                # 生成预签名URL，有效期2小时
                                display_url = cos_manager.get_safe_image_url(filename, use_presigned=True, expires_in=7200)
                            else:
                                # 如果不是COS URL，直接使用原URL
                                display_url = image_url
                            
                            # 显示图片
                            st.image(
                                display_url, 
                                caption=f"图片 {img.get('upload_order', img_index + 1)}",
                                use_container_width=True
                            )
                            # 显示图片信息
                            st.caption(f"ID: {img['id']}")
                        except Exception as e:
                            st.error(f"图片加载失败: {str(e)}")
                            # 显示调试信息
                            st.write(f"原始URL: {img.get('image_url', 'N/A')}")
    
    st.markdown("---")
    
    # 获取试卷相关的题目
    paper_questions = [q for q in all_questions if q['exam_paper_id'] == paper_id]
    
    # 计算统计信息
    total_questions = len(paper_questions)
    wrong_questions = [q for q in paper_questions if not q.get('is_correct', True)]
    wrong_count = len(wrong_questions)
    error_rate = (wrong_count / total_questions * 100) if total_questions > 0 else 0
    
    # 显示统计信息
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("总题数", total_questions)
    with col2:
        st.metric("错题数", wrong_count)
    with col3:
        st.metric("正确题数", total_questions - wrong_count)
    with col4:
        st.metric("错误率", f"{error_rate:.1f}%")
    
    st.markdown("---")
    
    # 题目列表
    st.subheader("📋 题目列表")
    
    # 创建题目数据
    questions_with_info = []
    for question in paper_questions:
        question_info = question.copy()
        question_info['status'] = '✅ 正确' if question.get('is_correct', True) else '❌ 错误'
        questions_with_info.append(question_info)
    
    # 按创建时间排序
    questions_with_info.sort(key=lambda x: x.get('created_time', ''), reverse=True)
    
    # 显示题目表格
    questions_df = pd.DataFrame(questions_with_info)
    if not questions_df.empty:
        columns_order = ['id', 'content', 'status', 'created_time']
        available_columns = [col for col in columns_order if col in questions_df.columns]
        questions_df = questions_df[available_columns]
    
    st.dataframe(questions_df, use_container_width=True)
    
    # 如果没有题目，显示提示信息
    if not paper_questions:
        st.info("该试卷暂无题目")

# 主页面
st.title("📄 试卷详情")

# 检查用户是否已登录
if not st.session_state.get("logged_in", False):
    st.error("❌ 请先登录才能访问试卷详情功能")
    st.info("💡 请返回首页进行登录")
    st.stop()

# 获取当前学生信息
if 'selected_student' not in st.session_state:
    st.session_state.selected_student = {
        'id': 1,
        'name': '默认学生',
        'user_id': 1
    }

current_student = st.session_state.selected_student
st.info(f"🎯 当前学生: **{current_student['name']}** (ID: {current_student['id']})")

# 获取所有试卷数据并按学生ID筛选
all_exam_papers = get_exam_papers()
student_exam_papers = [paper for paper in all_exam_papers if paper.get('student_id') == current_student['id']]

if not student_exam_papers:
    st.warning("⚠️ 该学生暂无试卷数据")
    st.info("💡 该学生还没有创建任何试卷")
    st.stop()

# 试卷筛选功能
st.subheader("🔍 选择试卷")

# 试卷名称筛选
search_term = st.text_input(
    "按试卷名称筛选",
    placeholder="输入试卷名称进行搜索...",
    key="paper_search"
)

# 根据搜索条件筛选试卷
filtered_papers = student_exam_papers
if search_term:
    filtered_papers = [
        paper for paper in student_exam_papers 
        if search_term.lower() in paper.get('title', '').lower()
    ]

if not filtered_papers:
    st.warning("⚠️ 没有找到匹配的试卷")
    st.info("💡 请尝试其他搜索关键词")
    st.stop()

# 试卷选择下拉框
paper_options = [f"{paper['id']} - {paper.get('title', '未命名试卷')}" for paper in filtered_papers]
selected_paper_option = st.selectbox(
    "选择要查看的试卷",
    options=paper_options,
    key="selected_paper"
)

if selected_paper_option:
    # 从选择的选项中提取试卷ID
    paper_id = int(selected_paper_option.split(' - ')[0])
    
    st.markdown("---")
    
    # 显示试卷详情
    show_exam_paper_detail(paper_id)
else:
    st.info("💡 请选择要查看的试卷")