from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)

# Load the fraud detection model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'fraud_detection_model.pkl')

try:
    with open(MODEL_PATH, 'rb') as model_file:
        model = pickle.load(model_file)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None  # Ensure the app does not crash if the model is missing

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        transaction_amount = float(request.form['transaction_amount'])
        customer_age = int(request.form['customer_age'])
        transaction_duration = int(request.form['transaction_duration'])
        login_attempts = int(request.form['login_attempts'])
        account_balance = float(request.form['account_balance'])
        hour = int(request.form['hour'])

        # Ensure model is loaded
        if model:
            input_data = [[transaction_amount, customer_age, transaction_duration, login_attempts, account_balance, hour]]
            prediction = model.predict(input_data)
            prediction_label = "Fraudulent" if prediction[0] == 1 else "Not Fraudulent"
        else:
            prediction_label = "Model not available"

        return render_template('index.html', prediction=prediction_label)
    
    except Exception as e:
        return render_template('index.html', prediction=f"Error: {str(e)}")

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0',port=8080)
