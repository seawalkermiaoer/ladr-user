# LADR - 学习分析与诊断报告系统

## 📖 项目简介

LADR（Learning Analytics and Diagnostic Report）是一个基于 Streamlit 的学习分析与诊断报告系统，专门用于管理学生试卷、题目分析和错题诊断。系统提供了完整的试卷管理、图片上传、题目标注和错题分析功能。

## 🏗️ 系统架构

### 技术栈
- **前端框架**: Streamlit
- **后端API**: FastAPI
- **数据库**: Supabase (PostgreSQL)
- **云存储**: 腾讯云COS
- **数据处理**: Pandas, NumPy
- **图像处理**: PIL
- **数据可视化**: Plotly

### 架构设计
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    FastAPI      │    │    Supabase     │
│   前端界面       │◄──►│    API服务      │◄──►│    数据库       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   页面组件       │    │   业务逻辑       │    │   数据模型       │
│   - 试卷管理     │    │   - CRUD操作     │    │   - 用户表       │
│   - 图片管理     │    │   - 批量处理     │    │   - 学生表       │
│   - 题目标注     │    │   - 数据验证     │    │   - 试卷表       │
│   - 错题分析     │    │   - 错误处理     │    │   - 题目表       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 项目结构

```
ladr/
├── .devcontainer/          # 开发容器配置
├── .github/                # GitHub配置
├── .streamlit/             # Streamlit配置
├── pages/                  # 页面组件
│   ├── login.py           # 登录页面
│   ├── student_selection.py # 学生选择
│   ├── exam_papers.py     # 试卷管理
│   ├── exam_paper_detail.py # 试卷详情
│   ├── exam_paper_images.py # 图片管理
│   ├── knowledge_points.py # 知识点管理
│   └── error_analysis.py  # 错题分析
├── streamlit_app.py       # 主应用入口
├── api_service.py         # API服务层
├── api_routes.py          # API路由定义
├── models.py              # 数据模型
├── supabase_handler.py    # 数据库处理
├── cos_uploader.py        # 云存储管理
└── requirements.txt       # 依赖包
```

## 🚀 功能特性

### 1. 用户管理
- 用户登录认证
- 学生信息管理
- 多学生切换支持

### 2. 试卷管理
- 试卷创建、编辑、删除
- 试卷列表展示
- 按学生筛选试卷
- 试卷统计信息（总题数、错题数、错误率）

### 3. 图片管理
- 试卷图片上传（支持腾讯云COS）
- 图片预览和管理
- 批量图片操作
- 图片URL签名访问

### 4. 题目管理
- 单个题目添加和编辑
- 批量题目导入（JSON格式）
- 题目正误标注
- 题目内容管理
- 图片关联管理

### 5. 知识点管理
- 知识点创建和管理
- 题目与知识点关联
- 知识点统计分析

### 6. 错题分析
- 错题统计和可视化
- 按知识点分析错题分布
- 学习诊断报告
- 数据导出功能

## 🛠️ 安装和部署

### 环境要求
- Python 3.8+
- pip 包管理器

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd ladr
```

2. **安装依赖**
```bash
pip3 install -r requirements.txt
```

3. **配置环境**

创建 `.streamlit/secrets.toml` 文件：
```toml
[supabase]
url = "your-supabase-url"
key = "your-supabase-key"

[oss]
secret_id = "your-cos-secret-id"
secret_key = "your-cos-secret-key"
region = "ap-beijing"
bucket_name = "your-bucket-name"
```

4. **启动应用**
```bash
streamlit run streamlit_app.py
```

### Docker 部署（可选）

如果项目包含 `.devcontainer` 配置，可以使用 Docker 进行部署：

```bash
# 使用开发容器
code . # 在VS Code中打开，选择在容器中重新打开
```

## 📊 数据库设计

### 核心数据表

1. **user** - 用户表
   - id, username, password_hash, created_at

2. **student** - 学生表
   - id, user_id, name, created_at

3. **exam_paper** - 试卷表
   - id, student_id, title, description, created_time

4. **exam_paper_image** - 试卷图片表
   - id, exam_paper_id, image_url, upload_order

5. **question** - 题目表
   - id, exam_paper_id, image_id, student_id, content, is_correct, remark

6. **knowledge_point** - 知识点表
   - id, name

7. **question_knowledge_point** - 题目知识点关联表
   - id, question_id, knowledge_point_id

### 关系设计
- 学生与试卷：一对多
- 试卷与图片：一对多
- 试卷与题目：一对多
- 题目与知识点：多对多
- 题目与图片：多对一

## 🔧 API 接口

### RESTful API 设计

所有API遵循RESTful设计原则，支持标准的CRUD操作：

- `GET /api/{resource}` - 获取资源列表
- `GET /api/{resource}/{id}` - 获取单个资源
- `POST /api/{resource}` - 创建资源
- `PUT /api/{resource}/{id}` - 更新资源
- `DELETE /api/{resource}/{id}` - 删除资源

### 支持的资源
- users - 用户管理
- students - 学生管理
- exam_papers - 试卷管理
- exam_paper_images - 图片管理
- questions - 题目管理
- knowledge_points - 知识点管理
- question_knowledge_points - 关联关系管理

### 特殊接口
- `POST /api/questions/batch` - 批量创建题目

## 🎯 使用指南

### 基本工作流程

1. **登录系统**
   - 使用用户名和密码登录
   - 系统会保持登录状态

2. **选择学生**
   - 在学生选择页面选择要管理的学生
   - 系统会记住当前选择的学生

3. **创建试卷**
   - 在试卷管理页面创建新试卷
   - 填写试卷标题和描述

4. **上传图片**
   - 在试卷图片管理页面上传试卷图片
   - 支持多张图片上传

5. **添加题目**
   - 在试卷详情页面添加题目
   - 可以单个添加或批量导入
   - 标注题目正误状态

6. **分析错题**
   - 在错题分析页面查看统计数据
   - 生成学习诊断报告

### 批量题目导入格式

```json
[
  {
    "content": "题目内容",
    "is_correct": true
  },
  {
    "content": "题目内容",
    "is_correct": false
  }
]
```

## 🔒 安全特性

- 用户密码哈希存储
- 会话状态管理
- API请求验证
- 图片URL签名访问
- 跨域请求保护

## 📈 性能优化

- Streamlit缓存机制（@st.cache_data）
- 数据库连接池
- 图片懒加载
- 分页查询支持
- 异步处理优化

## 🐛 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查 Supabase 配置是否正确
   - 确认网络连接正常

2. **图片上传失败**
   - 检查腾讯云COS配置
   - 确认存储桶权限设置

3. **题目创建失败**
   - 确保必需字段完整（image_id, student_id）
   - 检查数据格式是否正确

### 调试模式

在题目管理页面启用调试模式可以查看详细的错误信息和请求数据。

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 项目Issues: [GitHub Issues](https://github.com/your-repo/ladr/issues)
- 邮箱: your-email@example.com

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户。

---

**注意**: 请确保在生产环境中正确配置所有敏感信息，不要将密钥和配置信息提交到版本控制系统中。
