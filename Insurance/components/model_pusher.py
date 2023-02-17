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
from Insurance.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ModelPushArtifact
from Insurance.entity.config_entity import ModelPusherConfig
from Insurance.predictor import ModelResolver
from Insurance.utils import load_object, save_object

class ModelPusher:
    def __init__(self, model_pusher_config:ModelPusherConfig, data_transformation_artifact:DataTransformationArtifact,
                 model_trainer_artifact:ModelTrainerArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver(model_registry = self.model_pusher_config.saved_model_dir)  

        except Exception as e:
            raise InsuranceException(e, sys)
        
    def initiate_model_pusher(self)->ModelPushArtifact:

        try:
            transfomer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            model = load_object(file_path=self.model_trainer_artifact.model_path)
            target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)

            save_object(file_path=self.model_pusher_config.pusher_transfomer_path, obj=transfomer)
            save_object(file_path=self.model_pusher_config.pusher_model_path, obj=model)
            save_object(file_path=self.model_pusher_config.pusher_target_encoder_path, obj=target_encoder)

            transform_path = self.model_resolver.get_latest_save_transformer_path()
            model_path = self.model_resolver.get_latest_save_model_path()
            target_encoder_path = self.model_resolver.get_latest_save_target_encoder_path()

            save_object(file_path=transform_path, obj=transfomer)
            save_object(file_path=model_path, obj=model)
            save_object(file_path=target_encoder_path, obj=target_encoder)

            model_pusher_artifact = ModelPushArtifact(pusher_model_dir=self.model_pusher_config.pusher_model_dir,
                                                      saved_model_dir=self.model_pusher_config.saved_model_dir)
            
            return model_pusher_artifact

        except Exception as e:
            raise InsuranceException(e, sys)