# 🥗 Nutrition Calculator

A full-stack web application built with Django for tracking daily nutrition, managing a personal food library, and calculating the nutritional breakdown of custom meals.

![Django](https://img.shields.io/badge/Django-4.2-092E20?style=flat&logo=django)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Features

- **User Authentication**: Secure registration, login, and logout system.
- **Food Library Management (CRUD)**: Add, view, edit, and delete food items with detailed nutritional values (calories, protein, carbs, fat, fiber, sugar) per 100g.
- **CSV Data Import**: Easily import large food datasets (e.g., from Kaggle) using the built-in CSV uploader.
- **Meal Nutrition Calculator**: Select foods, input weight in grams, and instantly calculate total and per-ingredient nutritional values.
- **Calculation History**: Logged-in users can save and review past meal calculations.
- **Responsive Web Interface**: Clean and user-friendly interface that works on desktop and mobile.

## 🛠️ Technology Stack

| Component          | Technology               |
|--------------------|--------------------------|
| **Backend**        | Django 4.2               |
| **Frontend**       | HTML, CSS, JavaScript    |
| **Database**       | SQLite3                  |
| **Data Processing**| Pandas                   |
| **Language**       | Python 3.9+              |

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Oliviazkr/nutrition_calculator.git
    cd nutrition_calculator
    ```

2.  **Create and activate a virtual environment**
    *   **Windows**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   **macOS / Linux**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If you don't have a `requirements.txt` file yet, run `pip install django pandas`)*

4.  **Set up the database**
    ```bash
    python manage.py makemigrations calculator
    python manage.py migrate
    ```

5.  **Run the development server**
    ```bash
    python manage.py runserver
    ```

6.  **Open the application**
    Navigate to `http://127.0.0.1:8000/` in your web browser.

## 📖 How to Use

1.  **Register / Login**: Create a new account or use the demo account (`demo` / `demo123456`).
2.  **Build Your Food Library**:
    *   Go to **"Food Library"** from the navigation bar.
    *   Click **"Add Food"** to enter a new item manually, or use **"Import CSV"** to upload a spreadsheet of food data.
3.  **Calculate a Meal**:
    *   Go to the **"Calculator"** homepage.
    *   Use the left panel to search and select foods.
    *   Adjust the weight (in grams) for each selected item in the right panel.
    *   Click **"Calculate Nutrition"** to see the detailed macronutrient breakdown.
4.  **Review Past Meals**: Visit the **"History"** page to see all your previously calculated meals.

## 📂 Project Structure

```
nutrition_calculator/
├── calculator/                 # Main Django application
│   ├── management/commands/    # Custom management commands (e.g., import_data)
│   ├── migrations/             # Database migration files
│   ├── templates/calculator/   # HTML templates
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                # Form classes for user input
│   ├── models.py               # Database models (FoodItem, CalculationHistory)
│   ├── urls.py                 # Application URL routing
│   └── views.py                # Core logic and request handling
├── nutrition_calculator/       # Project configuration folder
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py             # Django project settings
│   ├── urls.py                 # Root URL configuration
│   └── wsgi.py
├── static/                     # Static files (CSS, JS, images)
├── db.sqlite3                  # SQLite database file
├── manage.py                   # Django's command-line utility
└── requirements.txt            # Python dependencies
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- Data is from https://www.kaggle.com/datasets/utsavdey1410/food-nutrition-dataset
- Built as a practical learning project for web development with Django.
