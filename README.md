# AI Interview Platform

## Overview

This project is a web-based platform developed to help users improve their interview skills. Built using Python Django, HTML, CSS, and JavaScript, the platform integrates with the OpenAI API to provide targeted and personalized feedback on users' interview answers. By using this platform, users can practice and enhance their interview techniques, leading to better performance in actual interviews.

## Features

- User registration and authentication
- Interactive interview practice sessions
- Real-time feedback using OpenAI API
- Personalized suggestions for improvement
- User dashboard to saved feedback

## Demo

[Demo video for Project](https://myntuac.sharepoint.com/sites/ComputerScienceDegreeShowcase2024/SitePages/Students/N0992216.aspx?web=1)

## Setup Instructions

To set up the project, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/AI-Interview-Site.git
    cd interview-practice-platform
    ```

2. **Install dependencies**:
    ```sh
    pip install -r Django, OpenAI
    ```

3. **Set up the environment variables**:
    Create a `.env` file in the project root and add your OpenAI API key and Django secret key:
    ```
    OPENAI_API_KEY=your_openai_api_key
    DJANGO_SECRET_KEY=your_django_secret_key
    ```

4. **Run database migrations**:
    ```sh
    python manage.py migrate
    ```

5. **Start the development server**:
    ```sh
    python manage.py runserver
    ```

## Usage

1. **Register a new account** or **log in** with an existing account.
2. **Start a new interview practice session** by selecting either custom interviews or mainpage.
3. **Answer the questions** and submit your responses.
4. **Receive feedback** from the AI, which includes personalized suggestions for improvement.
5. **Save your feedback** on the user dashboard.

## Acknowledgements

This project was developed as a final year project. Special thanks to the OpenAI team for providing the API and to the Django community for their excellent resources and support.
