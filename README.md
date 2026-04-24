# GP Radar: Patient-to-GP Ratio Analysis System

![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Overview

GP Radar is a comprehensive Django web application designed to provide actionable insights into GP practice capacity and patient demographics across Scotland. The system analyzes patient-to-GP ratios to help healthcare administrators, policymakers, and researchers understand healthcare resource distribution and identify areas requiring attention.

## 🎯 Key Features

- **Real-time Analytics**: Dynamic calculation and visualization of patient-to-GP ratios
- **Interactive Dashboard**: User-friendly interface for exploring healthcare data
- **Comprehensive Reporting**: Detailed reports on GP practice capacity and demographics
- **Data Visualization**: Charts and graphs for better data interpretation
- **Responsive Design**: Accessible across desktop and mobile devices

## 🏗️ Technical Architecture

- **Backend**: Django 4.2+ with Python 3.8+
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: PostgreSQL (development: SQLite)
- **Data Processing**: Pandas for data analysis and manipulation
- **Visualization**: Chart.js for interactive charts

## 👥 Development Team

| Role | Team Members |
|------|--------------|
| **Team Leaders** | Raoul, Faizan Khan |
| **Data Lead** | Raoul, David |
| **Frontend Lead** | Thomas |
| **Backend Lead** | Chia Chen, Enoch, Faizan Khan |
| **Quality Lead** | Faizan Khan |

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
   ```bash
   python manage.py migrate
   ```

5. **Load initial data**
   ```bash
   python manage.py import_data --data-path data --clear
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   Open your browser and navigate to `http://localhost:8000`

## 📁 Project Structure

```
GP-Radar/
├── gp_radar/              # Main Django application
│   ├── settings/          # Application settings
│   ├── urls.py           # URLs routing
│   └── views.py          # View logic
├── data/                 # Raw and processed datasets
├── static/               # CSS, JavaScript, images
├── templates/            # HTML templates
├── requirements.txt      # Python dependencies
├── manage.py            # Django management script
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
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

