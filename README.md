# Personal Portfolio Website

A modern, responsive, and customizable personal portfolio website built with Flask, Bootstrap 5, and custom JavaScript. Showcase your projects, skills, and experience with a clean and professional design.

## Features

- **Responsive Design**: Looks great on all devices
- **Dark/Light Mode**: Toggle between themes
- **Project Showcase**: Display your work with filters
- **Blog Section**: Share your thoughts and articles
- **Contact Form**: Let visitors get in touch
- **SEO Optimized**: Ready for search engines
- **Fast & Lightweight**: Optimized for performance
- **Modern UI/UX**: Clean and professional design

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual Environment (recommended)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/portfolio-website.git
   cd portfolio-website
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory and add your configuration:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///site.db
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-email-password
   ```

5. **Initialize the database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the development server**
   ```bash
   flask run
   ```

7. **Open your browser and visit**
   ```
   http://localhost:5000
   ```

## Project Structure

```
portfolio/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── auth.py
│   │   └── posts.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── style.css
│   │   │   └── portfolio.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── img/
│   │       └── profile.jpg
│   └── templates/
│       ├── base.html
│       ├── home.html
│       ├── about.html
│       ├── projects.html
│       ├── blog.html
│       ├── post.html
│       └── auth/
│           ├── login.html
│           └── register.html
├── migrations/
├── .env
├── .gitignore
├── config.py
├── requirements.txt
└── run.py
```

## Customization

### Change Colors
Edit the CSS variables in `static/css/portfolio.css` to match your brand colors:

```css
:root {
    --primary: #6366f1;
    --primary-light: #818cf8;
    --primary-dark: #4f46e5;
    --secondary: #8b5cf6;
    --accent: #ec4899;
    /* ... */
}
```

### Update Content
1. **Home Page**: Edit `templates/home.html`
2. **About Page**: Edit `templates/about.html`
3. **Projects**: Edit the projects section in `templates/projects.html`
4. **Blog**: Create and edit blog posts in the admin panel

### Add Your Information
Update the following files with your personal information:
- `app/static/js/main.js` (theme settings)
- `app/templates/base.html` (footer, social links)
- `app/templates/about.html` (personal info, skills, experience)

## Deployment

### Heroku
1. Create a `Procfile` in the root directory:
   ```
   web: gunicorn run:app
   ```

2. Install gunicorn:
   ```bash
   pip install gunicorn
   pip freeze > requirements.txt
   ```

3. Create a new Heroku app and deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku run flask db upgrade
   ```

### PythonAnywhere
1. Upload your code to GitHub
2. Create a new PythonAnywhere account and open a bash console
3. Clone your repository
4. Set up a virtual environment and install requirements
5. Configure the web app through the PythonAnywhere dashboard

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Bootstrap 5](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- [AOS - Animate On Scroll](https://michalsnik.github.io/aos/)
- [Flask](https://flask.palletsprojects.com/)

---

Built with ❤️ by [Your Name]
