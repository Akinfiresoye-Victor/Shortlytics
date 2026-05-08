# Mini URL Shortener

A Django-based URL shortener application that allows users to create shortened links and track their analytics, including click counts, IP addresses, and weekly click graphs.

## Features

- Shorten long URLs into compact links
- Track total clicks for each shortened URL
- View detailed analytics including click timestamps and IP addresses
- Generate weekly click graphs for visual analysis
- Delete unwanted shortened links
- Responsive web interface

## Technologies Used

- **Backend**: Django 5.2.1
- **Database**: SQLite (default), configurable for PostgreSQL
- **Frontend**: HTML, CSS, Bootstrap (via templates)
- **Data Visualization**: Matplotlib, Pandas
- **Deployment**: Gunicorn, WhiteNoise for static files
- **Other**: Python Decouple for configuration management

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd mini_url_app
   ```

2. Create a virtual environment:
   ```
   python -m venv url
   url\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables (optional):
   Create a `.env` file in the project root and add:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3  # or PostgreSQL URL
   ```

5. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser (optional, for admin access):
   ```
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Open your browser and navigate to `http://127.0.0.1:8000/`

## Usage

### Shortening URLs

1. Go to the home page
2. Enter the long URL you want to shorten
3. Optionally, provide a destination name
4. Click "Shorten URL"
5. Your shortened link will be generated and displayed

### Accessing Shortened Links

- Use the shortened URL (e.g., `http://127.0.0.1:8000/go/<uuid>`) to redirect to the original URL
- Each access is tracked with date and IP address

### Viewing Analytics

1. Navigate to the Analytics page
2. View all click data with pagination
3. See total clicks for each URL

### Viewing Graphs

- For each shortened URL, access the graph at `http://127.0.0.1:8000/graph/<uuid>`
- Displays a weekly click trend chart

### Deleting Links

- From the home page, click the delete button next to any shortened URL to remove it

## Project Structure

```
mini_url_app/
├── mini_url/              # Main Django project settings
├── url_shortner/          # Main app
│   ├── models.py          # Database models (URLModel, Click, DayData)
│   ├── views.py           # View functions
│   ├── forms.py           # Django forms
│   ├── urls.py            # URL patterns
│   ├── templates/         # HTML templates
│   └── migrations/        # Database migrations
├── url/                   # Virtual environment
├── db.sqlite3             # SQLite database
├── requirements.txt       # Python dependencies
└── manage.py              # Django management script
```

## API Endpoints

- `GET /` - Home page with URL shortening form
- `POST /` - Shorten a new URL
- `GET /go/<uuid>` - Redirect to original URL and track click
- `GET /check_analytics` - View click analytics
- `GET /graph/<uuid>` - Generate weekly click graph
- `POST /delete_link/<id>` - Delete a shortened URL

## Configuration

The application uses `python-decouple` for configuration. Key settings:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Enable/disable debug mode
- `DATABASE_URL`: Database connection string

## Deployment

For production deployment:

1. Set `DEBUG=False` in settings
2. Use a production database (PostgreSQL recommended)
3. Configure static files with WhiteNoise
4. Use Gunicorn as WSGI server
5. Set up proper environment variables

Example production command:
```
gunicorn mini_url.wsgi:application --bind 0.0.0.0:8000
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the license file for details.