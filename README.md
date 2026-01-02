# 🎓 Django Student Management System (SMS)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-4.2%2B-092E20?style=for-the-badge&logo=django)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

> **A centralized administrative platform for educational institutions to streamline student data, attendance, and academic performance.**



## 📋 Overview

The **Student Management System** is a comprehensive web application designed to digitize the administrative operations of a school or college. It replaces manual paperwork with a secure, digital database, allowing administrators to track student lifecycles from enrollment to graduation.

This project demonstrates skills in **relational database modeling**, **data visualization** (dashboards), and **CRUD operations** within a complex Django environment.

---

## 🏛️ Architecture: The Data Hierarchy

The system organizes data into three logical tiers to ensure data integrity and easy retrieval.

| Tier | Component | Description | Relationships |
| :--- | :--- | :--- | :--- |
| **Tier 1** | **Core Entities** | The people in the system. | `Students`, `Teachers`, `Staff` |
| **Tier 2** | **Academic Structure** | The framework of the institution. | `Courses`, `Departments`, `Classes/Sections` |
| **Tier 3** | **Transactional Data** | Daily operational records. | `Attendance Logs`, `Exam Results`, `Fee Payments` |

> **Why this matters:** This normalized structure prevents data redundancy and ensures that if a Student is deleted, their associated records (like grades) are handled securely via database cascading rules.

---

## ✨ Key Features

### 👨‍🎓 Student Module
* **Digital Profiles:** Complete records including bio-data, contact info, and guardian details.
* **Enrollment History:** Track current class, section, and roll number.
* **Document Locker:** Upload and store digital copies of certificates/ID proofs.

### 📚 Academic Module
* **Course Management:** Add subjects, assign teachers, and manage syllabi.
* **Attendance Tracking:** Daily attendance marking with monthly summary reports.
* **Result Processing:** Auto-calculate GPAs/Percentages based on exam scores.

### 📊 Administrative Dashboard
* **Live Stats:** View total student count, teacher count, and daily attendance at a glance.
* **Fee Management:** Track paid/unpaid fees and generate invoices.
* **Search:** Instant lookup for any student record by Roll Number or Name.

---

## 🛠️ Tech Stack

| Domain | Technologies Used |
| :--- | :--- |
| **Backend** | Python 3.8+, Django 4.2+ |
| **Frontend** | HTML5, CSS3 (Bootstrap 5), Chart.js (for stats) |
| **Database** | SQLite (Dev) / PostgreSQL (Production) |
| **Export** | ReportLab (PDF Generation for Results) |

---

## 🚀 Quick Start Guide

### Prerequisites
* Python 3.8+
* pip

### Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/your-username/student-management-system.git](https://github.com/your-username/student-management-system.git)
    cd student-management-system
    ```

2.  **Set up Virtual Environment**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create Admin User**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run Server**
    ```bash
    python manage.py runserver
    ```
    Visit `http://localhost:8000`

---


🎮 Usage Guide
1. Enrolling a New Student
Login as Admin.

Go to Students > Add New.

Fill in personal details, assign a Class/Section, and upload a photo.

Save to generate a unique Registration ID.

2. Marking Attendance
Navigate to Academics > Attendance.

Select the Class and Date.

Mark students as Present/Absent.

The system automatically updates the attendance percentage.

3. Generating Results
Go to Results > Add Marks.

Enter marks for specific subjects.

Click "Generate Report Card" to view the calculated GPA/Percentage.

🛡️ Security & Best Practices
Data Privacy: Sensitive student data is protected behind login decorators.

Role-Based Views: Teachers can only mark attendance; only Admins can delete student records.

Input Validation: Prevents invalid data entry (e.g., negative marks or future dates for birth).

📞 Contact & Author
Arpit Bhojani - Python Developer

📧 Email: bhojaniarpit1432@gmail.com

📱 Phone: +91 7383181094

<div align="center"> <sub>Built with ❤️ and Django.</sub> </div>

## 📂 Project Structure

<details>
<summary>Click to expand file tree</summary>

```text
sms_project/
├── students/            # Student Profiles & Enrollment
│   ├── models.py
│   ├── views.py
│   └── templates/
├── academics/           # Courses, Attendance, Results
│   ├── models.py
│   └── views.py
├── finance/             # Fee Management (Optional)
│   ├── models.py
│   └── views.py
├── core/                # Dashboard & Authentication
│   ├── views.py
│   └── templates/
├── manage.py
└── requirements.txt
</details>
