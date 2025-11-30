# AI Recycling System

A web-based application for automatic garbage classification using AI. Users can upload images of waste items, and the system detects, classifies, and provides recycling recommendations. The system also supports batch image processing and annotated images with bounding boxes.

---

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Frontend](#frontend)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- Classify individual images of waste items.
- Batch classification for multiple images at once.
- Annotated images with bounding boxes for detected objects.
- Waste category detection: Recyclable, Biodegradable, Non-Recyclable.
- Recycling recommendations based on detected items.
- Streamlit-based frontend for easy visualization.
- REST API using FastAPI.

---

## Technologies Used

- **Backend:** Python, FastAPI, Pydantic
- **Frontend:** Streamlit, Plotly (for optional visualizations)
- **AI Model:** YOLO-based classifier or custom CNN for garbage detection
- **Image Processing:** OpenCV, NumPy, Pillow
- **Deployment:** Uvicorn (ASGI server)

---

## 📦 Dataset

This project uses a **custom garbage classification dataset** containing **6 waste categories**:

- **Plastic**
- **Metal**
- **Glass**
- **Biodegradable**
- **Paper**
- **Cardboard**

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/KHbo7mid/ai_recycling_system.git
cd ai_recycling_system
```
2.  **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate     # Windows
```
3.  **Create a .env file**

```bash
cp .env.example .env 
```
4. **Install dependencies**
* install backend requirements

```bash
cd src
pip install -r requirements.txt 
```
* install frontend requirements
```bash
cd frontend
pip install -r requirements.txt 
```

5. **Run the backend server**
```bash
cd src
uvicorn src.main:app --reload
```

6. **Run the frontend**

```bash
cd frontent
streamlit run app.py
```