# Seller-Customer-Order Management Portal

A Flask-based web application for managing sellers, customers, and subscription orders with role-based access control. This application provides a comprehensive solution for managing business operations with separate interfaces for administrators and sellers.

## ✨ Features

- **Role-Based Access Control**
  - Admin: Full system access, manage sellers and view all data
  - Seller: Manage own customers and orders
- **Dashboard**
  - Admin: Overview of all sellers, customers, and orders
  - Seller: Personal dashboard with customer and order statistics
- **Customer Management**
  - Add, edit, and manage customer information
  - Track customer subscriptions and order history
- **Order Management**
  - Create and track subscription orders
  - Update order status and details
  - Generate order reports
- **Responsive Design**: Mobile-friendly interface built with Bootstrap 5

## 🛠 Tech Stack

- **Backend**: Python 3.8+
- **Web Framework**: Flask 2.3.3
- **Database**: SQLite (Production-ready databases like PostgreSQL can be configured)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Authentication**: Flask-Login
- **Form Handling**: Flask-WTF
- **Database ORM**: SQLAlchemy
- **Environment Management**: python-dotenv

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd python_project_tupi_final_sem
   ```

2. **Create and activate a virtual environment**

   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   - Copy `.env.example` to `.env`
   - Update the values in `.env` as needed:
     ```env
     # Application Settings
     FLASK_APP=run.py
     FLASK_ENV=development
     SECRET_KEY=your-secret-key-here
     DATABASE_URL=sqlite:///scom_portal.db
     DEFAULT_ADMIN_PASSWORD=change-this-password
     ```

5. **Initialize the database**

   ```bash
   python init_db.py
   ```

   This will create:

   - Admin user: `admin@example.com` / `admin123`
   - Test seller: `seller@example.com` / `seller123`

6. **Run the application**

   ```bash
   flask run
   # or
   python run.py
   ```

   Or on Windows:

   ```bash
   .\run_app.bat
   ```

7. **Access the application**
   Open your browser and go to: `http://127.0.0.1:5000`

## 🔐 Default Login Credentials

- **Admin Panel**:

  - Email: `admin@example.com`
  - Password: `admin123`

- **Seller Account**:
  - Email: `seller@example.com`
  - Password: `seller123`

## 🔧 Configuration

### Environment Variables

| Variable                 | Description                                                    | Default                    | Required |
| ------------------------ | -------------------------------------------------------------- | -------------------------- | -------- |
| `FLASK_APP`              | Entry point of the Flask application                           | `run.py`                   | ✅ Yes   |
| `FLASK_ENV`              | Environment (development/production)                           | `development`              | ❌ No    |
| `SECRET_KEY`             | Secret key for session management                              | -                          | ✅ Yes   |
| `DATABASE_URL`           | Database connection URL                                        | `sqlite:///scom_portal.db` | ❌ No    |
| `DEFAULT_ADMIN_PASSWORD` | Default password for admin user (only used during first setup) | -                          | ❌ No    |

### Database

By default, the application uses SQLite for development. For production, consider using a more robust database like PostgreSQL by updating the `DATABASE_URL` in your `.env` file:

```
DATABASE_URL=postgresql://username:password@localhost/dbname
```

## 📂 Project Structure

```
├── app/
│   ├── admin/            # Admin blueprint and routes
│   ├── auth/             # Authentication routes and forms
│   ├── seller/           # Seller blueprint and routes
│   ├── static/           # Static files (CSS, JS, images)
│   ├── templates/        # HTML templates
│   ├── __init__.py       # Application factory
│   ├── models.py         # Database models
│   └── routes.py         # Main application routes
├── instance/             # Instance folder for configuration and database
├── .env.example          # Example environment variables
├── init_db.py           # Database initialization script
├── requirements.txt      # Python dependencies
└── run.py               # Application entry point
```

## 🛠 Development

### Running in Development Mode

```bash
flask run --debug
# or
python run.py
```

### Running Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
pytest
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For any questions or feedback, please open an issue on the GitHub repository.

````

4. **Set up environment variables**
- Copy `.env.example` to `.env`
- Update the values in `.env` as needed

5. **Initialize the database**
```bash
python init_db.py
````

## Running the Application

### Development

```bash
# Windows
run_app.bat

# Linux/MacOS
export FLASK_APP=run.py
export FLASK_ENV=development
flask run
# or
python run.py
```

Then open your browser and navigate to `http://localhost:5000`

### Production

For production deployment, consider using a production WSGI server like Gunicorn or uWSGI behind a reverse proxy like Nginx.

## Default Login Credentials

- **Admin**

  - Username: admin
  - Password: (set in .env as DEFAULT_ADMIN_PASSWORD, defaults to 'admin123')

- **Test Seller**
  - Username: testseller
  - Password: seller123

## Project Structure

```
scom-portal/
├── app/
│   ├── __init__.py       # Application factory
│   ├── models.py         # Database models
│   ├── auth/             # Authentication routes
│   ├── admin/            # Admin panel routes
│   ├── seller/           # Seller panel routes
│   ├── templates/        # HTML templates
│   └── static/           # Static files (CSS, JS, images)
├── instance/             # Instance folder
├── migrations/           # Database migrations
├── .env.example          # Example environment variables
├── requirements.txt      # Python dependencies
├── run.py                # Application entry point
└── init_db.py           # Database initialization script
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask documentation
- Bootstrap 5
- Font Awesome
