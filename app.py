from flask import Flask, render_template, redirect, url_for, request, session,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import threading
import subprocess
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Configure the SQLite database (new database file: 'app_data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)





app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'prithwirajcharchigcsj@gmail.com'
app.config['MAIL_PASSWORD'] = 'lgtk wmjl xuns uowd'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    contact_no = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()
    
@app.route('/feedback', methods=['POST'])
def feedback():
    if request.method == 'POST':
        feedback_message = request.form['message']
        user_email = request.form['email']
        try:
            # Create message object
            msg = Message(subject="User Feedback",
                          sender=user_email,
                          recipients=["prithwirajcharchigcsj@gmail.com"],
                          body=feedback_message)
            msg.reply_to = user_email


            msg.body = f"Feedback from: {user_email}\n\nMessage:\n{feedback_message}"

            mail.send(msg)
            flash('Feedback sent successfully!')
            return redirect('/')
        except Exception as e:
            flash('Error sending feedback: ' + str(e))
            return redirect('/')

@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('index2'))  # Redirect to index2 if logged in
    return render_template('index.html')    # Show login and signup options if not logged in

@app.route('/index2')
def index2():
    if 'logged_in' in session and session['logged_in']:
        return render_template('index2.html')  # Only show logout option
    return redirect(url_for('index'))  # If not logged in, redirect to the main page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Fetch user by username
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and if password matches
        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            session['username'] = user.username
            return redirect(url_for('index2'))  # Redirect to index2 after successful login
        return 'Invalid credentials, please try again'
    
    return render_template('login.html')

@app.route('/signufp', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        contact_no = request.form['contact_no']
        username = request.form['username']
        password = request.form['password']
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return 'Username or Email already exists'
        
        # Create a new user and hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, contact_no=contact_no, username=username, password=hashed_password)
        
        # Add new user to the database
        db.session.add(new_user)
        db.session.commit()
        
        # Log the user in automatically after signup
        session['logged_in'] = True
        session['username'] = new_user.username
        return redirect(url_for('login'))  # Redirect to index2 after signup
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))  # Redirect to index page after logging out



# Other routes...
@app.route('/maleCategory')
def male_category():
    return render_template('maleCategory.html')

@app.route('/female_category')
def female_category():
    return render_template('fecategory.html')

@app.route('/senior_citizen')
def senior_citizen():
    return render_template('senior_citizen.html')

@app.route('/sports')
def sports():
    return render_template('sports.html')

@app.route('/video_series')
def video_series():
    return render_template('vdoseries.html')

@app.route('/mind')
def mind():
    return render_template('mind.html')

@app.route('/football')
def football():
    return render_template('football.html')

@app.route('/basketball')
def basketball():
    return "Basketball details page"

@app.route('/tennis')
def tennis():
    return "Tennis details page"

@app.route('/cricket')
def cricket():
    return "Cricket details page"



@app.route('/run')
def run():
    return render_template('run.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Get data from the form
    height = float(request.form['height'])
    weight = float(request.form['weight'])
    
    # Calculate BMI
    bmi = weight / (height * height)
    
    # Determine BMI category
    if bmi < 18.5:
        category = 'Underweight'
    elif 18.5 <= bmi < 24.9:
        category = 'Normal weight'
    elif 25 <= bmi < 29.9:
        category = 'Overweight'
    else:
        category = 'Obesity'
    
    return render_template('result.html', bmi=bmi, category=category)

@app.route('/bmi')
def bmi():
    return render_template('SIH.html')

@app.route('/lunges')
def lunges():
    return render_template('lung.html')

@app.route('/back')
def back():
    return redirect(url_for('index'))

@app.route('/lung')
def lung():
    return render_template('lung.html')


@app.route('/squats')
def squats():
    return render_template('sq.html')



@app.route('/shooting_drills')
def shooting_drills():
    return "demo after"

@app.route('/endurance_training')
def endurance_training():
    return "demo after"

@app.route('/swimming')
def swimming():
    return "Swimming details page"

@app.route('/cycling')
def cycling():
    return "Cycling details page"

@app.route('/javelin')
def javelin():
    return "Javelin Throw details page"


@app.route('/preg')
def preg():
    return render_template('pregnancy.html')

@app.route('/fteen')
def fteen():
    return "bad main"

@app.route('/fadult')
def fadult():
    return "bad main"

@app.route('/football_exercises')
def football_exercises():
    return render_template('football_exercises.html')



def run_squats_script():
    # Run the Lunges.py script
    subprocess.run(['python', 'Lunges.py'])


@app.route('/start_sq')
def start_sq():
     # Run the Python script
    thread = threading.Thread(target=run_squats_script)
    thread.start()
    return render_template('loading.html')



def run_running_script():
    # Run the Lunges.py script
    subprocess.run(['python', 'Lunges.py'])

    
@app.route('/start_run')
def start_run():
    # Run the Python script
    thread = threading.Thread(target=run_running_script)
    thread.start()
    return render_template('loading.html')


def run_lunges_script():
    # Run the Lunges.py script
    subprocess.run(['python', 'Lunges.py'])

@app.route('/start_lung')
def start_lung():
    # Start the script asynchronously
    thread = threading.Thread(target=run_lunges_script)
    thread.start()
    return render_template('loading.html')


@app.route('/days_15')
def days_15():
    return render_template('15days.html')

@app.route('/weekly')
def weekly():
    return "hlo"

@app.route('/monthly')
def monthly():
    return "hlo"

@app.route('/day1')
def day1():
    return render_template('day1.html')

@app.route('/day2')
def day2():
    return render_template('day2.html')

@app.route('/day3')
def day3():
    return render_template('day3.html')

@app.route('/day4')
def day4():
    return render_template('day1.html')
@app.route('/day5')
def day5():
    return render_template('day1.html')
@app.route('/day6')
def day6():
    return render_template('day1.html')
@app.route('/day7')
def day7():
    return render_template('day1.html')
@app.route('/day8')
def day8():
    return render_template('day1.html')
@app.route('/day9')
def day9():
    return render_template('day1.html')
@app.route('/day10')
def day10():
    return render_template('day1.html')
@app.route('/day11')
def day11():
    return render_template('day1.html')
@app.route('/day12')
def day12():
    return render_template('day1.html')
@app.route('/day13')
def day13():
    return render_template('day1.html')
@app.route('/day14')
def day14():
    return render_template('day1.html')
@app.route('/day15')
def day15():
    return render_template('day1.html')

@app.route('/mind1')
def mind1():
    return render_template('mind.html')

@app.route('/underweight', methods=['POST'])
def underweight():
    return render_template('under.html')

@app.route('/normal', methods=['POST'])
def normal():
    return render_template('normal.html')

@app.route('/overweight', methods=['POST'])
def overweight():
    return render_template('over.html')

@app.route('/feed')
def feed():
    return render_template('feedb.html')

@app.route('/under_nutrition')
def under_nutrition():
    return render_template('un_nutri.html')

@app.route('/under_exrercises')
def under_exercises():
    return "hlo"






if __name__ == '__main__':
    app.run(debug=True)
