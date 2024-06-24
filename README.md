# Automated infptainment Complaint Registration System

## Project Overview

This project is a comprehensive system designed to automate the infotainment complaint registration process. It features image verification using a TensorFlow model, a user-friendly web interface, PDF generation of complaint details, and deployment on an AWS EC2 instance. Additionally, the system integrates Google Dialogflow for natural language processing and communication, and a Telegram bot ([@ infotainment_service_bot](https://t.me/infotainment_service_bot)) for extended user interactions.

## Features

- **Flask-Based Web Application:** The core application is built using Flask for efficient web server management.
- **Image Verification:** Integrates a TensorFlow model to verify images of vehicle infotainment systems.
- **PDF Generation:** Generates PDF files of complaint details for easy download and sharing.
- **Deployment:** Hosted on an AWS EC2 instance for scalable and reliable access.
- **Dialogflow Integration:** Uses Google Dialogflow for natural language processing and communication.
- **Telegram Bot Integration:** Allows users to interact with the system via a Telegram bot https://t.me/infotainment_service_bot

## Prerequisites

- Python 
- Flask
- TensorFlow
- SQLite3
- Google Dialogflow
- AWS Account
- Telegram Bot Token

## Installation

1. **Clone the repository:**

 
    git clone https://github.com/uttam-bn/service_bot.git
    cd service_bot
   
2. **Install dependencies:**

    pip install -r requirements.txt


3. **Run the Flask application:**

    python app.py
    

4. **Access the application:**

    Open your web browser and navigate to `http://localhost:5000`.


