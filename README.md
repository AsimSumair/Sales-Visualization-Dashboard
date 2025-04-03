Data Visualization Dashboard with Django and D3.js

🎯 Project Overview
This project is a Data Visualization Dashboard built using Django for the backend and JavaScript/Bootstrap for the frontend. It processes data from a given JSON file, stores it in a database (SQLite3), and displays interactive visualizations using D3.js.

The dashboard provides valuable insights by analyzing variables such as intensity, likelihood, relevance, year, country, topics, and region, with various filters to refine the displayed information. The API serves the filtered data dynamically, making it easy to visualize complex data effectively.

Key Features
✅ Data Ingestion:

Import data from a provided JSON file and store it in an SQLite3 database.

Automatically map data fields to corresponding models.

✅ API Integration:

Django REST framework (DRF) API that retrieves and filters data dynamically from the database.

API endpoint to apply multiple filters and return JSON responses.

✅ Interactive Dashboard:

Visualize data through interactive graphs and charts created using D3.js.

Provide valuable insights using dynamic data visualizations.

Customize data views using multiple filters.

✅ Filters & Controls:

End Year

Topics

Sector

Region

PEST

Source

Country

Any additional filters that enhance user experience and data exploration.

✅ Admin Panel:

Admin credentials:
Username: admin  
Password: admin  


Secure Authentication:

Access the admin panel for managing and monitoring the data.

🛠️ Tech Stack
🎯 Backend:
Django Framework – Manages APIs and handles data processing.

Django REST Framework (DRF) – Exposes data endpoints and handles filtering.

SQLite3 – Database for storing data extracted from the JSON file.

🎨 Frontend:
HTML5, CSS3, Bootstrap – Builds an interactive and responsive UI.

JavaScript – Adds functionality and interactivity to the dashboard.

D3.js – Creates advanced, dynamic visualizations.


📊 Visualizations
The dashboard includes interactive and engaging visualizations to analyze:

Intensity, Likelihood, and Relevance: Displayed using bar charts, line graphs, or heatmaps.

Year-wise Analysis: Showing trends and patterns over different years.

Regional Breakdown: Distribution of data across various regions.

Country-wise Insights: Comparative analysis for different countries.

PEST Analysis: Representation of data based on political, economic, social, and technological factors.

Topic & Sector Analysis: Understanding data relevance across multiple sectors and topics.

 Project Workflow
🔥 Step 1: Setup and Installation
Clone the repository:


Set up a virtual environment:

python -m venv venv
venv\Scripts\activate

Install required dependencies:
pip install -r requirements.txt


run the project:
python manage.py runserver

Access the application at:
http://127.0.0.1:8000/
