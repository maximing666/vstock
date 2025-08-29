## vstock 项目说明（中文）

### 一、项目简介
vstock 是一个基于 Django 4.1 的轻量级 Web 项目，当前包含应用 `vkday`，用于展示按日期（`vdate`）记录的简短文本（`vtext`）列表。后端使用 MySQL 作为数据库，模板采用 Django 原生模板引擎渲染。

### 二、核心需求与功能
- **展示最新记录列表**：
  - 访问路径：`/vkday/`
  - 功能：查询表 `v1` 中的记录，按日期 `vdate` 倒序取前 5 条并展示。

> 当前代码仅包含列表页展示，不含详情页、增删改查接口和后台录入逻辑（可后续扩展）。

### 三、架构与模块设计
- **框架**：Django 4.1
- **数据库**：MySQL 8（字符集建议 `utf8mb4`）
- **主要应用**：`vkday`
  - `models_view.py`：定义 `Onedayk` 模型，映射到表 `v1`
  - `views.py`：定义 `index` 视图，读取最新 5 条记录并渲染模板
  - `templates/vkday/index.html`：列表页模板
  - `urls.py`：路由配置，根路径指向 `index`
- **全局配置**：`vstock/settings.py`、`vstock/urls.py`

### 四、目录结构
```
vstock/
  manage.py
  README.md
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
        db_table = 'v1'
```

- **表名**：`v1`
- **字段**：
  - `vdate`：日期
  - `vtext`：文本（最长 1024）
- **注意**：代码中未显式定义主键字段，Django 默认添加自增 `id` 主键。

### 六、路由与视图
- 全局路由（`vstock/urls.py`）：
  - `path('vkday/', include('vkday.urls'))`
- 应用路由（`vkday/urls.py`）：
  - `'' -> views.index`（命名 `index`）
- 视图（`vkday/views.py`）：
  - `index(request)`：查询 `Onedayk` 最近 5 条记录，渲染 `vkday/index.html`

模板（`vkday/templates/vkday/index.html`）示例输出：
```html
{% if latest_onedayk_list %}
  <ul>
    {% for onedayk in latest_onedayk_list %}
      <li>
        <a href="/vkday/{{ onedayk.id }}/">{{ onedayk.vdate }} : {{ onedayk.vtext }}</a>
      </li>
    {% endfor %}
  </ul>
{% else %}
  <p>No polls are available.</p>
{% endif %}
```

> 提示：模板中包含指向 `"/vkday/{{ id }}/"` 的链接，但当前并未实现详情页路由与视图，点击会 404。可作为后续迭代点。

### 七、运行环境与依赖
- Python 3.10+
- Django 4.1
- MySQL 8
- MySQL Python 驱动：`mysqlclient`

`README.md` 中已有简要提示：
1) MySQL 8；2) 字符集 `utf8mb4`；3) `pip3 install mysqlclient`。

### 八、配置说明（重要）
在 `vstock/settings.py` 中，数据库配置默认为本地 MySQL：
```python
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'HOST': '127.0.0.1',
    'NAME': 'vstock',
    'USER': 'vstocker',
    'PASSWORD': '*** 建议使用环境变量注入 ***',
    'PORT': '3306',
  }
}
```

- 建议将敏感信息改为环境变量读取，避免明文配置：
```python
import os
DATABASES['default']['USER'] = os.getenv('DB_USER', 'root')
DATABASES['default']['PASSWORD'] = os.getenv('DB_PASSWORD', '')
DATABASES['default']['HOST'] = os.getenv('DB_HOST', '127.0.0.1')
DATABASES['default']['NAME'] = os.getenv('DB_NAME', 'vstock')
```

### 九、快速开始
1. 安装依赖
```bash
pip install -U pip
pip install django==4.1 mysqlclient
```
2. 准备数据库
```sql
-- 创建数据库与用户（示例）
CREATE DATABASE vstock CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'vstocker'@'%' IDENTIFIED BY 'your_password_here';
GRANT ALL PRIVILEGES ON vstock.* TO 'vstocker'@'%';
FLUSH PRIVILEGES;
```
3. 迁移（如需使用 Django 管理表结构）
```bash
python manage.py makemigrations
python manage.py migrate
```
> 说明：当前模型绑定已有表名 `v1`，若数据库中已存在 `v1`，可直接使用；若需由 Django 迁移生成，确保迁移文件与表结构一致。

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
- 列表功能增强：分页、搜索、按日期区间筛选。
- 详情页：实现 `vkday/<int:id>/` 路由与详情模板。
- 数据录入：新增创建、编辑、删除接口与表单页，或集成 Django Admin。
- API 化：为列表与详情提供 REST API（如接入 Django REST Framework）。
- 认证与权限：为写操作添加登录、权限控制。
- 部署与安全：
  - 生产环境关闭 `DEBUG`，设置精确 `ALLOWED_HOSTS`
  - 安全管理 `SECRET_KEY` 和数据库凭据（环境变量/密钥管理）
  - 静态与媒体文件存储方案（Nginx/对象存储/CDN）

### 十二、常见问题
- 页面无数据：确认表 `v1` 已有记录，或调整视图查询逻辑。
- 数据库连接失败：检查 `mysqlclient` 是否安装、MySQL 是否允许远程连接、凭据是否正确、字符集是否为 `utf8mb4`。
- 点击列表链接 404：当前未实现详情页，属预期行为。

### 十三、变更记录
- 初始版本：提供列表页、MySQL 配置、基础项目结构。

—— 完 ——



