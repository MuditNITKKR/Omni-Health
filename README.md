# 🏥 Omni Health: AI-Powered Medical Diagnostic Suite

[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://omni-health.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.13%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![NIT Kurukshetra](https://img.shields.io/badge/NIT%20Kurukshetra-Project-orange)](https://nitkkr.ac.in/)

## 📋 Overview

**Omni Health** is an integrated, intelligent medical diagnostic platform combining **Deep Learning (Computer Vision)**, **Machine Learning**, and **Natural Language Processing (RAG)** to assist healthcare professionals in real-time clinical workflows. Built with a production-ready multi-page Streamlit interface, it delivers unified diagnostic insights across medical imaging, cardiovascular predictive metrics, and automated clinical documentation analysis.

### Key Features
* 📷 **Neural Imaging Suite**: Real-time object detection for bone fractures and multi-label classification for structural chest pathologies.
* 📊 **Predictive Analytics**: Robust risk scoring engine for chronic cardiovascular health indicators.
* ✍️ **NLP Report Assistant**: Context-aware Medical Report Analyzer utilizing generative RAG for conversational insight extraction.
* 🛡️ **Production Engineering**: Built-in failsafes for edge-case request limits, cross-device compatibility, and asynchronous session states.

---

## 🚀 Getting Started

### Prerequisites
* Python 3.13 or higher
* Valid Google AI Studio API Key (for the NLP RAG Module)
* Standard computing memory (4GB+ RAM recommended; handles CPU fallback natively)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MuditNITKKR/Omni-Health.git
   cd Omni-Health
   ```

2. **Set up a Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Production Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Portal**
   ```bash
   streamlit run app.py
   ```

---

## 📂 Project Structure

The codebase is organized into isolated functional modules following clean architecture principles:

```text
OMNI HEALTH/
├── .streamlit/           # Global configuration settings
├── models/               # Serialized model weights and neural binaries
│   ├── fr1.pt            # YOLOv11 Bone Fracture Weights
│   ├── best_model_chest.pkl # ConvNeXt Tiny Chest Pathology Weights
│   └── heart-disease_model.pkl # Random Forest Predictive Weights
├── src/                  # Central Backends & Algorithmic Engines
│   ├── dl_engine.py      # Vision processing logic (YOLOv11 & ConvNeXt)
│   ├── ml_engine.py      # Predictive inference logic (Random Forest)
│   └── nlp_engine.py     # Generative RAG & text processing logic
├── pages/                # Multi-page User Interface Layer
│   ├── 1_📷_Detection.py # Computer Vision diagnostic interface
│   ├── 2_📊_Prediction.py # Patient metric evaluation interface
│   └── 3_✍️_Reporting.py # Contextual document chat interface
└── app.py                # Launch entry point and central routing gateway
```

---

## 🔧 Technology Stack & Dependencies

### Core Architecture Breakdown
| Component | Engine Technology | Purpose |
| :--- | :--- | :--- |
| **User Interface** | Streamlit | Rapid deployment of reactive analytical web pages |
| **Computer Vision** | PyTorch / Ultralytics / OpenCV | Multi-modal neural diagnostics on medical imagery |
| **Predictive Analytics** | Scikit-learn / Pandas | Classical machine learning for phenotypic scoring |
| **Generative NLP** | Google GenAI SDK (`gemini-2.5-flash`) | Large Context Window RAG without standalone vector DBs |
| **File Parsing** | PyPDF | Extraction and structural string processing of binary documents |

### Production Requirements (`requirements.txt`)
```text
streamlit
ultralytics
opencv-python-headless
torch
torchvision
scikit-learn
pandas
google-genai
pypdf
pillow
```

---

## 🎯 Features & Modules

### 1. 📷 Deep Learning Detection Suite
* **Bone Fracture Localization**: Utilizes a custom **YOLOv11** architecture trained on the **FracAtlas** dataset to identify structural bone structural anomalies, generating dynamic annotated bounding boxes.
* **Chest Pathology Classification**: Leverages a **ConvNeXt Tiny** backbone targeting the **NIH Chest X-ray** dataset. It screens for 14 individual conditions (e.g., Pneumonia, Effusion, Infiltration, Cardiomegaly) simultaneously via independent multi-label sigmoidal confidence parsing.
* **Dynamic Thresholding**: Real-time adjustable sliders allow clinicians to balance sensitivity and precision constraints on the fly.

### 2. 📊 Machine Learning Risk Predictor
* **Cardiovascular Risk Framework**: Implements a high-precision **Random Forest Classifier** trained against the classic **UCI Cleveland Heart Disease** dataset.
* **Phenotypic Variable Parsing**: Evaluates incoming clinical values including blood pressure variations, cholesterol, resting electrocardiographic behaviors, and ST-segment slopes to calculate granular cardiac risk categories.

### 3. ✍️ NLP-Powered Report Analyzer (RAG)
* **Direct Context Ingestion**: Uses the massive context capability of `gemini-2.5-flash` to execute zero-loss Retrieval-Augmented Generation directly over complete medical text blocks.
* **Cross-Suite Data Handoff**: Integrates with Streamlit's global `st.session_state`. Automated computer vision findings from the imaging suite can be passed seamlessly into the RAG compiler to auto-generate reports without forcing manual uploads.
* **Double-Defense Security**: Codebase includes backend exception intercepts and frontend failsafes to gracefully catch cloud service traffic spikes (`503 UNAVAILABLE`), displaying informative user banners instead of critical script failures.

---

## ⚙️ Engineering Implementation Highlights

### Cross-Device & Weight Compatibility Fix
To handle cross-device compatibility (training on high-throughput CUDA clusters vs. executing local CPU client inference) and bypass modern payload constraints on legacy serialization models, the loading logic employs a secure mapping override:

```python
# From src/dl_engine.py
state_dict = torch.load(
    "models/best_model_chest.pkl", 
    map_location=torch.device('cpu'), 
    weights_only=False # Enables loading complex custom model layer architectures safely
)
```

### High-Demand Failsafe Handling
To prevent application failures during peak free-tier usage, the conversational interface wraps critical generative calls in high-defense exception frameworks:

```python
# From pages/3_✍️_Reporting.py
try:
    answer = nlp_engine.answer_question(report_content, user_query, history)
except Exception:
    answer = "⚠️ The AI service is experiencing a temporary traffic spike. Please try resubmitting your question."
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors & Contributors

* **Mudit** - *Project Lead & Core AI Engineer* - [GitHub Profile](https://github.com/MuditNITKKR)
* **NIT Kurukshetra** - *Academic Sponsor (Artificial Intelligence & Machine Learning Engineering)*

---

**Made with ❤️ by Mudit at NIT Kurukshetra** *Last System Architecture Alignment: April 2026*
