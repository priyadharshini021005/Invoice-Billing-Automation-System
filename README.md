# Invoice-Billing-Automation-System
A desktop-based Invoice &amp; Billing Automation System developed using Python Tkinter and MySQL to manage customers, products, invoices, and billing operations efficiently.
# Invoice & Billing Automation System

A desktop-based **Invoice & Billing Automation System** developed using **Python Tkinter and MySQL**. The system helps manage customers, products, invoices, and billing operations through a simple and user-friendly graphical interface.

## 📌 Project Overview

The Invoice & Billing Automation System is designed to simplify day-to-day billing activities by providing a centralized application for managing customer information, product details, invoices, and billing records.

The application uses **Python Tkinter** for the graphical user interface and **MySQL** for storing and managing application data.

## ✨ Features

* 🔐 User Login System
* 👥 Customer Management

  * Add customers
  * Update customer details
  * Delete customers
  * Search customers
* 📦 Product Management

  * Add products
  * Update product details
  * Delete products
  * Manage product stock
* 🧾 Billing Management

  * Select customers
  * Select products
  * Add products to billing
  * Calculate item totals
  * Calculate final bill amount
  * Store billing information
* 📄 Invoice Management

  * Generate and manage invoices
  * Store invoice details in MySQL
* 🗄️ MySQL Database Integration
* 🖥️ User-friendly Tkinter GUI
* 📊 Dashboard for accessing different modules

## 🛠️ Technologies Used

| Technology        | Purpose                             |
| ----------------- | ----------------------------------- |
| Python            | Application development             |
| Tkinter           | Graphical User Interface            |
| MySQL             | Database management                 |
| MySQL Connector   | Python–MySQL connectivity           |
| PyCharm / VS Code | Development                         |
| Git & GitHub      | Version control and project hosting |

## 📂 Project Structure

```text
Invoice-Billing-Automation-System/
│
├── main.py
├── login.py
├── dashboard.py
├── billing.py
├── customer.py
├── product.py
├── invoice.py
├── db.py
│
├── README.md
└── requirements.txt
```

## 🗃️ Database

The application uses a MySQL database named:

```text
invoice_billing_system
```

Main database modules include:

```text
users
customers
products
bills
bill_items
```

The database stores customer records, product information, billing transactions, invoice items, and user login information.

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Invoice-Billing-Automation-System.git
```

### 2. Open the Project

Open the project folder using **PyCharm** or **VS Code**.

### 3. Install Required Packages

Install the MySQL connector:

```bash
pip install mysql-connector-python
```

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Make sure MySQL Server is installed and running.

Create the database:

```sql
CREATE DATABASE invoice_billing_system;
```

Import or execute the project's database SQL script if provided.

### 5. Configure Database Connection

Update the MySQL connection details in:

```text
db.py
```

Example:

```python
host = "localhost"
user = "root"
password = "your_password"
database = "invoice_billing_system"
```

Use the MySQL username and password configured on your computer.

### 6. Run the Application

Run:

```bash
python main.py
```

or run `main.py` directly from PyCharm / VS Code.

## 🔄 Application Workflow

```text
Login
  ↓
Dashboard
  ↓
Customer Management
  ↓
Product Management
  ↓
Billing
  ↓
Bill Items
  ↓
Invoice
  ↓
MySQL Database
```

## 🧾 Billing Process

1. Login to the application.
2. Open the Billing module.
3. Select or enter customer details.
4. Select the required product.
5. Enter the quantity.
6. Add the product to the bill.
7. Review the selected items.
8. Calculate the total amount.
9. Save the bill.
10. Store bill and bill-item details in MySQL.
11. Generate/manage the invoice.

## 🎯 Objectives

* Automate manual billing operations.
* Reduce calculation errors.
* Maintain customer and product information efficiently.
* Store billing records in a centralized database.
* Provide an easy-to-use desktop billing application.
* Improve the efficiency of invoice management.

## 🚀 Future Enhancements

* PDF invoice generation
* Automatic invoice printing
* Advanced sales reports
* Date-wise sales analytics
* Low-stock notifications
* Customer purchase history
* Role-based access control
* Backup and restore functionality
* Power BI integration for advanced business analytics

## 👩‍💻 Author

**Priyadharshini**

BCA Graduate | Python | SQL | Power BI

## 📜 License

This project is developed for **educational and portfolio purposes**.

