# store_navigator_be

**Store Navigator Backend - Enhancing Grocery Shopping Experiences through Intelligent Store Navigation and Product Localization**

This repository contains the backend source code for the Store Navigator application, written in Python. The backend handles route generation and product search and localization. The backend does not store any user inputs or user data.

The API is deployed to https://api.storenav.uk/ and can be tested by visiting the routes defined in `app/routes.py` (e.g. https://api.storenav.uk/products will list all available products).

## Available API Endpoints:

### 1. **GET /stores**
- **Description**: Retrieve all available stores.
- **Example**: https://api.storenav.uk/stores

### 2. **GET /stores/<store_id>/shelves**
- **Description**: Retrieve all shelves in a specific store.
- **Parameters**:
  - `store_id` (path): The ID of the store.
- **Example**: https://api.storenav.uk/stores/09a8c436-90bf-41f4-a85d-56daf1d2688e/shelves

### 3. **GET /products**
- **Description**: Retrieve products based on optional search criteria.
- **Query Parameters**:
  - `search` (optional): Search for products by name.
  - `ids` (optional): Comma-separated list of product IDs to retrieve.
- **Example**:
  - List all products: https://api.storenav.uk/products
  - Search by name: https://api.storenav.uk/products?search=milk
  - Retrieve by IDs: https://api.storenav.uk/products?ids=a591e05c-f78e-42a4-b805-487e22e5f138

### 4. **GET /products/bulk-search**
- **Description**: Perform a bulk search for multiple products based on a multi-line query.
- **Query Parameters**:
  - `query` (required): Multi-line string containing product names to search.
- **Example**: https://api.storenav.uk/products/bulk-search?query=milk%0Abread%0Aeggs


### 5. **GET /get-traveling-routes**
- **Description**: Retrieve an optimal route to travel through multiple shelves in the store starting from the entrance. The response is in the form of an ordered list of coordinates (pixels) on the store's map.
- **Query Parameters**:
  - `start` (optional): Starting section ID (default: `section_entrance`).
  - `section_ids` (required): Comma-separated list of section IDs to visit.
- **Example**: https://api.storenav.uk/get-traveling-routes?section_ids=section_1,section_4,section_10

### 6. **GET /get-route**
- **Description**: Retrieve a path between two sections in the store. The response is in the form of an ordered list of coordinates (pixels) on the store's map.
- **Query Parameters**:
  - `start` (required): Starting section ID.
  - `end` (required): Ending section ID.
- **Example**: https://api.storenav.uk/get-route?start=section_1&end=section_12

### 7. **GET /get-grid**
- **Description**: Retrieve the grid representation of the store floor plan with 1s representing obstacles and 0s representing empty spaces.
- **Example**: https://api.storenav.uk/get-grid




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
- You can test the application by opening a browser or API client (e.g., Postman) and visiting the API endpoints described above, replacing the domain name with `http://127.0.0.1:5000/`.

## Notes

The `app/routes.py` file contains all of the API routes in the application. The route generation algorithms can be found in `app/route_generation.py`, while `app/search.py` file contains the functions for searching for products.

## Additional Resources

- [Python Documentation](https://docs.python.org/3/): Official Python documentation.
- [Flask Documentation](https://flask.palletsprojects.com/) or [FastAPI Documentation](https://fastapi.tiangolo.com/): Depending on the backend framework used.
- [Virtualenv Guide](https://virtualenv.pypa.io/en/latest/): Setting up and managing virtual environments.


