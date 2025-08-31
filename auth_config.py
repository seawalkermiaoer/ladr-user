#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
认证配置模块
使用 streamlit-authenticator 库进行用户认证
"""

import streamlit_authenticator as stauth
import streamlit as st

def get_authenticator():
    """
    获取认证器实例（使用缓存避免重复初始化）
    
    Returns:
        stauth.Authenticate: 认证器实例
    """
    try:
        # 直接从 secrets 获取用户信息
        username = st.secrets["login"]["username"]
        password = st.secrets["login"]["password"]
        
        # 创建用户凭据字典
        credentials = {
            'usernames': {
                username: {
                    'email': 'admin@example.com',
                    'failed_login_attempts': 0,
                    'first_name': username,
                    'last_name': '',
                    'logged_in': False,
                    'password': password  # 让 streamlit-authenticator 自动处理哈希
                }
            }
        }
        
        # 创建认证器实例
        authenticator = stauth.Authenticate(
            credentials,
            'ladr_auth_cookie',  # cookie name
            'ladr_auth_key',     # cookie key
            30                   # cookie expiry days
        )
        
        return authenticator
        
    except Exception as e:
        st.error(f"初始化认证器失败: {str(e)}")
        return None