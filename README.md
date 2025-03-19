# BuyEasy Project

BuyEasy is an e-commerce website project based on Django, providing functions such as user registration, login, product browsing, shopping cart, order management and Stripe payment.

---

## Quick Start

### 1. Clone the repository
Run the following command in the terminal to clone the repository on GitLab:
```bash
git clone https://stgit.dcs.gla.ac.uk/programming-and-systems-development-m/2024/lb03-14/it-project.git
cd BuyEasy

2. Create and activate a virtual environment
It is recommended to use a virtual environment to isolate project dependencies.
windows:
python -m venv .venv
.\.venv\Scripts\activate
Linux & macOS
python3 -m venv .venv
source .venv/bin/activate

3. Install project dependencies
pip freeze > requirements.txt
Then install dependencies:
pip install -r requirements.txt

4. Create a .env file in the root directory
Copy the following code into the .env file
STRIPE_PUBLIC_KEY=pk_test_51R0pkv4M4g9KMkeSQPgKegr7cxhCej7jEqoP5zS3qytxEdePPHvj0nCuFgP6l5ZuNaKsescmhcx1ZlGjE6eCKT5S00yhDSq0jk
STRIPE_SECRET_KEY=sk_test_51R0pk v4M4g9KMkeS0jHu1WsNRhfOMPno4lDeB39kZLSGkUDEQMGLE5T8ll7RMLpLIzUjVGtkEbF9nW8PnvKO6v2V00wDHGLAX2

DATABASE_NAME=buyeasy
DATABASE_USER=root
DATABASE_PASSWORD=123456
DATABASE_HOST=127.0.0.1
DATABASE_PORT=3306

5. Database migration (the database uses MySql, you can download Naicat to connect):
Make sure the MySQL database is started and configured correctly, then run the database migration command:
python manage.py makemigrations
python manage.py migrate

6. Static files:
This step is usually not required in the development environment. If deploying a production environment, please run
python manage.py collectstatic

7. Run the development server
Start the Django development server:
python manage.py runserver

Visit http://127.0.0.1:8000 in the browser to check whether the project is running normally.