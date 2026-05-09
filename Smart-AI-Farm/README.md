# Smart AI Farm Assistant

A complete professional AI-powered platform designed for farmers to help detect crop diseases, predict weather, monitor crops using satellite APIs, set farming reminders, and get intelligent answers through an AI chatbot.

## Features Built
1. **User Authentication:** OTP based Phone Login interface (mock logic for demo testing).
2. **Crop Image Input System:** Mobile-friendly UI to upload via camera or gallery with HTML5 getUserMedia API and interactive loaders.
3. **AI Model (Transfer Learning):** Complete Python script to setup, augment data, and train MobileNetV2 locally. 
4. **Weather System:** 5-Day forecast UI integrated into the application (using mock/proxy OpenWeatherMap API blueprint).
5. **Disaster Alerts:** UI indicators for Heavy Rain, Cyclone, etc.
6. **Smart Reminders:** Create reminders for Pesticides or Irrigation with notifications.
7. **Satellite Monitoring Data:** API endpoints serving NDVI and crop health metrics.
8. **Soil Nutrient API:** Predicts NPK data for recommendation.
9. **Tamil Voice Assistant:** Web Speech API integration in the Chatbot for Tamil and English.
10. **Market Price Prediction:** Fetches prices globally.
11. **Emergency Help Page:** Quick 1-tap call links to Kisan Call Center, Disaster Management.

## Deployment Guide

### Local Setup
1. Define your environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Train the AI Model:
   - Make sure your `dataset/train/` and `dataset/validation/` folders contain images categorized by folders. Run:
     ```bash
     python model/train_model.py
     ```
4. Run the Flask Web Server:
   ```bash
   python backend/app.py
   ```
5. Access the application in your browser at `http://localhost:5000/`.

### Deployment Options

#### 1. Deploy on Render
- Push this source code to a GitHub repository.
- Go to [Render](https://render.com/), click "New Web Service".
- Connect the GitHub repository.
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn backend.app:app`
- Render provides an HTTPS URL automatically.

#### 2. Deploy on AWS (EC2)
- Launch an Ubuntu EC2 instance on AWS.
- Open Port 80 and 5000 in Security Groups.
- Connect via SSH and run:
  ```bash
  sudo apt update
  sudo apt install python3-pip
  git clone <YOUR_REPO>
  cd Smart-AI-Farm
  pip3 install -r requirements.txt
  python3 backend/app.py
  ```
- For production, configure Gunicorn and Nginx as a reverse proxy.

#### 3. Deploy on Google Cloud (App Engine)
- Add an `app.yaml` file to the root:
  ```yaml
  runtime: python39
  entrypoint: gunicorn -b :$PORT backend.app:app
  ```
- Install Google Cloud SDK, login, and deploy:
  ```bash
  gcloud init
  gcloud app deploy
  ```

---
*Developed for intelligent, accessible, and automated farming assistance.*
