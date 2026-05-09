import streamlit as st
import json
import base64
import re
from groq import Groq

# --- MEDICINE DATABASE (AS REQUESTED) ---
MEDICINE_DB = {
    "Tomato": {
        "Early Blight": {"med": "Mancozeb 75% WP", "treat": "Remove infected leaves and apply fungicide."},
        "Late Blight": {"med": "Metalaxyl", "treat": "Improve drainage and spray Metalaxyl fungicide."},
        "Leaf Mold": {"med": "Chlorothalonil", "treat": "Reduce humidity and apply Chlorothalonil spray."},
        "Fruit Borer": {"med": "Emamectin Benzoate", "treat": "Use pheromone traps and spray insecticide."}
    },
    "Brinjal": {
        "Shoot Borer": {"med": "Spinosad", "treat": "Prune infested shoots and apply Spinosad."},
        "Little Leaf": {"med": "Imidacloprid", "treat": "Remove affected plants and control vectors with Imidacloprid."}
    },
    "Potato": {
        "Late Blight": {"med": "Metalaxyl", "treat": "Destroy infected tubers and apply copper-based fungicide."}
    },
    "Corn": {
        "Leaf Blight": {"med": "Propiconazole", "treat": "Apply Propiconazole fungicide at first sign of spots."},
        "Armyworm": {"med": "Chlorantraniliprole", "treat": "Regular scouting and application of Chlorantraniliprole."}
    },
    "Rice": {
        "Blast": {"med": "Tricyclazole", "treat": "Avoid excessive nitrogen and apply Tricyclazole."},
        "Brown Spot": {"med": "Carbendazim", "treat": "Improve soil nutrition and spray Carbendazim."}
    },
    "Onion": {
        "Purple Blotch": {"med": "Mancozeb", "treat": "Ensure proper spacing and spray Mancozeb."}
    },
    "Sugarcane": {
        "Red Rot": {"med": "Carbendazim", "treat": "Use disease-free sets and drench soil with Carbendazim."}
    },
    "Banana": {
        "Sigatoka": {"med": "Propiconazole", "treat": "Improve drainage, remove infected leaves, spray Propiconazole."},
        "Panama Wilt": {"med": "Trichoderma Viride", "treat": "Quarantine area, apply Trichoderma bio-fungicide."}
    },
    "Coconut": {
        "Bud Rot": {"med": "Copper Oxychloride", "treat": "Cut and burn infected tissues, apply Bordeaux paste."}
    },
    "Groundnut": {
        "Tikka Disease": {"med": "Chlorothalonil", "treat": "Crop rotation and spray Chlorothalonil."}
    },
    "Cotton": {
        "Bollworm": {"med": "Chlorantraniliprole", "treat": "Use pheromone traps and apply specific insecticides."}
    },
    "Maize": {
        "Leaf Blight": {"med": "Propiconazole", "treat": "Apply Propiconazole fungicide at first sign of spots."},
        "Armyworm": {"med": "Chlorantraniliprole", "treat": "Regular scouting and application of Chlorantraniliprole."}
    },
    "Ragi": {
        "Blast": {"med": "Tricyclazole", "treat": "Use resistant varieties and spray Tricyclazole."}
    },
    "Sorghum": {
        "Shoot Fly": {"med": "Imidacloprid", "treat": "Early sowing and seed treatment with Imidacloprid."}
    },
    "Gram": {
        "Yellow Mosaic": {"med": "Thiamethoxam", "treat": "Control vectors with Thiamethoxam."},
        "Pod Borer": {"med": "Emamectin Benzoate", "treat": "Monitor with pheromone traps and spray."}
    },
    "Turmeric": {
        "Leaf Spot": {"med": "Mancozeb", "treat": "Ensure good drainage and spray Mancozeb."}
    },
    "Chilli": {
        "Leaf Curl": {"med": "Diafenthiuron", "treat": "Uproot infected plants and control whiteflies."}
    },
    "Paddy": {
        "Blast": {"med": "Tricyclazole", "treat": "Avoid excessive nitrogen and apply Tricyclazole."},
        "Brown Spot": {"med": "Carbendazim", "treat": "Improve soil nutrition and spray Carbendazim."}
    }
}

# Configuration
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Smart AI Farm Analyst", layout="wide")

st.title("🌱 Smart AI Crop Disease & Pest Detection")
st.write("Universal Analysis for Leaf, Fruit, Whole Plant, Stem, and Roots")

uploaded_file = st.file_uploader("Upload an image for analysis...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display Image
    cols = st.columns([1, 1])
    with cols[0]:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    
    with cols[1]:
        with st.spinner("Executing 3-Stage AI Analysis..."):
            # Encode for API
            base64_image = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
            
            # --- 3-STAGE PROMPT LOGIC ---
            prompt = """
            STAGE 1: Part Detection (Leaf, Fruit, Whole Plant, Stem, Root).
            STAGE 2: Crop ID (Tomato, Brinjal, Potato, Paddy, Rice, Wheat, Corn, Maize, Onion, Sugarcane, Banana, Coconut, Groundnut, Cotton, Ragi, Sorghum, Gram, Turmeric, Chilli).
            STAGE 3: Diagnosis (Find Disease/Pest or Healthy).

            Output ONLY valid JSON:
            {
              "part": "string",
              "crop": "string",
              "status": "Healthy/Disease/Pest",
              "diagnosis": "Name of disease or pest or 'Healthy'",
              "confidence": float
            }
            """
            
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}],
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    temperature=0.1
                )
                
                content = response.choices[0].message.content
                match = re.search(r'\{.*\}', content, re.DOTALL)
                if match:
                    res = json.loads(match.group())
                else:
                    raise ValueError("Could not parse JSON from response")
                
                crop = res.get('crop', 'Unknown')
                part = res.get('part', 'Unknown')
                diagnosis = res.get('diagnosis', 'Healthy')
                confidence = res.get('confidence', 95.0)
                status = res.get('status', 'Healthy')
                
                # Fetch Medicine and Treatment
                med_info = MEDICINE_DB.get(crop, {}).get(diagnosis, {"med": "Consult Expert", "treat": "Monitor plant health and consult a local agricultural officer."})
                
                # --- STRICTOR FORMAT OUTPUT (AS REQUESTED) ---
                st.subheader("🎯 Analysis Results")
                
                if status == "Healthy":
                    st.success(f"🌱 Crop: {crop}\n\n🌿 Part: {part}\n\n✅ Status: Healthy\n\n📊 Confidence: {confidence}%")
                    st.info("✔ No treatment needed.")
                else:
                    st.error(f"🌱 Crop: {crop}\n\n🌿 Part: {part}")
                    if status == "Disease":
                        st.write(f"🦠 Disease: {diagnosis}")
                        st.write(f"🐛 Pest: None")
                    else:
                        st.write(f"🦠 Disease: None")
                        st.write(f"🐛 Pest: {diagnosis}")
                    
                    st.write(f"📊 Confidence: {confidence}%")
                    
                    st.markdown("---")
                    st.warning(f"💊 **Treatment:**\n{med_info['treat']}")
                    st.info(f"🧴 **Medicine:**\n{med_info['med']}")
                    
                    buy_link = f"https://www.amazon.in/s?k={med_info['med'].replace(' ', '+')}"
                    st.link_button("🛒 Buy Now on Amazon", buy_link)

            except Exception as e:
                st.error(f"Analysis Failed: {str(e)}")
                st.write("Please ensure the image is clear and focused on the plant part.")
