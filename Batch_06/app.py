# from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
# import joblib
# import csv

# app = Flask(__name__, static_url_path='/static', static_folder='static')
# app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# # Load the trained model from the 'model.pkl' file
# model = joblib.load('model.pkl')

# # Create a dictionary to store user data (for demonstration purposes)
# # In a real application, you would use a database to store user information securely
# users = {
#     'username': 'password'  # Replace with actual usernames and hashed passwords
# }

# # Create a dictionary to store company data and calculate low and high values
# company_data = {}

# # Read company data from the CSV file and calculate low and high values
# with open('company_stock_data.csv', mode='r') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         company_name = row['company_name']
#         low_amount = float(row['low'])
#         high_amount = float(row['high'])

#         company_data[company_name] = {
#             'low': low_amount,
#             'high': high_amount,
#             'open': float(row['open'])
#         }

# @app.route('/signup', methods=['GET'])
# def signup():
#     return render_template('signup.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         # Check if the username and password are valid (for demonstration purposes)
#         if username in users and users[username] == password:
#             session['username'] = username
#             flash('Login successful!', 'success')
#             return redirect(url_for('index'))
#         else:
#             flash('Login failed. Please check your credentials.', 'error')

#     return render_template('login.html')

# @app.route('/')
# def index():
#     return render_template('index.html', companyData=company_data)

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # Get user input values from the form
#         company_name = request.form['company_name']
#         volume_amount = float(request.form['volume'])

#         if company_name in company_data:
#             low_amount = company_data[company_name]['low']
#             high_amount = company_data[company_name]['high']
#             open_amount = company_data[company_name]['open']

#             # Make predictions
#             new_data = [[open_amount, low_amount, high_amount, volume_amount]]
#             predicted_price = model.predict(new_data)

#             return render_template('predicted_result.html', company_name=company_name, volume=volume_amount,
#                                    open=open_amount, low=low_amount, high=high_amount,
#                                    predicted_price=predicted_price[0])
#         else:
#             return jsonify({'error': 'Company not found'})
#     except Exception as e:
#         return jsonify({'error': str(e)})

# @app.route('/chart_data', methods=['POST'])
# def chart_data():
#     try:
#         # Get user input values from the form
#         company_name = request.form['company_name']
#         volume_amount = float(request.form['volume'])

#         if company_name in company_data:
#             low_amount = company_data[company_name]['low']
#             high_amount = company_data[company_name]['high']
#             open_amount = company_data[company_name]['open']

#             # Create a list of timestamps or labels for your charts (e.g., dates)
#             timestamps = ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"]  # Replace with actual timestamps or labels

#             # Simulate example data for input and predicted output (replace with actual data)
#             input_data = [10, 20, 30, 40]  # Example input data
#             predicted_data = [40, 30, 20, 10]  # Example predicted data

#             # Create a dictionary to store the data for input and predicted output
#             chart_data = {
#                 'timestamps': timestamps,
#                 'input_data': input_data,
#                 'predicted_data': predicted_data
#             }

#             return jsonify(chart_data)
#         else:
#             return jsonify({'error': 'Company not found'})
#     except Exception as e:
#         return jsonify({'error': str(e)})

# # Define routes for additional pages
# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/service')
# def service():
#     return render_template('service.html')

# @app.route('/why')
# def why():
#     return render_template('why.html')

# @app.route('/team')
# def team():
#     return render_template('team.html')

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import joblib
import csv
from flask import send_file
import io
import matplotlib.pyplot as plt
import base64

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Load the trained model from the 'model.pkl' file
model = joblib.load('model.pkl')

# Create a dictionary to store user data (for demonstration purposes)
# In a real application, you would use a database to store user information securely
users = {
    'username': 'password'  # Replace with actual usernames and hashed passwords
}

# Create a dictionary to store company data and calculate low and high values
company_data = {}

# Read company data from the CSV file and calculate low and high values
with open('company_stock_data.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        company_name = row['Company']
        date = row['Date']
        close_price = row['Close/Last'].strip('$')
        volume = int(row['Volume'])
        open_price = row['Open'].strip('$')
        high_price = row['High'].strip('$')
        low_price = row['Low'].strip('$')

        company_data[f'{company_name}_{date}'] = {
            'date': date,
            'close_price': close_price,
            'volume': volume,
            'open_price': open_price,
            'high_price': high_price,
            'low_price': low_price,
        }

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are valid (for demonstration purposes)
        if username in users and users[username] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your credentials.', 'error')

    return render_template('login.html')

@app.route('/')
def index():
    return render_template('index.html', companyData=company_data)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get user input values from the form
        company_name = request.form['company_name']
        date = request.form['date']
        volume_input = request.form['volume']

        # Check if volume input is "random"
        if volume_input.lower() == "random":
            # Fetch data based on company name and date, ignoring volume
            search_key = f'{company_name}_{date}_random'
        else:
            volume_amount = int(volume_input)
            search_key = f'{company_name}_{date}'

        if search_key in company_data:
            data = company_data[search_key]

            # Make predictions
            new_data = [
                [
                    float(data['open_price']),
                    float(data['low_price']),
                    float(data['high_price']),
                    float(volume_input)
                ]
            ]
            predicted_price = model.predict(new_data)

            return render_template('predicted_result.html', company_name=company_name, date=data['date'],
                volume=volume_input, open=data['open_price'], low=data['low_price'], high=data['high_price'],
                close=data['close_price'], predicted_price=predicted_price[0])
        else:
            print("Data not found for the given date and volume.")
            return jsonify({'error': 'Data not found for the given date and volume.'})
    except Exception as e:
        return jsonify({'error': str(e)})
# Define routes for additional pages
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/why')
def why():
    return render_template('why.html')

@app.route('/team')
def team():
    return render_template('team.html')

if __name__ == '__main__':
    app.run(debug=True)


