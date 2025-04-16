# Urban Problems Reporter

A web application for reporting and tracking urban issues like potholes, broken streetlights, and pollution.

## Project Overview

The Urban Problems Reporter is a Django-based web application that creates a centralized platform for citizens to report urban infrastructure issues and for authorities to manage and resolve them. The application features user authentication, issue reporting with image uploads, status tracking, comments, and success stories.


## Installation & Setup

### Option 1: Using Docker Compose (Recommended)

1. Clone the repository:
   ```
   git clone https://github.com/MahmoodAlbadaai/urban-problems-reporter.git
   cd urban-problems-reporter
   ```

2. Build and start the containers:
 
   docker-compose up --build

3. The application will be available at http://localhost:8000

### Option 2: Manual Setup

1. Clone the repository:

   git clone https://github.com/MahmoodAlbadaai/urban-problems-reporter.git
   cd urban-problems-reporter


2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your MySQL database:
   - Create a database named `myappdb`
   - Create a user `myappdbuser` with password `myappdbpass`
   - Grant all privileges on `myappdb` to `myappdbuser`

5. Configure the database connection:
   ```
   export DATABASE_URL="mysql://myappdbuser:myappdbpass@localhost:3306/myappdb"
   ```
   On Windows, use `set` instead of `export`.

6. Apply migrations:
   ```
   python manage.py migrate
   ```

7. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

8. Start the development server:
   ```
   python manage.py runserver
   ```

9. The application will be available at http://localhost:8000

## Using the Application

### Regular User Actions
- Register a new account at `/register/`
- Log in at `/login/`
- Report an issue at `/report/`
- View all issues at `/map/`
- View issue details at `/issue/<id>/`
- Add comments to issues
- View success stories at `/success/`

### Authority User Actions
For testing authority features, you need to:
1. Create a regular user account
2. Access the Django admin at `/admin/` using the superuser credentials
3. Find your user in the Users list and check the "Staff status" checkbox
4. Save the changes

Authority users can:
- Access the authority dashboard at `/authority-dashboard/`
- Update issue status at `/issue/<id>/update/`
- Add resolutions at `/issue/<id>/resolve/`
- Mark resolutions as featured success stories

## Project Structure

- `core/` - Main Django app containing all functionality
- `config/` - Django project settings
- `static/` - CSS, JS, and image files
- `templates/` - HTML templates
- `media/` - User-uploaded files (issue images, etc.)
- `docker-compose.yml` - Docker Compose configuration
- `Dockerfile` - Docker configuration
- `docker_entrypoint.sh` - Docker startup script

## Accessing the Admin Interface

The Django admin interface is available at `/admin/`. Use the superuser credentials created during setup to log in.
