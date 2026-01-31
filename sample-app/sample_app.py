# Add to this file for the sample app lab
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from flask import send_from_directory
from flask import jsonify
from datetime import datetime




# Conditional import of mysql.connector to allow tests to run
try:
    import mysql.connector
except ImportError:
    mysql = None
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

sample = Flask(__name__)
sample.secret_key = "123"

UPLOAD_FOLDER = "uploads"
IMAGES_DB = "uploads/images.txt"

import os
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(IMAGES_DB), exist_ok=True)


# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "5f4qza.h.filess.io"),
    "user": os.getenv("DB_USER", "C270 DevOps_searchten"),
    "password": os.getenv("DB_PASSWORD", "9a592585756f756e1d86f580ac6e7cfb69f2607a"),
    "port": int(os.getenv("DB_PORT", "3307")),
    "database": os.getenv("DB_NAME", "C270 DevOps_searchten"),
}

def get_db_connection():
    """Return a MySQL connection if available, else raise RuntimeError."""
    if mysql is None:
        raise RuntimeError("MySQL connector not available")
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    """Check database connection"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(buffered=True)
        # Just verify we can connect
        cursor.execute("SELECT 1")
        cursor.fetchone() 
        cursor.close()
        conn.close()
        print("✓ Database connection successful")
    except Exception as e:
        print(f"✗ Database connection error: {e}")
        print("  App will continue but database features may not work")

# Show backend
@sample.route("/system", methods=["GET"])
def system_status():
    # ---- Database check (safe) ----
    db_ok = False
    db_error = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(buffered=True)
        cur.execute("SELECT 1")
        cur.fetchone()
        cur.close()
        conn.close()
        db_ok = True
    except Exception as e:
        db_error = str(e)

    # ---- System report ----
    return jsonify({
        "ok": True,
        "backend": "running",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "checks": {
            "flask_app": True,
            "session_enabled": bool(sample.secret_key),
            "database_connected": db_ok,
            "database_error": db_error,
            "upload_folder_exists": os.path.exists(UPLOAD_FOLDER),
            "images_db_exists": os.path.exists(IMAGES_DB),
        },
        "environment": {
            "PORT": os.getenv("PORT", "not set"),
            "RENDER": os.getenv("RENDER", "not set"),
            "PYTHON_VERSION": os.getenv("PYTHON_VERSION", "unknown")
        }
    })

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def load_images():
    try:
        with open(IMAGES_DB, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def save_images(images):
    with open(IMAGES_DB, "w") as f:
        for img in images:
            f.write(img + "\n")

@sample.route("/", methods=["GET"])
def home():
    return main()

@sample.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            return render_template("login.html", error="Username and password are required")
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, password FROM users WHERE username = %s', (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user and check_password_hash(user[1], password):
                session['user_id'] = user[0]
                session['username'] = username
                return redirect('/')
            else:
                return render_template("login.html", error="Invalid username or password")
        except Exception as e:
            return render_template("login.html", error="Database error occurred")
    
    return render_template("login.html")

@sample.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if not username or not password or not confirm_password:
            return render_template("register.html", error="All fields are required")
        
        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match")
        
        if len(password) < 6:
            return render_template("register.html", error="Password must be at least 6 characters long")
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if username already exists
            cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return render_template("register.html", error="Username already exists")
            
            # Create new user with hashed password
            hashed_pwd = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)',
                         (username, hashed_pwd))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return render_template("register.html", success="Account created successfully! You can now login.")
        except Exception as e:
            return render_template("register.html", error="An error occurred during registration")
    
    return render_template("register.html")

@sample.route("/logout", methods=["GET"])
def logout():
    """Handle user logout"""
    session.clear()
    return redirect('/login')

@sample.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

def main():
    images = load_images()
    count = len(images)
    
    gallery = ""

    if images:
        if count % 2 == 0:
            gallery = '<div class="grid even">'
        else:
            gallery = '<div class="grid odd">'

        for img in images:
            gallery = gallery + (
                '<div class="card">'
                '<img src="/uploads/' + img + '">'
                '</div>'
            )

        gallery = gallery + '</div>'
    
    is_logged_in = 'user_id' in session
    return render_template("index.html", gallery=gallery, is_logged_in=is_logged_in, username=session.get('username'))

@sample.route("/add", methods=["GET"])
def add_page():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template("Add.html")


@sample.route("/upload", methods=["POST"])
def upload():
    if 'user_id' not in session:
        return redirect('/login')
    
    files = request.files.getlist("images")
    if not files:
        return redirect("/")

    images = load_images()

    for file in files:
        if not file or file.filename == "":
            continue
        filename = file.filename
        file.save(UPLOAD_FOLDER + "/" + filename)
        images.append(filename)

    save_images(images)
    return redirect("/")


if __name__ == "__main__":
    print("Starting Flask app...")
    print("Note: Make sure the 'users' table exists in your database")
    init_db()
    sample.run(host="0.0.0.0", port=8080, threaded=True)