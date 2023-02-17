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
from Insurance.predictor import ModelResolver
from Insurance.logger import logging
from Insurance.utils import load_object
from Insurance.config import TARGET_COLUMN


class ModelEvaluation:
    def __init__(self, model_evaluation_config:config_entity.ModelEvaluationConfig,
                data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact,
                model_trainer_artifact:artifact_entity.ModelTrainerArtifact):

        try:
            self.model_evaluation_config = model_evaluation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver()

        except Exception as e:
            raise InsuranceException(e, sys)

        
    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            latest_dir_path = self.model_resolver.get_latest_dir_path()

            if latest_dir_path == None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, improved_accuracy=None)
                logging.info(f"Model evaluation artifact: {model_eval_artifact}")
                return model_eval_artifact

            # path of previous model
            transformer_path = self.model_resolver.get_latest_transfomer_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_encoder_path = self.model_resolver.get_latest_save_target_encoder_path()

            # previous model
            transformer = load_object(file_path=transformer_path)
            model = load_object(file_path=model_path)
            target_encoder = load_object(file_path=target_encoder_path)

            # path of current model
            current_transformer_path = self.data_transformation_artifact.transform_object_path
            current_model_path = self.model_trainer_artifact.model_path
            current_target_encoder_path = self.data_transformation_artifact.target_encoder_path

            # current model
            current_transformer = load_object(file_path=current_transformer_path)
            current_model = load_object(file_path=current_model_path)
            current_target_encoder = load_object(file_path=current_target_encoder_path)

            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df = test_df[TARGET_COLUMN]
            y_true = target_df

            input_feature_name = list(transformer.feature_names_in_)
            for i in input_feature_name:
                if test_df[i].dtypes == 'O':
                    test_df[i] = target_encoder.fit_transform(test_df[i])

            input_arr = transformer.transform(test_df[input_feature_name])
            y_pred = model.predict(input_arr)

            input_arr = current_transformer.tranform(test_df[input_feature_name])
            current_y_pred = current_model.predict(input_arr)
        
            previous_mdoel_score = r2_score(y_true, y_pred) # accuracy of old model 
            logging.info(f"Accuracy of previous trained mdoel:{previous_mdoel_score}")
            
            current_model_score = r2_score(y_true, current_y_pred) # accuracy of new model
            logging.info(f"Accuracy of new trained mdoel:{current_model_score}")
            
            # comparison between new model and old model
            if current_model_score <= previous_mdoel_score:
                logging.info(f"Current model is not better than previous model")
                raise Exception("Current model is not better than previous model")
            
            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                                                                          improved_accuracy=current_model_score-previous_mdoel_score)
            
            return model_eval_artifact
        
        except Exception as e:
            raise InsuranceException(e, sys)