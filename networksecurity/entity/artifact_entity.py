from dataclasses import dataclass
from typing import Any

@dataclass
class DataIngestionArtifact:
    training_file_path: str
    testing_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: Any
    valid_test_file_path: Any
    invalid_train_file_path: Any
    invalid_test_file_path: Any
    drift_report_file_path: Any