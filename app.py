from flask import Flask, request, render_template
import pickle
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load your model
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'  # Create this folder in your project directory
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction_result = None
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return render_template('index.html', error='No file uploaded')

        file = request.files['file']

        # Ensure the file is valid
        if file.filename == '':
            return render_template('index.html', error='No selected file')

        # Save the uploaded file securely
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Extract text from the uploaded file
        with open(filepath, 'r') as f:
            text = f.read()  # Read text from the .txt file

        # Make a prediction using the model
        prediction = model.predict([text])

        # Convert prediction from int64 to int
        prediction_value = int(prediction[0])  # Modify this according to your model's output
        prediction_result = 'Fraudulent' if prediction_value == 1 else 'Not Fraudulent'

    return render_template('index.html', prediction=prediction_result)

if __name__ == '__main__':
    app.run(debug=True)
