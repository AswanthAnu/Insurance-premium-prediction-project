from Insurance.pipeline.batch_prediction import start_batch_prediciton
from Insurance.pipeline.training_pipeline import start_training_pipeline

# file_path = r"C:\Users\aswan\Documents\Insurance premium prediction\Insurance-premium-prediction-project\medicall.csv"

if __name__ == "__main__":
    try:
        output = start_training_pipeline()
        print(output)
        # output = start_batch_prediciton(input_file_path=file_path)
    except Exception as e:
        print(e)
