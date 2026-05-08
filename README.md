# GP Radar: Patient-to-GP Ratio Analysis System

![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Overview

GP Radar is a comprehensive Django web application designed to provide actionable insights into GP practice capacity and patient demographics across Scotland. The system analyzes patient-to-GP ratios to help healthcare administrators, policymakers, and researchers understand healthcare resource distribution and identify areas requiring attention. It is deployed on Render on the following link: https://test-deployment-gqhq.onrender.com/.

## 🎯 Key Features

- **Real-time Analytics**: Dynamic calculation and visualization of patient-to-GP ratios
- **Interactive Dashboard**: User-friendly interface for exploring healthcare data
- **Comprehensive Reporting**: Detailed reports on GP practice capacity and demographics
- **Data Visualization**: Charts and graphs for better data interpretation
- **Responsive Design**: Accessible across desktop and mobile devices

## 🏗️ Technical Architecture

- **Backend**: Django 4.2+ with Python 3.8+
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Database**: MySQL/PostgreSQL (production), SQLite (development)
- **Mapping**: Leaflet.js with OpenStreetMap
- **Charts**: Chart.js
- **UI Framework**: Bootstrap 5.3
- **Icons**: Font Awesome 6.4
- **Data Processing**: Pandas for data analysis and manipulation
- **Visualization**: Chart.js for interactive charts

## System Architecture

### Backend Components
- Django Models: GPPractices, GPPractitioners, GPDetails, GPPopulations
- View Controllers: Filtering, pagination, and data processing
- Error Handling: Comprehensive exception management
- Security: Input validation and sanitisation

### Database Design
- Normalised schema for data integrity
- Foreign key relationships for data consistency
- Optimised indexing for performance
- Migration system for schema evolution

## 👥 Development Team

| Role | Team Members |
|------|--------------|
| **Team Leaders** | Raoul Amisial, Faizan Khan |
| **Data team** | Raoul Amisial, Oluwaniyi Toyinbo |
| **Frontend team** | Thomas McGuigan, Enoch Agbledzorwu |
| **Backend team** | Chia Chen Wu, Enoch Agbledzorwu, Faizan Khan |
| **Quality team** | Faizan Khan |

## 📊 Data Sources

This application utilizes official healthcare data from Public Health Scotland:

### Primary Datasets

| Dataset | Description | Location |
|---------|-------------|----------|
| **GP Practices and List Sizes** | Practice contact details and patient list sizes (January 2026) | `/data/gp-practices-list-sizes.csv` |
| **GP Details** | General practitioner contact information (January 2026) | `/data/gp-details.csv` |
| **GP Practice Populations** | Demographic breakdown by practice (January 2026) | `/data/gp-practice-populations.csv` |

### Data Source Links

- [GP Practices and List Sizes January 2026](https://www.opendata.nhs.scot/dataset/gp-practice-contact-details-and-list-sizes/resource/ceddbf27-0686-4f4b-b9a2-0090d28c3864)
- [GP Details January 2026](https://www.opendata.nhs.scot/dataset/general-practitioner-contact-details/resource/abbed17f-c63b-4180-b978-c03ed3ee0458)
- [GP Practice Populations January 2026](https://www.opendata.nhs.scot/dataset/gp-practice-populations/resource/c45f9c1c-4dd9-4ebe-b65f-72f1b884ee2c)

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/KanoWuTW/CS551Q-Alpha_Assessment2.git
   cd CS551Q-Alpha_Assessment2
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   GP Radar supports two database options: **SQLite** (default, no setup required) and **MySQL** (recommend for full features including geocoding).

   #### Option 1 - SQLite (quick start)
   ```bash
   cd GP_Radar
   python manage.py migrate
   python manage.py import_data
   ```

   #### Option 2 - MySQL

   **Step 1 - Install MySQL Server**
   Download and install from `https://dev.mysql.com/downloads/mysql/`. Keep the username as `root`and set a password you will remember. MySQL     
   Workbench can be installed alongside it.

   **Step 2 - Configure your environment**
   Rename the variables in `.env` to match your database information

   **Step 3 - Create the database**
   ```bash
   mysql -u root -p
   ```

   Then inside MySQL:
   ```sql
   CREATE DATABASE gp_radar CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   EXIT;
   ```

   **Step 4 - Run migrations and load data**
   ```
   cd GP_Radar
   python manage.py makemigrations catalog
   python manage.py migrate
   python manage.py import_data
   ```

   *NOTE:* As per Nominatim policy, the data loader enforces a 1-second delay per practice to comply with geocoding rate limits, so importing all   
   880 GP Practices takes approximately 15 minutes to complete. Messages saying "Could not find coordinates for ..." are expected and indicate
   practices where the address could not be identified, not failures in the import itself.

   **Step 5 - Verify the data loaded correctly**
   ```
   bash
   python manage.py shell
   ```

   ```
   python
   from catalog.models import GPPractices, GPPractitioners, GPDetails, GPPopulations
   print("Practices:", GPPractices.objects.count())
   print("Practitioners:", GPPractitioners.objects.count())
   print("Details:", GPDetails.objects.count())
   print("Populations:", GPPopulations.objects.count())
   exit()
   ```

   Expected output:
   ```
   Practices: 880
   Practitioners: 5367
   Details: 5632
   Populations: 1760
   ```


5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:8000`

## 📁 Project Structure

```
GP_Radar/
├── GP_Radar/              # Main Django project configuration
│   ├── __init__.py
│   ├── settings.py        # Django settings
│   ├── urls.py           # Main URL routing
│   ├── wsgi.py           # WSGI configuration
│   └── asgi.py           # ASGI configuration
├── apps/                 # Django applications
│   ├── catalog/           # Catalog management app
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── management/
│   │   │   └── commands/
│   │   └── migrations/
│   ├── core/              # Core functionality app
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── templates/
│   │   │   └── core/
│   │   │       └── base.html
│   │   ├── static/
│   │   │   └── core/
│   │   │       └── custom.css
│   │   └── migrations/
│   ├── table/             # Table/dashboard app
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── templates/
│   │   │   └── table/
│   │   │       └── dashboard.html
│   │   ├── static/
│   │   │   └── table/
│   │   │       └── dashboard.js
│   │   └── migrations/
│   └── map/               # Map functionality app
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       └── migrations/
├── data/                 # Raw and processed datasets
│   ├── GPDetails.csv
│   ├── GPPopulations.csv
│   └── GPPractices.csv
├── tests/                # Test files
├── static/               # Global static files
├── templates/            # Global templates
├── .env                  # Environment variables
├── .gitignore           # Git ignore file
├── db.sqlite3           # SQLite database (development)
├── manage.py            # Django management script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```


## 📈 Usage

1. **Dashboard**: View overall statistics and trends
2. **Practice Search**: Find specific GP practices and their details
3. **Ratio Analysis**: Compare patient-to-GP ratios across regions
4. **Reports**: Generate and export detailed reports
5. **Data Management**: Update and maintain dataset integrity

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## 🙏 Acknowledgments

- Public Health Scotland for providing the healthcare datasets
- The development team for their dedication and expertise
- University of Aberdeen for supporting this enterprise software development project

