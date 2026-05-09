import os
import json
import base64
import httpx
from flask import Blueprint, request, jsonify, session, current_app
from werkzeug.utils import secure_filename
from groq import Groq
# Using the provided Groq API key (allows override via environment variable)
GROQ_API_KEY = os.environ.get(
    "GROQ_API_KEY", "")

chatbot_bp = Blueprint('chatbot', __name__)

# FIX: Explicitly disable proxies
client = Groq(
    api_key=GROQ_API_KEY,
    http_client=httpx.Client(proxy=None)
)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    # Handle multipart form data for multi-image support
    if request.is_json:
        data = request.get_json()
        user_msg = data.get('message', '')
        lang_code_pref = data.get('lang_code', 'en-US')
        is_voice = data.get('is_voice', False)
        images = []
    else:
        user_msg = request.form.get('message', '')
        lang_code_pref = request.form.get('lang_code', 'en-US')
        is_voice = request.form.get('is_voice', 'false').lower() == 'true'
        images = request.files.getlist('images')

    if not user_msg.strip() and not images:
        return jsonify({"reply": "", "lang_code": "en-US"}), 200

    try:
        # Initialize session history if not exists
        if 'chat_history' not in session:
            session['chat_history'] = []

        # Context management: check for explicit reset
        lower_msg = user_msg.lower()
        if any(cmd in lower_msg for cmd in ["clear chat", "reset chat", "restart conversation"]):
            session['chat_history'] = []

        if "headache" in lower_msg or "pain" in lower_msg:
            # Safety check, but don't return early unless it's just a health query
            pass

        # Specialized Agricultural Knowledge Injection
        system_instruction = (
            f"You are 'Smart AI Farm Assistant', an expert agricultural scientist. "
            f"MANDATORY: You MUST reply in the language matching code: {lang_code_pref}. "
            f"If 'ta-IN', use Tamil. If 'hi-IN', use Hindi. If 'en-US', use English.\n"
            "YOUR KNOWLEDGE BASE:\n"
            "- PLANT PARTS: You are an expert in diagnosing issues across leaves, fruits, stems, and roots.\n"
            "- ROOT ISSUES: Can handle root rot, nematodes, and soil-borne pathogens.\n"
            "- STEM ISSUES: Expert in borers, cankers, and vascular wilts.\n"
            "- FRUIT/LEAF: Expert in blights, mildews, spots, and nutrient deficiencies.\n\n"
            "SUPPORTED CROPS DATASET: Paddy (Rice), Sugarcane, Banana, Coconut, Groundnut, Cotton, Maize (Corn), Ragi, Sorghum, Black Gram, Green Gram, Red Gram, Turmeric, Chilli, Onion, Potato, Tomato, Brinjal, Wheat.\n"
            "LANGUAGE RULES:\n"
            "1. DETECT language of user message.\n"
            "2. REPLY only in that exact language (Tamil -> Tamil, English -> English, etc.).\n"
            "3. If Hindi, use Devanagari script. If Tamil, use Tamil script.\n"
            "4. OUTPUT JSON: {\"reply\": \"...\", \"lang_code\": \"...\"}.\n"
            "5. Values for lang_code: 'ta-IN' for Tamil, 'en-US' for English, 'hi-IN' for Hindi, 'te-IN' for Telugu.\n"
            "TONE: Short, clear, factual, max 2 sentences.\n"
            "DO NOT use symbols like ** or ###."
        )

        content_parts = []
        if user_msg:
            content_parts.append({"type": "text", "text": user_msg})
        else:
            content_parts.append(
                {"type": "text", "text": "What do you see in these images?"})

        temp_paths = []
        vision_active = False

        if images and len(images) > 0 and images[0].filename != '':
            vision_active = True
            upload_dir = current_app.config.get('UPLOAD_FOLDER', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            for img_file in images:
                if img_file.filename:
                    filename = secure_filename(img_file.filename)
                    temp_path = os.path.join(
                        upload_dir, 'temp_chat_' + filename)
                    img_file.save(temp_path)
                    temp_paths.append(temp_path)
                    base64_image = encode_image(temp_path)
                    content_parts.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    })

        from typing import Any, Dict, List
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": system_instruction}]

        # Add history (last 5 messages for context)
        for hist in session['chat_history'][-5:]:
            messages.append({"role": hist['role'], "content": hist['content']})

        messages.append(
            {"role": "user", "content": content_parts if vision_active else user_msg})

        # Use Verified Groq models
        model_name = "llama-3.2-11b-vision-preview" if vision_active else "llama-3.3-70b-versatile"

        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model_name,
            temperature=0.3,
            max_tokens=600,
            response_format={"type": "json_object"}
        )

        raw_reply = chat_completion.choices[0].message.content.strip()

        # Clean possible markdown wrapping
        if "```json" in raw_reply:
            raw_reply = raw_reply.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_reply:
            raw_reply = raw_reply.split("```")[1].strip()

        data = json.loads(raw_reply)
        bot_reply = data.get("reply", "I am here to help.")
        lang_code = data.get("lang_code", "en-US")

        # Save to history
        session['chat_history'].append({"role": "user", "content": user_msg})
        session['chat_history'].append(
            {"role": "assistant", "content": bot_reply})
        session.modified = True

    except Exception as e:
        print("Chatbot error:", e)
        bot_reply = "I'm sorry, I'm having trouble connecting right now. Please try again."
        lang_code = "en-US"

    finally:
        if 'temp_paths' in locals():
            for tp in temp_paths:
                if os.path.exists(tp):
                    try:
                        os.remove(tp)
                    except:
                        pass

    return jsonify({"reply": bot_reply, "lang_code": lang_code}), 200
