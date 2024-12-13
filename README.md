# PMA System

This repository contains the PMA (Project Management and Assignment) system designed during **CS3240 - Advanced Software Development** at the University of Virginia. The project was developed collaboratively by:

- **Taylor Candenas (Test Manager)**
- **Steven Chen (Scrum Master)**
- **Ekow Daniels (Requirement Manager)**
- **Xiping Ye** (DevOps)

## About the Project
The PMA system is a web-based platform designed to streamline project management and assignment processes for students and instructors. The application allows users to:

- Manage projects and tasks.
- Track progress.
- Collaborate effectively within a team environment.
- Enroll in courses and participate in assigned projects.

As the **DevOps lead**, I was responsible for implementing most of the core functionality, setting up the deployment pipeline, and ensuring seamless integration of all components.

## Features
- **User Authentication**: Secure login system with role-based access for users.
- **Project Management**: Create, assign, and track tasks across multiple projects.
- **Enrollment System**: Manage student enrollment in courses and projects.
- **Progress Tracking**: Visualize project progress through interactive dashboards.
- **Responsive Design**: A user-friendly interface accessible on both desktop and mobile devices.

## Technologies Used
The PMA system is built with the following technologies:

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL
- **Deployment**: Heroku
- **Version Control**: Git/GitHub

## Project Setup

### Prerequisites
- Python 3.9 or later
- PostgreSQL
- Node.js (for optional frontend development)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pma-system.git
   cd pma-system
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000/`.

## Deployment
This project is deployed on Heroku. The following steps outline how to deploy updates:

1. Push changes to the GitHub repository.
2. Heroku will automatically build and deploy the latest codebase.

For manual deployment:
```bash
heroku login
heroku git:remote -a your-heroku-app-name
git push heroku main
```

## Contributing
Contributions are welcome! Please follow the steps below:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
- **Professor Robbie Hott**: For guidance and support throughout CS3240.
- The University of Virginia: For providing an excellent learning environment and resources.

---

Feel free to reach out for further inquiries or contributions!



