# app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# --- App Initialization ---
app = Flask(__name__)
# Using SQLite for simplicity. Replace with your RDBMS URI if needed.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_resources.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'a_very_secret_key' # Important for sessions/security
db = SQLAlchemy(app)

# --- Database Models (Mapping to SQL Tables) ---
class Student(db.Model):
    __tablename__ = 'Student'
    studentID = db.Column(db.Integer, primary_key=True)
    studentName = db.Column(db.String(80), unique=True, nullable=False)
    studentEmail = db.Column(db.String(120), unique=True, nullable=False)
    studentPassHash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        # Uses werkzeug.security (equivalent to Bcrypt for demonstration)
        self.studentPassHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.studentPassHash, password)

# --- Resource Helper Model (Conceptual - for map data) ---
# In a real app, you would define models for all resource tables (HealthRecord, TutoringRecord, etc.)
# For the map API, we'll use a simplified structure that requires manual data fetching.

# --- Resource Icon Mapping (for API) ---
RESOURCE_ICONS = {
    'Health Services': {'icon': 'health.png', 'color': '#FF5733'},
    'Academic Advising': {'icon': 'advisor.png', 'color': '#33FF57'},
    'Academic Support': {'icon': 'support.png', 'color': '#3357FF'},
    'Funding': {'icon': 'funding.png', 'color': '#FF33A1'},
    'Tutoring': {'icon': 'tutoring.png', 'color': '#33FFF6'},
    'Student Supplies': {'icon': 'supplies.png', 'color': '#FFC733'},
}

# --- Utility Function for Resource API Data ---
def fetch_resource_locations():
    # Placeholder: In a real app, this would query all resource models (HealthRecord, etc.)
    # and combine the data. Here's a placeholder example with static data.
    
    # NOTE: Your actual database queries would fetch the 'Location' string 
    # (which must be parsed into latitude and longitude).
    
    # Static Example Data: (Location is assumed to be "lat,lng" string)
    raw_data = [
        ('Health Services', 'Health Center', '37.3382, -121.8863', 'https://health.link'),
        ('Tutoring', 'Math Lab', '37.3395, -121.8880', None),
        ('Funding', 'Financial Aid Office', '37.3370, -121.8850', 'https://funding.link'),
    ]

    markers = []
    for type, service, location_str, link in raw_data:
        icon_data = RESOURCE_ICONS.get(type, {'icon': 'default.png', 'color': '#808080'})
        try:
            lat, lng = map(float, location_str.split(','))
            markers.append({
                'type': type,
                'lat': lat,
                'lng': lng,
                'service': service,
                'link': link,
                'icon': icon_data['icon'],
                'color': icon_data['color']
            })
        except ValueError:
            print(f"Skipping resource {service}: Invalid location format.")
    return markers

# --- Routes ---

@app.route('/')
def index():
    # Redirect to login or render a simple index page
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = Student.query.filter_by(studentName=username).first()
        
        if user and user.check_password(password):
            # In a real app, you would set a session here: session['user_id'] = user.studentID
            return redirect(url_for('dashboard')) # Success
        else:
            error = 'Invalid Username or Password. Please try again.'

    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            error = "Passwords do not match."
        elif Student.query.filter_by(studentName=username).first():
            error = "Username already exists."
        elif Student.query.filter_by(studentEmail=email).first():
            error = "Email already registered."
        else:
            new_user = Student(studentName=username, studentEmail=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login')) # Success

    return render_template('register.html', error=error)

@app.route('/join_session', methods=['GET', 'POST'])
def join_session():
    # This route is simplified, assuming basic session joining logic
    error = None
    if request.method == 'POST':
        session_id = request.form['session_id']
        # Add logic to validate and join the session
        # ...
        error = f"Attempted to join session {session_id}. (Logic not implemented)"

    return render_template('join_session.html', error=error)

@app.route('/dashboard')
def dashboard():
    # Simple dashboard placeholder
    return "Welcome to the Dashboard! <a href='/map'>View Resources Map</a>"

# --- API Endpoint for Google Maps ---
@app.route('/api/resources/map', methods=['GET'])
def get_map_markers():
    """Returns a JSON list of all resource locations for the Google Maps frontend."""
    markers = fetch_resource_locations()
    return jsonify(markers)

# --- Database Setup (Run once) ---
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
