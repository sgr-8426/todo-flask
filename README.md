# To-Do Application

A Flask-based To-Do application with user authentication and task management features.

## Features

- User authentication with email OTP verification
- Task management (Create, Read, Update, Delete)
- Task categorization
- Task search functionality
- Remember me functionality
- Responsive web interface

## Prerequisites

- Python 3.x
- Flask
- SQLAlchemy
- SQLite

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv env
   ```
3. Activate the virtual environment:
   - Windows: `env\Scripts\activate`
   - Unix/MacOS: `source env/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Update the email configuration in `app.py` with your email credentials:
   ```python
   sender_email = "your-email@gmail.com"
   sender_password = "your-app-specific-password"
   ```
2. Make sure to use an app-specific password if using Gmail

## Running the Application

1. Activate the virtual environment (if not already activated)
2. Run the application:
   ```
   python app.py
   ```
3. Access the application at `http://localhost:5000`

## Project Structure

- `app.py`: Main application file with routes and database models
- `templates/`: HTML templates
  - `base.html`: Base template with common layout
  - `home.html`: Landing page
  - `login.html`: Login page
  - `tasks.html`: Task management interface
- `static/`: Static files (CSS, JavaScript, images)
- `instance/`: SQLite database file location

## Security Features

- OTP-based email verification
- Secure session management
- Password-free authentication
- Remember me functionality with secure cookies
