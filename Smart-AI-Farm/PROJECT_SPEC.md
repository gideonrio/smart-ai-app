# AI Crop Disease & Pest Detection System

I am building a Smart AI-Powered Crop Disease & Pest Detection Web App using Deep Learning (CNN + Transfer Learning) / Vision AI.

## 🎯 PROJECT GOAL
If the user uploads an image (camera/gallery), the system must:
- ✔ Identify crop name
- ✔ Detect plant part (leaf / fruit / whole plant)
- ✔ Detect disease or pest
- ✔ Tell healthy or affected
- ✔ Show confidence %
- ✔ Suggest treatment
- ✔ Suggest pesticide
- ✔ Provide buy link
- ✔ Show result within 1–3 seconds

## 🧠 SYSTEM WORKFLOW

### 1️⃣ Image Input
User uploads image using:
- ✔ Gallery
- ✔ Camera

System must:
- ✔ Show uploaded image
- ✔ Detect crop automatically
- ✔ Detect disease/pest automatically

### 2️⃣ AI Prediction Process
System should:
1. Preprocess image (resize + normalize)
2. Detect plant part
3. Load correct model/prompt
4. Predict disease
5. Show result with confidence

## 🎯 OUTPUT FORMAT (FINAL)

### 🌱 AI Prediction Result
- 📌 **Crop Name**: Tomato
- 🌿 **Plant Part**: Leaf
- 📊 **Confidence**: 96%
- 🦠 **Status**: Affected
- 📍 **Disease**: Early Blight
- 💊 **Treatment**: Remove infected leaves and apply fungicide
- 🧴 **Medicine**: Mancozeb
- 🛒 **Buy Link**: Amazon/Agristore link

### ✅ Healthy Example
- 📌 **Crop Name**: Brinjal
- 🌿 **Plant Part**: Leaf
- 📊 **Confidence**: 97%
- 🟢 **Status**: Healthy
- ✔ No treatment needed

---

## 🚀 ADDITIONAL SMART FEATURES

### 🌍 3️⃣ Location + Weather System
System must show:
- 📍 Current Location
- 🌡 Temperature
- 💧 Humidity
- 🌦 Weather condition

Example:
> 📍 Chennai | 🌡 33°C | 🌦 Cloudy

### ⛈ 4️⃣ Disaster Prediction
System shows alerts:
- ⚠ Heavy rain expected
- ⚠ Flood warning
- ⚠ Heatwave alert

### 📊 5️⃣ Disease Risk Prediction
System predicts:
- ✔ Future disease chance
- ✔ Prevention tips
Example: "High humidity may cause fungal disease."

### 📞 6️⃣ Emergency Support Feature
System shows:
- 📞 Agriculture Helpline
- 📞 Local Government Support
Example: Kisan Call Center: 18001801551

### 📚 7️⃣ Recommendation Engine
System suggests:
- ✔ Fertilizer advice
- ✔ Watering advice
- ✔ Organic treatment
- ✔ Chemical treatment

### 🎤 8️⃣ Voice Assistant Feature (Optional)
System supports:
- ✔ Tamil
- ✔ English
- ✔ Hindi
Example: "உங்கள் செடிக்கு இலை நோய் உள்ளது"

### 📆 9️⃣ History Tracking Feature
System stores:
- ✔ Uploaded images
- ✔ Disease results
- ✔ Date
Helps farmers track disease progress.

---

## ⚡ SPEED REQUIREMENT
System must:
- ✔ Show result in 1–3 sec
- ✔ Extremely fast inference (powered by Groq Vision LLM / MobileNetV2 backend)

## 🖥 TECH STACK
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Backend**: Python, Flask
- **AI**: Groq Vision / TensorFlow Keras
- **APIs**: Weather API, Location API

## 🎤 VIVA EXPLANATION (SHORT)
"Our system uses advanced AI and machine learning to detect crop diseases. The system predicts the crop type, part, and disease within 2 seconds. We display confidence percentages instead of assuming 100% accuracy, providing farmers with actionable treatment recommendations, immediate weather context, and emergency agricultural helplines."
