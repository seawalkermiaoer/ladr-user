# LADR - 学习分析与诊断报告系统

> 基于 Streamlit 的智能学习分析平台，专注于试卷管理和错题诊断

## ✨ 功能特性

- 📝 **试卷管理** - 创建、编辑试卷，支持图片上传
- 📊 **错题分析** - 智能统计分析，生成学习诊断报告
- 👤 **用户管理** - 多学生支持，个性化学习跟踪
- 🔍 **题目标注** - 便捷的题目正误标注和内容管理

## 🚀 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动应用
```bash
streamlit run streamlit_app.py
```

### 🔐 认证功能
- 使用 `streamlit-authenticator` 库实现用户认证
- 支持 **Cookie 持久化登录**，刷新页面后登录状态保持
- Cookie 有效期：30天
- 安全的密码哈希存储

## 🛠️ 技术栈

- **前端**: Streamlit
- **数据库**: Supabase (PostgreSQL)
- **云存储**: 腾讯云 COS
- **数据处理**: Pandas, Plotly
## 📁 项目结构

```
ladr/
├── pages/                  # 页面组件
│   ├── login.py           # 登录页面
│   ├── exam_paper_detail.py # 试卷详情
│   └── error_analysis.py  # 错题分析
├── streamlit_app.py       # 主应用入口
├── api_service.py         # API服务层
├── supabase_handler.py    # 数据库处理
├── cos_uploader.py        # 云存储管理
└── requirements.txt       # 依赖包
```

## 📊 核心功能

### 试卷管理
- 创建和编辑试卷
- 图片上传和预览
- 题目批量导入（JSON格式）

### 错题分析
- 错题统计可视化
- 学习趋势分析
- 诊断报告生成

### 数据管理
- 用户认证系统
- 多学生支持
- 云端数据同步

## 📝 使用说明


## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进项目。

## 📄 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件了解详情。
