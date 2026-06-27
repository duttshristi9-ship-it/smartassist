

# SmartAssist: AI-Powered Disaster Management Support 

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A5%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/duttshristi9-ship-it/smartassist)

 **Live Demo on Hugging Face Spaces**: **[https://huggingface.co/spaces/duttshristi9-ship-it/smartassist](https://huggingface.co/spaces/duttshristi9-ship-it/smartassist)**

SmartAssist is a complete Python-centric disaster management platform utilizing advanced NLP, ML feedback loops, and real-time WebSockets to provide immediate emergency guidance, rescue coordination, and shelter routing.

## Features

- **Advanced NLP Chatbot**: Powered by `spaCy` and `scikit-learn` to handle emergency intents (flood, fire, earthquake, medical, etc.) with confidence scoring and severity classification.
- **ML Feedback Response Engine**: Adaptive AI response engine using `SGDRegressor` to learn and rank the best responses based on user feedback.
- **Real-time Live Agent**: WebSockets (`Flask-SocketIO`) enable real-time chat, typing indicators, and immediate admin takeover of critical emergency sessions.
- **Disaster Map Integrations**: `Leaflet.js` with Python backend APIs displaying nearby resources and live emergency hotspots.
- **Automated Alerts**: Asynchronous emergency alerting system using `Twilio` (SMS) and `Flask-Mail` (Email) powered by `Celery` and `Redis`.
- **Advanced Security**: Protected by `Flask-JWT-Extended`, `Flask-Limiter` for rate-limiting, and CSRF protections.
- **Dynamic AI Training Admin**: Custom Admin dashboard for visualizing chatbot intent distributions and manually retraining the NLP models on-the-fly.
- **Vibrant UI**: Modern Glassmorphism aesthetic, rich dark mode, and dynamic micro-animations.

## Technology Stack

- **Backend**: Python 3.10, Flask, Flask-RESTful, Flask-SocketIO
- **AI/ML**: spaCy (NER & NLP), scikit-learn (TF-IDF, Naive Bayes, SGDRegressor)
- **Database**: PostgreSQL 15, SQLAlchemy ORM
- **Async & Performance**: Redis, Celery Workers, eventlet
- **Deployment**: Docker, docker-compose, Gunicorn
- **Frontend**: HTML5, CSS3 (Vanilla Glassmorphism), JS, Leaflet.js

## Quick Start Deployment (Docker)

1. Clone the repository and navigate to the project directory:
   ```bash
   cd "Disaster Management"
   ```

2. Create a `.env` file from the variables defined in `docker-compose.yml`:
   ```env
   FLASK_ENV=production
   DATABASE_URL=postgresql://smartassist_user:smartassist_pass@db:5432/smartassist_db
   REDIS_URL=redis://redis:6379/0
   SECRET_KEY=your_super_secret_key
   TWILIO_ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_token
   TWILIO_FROM_NUMBER=+1234567890
   ```

3. Build and launch the platform:
   ```bash
   docker-compose up --build -d
   ```

4. Access the application:
   - **User Portal**: `http://localhost:5000`
   - **Admin Panel**: `http://localhost:5000/admin` (admin@smartassist.com / Admin@123)

## Testing

Run the automated test suite with `pytest`:

```bash
# Enter the web container
docker-compose exec web bash

# Run tests
pytest tests/
```

## Architecture

- `app.py`: Application factory and socket initialization.
- `ai_engine/`: Contains the `intent_classifier.py` (NLP) and `response_engine.py` (ML).
- `models/`: SQLAlchemy data models (`chat`, `reports`, `user`).
- `routes/`: Blueprint controllers handling API endpoints and UI rendering.
- `services/`: External integrations (Twilio, Email).
- `static/css/main.css`: The central styling engine featuring Glassmorphism.
