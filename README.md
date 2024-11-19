# FlowVis: A Social Media for Racing Enthusiasts

FlowVis is a social network designed for fans of car racing, karting, automotive events, and related activities. Our goal is to create a safe and interactive environment for enthusiasts to connect in a meaningful and reliable way.

> This project was developed as part of the evaluation requirements for the courses: *Theory and Systems Development, **Web Applications, and **Programming Language, under the guidance of Professors **Andre Evandro* and *Leonardo Motta*.

---

## 📋 Project Structure

This project uses *Flask*, a Python framework for web application development, and has the following basic structure:

### Technologies Used:
- *Programming Languages*:
  - Python
  - HTML
  - CSS
- *Frameworks*:
  - Flask 3.0.2 (full-stack)
  - Bootsrap (front-end)
- *Database*:
  - SQLite (or other specified)

---

## 📁 Repository Structure

The repository contains:
- *Back-End Code*: Manages the system logic and database connection.
- *Front-End Code*: Responsible for the user interface (UI) and user experience (UX).
- *Static Resources*: Images, custom CSS styles, and JavaScript scripts.

---

## 🛠️ Installation and Configuration

To run the project on your local machine, follow these steps:

1. Clone the repository:
bash
git clone https://github.com/YourUsername/flowvis.git
cd flowvis


2. Create and activate a virtual environment:

bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows


3. Install the dependencies listed in the requirements.txt file:
bash
pip install -r requirements.txt


4. Run the Flask server:
bash
flask run


5. Access the application in your browser at:
 bash
http://127.0.0.1:5000


## 🚀 How to Run
To start the application, follow the steps in the Installation and Configuration section. Once the Flask server is running, you can interact with the social network, explore events, and connect with other users.

## 📖 Additional Information
### Directory Structure:
```plaintext
flowvis/
├── app/
│   ├── static/          # CSS, JS, and image files
│   ├── templates/       # HTML files (pages)
│   ├── routes.py        # Flask routes
│   ├── models.py        # Database models
│   └── __init__.py      # Flask application configuration
├── migrations/          # Database migration files
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

**Features:**
- User login and registration.
- A feed with posts about events and groups.
- Event creation and exploration for races.
- Interaction with other users (likes, comments etc.).

## 👩‍💻 Authors
This collaborator was responsible for designing and developing the front-end of this social network.
- [Alice Maria](https://github.com/LiceeIF)

This collaborator was responsible for developing the back-end of this social network.
- [Rodrigo Baesa](https://github.com/RodrigoBaesa)

## 📆 Project
This project was developed in 2024 as part of an academic activity.