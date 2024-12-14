### MEMBERS:

Anas BELHAMRA
Adam NAJIB
Adnane MARBOUH
Souhail ELKHALMADANI
Hatim FAQDAOUI

# 📘 **Shop App API on Azure Cloud**

This project demonstrates a simple **Flask** application deployed on **Azure** using **Terraform**. The app serves as the backend for an e-commerce platform with features like user authentication, product management, and order processing. 

---

## 📋 **Project Structure**

- **api/**: Contains the Flask application code, including routes, models, and controllers.
- **infrastructure/**: Contains the **Terraform** code to provision the Azure infrastructure.
- **.github/**: Contains **GitHub Actions** workflows for **CI/CD**.

## 🚀 **Getting Started**

### 🛠 **Prerequisites**
- Python 3.9 or later
- Terraform 1.5 or later
- Azure account

### 🏃‍♂️ **Running the Application Locally**
1. Install dependencies:
   
bash
   pip install -r api/requirements.txt
2. Run the app
bash
   python api/app.py
### 🧪 **Running the Tests Locally**
1. Install pytest
    
bash 
    pip install pytest
2. Run tests using pytest
bash
    pytest api/tests

## 🧑‍💻 **Flask Application**

### 📜 **Overview**

The **Flask-based** application serves as the core API for the e-commerce platform. It handles user authentication, product management, shopping cart functionality, and order processing.

### 🔑 **Key Features**

- **User Authentication**: Customers can sign up, log in, and reset their passwords using **Flask-Login**.
- **Product Management**: Allows customers to search for products and add them to their shopping cart.
- **Admin Controls**: Admin users can manage product stock levels and update order statuses.
- **Forms**: **Flask-WTF** is used for secure and easy handling of forms, including login, registration, and product management forms.

### ⚙️ **How it Works**

The app follows the **Model-View-Controller (MVC)** architecture:

- **Model**: Uses **SQLAlchemy** for database interactions, defining models for entities like users, products, orders, etc. SQLAlchemy ensures that the app communicates efficiently with the database to store and retrieve data.
  
- **View**: Since this is an API-based application, the "view" is primarily the **JSON responses** returned by various API endpoints. The views are rendered dynamically by the **Flask** route handlers, which generate and send JSON objects in response to HTTP requests.

- **Controller**: The **routes** defined in app.py handle the business logic of each API endpoint. These routes control how the application interacts with the user, such as handling login, product search, adding items to a cart, and processing orders.

### 📂 **Application Flow**

1. **User Authentication**:
   - **Sign up**: Users can create a new account.
   - **Login**: Existing users can log in using their credentials.
   - **Password Reset**: Users can reset their passwords using email verification.

2. **Product Management**:
   - Customers can view available products, search for specific items, and add them to their shopping cart.
   - Admin users have the ability to update product stock levels and manage product details.

3. **Order Processing**:
   - Users can place orders, and admins can update the order status (e.g., processing, shipped).

4. **Form Handling**:
   - Forms, such as the login form and product management form, are managed using **Flask-WTF**, ensuring secure and easy handling of user input.

### 🔧 **Flask Extensions Used**

- **Flask-Login**: Manages user sessions and authentication.
- **Flask-SQLAlchemy**: Facilitates database operations, allowing interaction with the app's models.
- **Flask-WTF**: Simplifies form handling and ensures secure data validation.
- **Flask**: The lightweight framework used to build the API.