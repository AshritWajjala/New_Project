import mlflow
import dagshub

dagshub.init(repo_owner='AshritWajjala', repo_name='New_Project', mlflow=True)
mlflow.set_tracking_uri("https://dagshub.com/AshritWajjala/New_Project.mlflow")

mlflow.set_experiment("dagshub_test")

with mlflow.start_run():
    mlflow.log_metric("accuracy", 0.95)
