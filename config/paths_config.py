from pathlib import Path

# Go up to project root
BASE_DIR = Path(__file__).resolve().parents[1]

################# DATA INGESTION #######################
RAW_DIR = BASE_DIR / "artifacts" / "raw"
RAW_FILE_PATH = RAW_DIR / "raw.csv"
TRAIN_FILE_PATH = RAW_DIR / "train.csv"
TEST_FILE_PATH = RAW_DIR / "test.csv"
CONFIG_PATH = BASE_DIR / "config" / "config.yaml"

################# DATA PROCESSING #######################
PROCESSED_DIR = BASE_DIR / "artifacts" / "processed"
PROCESSED_TRAIN_DATA_PATH = PROCESSED_DIR / "processed_train.csv"
PROCESSED_TEST_DATA_PATH = PROCESSED_DIR / "processed_test.csv"

################# MODEL TRAINING #######################
MODEL_OUTPUT_PATH = BASE_DIR / "artifacts" / "model" / "lgbm_model.pkl"

