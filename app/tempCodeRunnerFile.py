from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
import os, json

main = Blueprint('main', __name__)
DATA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), 'static')
)
@app.route('/')
def home():
    return render_template('main_page.html')

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

@main.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        data = {
            'location': request.form.get('location'),
            'description': request.form.get('description'),
        }
        # Note: Photo handling is optional and not saving it here
        save_to_json('reports.json', data)
        flash('Report saved!')
        return redirect(url_for('main.report'))
    return render_template('report.html')

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
    return render_template('register.html')

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
            'incident': request.form.get('incident')
        }
        save_to_json('cruelty_reports.json', data)
        flash('Cruelty report submitted!')
        return redirect(url_for('main.report_cruelty'))
    return render_template('report_cruelty.html')
