# ♻️ AI Recycling System

### **YOLOv11-based Smart Waste Detection | FastAPI Backend | Streamlit Frontend**

This project is an end-to-end intelligent waste detection system powered by a **custom-trained YOLOv11 model**.  
It includes:

- ✔️ YOLOv11 model trained on 6 garbage classes  
- ✔️ FastAPI backend for image classification & batch processing  
- ✔️ Streamlit frontend for easy visualization  
- ✔️ Annotated images with bounding boxes  
- ✔️ Automatic recycling tips & waste categorization  

---

## Technologies Used

- **Backend:** Python, FastAPI, Pydantic
- **Frontend:** Streamlit
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

## Model Training

Training is done using Ultralytics YOLOv11n:

~~~python
import os
from ultralytics import YOLO

model = YOLO("yolo11n.pt")
results = model.train(
    data="./dataset/data.yaml",
    epochs=100
)
~~~

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/KHbo7mid/ai_recycling_system.git
cd ai_recycling_system
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate     # Windows
```

3. **Create a .env file**

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
## API Endpoints

* Health Check
| Method | Endpoint      | Description      |
| ------ | ------------- | ---------------- |
| GET    | `/api/health` | API availability |

* Classification

| Method | Endpoint                       | Description                       |
| ------ | ------------------------------ | --------------------------------- |
| POST   | `/api/classify`                | Classify a single image           |
| POST   | `/api/classify/annotate-image` | Return annotated image with boxes |

* Batch Classification

| Method | Endpoint              | Description              |
| ------ | --------------------- | ------------------------ |
| POST   | `/api/batch_classify` | Classify multiple images |

* Helper Routes

| Method | Endpoint               | Description                       |
| ------ | ---------------------- | --------------------------------- |
| GET    | `/api/recycling-guide` | Retrieve recycling tips           |
| GET    | `/api/classes`         | Get supported classes information |


## 👤 Author
### Ahmed Khiari 
AI & Software Engineer
AI recycling system --2025