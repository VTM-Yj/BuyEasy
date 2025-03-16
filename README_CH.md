# BuyEasy 项目

BuyEasy 是一个基于 Django 的电商网站项目，提供用户注册、登录、商品浏览、购物车、订单管理和 Stripe 支付等功能。

---

## 快速开始

### 1. 克隆仓库
在终端中运行以下命令克隆 GitLab 上的仓库：
```bash
git clone https://stgit.dcs.gla.ac.uk/programming-and-systems-development-m/2024/lb03-14/it-project.git
cd BuyEasy

2. 创建并激活虚拟环境
建议使用虚拟环境隔离项目依赖。
windows:
python -m venv .venv
.\.venv\Scripts\activate
Linux & macOS
python3 -m venv .venv
source .venv/bin/activate

3. 安装项目依赖
pip freeze > requirements.txt
然后安装依赖:
pip install -r requirements.txt

4.根目录下创建.env文件
复制下面代码到.env文件中
STRIPE_PUBLIC_KEY=pk_test_51R0pkv4M4g9KMkeSQPgKegr7cxhCej7jEqoP5zS3qytxEdePPHvj0nCuFgP6l5ZuNaKsescmhcx1ZlGjE6eCKT5S00yhDSq0jk
STRIPE_SECRET_KEY=sk_test_51R0pkv4M4g9KMkeS0jHu1WsNRhfOMPno4lDeB39kZLSGkUDEQMGLE5T8ll7RMLpLIzUjVGtkEbF9nW8PnvKO6v2V00wDHGLAX2

DATABASE_NAME=buyeasy
DATABASE_USER=root
DATABASE_PASSWORD=123456
DATABASE_HOST=127.0.0.1
DATABASE_PORT=3306

5. 数据库迁移(数据库使用MySql，可以下载Naicat进行连接):
确保 MySQL 数据库已启动且配置正确，然后运行数据库迁移命令：
python manage.py makemigrations
python manage.py migrate

6. 静态文件:
开发环境下通常不需要此步骤。若部署生产环境，请运行
python manage.py collectstatic

7. 运行开发服务器
启动 Django 开发服务器:
python manage.py runserver

在浏览器中访问 http://127.0.0.1:8000 检查项目是否正常运行。