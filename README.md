# 🛡️ Network Security Phishing Detection

A machine learning-powered phishing detection application that processes network-related data and classifies URLs or patterns to detect potential phishing threats.

---

## 📁 Project Structure

```
.
├── app.py                      # Flask app entry point
├── main.py / main2.py         # Scripts to trigger the pipeline
├── Dockerfile                 # For containerization
├── requirements.txt           # Python dependencies
├── .github/workflows/         # GitHub Actions CI/CD workflows
├── networksecurity/           # Core ML pipeline code
│   ├── cloud/                 # AWS S3 sync logic
│   ├── components/            # Data ingestion, transformation, validation, and model training
│   ├── constants/             # Pipeline-wide constants
│   ├── entity/                # Entity and artifact definitions
│   ├── exception/             # Custom exception class
│   ├── logging/               # Logger utility
│   ├── pipeline/              # Entry points for training/prediction
│   ├── utils/                 # Helper functions
│   └── ml_utils/              # Model evaluation and scoring
├── templates/                 # HTML template for output table
├── prediction_output/         # Stores model predictions (e.g., output.csv)
├── valid_data/                # Stores valid input data (e.g., test.csv)
├── phisingData.csv            # Original training dataset
├── best_model.joblib          # Serialized trained model
```

---

## 🚀 How to Run the Project Locally

### 🔧 1. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 📦 2. Install requirements
```bash
pip install -r requirements.txt
```

### 🧪 3. Run the pipeline
```bash
python main.py
```

### 🌐 4. Launch the Flask app
```bash
python app.py
```

Once running, navigate to: [http://localhost:8000](http://localhost:8000)

---

## 🐳 Docker Support

You can also containerize the app using Docker:

```bash
docker build -t networksecurity .
docker run -d -p 8000:8000 --name networksecurity networksecurity
```

---

## 🔁 CI/CD – Fully Automated with GitHub Actions

This project uses **GitHub Actions** to automatically handle:

1. **Continuous Integration (CI)**
   - Triggered when code is pushed to the `main` branch
   - Runs basic linting and placeholder unit tests

2. **Continuous Delivery (CD)**
   - **Builds the Docker image** from your codebase
   - **Pushes the image to AWS Elastic Container Registry (ECR)**
   - **Deploys the image** on a self-hosted GitHub Actions runner (EC2)

All steps—from code commit to running the updated container—are handled **without manual intervention**.

### 💡 How it works

1. Developer pushes code → triggers GitHub Actions
2. Workflow:
   - Cleans up disk space
   - Logs into AWS
   - Builds and pushes Docker image
   - SSHs into EC2 self-hosted runner
   - Stops old container and runs the new one with latest image

✅ You **don’t need AWS CLI manually on EC2** — it’s handled by the GitHub workflow.

---

## 📊 Data Source

The model is trained using the `phisingData.csv` dataset which includes labeled examples of phishing indicators across multiple features.

---

## 📬 Contact

Created with ❤️ by Ashrit Wajjala  
For questions or feedback, feel free to reach out on [LinkedIn](https://www.linkedin.com/in/ashritwajjala/)

