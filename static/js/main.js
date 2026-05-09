let stream = null;
const HISTORY_KEY = 'crop_guard_history';
const video = document.getElementById('video-feed');
const canvas = document.getElementById('capture-canvas');
const uploadContainer = document.getElementById('upload-mode-container');
const cameraContainer = document.getElementById('camera-mode-container');
const btnUploadMode = document.getElementById('btn-upload-mode');
const btnCameraMode = document.getElementById('btn-camera-mode');
const preview = document.getElementById('image-preview');

// Mode Switching
btnUploadMode.addEventListener('click', () => {
    stopCamera();
    uploadContainer.style.display = 'block';
    cameraContainer.style.display = 'none';
    btnUploadMode.classList.add('active');
    btnCameraMode.classList.remove('active');
});

btnCameraMode.addEventListener('click', async () => {
    uploadContainer.style.display = 'none';
    cameraContainer.style.display = 'block';
    btnUploadMode.classList.remove('active');
    btnCameraMode.classList.add('active');
    await startCamera();
});

async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
        video.srcObject = stream;
    } catch (err) {
        console.error("Error accessing camera:", err);
        alert("Could not access camera. Please check permissions.");
    }
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
}

// CAPTURE BUTTON
document.getElementById('btn-capture').addEventListener('click', () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);

    const dataUrl = canvas.toDataURL('image/jpeg');
    preview.src = dataUrl;
    preview.style.display = 'block';

    // Switch back to upload mode implicitly or just show preview
    stopCamera();
    cameraContainer.style.display = 'none';
    uploadContainer.style.display = 'block';
});

// Update Prediction Submit to handle captured blob
document.getElementById('predict-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById('image-upload');

    let imageBlob = null;

    if (preview.src.startsWith('data:image')) {
        // Captured from camera
        const response = await fetch(preview.src);
        imageBlob = await response.blob();
        formData.append('file', imageBlob, 'capture.jpg');
    } else if (fileInput.files.length > 0) {
        // Uploaded from file
        formData.append('file', fileInput.files[0]);
    } else {
        alert("Please select or capture an image first!");
        return;
    }

    const resultCard = document.getElementById('result-card');
    const btn = e.target.querySelector('button[type="submit"]');

    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processing...';

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            alert("Error: " + data.error);
        } else {
            document.getElementById('res-title').innerText = data.title;
            document.getElementById('res-part').innerText = data.part;
            document.getElementById('res-pest').innerText = data.pest || "None";
            document.getElementById('res-confidence').innerText = data.confidence + "%";
            document.getElementById('res-recommendation').innerText = data.recommendation;
            document.getElementById('res-pesticide').innerText = data.pesticide;
            document.getElementById('res-buy').href = data.buy_link;

            resultCard.style.display = 'block';
            window.scrollTo({ top: resultCard.offsetTop - 50, behavior: 'smooth' });

            // Save to history
            saveToHistory({
                title: data.title,
                confidence: data.confidence,
                part: data.part
            });
        }
    } catch (error) {
        console.error("Error prediction:", error);
        alert("An error occurred during prediction.");
    } finally {
        btn.disabled = false;
        btn.innerHTML = 'Detect Disease';
    }
});

// Sync file input preview
document.getElementById('image-upload').addEventListener('change', function (e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (event) {
            preview.src = event.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});

// Weather Integration
async function fetchWeather() {
    try {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(async (pos) => {
                const { latitude, longitude } = pos.coords;
                const res = await fetch(`/weather?lat=${latitude}&lon=${longitude}`);
                const data = await res.json();
                updateWeatherUI(data);
            }, async (error) => {
                console.warn("Location access denied, using default.");
                const res = await fetch('/weather');
                const data = await res.json();
                updateWeatherUI(data);
            });
        } else {
            const res = await fetch('/weather');
            const data = await res.json();
            updateWeatherUI(data);
        }
    } catch (err) {
        console.error("Weather error:", err);
    }
}

function updateWeatherUI(data) {
    document.getElementById('weather-temp').innerText = `${Math.round(data.temp)}°C`;
    document.getElementById('weather-humidity').innerText = `${data.humidity}%`;
    const riskEl = document.getElementById('disease-risk');
    riskEl.innerText = data.risk;
    riskEl.className = data.risk === 'High' ? 'text-danger fw-bold' : (data.risk === 'Moderate' ? 'text-warning fw-bold' : 'text-success fw-bold');

    if (data.tips) loadTips(data.tips);
}

// Expert Tips
function loadTips(tips) {
    const container = document.getElementById('tips-container');
    container.innerHTML = tips.map(tip => `
        <div class="tip-card">
            <i class="${tip.icon} text-success"></i>
            <h6>${tip.title}</h6>
            <p class="small opacity-75 mb-0">${tip.content}</p>
        </div>
    `).join('');
}

// History Management
function saveToHistory(detection) {
    let history = JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]');
    history.unshift({
        ...detection,
        date: new Date().toLocaleDateString(),
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    });
    history = history.slice(0, 5);
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
    renderHistory();
}

function renderHistory() {
    const history = JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]');
    const container = document.getElementById('history-list');
    const historyCard = document.getElementById('history-card');

    if (history.length === 0) {
        historyCard.style.display = 'none';
        return;
    }

    historyCard.style.display = 'block';
    container.innerHTML = history.map(item => `
        <div class="history-item d-flex justify-content-between align-items-center">
            <div>
                <h6 class="mb-0 text-white">${item.title}</h6>
                <small class="opacity-50">${item.date} at ${item.time}</small>
            </div>
            <span class="badge bg-success">${item.confidence}%</span>
        </div>
    `).join('');
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    fetchWeather();
    renderHistory();
});
