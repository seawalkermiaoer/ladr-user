import streamlit as st
import sys
import os

# 添加父目录到路径以导入认证配置
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_config import get_authenticator


def show_login_page():
    """显示登录页面（使用 streamlit-authenticator）
    使用 v0.4.x API：authenticator.login 在渲染小部件时不返回三元组，
    需要从 st.session_state 中读取 name、authentication_status、username。
    """
    st.title("🔐 错误和重复的密度才是阶梯")
    st.markdown("---")

    # 获取认证器
    authenticator = get_authenticator()
    if not authenticator:
        st.error("认证系统初始化失败")
        return

    # 创建居中的登录表单区域（避免元组解包导致的 NoneType 错误）
    cols = st.columns([1, 2, 1])

    with cols[1]:
        # 渲染登录组件（v0.4.x 渲染时返回 None）
        authenticator.login(location='main', key='Login')

        # 从会话状态读取登录结果
        authentication_status = st.session_state.get('authentication_status', None)
        name = st.session_state.get('name')
        username = st.session_state.get('username')

        # 处理登录状态
        if authentication_status is False:
            st.error('❌ 用户名或密码错误，请重试。')
        elif authentication_status is None:
            st.warning('请输入用户名和密码')
        elif authentication_status:
            # 登录成功，设置会话状态（补全必要字段）
            st.session_state.logged_in = True
            if username:
                st.session_state.username = username
            if name:
                st.session_state.name = name
            # 这里根据实际业务设置用户/学生信息
            st.session_state.user_id = st.session_state.get('user_id', 1)
            st.session_state.student_id = st.session_state.get('student_id', 1)

            st.success(f'欢迎 {name or username or "用户"}！')
            st.rerun()

        # 添加说明信息
        st.markdown("---")
        st.info("💡 错误是触发神经可塑性的唯一钥匙；没有错误，大脑就默认一切正常，不会升级回路。")
        st.info("🔑 10 分钟高能错误练习 > 2 小时无脑重复")

        # 显示默认登录信息
        with st.expander("💡 登录提示"):
            try:
                default_username = st.secrets["login"]["username"]
                st.info(f"默认用户名: {default_username}")
            except Exception:
                st.info("请检查配置文件")


def check_login():
    """检查登录状态（基于 authenticator 的会话状态）

    - 优先读取 st.session_state['authentication_status']。
    - 与自定义的 logged_in 状态保持同步，避免库的登出按钮清 cookie 但未同步自定义标志的情况。

    Returns:
        bool: 当前是否已登录
    """
    auth_status = st.session_state.get('authentication_status', None)
    if auth_status is True:
        st.session_state.logged_in = True
        return True
    # 未登录或已登出：同步标志为 False
    st.session_state.logged_in = False
    return False


def logout():
    """登出功能（清除 Cookie 和会话状态）

    为了确保立即生效并避免再次渲染登出按钮，这里优先使用
    authenticator.logout() 进行编程式登出；若版本签名不兼容，则回退到
    location='unrendered' 的方式清除认证 Cookie；随后手动清理会话状态并触发 rerun。
    """
    authenticator = get_authenticator()

    # 1) 清除认证 Cookie（不渲染按钮）
    if authenticator:
        try:
            # v0.4.x 支持直接 programmatic 调用，无需参数
            authenticator.logout()
        except TypeError:
            # 回退到未渲染方式，显式提供唯一 key，兼容旧签名
            try:
                authenticator.logout(location='unrendered', key='LogoutSilent')
            except Exception as e:
                st.info(f"登出提示：{str(e)}")
        except Exception as e:
            st.info(f"登出提示：{str(e)}")

    # 2) 清除与认证相关的会话状态
    st.session_state.logged_in = False
    st.session_state['authentication_status'] = None
    for key in ['username', 'name', 'user_id', 'student_id']:
        if key in st.session_state:
            del st.session_state[key]

    # 3) 触发重载，回到未登录状态
    st.rerun()


def show_logout_button():
    """显示登出按钮（由 streamlit-authenticator 负责清 Cookie）

    在侧边栏渲染官方登出按钮，并使用唯一 key，避免多页应用的重复 key 问题。
    """
    with st.sidebar:
        st.markdown("---")
        name = st.session_state.get("name", st.session_state.get("username", "用户"))
        st.write(f"👤 欢迎, {name}")

        authenticator = get_authenticator()
        if authenticator:
            # 渲染官方登出按钮，库会负责清除 cookie 和将 authentication_status 置为 None
            try:
                authenticator.logout(button_name='🚪 登出', location='sidebar', key='LogoutSidebar', use_container_width=True)
            except TypeError:
                # 兼容旧签名（可能不支持 button_name/use_container_width 作为关键字参数）
                authenticator.logout('🚪 登出', 'sidebar', key='LogoutSidebar')