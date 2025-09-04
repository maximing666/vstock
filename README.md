## vstock 项目说明（中文）

### 一、项目简介
vstock 是一个基于 Django 4.1 的轻量级 Web 项目，当前包含应用 `vkday`，用于展示按日期（`vdate`）记录的简短文本（`vtext`）列表。后端使用 MySQL 作为数据库，模板采用 Django 原生模板引擎渲染。

### 二、核心功能
- **展示最新记录列表**：
  - 访问路径：`/vkday/`
  - 功能：查询表 `viewrecommend` 中的记录，按 `vdate` 倒序取前 3 条展示。

> 当前代码仅包含列表页展示，不含详情页与增删改查接口（可后续扩展）。

### 三、架构与模块
- **框架**：Django 4.1
- **数据库**：MySQL 8（字符集建议 `utf8mb4`）
- **主要应用**：`vkday`
  - `models_view.py`：定义 `Onedayk` 模型，映射到表 `viewrecommend`
  - `views.py`：定义 `index` 视图，读取最新 3 条记录并渲染模板
  - `templates/vkday/index.html`：列表页模板
  - `urls.py`：应用路由配置
- **全局配置**：`vstock/settings.py`、`vstock/urls.py`

### 四、目录结构
```
vstock/
  manage.py
  readme1.md
  vkday/
    admin.py
    apps.py
    migrations/
    models.py
    models_view.py
    templates/vkday/index.html
    urls.py
    views.py
  vstock/
    settings.py
    urls.py
    wsgi.py / asgi.py
```

### 五、数据模型
模型定义在 `vkday/models_view.py`：
```python
class Onedayk(models.Model):
    vdate = models.DateField()
    vtext = models.CharField(max_length=1024)
    class Meta:
        db_table = 'view_dayk_one'
```

- **表名**：`viewrecommend`
- **字段**：
  - `vdate`：日期
  - `vtext`：文本（最长 1024）
- **说明**：未显式定义主键时，Django 默认添加自增 `id` 主键。

### 六、路由与视图
- 全局路由（`vstock/urls.py`）：
  - `path('vkday/', include('vkday.urls'))`
- 应用路由（`vkday/urls.py`）：
  - `'' -> views.index`（命名 `index`）
- 视图（`vkday/views.py`）：
  - `index(request)`：查询 `Onedayk` 最近 3 条记录，渲染 `vkday/index.html`

模板（`vkday/templates/vkday/index.html`）输出为表格：
```html
{% if latest_onedayk_list %}
    <table border="1">
    {% for onedayk in latest_onedayk_list %}
        <tr>
            <td width="25%" valign="top" style="font-size: 30pt">{{ onedayk.vdate | date:'Y-m-d' }}</td>
            <td>{{ onedayk.vtext | safe }}</td>
        </tr>
    {% endfor %}
    </table>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```

### 七、运行环境与依赖
- Python 3.10+
- Django 4.1
- MySQL 8
- MySQL Python 驱动：使用 `PyMySQL`（非 `mysqlclient`）

依赖文件：`requirements.txt`
```
PyMySQL
cryptography
```

项目已在 `vstock/__init__.py` 中启用了：
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### 八、配置说明（重要）
当前 `vstock/settings.py` 的数据库配置示例：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '120.46.46.142',
        'NAME': 'vstock',
        'USER': 'root',
        'PASSWORD': '...省略...',
        'PORT': '13306',
    }
}
```

- 建议将敏感信息改为环境变量读取，避免明文配置：
```python
import os
DATABASES['default']['USER'] = os.getenv('DB_USER', DATABASES['default']['USER'])
DATABASES['default']['PASSWORD'] = os.getenv('DB_PASSWORD', DATABASES['default']['PASSWORD'])
DATABASES['default']['HOST'] = os.getenv('DB_HOST', DATABASES['default']['HOST'])
DATABASES['default']['PORT'] = os.getenv('DB_PORT', DATABASES['default']['PORT'])
DATABASES['default']['NAME'] = os.getenv('DB_NAME', DATABASES['default']['NAME'])
```

- 其他关键设置：
  - `DEBUG = False`（仓库当前已关闭调试）
  - `ALLOWED_HOSTS = ['*']`（生产建议改为精确域名列表）

### 九、快速开始
1. 安装依赖
```bash
pip install -U pip
pip install -r requirements.txt
```
2. 准备数据库（示例）
```sql
CREATE DATABASE vstock CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- 如需独立账号，自行创建并授权
```
3. 迁移（如需使用 Django 管理表结构）
```bash
python manage.py makemigrations
python manage.py migrate
```
> 说明：当前模型绑定到已有表 `view_dayk_one`，若数据库中已存在该表可直接使用；若需由迁移生成，请确保迁移文件与表结构一致。

4. 启动开发服务器
```bash
python manage.py runserver 0.0.0.0:8000
```
访问 `http://localhost:8000/vkday/` 查看列表页。

### 十、开发约定与命名
- 函数命名：驼峰格式（示例：`getLatestOnedaykList`）。
- 代码风格：遵循 Django 与 PEP8 基本约定，模板采用 Django 语法。
- 国际化：当前 `LANGUAGE_CODE='en-us'`，`TIME_ZONE='UTC'`，视需要调整。

### 十一、扩展与规划建议
- 列表增强：分页、搜索、按日期区间筛选。
- 详情页：实现 `vkday/<int:id>/` 路由与详情模板。
- 数据录入：新增创建、编辑、删除接口与表单页，或集成 Django Admin。
- API 化：为列表与详情提供 REST API（如接入 DRF）。
- 部署与安全：
  - 生产关闭 `DEBUG`，精确配置 `ALLOWED_HOSTS`
  - 使用环境变量/密管服务管理 `SECRET_KEY` 与数据库凭据
  - 规划静态与媒体文件存储（Nginx/对象存储/CDN）

### 十二、常见问题
- 页面无数据：确认表 `viewrecommend` 已有记录，或检查视图查询逻辑是否限制为 3 条。
- 数据库连接失败：确认已安装 `PyMySQL`，网络连通与凭据正确，字符集为 `utf8mb4`。

### 十三、变更记录
- 当前版本：改用 `PyMySQL`；模型表名为 `viewrecommend`；列表展示条数为 3；`DEBUG=False`。

—— 完 ——