import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import  *
from utils.common_funtion import read_yaml

logger = get_logger(__name__)

class DataIngestion:

    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.bucket_file_name = self.config["bucket_file_name"]
        self.train_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info(f"Data ingestion started with {self.bucket_name} with  filename {self.bucket_file_name}")

    
    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)

            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"Raw file is successfully downloaded to {RAW_FILE_PATH}")

        except Exception as e:

            logger.error("Error while downloading the csv file")
            raise CustomException("Failed to downlaod the csv file ", e)
        
    def split_data(self):
        try:
            logger.info("Staring the spliting process")
            data = pd.read_csv(RAW_FILE_PATH)

            train_data, test_data =  train_test_split(data, test_size=1-self.train_ratio,random_state=34)

            train_data.to_csv(TRAIN_FILE_PATH)
            logger.info(f"Train data saved to {TRAIN_FILE_PATH}")

            test_data.to_csv(TEST_FILE_PATH)
            logger.info(f"Test data saved to {TEST_FILE_PATH}")

        except Exception as e:

            logger.error("Error while Spliting Data")
            raise CustomException("Failed to split the Data into Train and Test ", e)
        
    def run(self):

        try:
            logger.info("Starting Data Ingestion process")

            self.download_csv_from_gcp()
            self.split_data()

            logger.info("Data Ingestion completed successfully")

        except Exception as ce:
            logger.error(f"Custom Exception : {str(ce)}")

        finally:
            logger.info("Data Ingestion completed")


if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()


