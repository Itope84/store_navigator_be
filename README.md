# store_navigator_be

**Store Navigator Backend - Enhancing Grocery Shopping Experiences through Intelligent Store Navigation and Product Localization**

This repository contains the backend source code for the Store Navigator application, written in Python. The backend handles route generation and product search and localization. The backend does not store any user inputs or user data.

## How to Run Locally

### Prerequisites

Before running the application, ensure you have the following installed:
- Python 3.8 or later: [Python Installation Guide](https://www.python.org/downloads/)
- pip: Python's package installer is typically included with Python installation.

Additionally, consider using a virtual environment to isolate dependencies:
- [Virtualenv Documentation](https://virtualenv.pypa.io/en/latest/)

### Steps to Run the App

1. **Clone the Repository**

```bash
git clone https://github.com/Itope84/store_navigator_be.git
cd store_navigator_be
```

2. **Set Up a Virtual Environment**
- Create a virtual environment:
  ```
  python -m venv venv
  ```
- Activate the virtual environment:
  - On Windows:
    ```
    venv\Scripts\activate
    ```
  - On macOS/Linux:
    ```
    source venv/bin/activate
    ```

3. **Install Dependencies**
- Install all required dependencies:
  ```
  pip install -r requirements.txt
  ```

#### Setting Up PostgreSQL

The application uses a PostgreSQL database to store the products and shelf information required for localization and navigation within the store.

4. **Install PostgreSQL**
   - Follow the official guide to install PostgreSQL for your operating system:
     - [PostgreSQL Installation Guide](https://www.postgresql.org/download/)

5. **Create a New Database**
   - Open the PostgreSQL interactive terminal (`psql`) or use a GUI tool like pgAdmin.
   - Run the following command to create a new database:
     ```sql
     CREATE DATABASE store_navigator;
     ```

6. **Provide the `DATABASE_URL`**
   - Construct the `DATABASE_URL` using the following format:
     ```
     postgres://<username>:<password>@<host>:<port>/<database_name>
     ```
     For example:
     ```
     postgres://store_user:secure_password@localhost:5432/store_navigator
     ```

   - Create a `.env` file in the cloned repository root folder and add the `DATABASE_URL` to the `.env` file:
     ```
     DATABASE_URL=postgres://store_user:secure_password@localhost:5432/store_navigator
     ```

#### Running the Application

7. **Set up the database tables and seeds**

- Run the `db_setup.py` script to create the database tables:
    ```
    python db_setup.py
    ```

- Run the `seed.py` script to populate the tables with seed data extracted from the Tesco UK groceries dataset:
    ```
    python seed.py
    ```


8. **Run the Application**
- Start the backend application:
  ```
  python wsgi.py
  ```

6. **Test the Application**
- Open a browser or API client (e.g., Postman) and view all products by visiting `http://127.0.0.1:5000/products`.

- Get the route between two sections by visiting `http://127.0.0.1:5000/get-route?start=section_1&end=section_12`

- Get the route to travel through multiple shelves from the entrance by visiting `http://127.0.0.1:5000/get-traveling-routes?section_ids=section_1,section_4,section_10,section_13,section_21`

## Notes

The `app/routes.py` file contains all of the API routes in the application. The route generation algorithms can be found in `app/route_generation.py`, while `app/search.py` file contains the functions for searching for products.

## Additional Resources

- [Python Documentation](https://docs.python.org/3/): Official Python documentation.
- [Flask Documentation](https://flask.palletsprojects.com/) or [FastAPI Documentation](https://fastapi.tiangolo.com/): Depending on the backend framework used.
- [Virtualenv Guide](https://virtualenv.pypa.io/en/latest/): Setting up and managing virtual environments.


