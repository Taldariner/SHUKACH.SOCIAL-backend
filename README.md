### SHUKACH.SOCIAL

SHUKACH.SOCIAL is a new iteration of web scrapping system Shukach.info (Mediaresearch.store), intended to work with social medias rather then classic websites.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Contact](#contact)

## Features

- **Advanced Analytics**: Gain insights with our advanced analytics tools.
- **Real-time Monitoring**: Monitor social media in real-time to stay updated with the latest conversations and trends.
- **Powerful AI Tools**: Leverage the power of artificial intelligence to analyze large volumes of social media data.
- **Comprehensive Reports**: Generate comprehensive and customizable reports with ease.
- **Data Security**: Ensure the security and privacy of your social media data with our robust data protection measures.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Taldariner/shukach_social.git
    cd shukach_social
    ```

2. **Create a virtual environment and activate it:**
    ```bash
    python -m venv __venv__
    source ./__venv__/bin/activate  # On Windows use `.\__venv__\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    python -m spacy download uk_core_news_lg
    python -m spacy download en_core_web_lg
    python -m spacy download ru_core_news_lg
    ```

4. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

5. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## Usage

1. **Access the application:**
    Open your browser and go to `http://127.0.0.1:8000`.

2. **Explore features:**
    Navigate through the application to explore the various features provided by SHUKACH.SOCIAL.

## Contributing

1. **Fork the repository.**
2. **Create a new branch:**
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. **Make your changes and commit them:**
    ```bash
    git commit -m 'Add some feature'
    ```
4. **Push to the branch:**
    ```bash
    git push origin feature/your-feature-name
    ```
5. **Create a new Pull Request.**

## Contact

- **Author**: Vladyslav Tytarchuk
- **Email**:  taldariner@gmail.com
- **GitHub**: [Taldariner](https://github.com/Taldariner)
