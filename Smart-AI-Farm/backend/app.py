import os
from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from flask_caching import Cache
import sys


def create_app():
    # Configure template and static folders
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if BASE_DIR not in sys.path:
        sys.path.append(BASE_DIR)

    template_dir = os.path.join(BASE_DIR, 'frontend', 'templates')
    static_dir = os.path.join(BASE_DIR, 'frontend', 'static')

    app = Flask(__name__, template_folder=template_dir,
                static_folder=static_dir)
    app.secret_key = "super_secret_farm_key"

    # 🔒 Production Security & CORS
    CORS(app)
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB limit

    # 📁 Persistent Storage Configuration (Handles Read-Only Vercel /tmp)
    STORAGE_DIR = "/storage/uploads"
    if not os.path.exists(STORAGE_DIR):
        if os.environ.get('VERCEL'):
            STORAGE_DIR = "/tmp/uploads"
        else:
            STORAGE_DIR = os.path.join(BASE_DIR, 'dataset', 'uploads')
    
    try:
        os.makedirs(STORAGE_DIR, exist_ok=True)
    except OSError:
        STORAGE_DIR = "/tmp/uploads"
        os.makedirs(STORAGE_DIR, exist_ok=True)
        
    app.config['UPLOAD_FOLDER'] = STORAGE_DIR


    # ⚡ Caching for speed
    cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
    app.cache = cache

    # Register Blueprints
    from backend.auth import auth_bp
    from backend.weather import weather_bp
    from backend.predict import predict_bp
    from backend.alerts import alerts_bp
    from backend.reminder import reminder_bp
    from backend.market_prices import market_prices_bp
    from backend.soil_prediction import soil_prediction_bp
    from backend.satellite_monitor import satellite_monitor_bp
    from backend.chatbot import chatbot_bp
    from backend.news import news_bp
    from backend.schemes import schemes_bp
    from backend.irrigation import irrigation_bp
    from backend.store import store_bp
    from backend.crop_calendar import calendar_bp
    from backend.yield_prediction import yield_prediction_bp
    from backend.community import community_bp
    from backend.rental import rental_bp
    from backend.seasonal_planning import seasonal_planning_bp
    from backend.wallet import wallet_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(predict_bp, url_prefix='/api')
    app.register_blueprint(weather_bp, url_prefix='/api')
    app.register_blueprint(alerts_bp, url_prefix='/api')
    app.register_blueprint(reminder_bp, url_prefix='/api')
    app.register_blueprint(market_prices_bp, url_prefix='/api')
    app.register_blueprint(soil_prediction_bp, url_prefix='/api')
    app.register_blueprint(satellite_monitor_bp, url_prefix='/api')
    app.register_blueprint(chatbot_bp, url_prefix='/api')
    app.register_blueprint(news_bp, url_prefix='/api')
    app.register_blueprint(schemes_bp, url_prefix='/api')
    app.register_blueprint(irrigation_bp, url_prefix='/api')
    app.register_blueprint(store_bp, url_prefix='/api')
    app.register_blueprint(calendar_bp, url_prefix='/api')
    app.register_blueprint(yield_prediction_bp, url_prefix='/api')
    app.register_blueprint(community_bp, url_prefix='/api/community')
    app.register_blueprint(rental_bp, url_prefix='/api/rental')
    app.register_blueprint(seasonal_planning_bp, url_prefix='/api')
    app.register_blueprint(wallet_bp, url_prefix='/api')

    # Routes to serve frontend HTML
    @app.route('/')
    def index():
        return render_template('login.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/otp-verification')
    def otp_verification():
        return render_template('otp_verification.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/upload')
    def upload():
        return render_template('upload.html')

    @app.route('/result')
    def result():
        return render_template('result.html')

    @app.route('/weather')
    def weather():
        return render_template('weather.html')

    @app.route('/history')
    def history():
        return render_template('history.html')

    @app.route('/reminder')
    def reminder():
        return render_template('reminder.html')

    @app.route('/emergency')
    def emergency():
        return render_template('emergency.html')

    @app.route('/chatbot')
    def chatbot_page():
        return render_template('chatbot.html')

    @app.route('/calculators')
    def calculators():
        return render_template('calculators.html')

    @app.route('/news')
    def agric_news():
        return render_template('news.html')

    @app.route('/schemes')
    def schemes():
        return render_template('schemes.html')

    @app.route('/irrigation')
    def irrigation():
        return render_template('irrigation.html')

    @app.route('/store')
    def store():
        return render_template('store.html')

    @app.route('/calendar')
    def crop_calendar():
        return render_template('crop_calendar.html')

    @app.route('/yield')
    def yield_page():
        return render_template('yield_prediction.html')

    @app.route('/field-map')
    def field_map():
        return render_template('field_map.html')

    @app.route('/profit')
    def profit():
        return render_template('profit.html')

    @app.route('/community')
    def community():
        return render_template('community_forum.html')

    @app.route('/rental')
    def rental():
        return render_template('equipment_rental.html')

    @app.route('/farmer-chat')
    def farmer_chat():
        return render_template('farmer_chat.html')

    @app.route('/market')
    def market_page():
        return render_template('market.html')

    @app.route('/seasonal-planning')
    def seasonal_planning():
        return render_template('seasonal_planning.html')

    @app.route('/profile')
    def profile():
        return render_template('profile.html')

    @app.route('/wallet')
    def wallet():
        return render_template('wallet.html')

    @app.route('/storage/uploads/<path:filename>')
    def protected_uploads(filename):
        # Prevention of direct unauthorized access can be added here
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
