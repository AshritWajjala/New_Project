# 🛡️ Network Security - Phishing Detection & Response

This project is a containerized FastAPI application designed to detect phishing websites using machine learning. It automates the entire process — from data ingestion and model training to prediction, visualization, and deployment on AWS using GitHub Actions.

---

## 📁 Project Structure

```
.
├── app.py
├── main.py
├── requirements.txt
├── Dockerfile
├── networksecurity/
│   ├── cloud/
│   ├── components/
│   ├── constants/
│   ├── entity/
│   ├── exception/
│   ├── logging/
│   ├── ml_utils/
│   ├── pipeline/
│   ├── utils/
├── prediction_output/
├── valid_data/
├── templates/
├── .github/workflows/main.yml   # CI/CD pipeline
└── phisingData.csv              # Raw phishing dataset
```

---

## ⚙️ Setup Instructions (Local)

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/networksecurity.git
   cd networksecurity
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/Mac
   venv\Scripts\activate.bat   # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

---

## 🐳 Docker Usage

### Build Docker Image
```bash
docker build -t networksecurity:latest .
```

### Run Docker Container
```bash
docker run -d -p 8000:8000 --name networksecurity networksecurity:latest
```

---

## 🚀 CI/CD with GitHub Actions + AWS ECR + EC2

- CI: Code is linted and unit-tested on every push to `main`.
- CD: The Docker image is built and pushed to AWS ECR.
- Deployment: A self-hosted EC2 runner pulls the image and serves the FastAPI app inside a container.

### Secrets Needed

Make sure the following secrets are configured in your GitHub repository:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `AWS_ECR_LOGIN_URI`
- `ECR_REPOSITORY_NAME`

---

## 📊 MLflow & DagsHub Integration

This project uses **MLflow** for:
- Experiment tracking
- Model versioning
- Comparing evaluation metrics

And **DagsHub** for:
- Hosting MLflow logs and artifacts remotely
- Visualizing experiments and model performance
- Collaborating in a Git-style ML workflow

---

## 📊 Dataset

- **Source**: `phisingData.csv`
- **Goal**: Predict whether a URL is phishing (`0` or `1`) based on engineered features.

---

## 📬 Contact

For issues, suggestions or improvements:  
**Ashrit Wajjala**  
[LinkedIn](https://www.linkedin.com/in/ashritwajjala) | [GitHub](https://github.com/AshritWajjala)
