import joblib
import pandas as pd
from typing import Dict
import logging
from pathlib import Path

from app.core.config import settings

logger = logging.getLogger(__name__)


class ModelService:

    def __init__(self):
        self.model = None
        self.feature_columns = None

    def load_model(self)->None:
        try:
            model_path = Path(settings.MODEL_PATH)

            if not model_path.exists():
                raise FileNotFoundError(f"Model file not found at {model_path}")

            self.model = joblib.load(model_path)

            self.feature_columns = list(self.model.feature_names_in_)

            logger.info(f"Model loaded successfully from {model_path}")
            logger.info(f"Expected features: {len(self.feature_columns)} columns")
            logger.info(f"List of features: {self.feature_columns}")

        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise


    def prepare_input(self, input_data: Dict) -> pd.DataFrame:
        try:
            df = pd.DataFrame([{
                'longitude': input_data['longitude'],
                'latitude': input_data['latitude'],
                'housing_median_age': input_data['housing_median_age'],
                'total_rooms': input_data['total_rooms'],
                'total_bedrooms': input_data['total_bedrooms'],
                'population': input_data['population'],
                'households': input_data['households'],
                'median_income': input_data['median_income'],
                'ocean_proximity': input_data['ocean_proximity']
            }])
            df = pd.get_dummies(df, columns=['ocean_proximity'])
            for col in self.feature_columns:
                if col not in df.columns:
                    df[col] = 0
            df = df[self.feature_columns]

            return df

        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            raise ValueError(f"Missing required field: {e}")
        except Exception as e:
            logger.error(f"Error preparing input: {e}")
            raise

    def predict(self, input_data: Dict) -> float:
        if self.model is None:
            raise RuntimeError("Model not loaded")

        try:
            df = self.prepare_input(input_data)
            prediction = self.model.predict(df)
            return float(prediction[0])

        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise

    def is_loaded(self) -> bool:
        return self.model is not None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    service = ModelService()
    service.load_model()

    test_input = {
        "longitude": -122.64,
        "latitude": 38.01,
        "housing_median_age": 36.0,
        "total_rooms": 1336.0,
        "total_bedrooms": 258.0,
        "population": 678.0,
        "households": 249.0,
        "median_income": 5.5789,
        "ocean_proximity": 'NEAR OCEAN'
    }

    print("\n Model loaded:", service.is_loaded())
    df = service.prepare_input(test_input)
    print("\nPrepared input shape:", df.shape)
    print("Columns:", list(df.columns))

    prediction = service.predict(test_input)
    print(f"\nPrediction: {prediction}")