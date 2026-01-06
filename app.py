from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector, os

SERVER_RESTART_TOKEN = os.urandom(24)

app = Flask(__name__, template_folder='./templates')
app.secret_key = b'~\xb5\xb7D\x86s\xd4\x0b\xcfQ \xf4\xb2\x90\xce\x99'  # Replace with a strong, unique key

# Database connection
import mysql.connector
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your DB username
        password="pass@123",  # Replace with your DB password
        database="eventease"
    )

                    # for sign up

from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:  # Check if user is logged in
            return redirect(url_for('login_user'))  # Redirect to login page
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def restrict_access():
    allowed_routes = ['login_user', 'sign_up_user', 'sign_up_provider', 'login_provider', 'static']
    
    # Allow access if user or provider is logged in
    if 'user_id' not in session and 'provider_id' not in session and request.endpoint not in allowed_routes:
        return redirect(url_for('login_user'))  # Redirect to login if no valid session


@app.route('/')
def home():
    print("Rendering home page")
    return render_template('index.html')


# @app.route('/index')
# def index():
#     return render_template('index.html')



@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/booknow')
def booknow():
    return render_template('booknow.html')


# Registration route
# @app.route('/sign_up', methods=['GET', 'POST'])
# def sign_up():
#     if 'user_id' in session:
#         return redirect(url_for('home'))  # Redirect if already logged in

#     if request.method == 'POST':
#         name = request.form['name']
#         phone = request.form['phone']
#         email = request.form['email']
#         password = request.form['password']
#         hashed_password = generate_password_hash(password)

#         # Save user to the database
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         try:
#             cursor.execute(
#                 "INSERT INTO users (name, phone, email, password) VALUES (%s, %s, %s, %s)",
#                 (name, phone, email, hashed_password)
#             )
#             conn.commit()
#             flash('Registration successful! Please log in.', 'success')
#             return redirect(url_for('login'))
#         except mysql.connector.IntegrityError:
#             flash('Email already registered. Please log in.', 'danger')
#         finally:
#             cursor.close()
#             conn.close()

#     return render_template('signup.html')


# # Login route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         # Database connection and fetching user from the database
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)

#         cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#         user = cursor.fetchone()

#         if user and check_password_hash(user['password'], password):
#             # Set session variables
#             session['user_id'] = user['id']
#             session['user_name'] = user['name']
#             print("Session set after login:", session)  # Debugging output
#             flash('Login successful!', 'success')
#             return redirect(url_for('home'))
#         else:
#             flash('Invalid email or password.', 'danger')

#         cursor.close()
#         conn.close()
#     return render_template('login.html')


from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
import mysql.connector

# Signup for User
@app.route('/sign_up_user', methods=['GET', 'POST'])
def sign_up_user():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        # Insert user data into database with user_type as 'user'
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO users (name, phone, email, password, user_type) 
                VALUES (%s, %s, %s, %s, 'user')
            """, (name, phone, email, hashed_password))
            conn.commit()
            flash('User registration successful. Please log in.', 'success')
            return redirect(url_for('login_user'))
        except Exception as e:
            flash('Error registering user.', 'danger')
            print(e)
        finally:
            cursor.close()
            conn.close()

    return render_template('signup.html', user_type='user')

# Signup for Service Provider
@app.route('/sign_up_provider', methods=['GET', 'POST'])
def sign_up_provider():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        # Insert service provider data into database with user_type as 'service_provider'
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO users (name, phone, email, password, user_type) 
                VALUES (%s, %s, %s, %s, 'service_provider')
            """, (name, phone, email, hashed_password))
            conn.commit()
            flash('Service provider registration successful. Please log in.', 'success')
            return redirect(url_for('login_provider'))
        except Exception as e:
            flash('Error registering service provider.', 'danger')
            print(e)
        finally:
            cursor.close()
            conn.close()

    return render_template('signup.html', user_type='provider')

# Login Route for User
@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check user credentials
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email = %s AND user_type = 'user'", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_type'] = 'user'
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')

        cursor.close()
        conn.close()
    return render_template('login.html', user_type='user')

# Login Route for Service Provider
@app.route('/login_provider', methods=['GET', 'POST'])
def login_provider():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check service provider credentials
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email = %s AND user_type = 'service_provider'", (email,))
        provider = cursor.fetchone()

        if provider and check_password_hash(provider['password'], password):
            session['user_id'] = provider['id']
            session['name'] = provider['name']
            session['user_type'] = 'service_provider'
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to service provider post service page
        else:
            flash('Invalid email or password.', 'danger')

        cursor.close()
        conn.close()

    return render_template('login.html', user_type='provider')

# Logout route
@app.route('/logout')
def logout():
    # Clear the session to log out the user
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login_user'))  # Redirect to login page after logout










from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os

# Configure file upload settings
UPLOAD_FOLDER = 'static/uploads'  # Folder to save uploaded files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Service posting route, restricted to logged-in users
@app.route('/post_service', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in before posting a service
def post_service():
    if request.method == 'POST':
        # Get form data for the service
        brand_name = request.form['brand_name']
        email = request.form['email']
        phone = request.form['phone']
        location = request.form['location']
        category = request.form['category']
        description = request.form['description']
        rating = request.form['rating']
        user_id = session['user_id']  # Logged-in user's ID from the session

        images = request.files.getlist('images')
        filenames = []

        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(filepath)
                filenames.append(filename)
            else:
                flash(f'Invalid file: {image.filename}', 'danger')
                return redirect(request.url)
        

        # Save service data to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                            INSERT INTO services (user_id, brand_name, description, category, location, email, phone, rating)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (user_id, brand_name, description, category, location, email, phone, rating))
            service_id = cursor.lastrowid
            conn.commit()

            for filename in filenames:
                cursor.execute("""
                                INSERT INTO service_images (service_id, filename)
                                VALUES (%s, %s)
                            """, (service_id, filename))

            flash('Service posted successfully!', 'success')
            return redirect(url_for('services'))  # Redirect to the services page after posting
        
        except Exception as e:
            flash('An error occurred while posting the service.', 'danger')
            print(e)  # For debugging
        finally:
            conn.commit()
            cursor.close()
            conn.close()

    return render_template('post_service.html')  # Render post service form









# Services route (restricted to logged-in users)
from flask import session, flash, redirect, url_for, render_template
import mysql.connector

# Route to display services
@app.route('/services')
def services():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to view services.', 'danger')
        return redirect(url_for('login'))  # Redirect to login if not logged in
    user_type = session.get('user_type')

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch all services from the database
        cursor.execute("""
            SELECT service_id, brand_name, email, phone, location, category, description, rating, filename 
            FROM services
        """)
        services = cursor.fetchall()
        for service in services:
            service['short_description'] = service['description'].split('.', 1)[0] + '.'

        # Fetch related images for each service
        for service in services:
            cursor.execute("SELECT filename FROM service_images WHERE service_id = %s", (service['service_id'],))
            service['images'] = [img['filename'] for img in cursor.fetchall()]
    except Exception as e:
        flash('Error fetching services.', 'danger')
        services = []
    finally:
        cursor.close()
        conn.close()

    # Render the template and pass the services data
    return render_template('services.html', services=services, user_type=user_type)







@app.route('/service_details/<int:service_id>', methods=['GET', 'POST'])
@login_required
def service_details(service_id):
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to view services.', 'danger')
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch all services from the database
        cursor.execute("""
            SELECT service_id, brand_name, email, phone, location, category, description, rating
            FROM services
            WHERE service_id = %s
        """,(service_id,))
        service = cursor.fetchone()

        # Fetch related images
        cursor.execute("SELECT filename FROM service_images WHERE service_id = %s", (service_id,))
        service_images = cursor.fetchall()
    except Exception as e:
        flash('Error fetching services.', 'danger')
    finally:
        cursor.close()
        conn.close()

    # Render the template and pass the services data
    return render_template('service_details.html', service=service, service_images=service_images)








from datetime import datetime, date
# Booking a service
@app.route('/book/<int:service_id>', methods=['GET', 'POST'])
@login_required
def book_service_page(service_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT service_id, brand_name, description
        FROM services
        WHERE service_id = %s
    """, (service_id,))
    service = cursor.fetchone()
    if 'service_id' not in service:
        return "Service ID not found", 404
    cursor.close()

    if request.method == 'POST':
        booking_date = request.form.get('booking_date')
        user_id = session['user_id']

        try:
            booking_date_obj = datetime.strptime(booking_date, '%Y-%m-%d').date()
            if booking_date_obj < date.today():
                flash('Invalid booking date!', 'danger')
                return redirect(url_for('book_service_page', service_id=service_id))

            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bookings (user_id, service_id, booking_date)
                VALUES (%s, %s, %s)
            """, (user_id, service_id, booking_date))
            conn.commit()
            cursor.close()

            flash('Service booked successfully!', 'success')
            return redirect(url_for('bookings'))
        except ValueError:
            flash('Invalid date format!', 'danger')
            return redirect(url_for('book_service_page', service_id=service_id))

    return render_template('book_services.html', service=service)




# Displaying bookings
@app.route('/bookings')
@login_required
def bookings():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT b.id AS booking_id, b.service_id, b.booking_date, DATE(b.created_at) AS created_date, b.status,
                   s.brand_name, s.phone, s.location, s.category, s.email
            FROM bookings b
            JOIN services s ON b.service_id = s.service_id
            WHERE b.user_id = %s
        """, (session['user_id'],))
        bookings = cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        flash('Error fetching bookings!', 'danger')
        return redirect(url_for('services'))
    finally:
        conn.close()
        cursor.close()

    return render_template('bookings.html', bookings=bookings)







                                                    # schedule













                                                    #comments



# Service posting route, restricted to logged-in users
@app.route('/add_review', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in before posting a service
def add_review():
    if request.method == 'POST':
        # Get form data for the service
        rating=request.form['rating']
        id=session['user_id']
        message=request.form['message']
        name=session['user_name']
        # Save service data to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO reviews (id, name, message, rating)
                VALUES (%s, %s, %s, %s)
            """, (id, name, message, rating))
            conn.commit()
            flash('Review posted successfully!', 'success')
            return redirect(url_for('services'))  # Redirect to the services page after posting
        except Exception as e:
            flash('An error occurred while posting the review.', 'danger')
            print(e)  # For debugging
        finally:
            cursor.close()
            conn.close()

    return render_template('services.html')  # Render post service form



@app.route('/index')
def index():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to view reviews.', 'danger')
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch all services from the database
        cursor.execute("""
            SELECT name, message, rating, DATE(created_at) AS created_date
            FROM reviews
        """)
        reviews = cursor.fetchall()
    except Exception as e:
        flash('Error fetching reviews.', 'danger')
        print(e)
        reviews = []
    finally:
        cursor.close()
        conn.close()

    # Render the template and pass the services data
    return render_template('index.html', reviews=reviews)

@app.route('/services')
def success_page():
    return "Review submitted successfully!"
















# Run the app
if __name__ == '__main__':
    app.run(debug=True)




