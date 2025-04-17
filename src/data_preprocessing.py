import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_funtion import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE



logger = get_logger(__name__)

class DataProcessor:

    def __init__(self, train_path, test_path, processed_dir,config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
            logger.info(f"self.processed_dir is created")
    
    def preprocess_data(self, df):
        try:
            logger.info("Starting our Data Processing step")
            logger.info("dropping columns")
            df.drop(columns=["Unnamed: 0","Booking_ID"],inplace=True)
            logger.info("dropping duplicates")
            df.drop_duplicates(inplace=True)

            logger.info("fetching columns")

            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config["data_processing"]["numerical_columns"]

            logger.info("Applying Lable Encoding")

            mappings = {}
            label_encoder = LabelEncoder()

            for col in cat_cols:
                label_encoder = LabelEncoder()
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = {
                    (label.item() if isinstance(label, np.generic) else label):
                    int(code)
                    for label, code in zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))
                }
            logger.info("label mapping are : ")
            for col, mapping in mappings.items():
                logger.info(f"{col}: {mapping}")

            logger.info("Handeling Skewness")

            skewness_threshold = self.config["data_processing"]["skewness_threshold"]
            skewness = df[num_cols].apply(lambda x:x.skew())


            for column in skewness[skewness > skewness_threshold].index:
                df[column] = np.log1p(df[column])

            return df
        
        except Exception as e:
            logger.info(f"Error during preprocess step {e}")
            raise CustomException("Error while preprocessing data", e)
        
    def balance_data(self, df):

        try:
            logger.info("Handeling Imbalance Data")
            X = df.drop(columns="booking_status")
            y = df["booking_status"]
            smote = SMOTE(random_state= self.config["data_processing"]["random_state"])
            X_resampled, y_resampled = smote.fit_resample(X,y)

            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df["booking_status"] = y_resampled

            logger.info("data balanced successfully")
            return balanced_df

        except Exception as e:
            logger.info(f"Error during balancing step {e}")
            raise CustomException("Error while balancing data", e)
        
    
    def feature_selection(self, df):

        try:

            logger.info("starting our featear selection step")

            X = df.drop(columns="booking_status")
            y = df["booking_status"]

            model = RandomForestClassifier(random_state=32)
            model.fit(X,y)

            feature_importance = model.feature_importances_

            feautre_importance_df = pd.DataFrame({
                                        'feature': X.columns,
                                        'importance':feature_importance
                                    })
            
            top_imporatance_features_df = feautre_importance_df.sort_values(by="importance", ascending=False)

            top_10_features = top_imporatance_features_df["feature"].head(self.config["data_processing"]["number_of_feature"]).values

            logger.info(f"Top 10 feature {top_10_features}")

            top_10_df = df[top_10_features.tolist() + ["booking_status"]]

            logger.info("Feature selectin completedd successfully")

            return top_10_df


        except Exception as e:
            logger.info(f"Error during feature selection step {e}")
            raise CustomException("Error while feature selection", e)
        
    def save_data(self, df, file_path):

        try:
            logger.info("saving the data in a processed folder")

            df.to_csv(file_path, index = False)

            logger.info(f"Data saved succesfully to {file_path}")
        
        except Exception as e:
            logger.info(f"Error during saving data {e}")
            raise CustomException("Error while saving data", e)
        
    def process(self):

        try:

            logger.info("loading data from RAW directory")
            
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)

            train_df = self.feature_selection(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df,PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df,PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing completed successfully")
        
        except Exception as e:
            logger.info(f"Error during preprocessing pipeline {e}")
            raise CustomException("Error while preprocessing data", e)
        


if __name__ == "__main__":
    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()




            







