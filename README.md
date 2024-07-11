# # GenAI Upraised Backend Using Django

## Overview

This is a Django application designed to serve the result using some defined endpoints.



## Endpoints

### 1. Contract Summarization

**Endpoint:** `contract/summarization/`

**Payload:**
```json
{
    "contract_pdf_filename": "example.jpg",
    "contract_pdf":"JVBERi0xLjQNJeLjz9M..."
}
```

### 2. Contract Authoring

**Endpoint:** `contract/authoring/`

**Payload:**
```json
{
    "contract_pdf_filename": "example.jpg",
    "contract_pdf":"JVBERi0xLjQNJeLjz9M..."
}
```

### 3. Contract Spend Analytics

**Endpoint:** `contract/spend-analytics/`

**Payload:**
```json
{
    "contract_pdf_filename": "example.jpg",
    "contract_pdf":"JVBERi0xLjQNJeLjz9M..."
}
```

### 4. Contract Comparison

**Endpoint:** `contract/comparison/`

**Payload:**
```json
{
    "contract_pdf":"JVBERi0xLjQNJeLjz9M...",
    "master_contract_pdf":"JVBERi0xLjQNJeLjz9M...",
}
```

---

Feel free to replace the example payloads with your actual payload structures.
## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.10.12 installed on your machine
- Django 5.0.6
- Virtualenv (optional but recommended)
- Docker installed (if you plan to use Docker)
- Git installed (optional for version control)

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/Jobstop-Solutions/GenAI
    cd upraised_backend
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    ## Creational Virtual Environment

    Create a new Python virtual environment for your Django app:

    ### On Windows:

    ```sh
    python -m venv venv
    ```

    ### On macOS and Linux:

    ```sh
    python3 -m venv venv
    ```

    This will create a new directory named `venv` that contains the virtual environment.

    ## Activate the Virtual Environment

    Activate the virtual environment to start using it:

    ### On Windows (cmd):

    ```sh
    venv\Scripts\activate
    ```

    ### On Windows (PowerShell):

    ```sh
    venv\Scripts\Activate.ps1
    ```

    ### On macOS and Linux:

    ```sh
    source venv/bin/activate
    ```


3. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    ```sh
    python manage.py migrate
    ```

5. **Create a superuser (for accessing the admin interface):**

    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

## Configuration

### Environment Variables

Create a `.env` file in the root directory and add the following environment variables:

```env
SECRET_KEY=your_secret_key
DEBUG=True
# Add any other environment-specific variables here
```

## Usage

- Access the application at `http://127.0.0.1:8000/`
- Access the admin interface at `http://127.0.0.1:8000/admin/` using the superuser credentials



## License

This project is licensed under the [Apache License](LICENSE).

## Acknowledgements

- [Django Documentation](https://docs.djangoproject.com/)

---

Feel free to customize this template according to the specific needs and structure of your Django application.
