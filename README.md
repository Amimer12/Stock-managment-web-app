## Inventory Management System (Gestion de Stock)

This is a **Django-based Inventory Management System** with a custom **Jazzmin-admin interface**. The application helps manage stock levels and account-specific data with an integrated feature to link and interact with **Excel sheet files**.

## 🔧 Features

- User-friendly Django Admin Panel customized with **Jazzmin**.
- Manage stock items, accounts, and transactions.
- Export and link data to **Excel sheets** (.xlsx) for a selected account.
- Clean and modern UI for managing inventory efficiently.
- **Deployed with Render** (for web hosting) and **Neon** (for PostgreSQL database).
## 📁 Project Structure

- `project_GS/` — Main Django project folder.
- `virtual_env/` — Python virtual environment.

## ✅ Requirements

Make sure you have **Python 3.8+** installed.

Install the required Python packages:

```bash
pip install django
pip install xlsxwriter
pip install pandas openpyxl
```
## 🚀 Getting Started Locally
Create and activate a virtual environment:

```bash
python -m venv virtual_env
virtual_env/Scripts/activate  # On Windows
# source virtual_env/bin/activate  # On macOS/Linux
```
- Install dependencies:

```bash
pip install django
pip install xlsxwriter
pip install pandas openpyxl
```
Navigate to the Django project directory:

```bash
- cd project_GS
```
Run the development server:

```bash
python manage.py runserver
```
## 📊 Excel Integration Feature
A key feature of this application is the ability to link and synchronize data for a selected account with an Excel sheet (.xlsx). This allows easy data export, backup, and integration with reporting tools.

## 🎨 Admin UI Customization
The project uses Jazzmin to enhance the default Django admin interface with a modern and responsive design, improving usability and visual appeal.

## ☁️ Deployment
Web Hosting: Render

Database: Neon – A serverless PostgreSQL platform.

The application is configured to use environment variables for secret keys and database URLs when deployed.
