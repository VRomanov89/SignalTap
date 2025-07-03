# SignalTap - Modern PLC Tag Management & Monitoring

A full-stack web application for live monitoring and management of PLC (Programmable Logic Controller) tags.  
**Backend:** FastAPI (Python)  
**Frontend:** React (Vite) + Material-UI (MUI)  
**Branding:** Custom logo, vibrant palette, professional footer with LinkedIn and Joltek links.

---

## 🚀 Features

- **Live Tag Value Updates:** Real-time polling and display of tag values.
- **Modern UI/UX:** Responsive, accessible, and dark-themed interface using Material-UI.
- **Tag Filtering & Search:** Instantly filter tags by name or hide unreadable tags.
- **Easy PLC Connection:** Connect to Rockwell Allen-Bradley CompactLogix PLCs.
- **REST API:** Modern, documented endpoints for tag scanning, reading, writing, and PLC info.
- **Professional Branding:** Custom SVG logo, favicon, and footer with personal/company links.

---

## 📦 Requirements

- Python 3.10+
- Node.js 18+
- Network access to Rockwell Allen-Bradley CompactLogix PLCs

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/VRomanov89/SignalTap.git
cd SignalTap
```

### 2. Backend Setup

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/macOS

pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

---

## 🚦 Running the App

### Backend

```bash
# From project root
.venv\Scripts\activate  # Windows
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend

```bash
cd frontend
npm run dev
```

---

## 🌐 Usage

- Open your browser to [http://localhost:5173](http://localhost:5173) for the frontend UI.
- API docs available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 🏗️ Project Structure

```
app/         # FastAPI backend
frontend/    # React + MUI frontend
```

---

## 👤 Author & Links

- **Vladimir Romanov**  
  [LinkedIn](https://www.linkedin.com/in/vladromanov/)  
  [Joltek](https://joltek.com/)

---

## 📄 License

MIT License

--- 