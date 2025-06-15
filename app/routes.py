from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
import os, json
from werkzeug.utils import secure_filename
main = Blueprint('main', __name__)
DATA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

# Your main Flask app object will import and register this Blueprint from app.py
# So no need to create `app = Flask(...)` here again

def save_to_json(file, new_data):
    path = os.path.join(DATA_FOLDER, file)
    if os.path.exists(path):
        with open(path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    data.append(new_data)
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

# ------------------ ROUTES ------------------

@main.route('/')
def home():
    return render_template('main_page.html')

@main.route('/home')
def home_page():
    return render_template('home.html')

@main.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        location = request.form.get('location')
        description = request.form.get('description')
        photo = request.files.get('photo')

        # Save image (optional)
        if photo and photo.filename != '':
            filename = secure_filename(photo.filename)
            upload_path = os.path.join('static', 'uploads', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            photo.save(upload_path)
        else:
            filename = None

        data = {
            'location': location,
            'description': description,
            'photo_filename': filename
        }

        save_to_json('reports.json', data)
        flash('Report saved successfully!')
        return redirect(url_for('main.report'))  # Reload form after submission

    return render_template('report_sick.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = {
            'name': request.form.get('name'),
            'clinic': request.form.get('clinic'),
            'city': request.form.get('city'),
            'contact': request.form.get('contact')
        }
        save_to_json('doctors.json', data)
        flash('Doctor registered!')
        return redirect(url_for('main.register'))
    return render_template('register_doctor.html')

@main.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'amount': request.form.get('amount')
        }
        save_to_json('donations.json', data)
        flash('Donation saved!')
        return redirect(url_for('main.donate'))
    return render_template('donate.html')

@main.route('/report_cruelty', methods=['GET', 'POST'])
def report_cruelty():
    if request.method == 'POST':
        data = {
            'location': request.form.get('location'),
            'animal_type': request.form.get('animal_type'),
            'incident': request.form.get('incident')
        }
        save_to_json('cruelty_reports.json', data)
        flash('Cruelty report submitted!')
        return redirect(url_for('main.report_cruelty'))
    return render_template('report_cruelty.html')

@main.route('/view_reports')
def view_reports():
    try:
        with open(os.path.join(DATA_FOLDER, 'reports.json'), 'r') as f:
            sick_reports = json.load(f)
    except:
        sick_reports = []

    try:
        with open(os.path.join(DATA_FOLDER, 'cruelty_reports.json'), 'r') as f:
            cruelty_reports = json.load(f)
    except:
        cruelty_reports = []

    return render_template(
        'view_reports.html',
        sick_reports=sick_reports,
        cruelty_reports=cruelty_reports
    )

# ------------------ STATIC PAGES ------------------

@main.route('/rescue')
def rescue_updates():
    return render_template('rescue.html')

@main.route('/map')
def map_page():
    return render_template('map.html')

@main.route('/awareness')
def awareness():
    return render_template('awareness.html')

@main.route('/blog')
def blog():
    return render_template('blog.html')