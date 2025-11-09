# AIS Backend Developer assignment

This repository implements the AIS Backend Developer assignment. 

## Descriptions

The program predicts the cost of a house based on real estate parameters.
In order for the user to receive a prediction, they must first obtain a token. To do this, they must enter their login and password, and if this information is in the database, they will receive a temporary token, which they can use to obtain a predicted housing price.

## How to start

### Local Launch

To run the application locally (without Docker):

You must have Python version 3.9.

```
git clone https://github.com/Oroch1maru/housing_prices_dashboard.git
cd housing-api

pip install --upgrade pip

pip install -r requirements.txt
```
Next, in the project root, create a .env file that will contain the following data

| Variable | Description | Default                    |
|-----------|-------------|----------------------------|
| **SECRET_KEY** | JWT secret key | Required                   |
| **ACCESS_TOKEN_EXPIRE_MINUTES** | Token lifetime | 60                         |
| **RATE_LIMIT_PER_MINUTE** | Max requests per minute | 60                         |
| **DATABASE_URL** | Database connection | `sqlite:///./data/user.db` |
| **ALLOWED_ORIGINS** | Comma-separated list of frontend origins allowed for CORS | `["http://localhost:3000","http://127.0.0.1:8000"]`              |


After creation, simply start the server with the command:

```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The application will be available at:

http://127.0.0.1:8000/

To stop the server: _CTRL + C_

### Docker Launch

If you prefer to run the app inside a container:

```
docker-compose up --build
```

The application will be available at:

http://127.0.0.1:8000/

To stop the server: _CTRL + C_ and prescribe the command

```
docker-compose down
```

## Description of CI/CD

Each push to this repository triggers a pipeline that has two stages: testing and building. 

During the testing stage, written tests are run to verify the correctness of authorization and prediction. 

During the building stage, an image is created, which is then pushed to Docker Hub.