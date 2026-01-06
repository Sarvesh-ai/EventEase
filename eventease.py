# from flask import Flask, request, render_template, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# import os
# from werkzeug.utils import secure_filename

# # Initialize Flask app and SQLAlchemy
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass%40123@localhost/eventease'  # Replace with your MySQL credentials
# app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Folder where images will be saved
# app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Allowed image formats
# app.secret_key = 'supersecretkey'  # For form security

# db = SQLAlchemy(app)

# # Define a model for storing service data and image filenames
# class Service(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     brand_name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     phone = db.Column(db.String(15), nullable=False)
#     location = db.Column(db.String(100), nullable=False)
#     category = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     rating = db.Column(db.Float, nullable=False)
#     filename = db.Column(db.String(100), nullable=False)

# # Ensure the database tables are created
# with app.app_context():
#     db.create_all()

# # Check if file extension is allowed
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# # Route to handle the service form and image upload
# @app.route('/post_service', methods=[ 'POST'])
# def post_service():
#     if request.method == 'POST':
#         # Handle text fields
#         brand_name = request.form['brand_name']
#         email = request.form['email']
#         phone = request.form['phone']
#         location = request.form['location']
#         category = request.form['category']
#         description = request.form['description']
#         rating = request.form['rating']

#         # Handle file upload
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             # Secure the filename to prevent directory traversal
#             filename = secure_filename(file.filename)
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(file_path)  # Save the file

#             # Save service data to the database
#             new_service = Service(
#                 brand_name=brand_name,
#                 email=email,
#                 phone=phone,
#                 location=location,
#                 category=category,
#                 description=description,
#                 rating=rating,
#                 filename=filename
#             )
#             db.session.add(new_service)
#             db.session.commit()

#             flash('Service posted successfully!', 'success')
#             return redirect(url_for('post_service'))

#     return render_template('post_service.html')

# # Route to display uploaded image
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return f'<h1>Image Uploaded!</h1><img src="/static/uploads/{filename}" alt="Uploaded Image">'

# if __name__ == '__main__':
#     app.run(debug=True)






                    # for sign up

# from flask import Flask, render_template, request, redirect, url_for, session, flash
# from werkzeug.security import generate_password_hash, check_password_hash
# import mysql.connector

# app = Flask(__name__)
# app.secret_key =  'b~\xb5\xb7D\x86s\xd4\x0b\xcfQ \xf4\xb2\x90\xce\x99'  # Replace with a strong, unique key

# # Database connection
# def get_db_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",  # Replace with your DB username
#         password="pass@123",  # Replace with your DB password
#         database="eventease"
#     )

# # Home route
# @app.route('/')
# def home():
#     return render_template('index.html')

# # Registration route
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']
#         phone = request.form['phone']
#         email = request.form['email']
#         password = request.form['password']
#         hashed_password = generate_password_hash(password)

#         # Save user to database
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
#             return redirect(url_for('services'))
#         else:
#             flash('Invalid email or password.', 'danger')

#         cursor.close()
#         conn.close()

#     return render_template('login.html')

# # def login():
# #     if request.method == 'POST':
# #         email = request.form['email']
# #         password = request.form['password']

# #         conn = get_db_connection()
# #         cursor = conn.cursor(dictionary=True)

# #         cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
# #         user = cursor.fetchone()

# #         if user and check_password_hash(user['password'], password):
# #             session['user_id'] = user['id']
# #             session['user_name'] = user['name']
# #             flash('Login successful!', 'success')
# #             return redirect(url_for('services'))

# #         flash('Invalid email or password.', 'danger')

# #         cursor.close()
# #         conn.close()

# #     return render_template('login.html')

# # Services route (restricted to logged-in users)
# @app.route('/services')
# def services():
#     if 'user_id' not in session:
#         flash('You must log in to access the services page.', 'danger')
#         return redirect(url_for('login'))
#     return render_template('services.html')

# # Logout route
# @app.route('/logout')
# def logout():
#     session.clear()
#     flash('Logged out successfully.', 'success')
#     return redirect(url_for('login'))

# # Run the app
# if __name__ == '__main__':
#     app.run(debug=True)
