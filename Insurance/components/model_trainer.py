from Insurance.entity import artifact_entity, config_entity
from Insurance.exception import InsuranceException
import sys
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer 
from sklearn.preprocessing import RobustScaler
from Insurance.config import TARGET_COLUMN
from sklearn.preprocessing import LabelEncoder
from Insurance import utils 
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score




class ModelTrainer:
    def __init__(self, model_trainer_config:config_entity.ModelTrainingConfig,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact):
                
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transfomation_artifact = data_transformation_artifact
        except Exception as e:
            raise InsuranceException(e, sys)

    def train_model(self, X, y):
        try:
            lr = LinearRegression()
            lr.fit(X, y)
            return lr
        except Exception as e:
            raise InsuranceException(e, sys)

    def initiate_model_trainer(self,)->artifact_entity.ModelTrainerArtifact:
        try:
            train_arr = utils.load_numpy_array_data(file_path=self.data_transfomation_artifact.transformed_train_path)
            test_arr = utils.load_numpy_array_data(file_path=self.data_transfomation_artifact.transformed_test_path)
        
            x_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            x_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            model = self.train_model(x_train, y_train)

            yhat_train = model.predict(x_train)
            r2_train_score = r2_score(y_train, yhat_train)

            yhat_test = model.predict(x_test)
            r2_test_score = r2_score(y_test, yhat_test)

            if r2_test_score < self.model_trainer_config.expected_accuracy:
                raise Exception(f"Model is not good as it is not able to give expected accurarcy:\
                    {self.model_trainer_config.expected_accuracy}: model actual accuracy:{r2_test_score}")

            diff = abs(r2_test_score - r2_train_score)
            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train model and test score diff:{diff} is more than overfitting threshold {self.model_trainer_config.overfitting_threshold}")

            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)
            
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path,
                        r2_train_score=r2_train_score, r2_test_score=r2_test_score)

            return model_trainer_artifact

        except Exception as e:
            raise InsuranceException(e, sys)