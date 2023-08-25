from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///indicators.db'
app.secret_key = 'some_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}
db = SQLAlchemy(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def str_to_bool(value):
    try:
        return bool(int(value))
    except ValueError:
        return False

def import_from_csv(filepath, db_session):
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            # Unpack values, now including the new columns
            name, definition, SPA, SPB, SPD, SPE, SPF, EFA, EFB, EFC, EFD = row

            new_indicator = Indicator(
                name=name,
                definition=definition,
                SPA = str_to_bool(SPA),
                SPB=str_to_bool(SPB),
                SPD=str_to_bool(SPD),
                SPE=str_to_bool(SPE),
                SPF=str_to_bool(SPF),
                EFA=str_to_bool(EFA),
                EFB=str_to_bool(EFB),
                EFC=str_to_bool(EFC),
                EFD=str_to_bool(EFD)
            )

            db_session.session.add(new_indicator)
    db_session.session.commit()

class Indicator(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    definition = db.Column(db.String(500), nullable=False)
    SPA = db.Column(db.Boolean, default=False)
    SPB = db.Column(db.Boolean, default=False)
    SPC = db.Column(db.Boolean, default=False)
    SPD = db.Column(db.Boolean, default=False)
    SPE = db.Column(db.Boolean, default=False)
    SPF = db.Column(db.Boolean, default=False)
    EFA = db.Column(db.Boolean, default=False)
    EFB = db.Column(db.Boolean, default=False)
    EFC = db.Column(db.Boolean, default=False)
    EFD = db.Column(db.Boolean, default=False)

class IndicatorHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    indicator_ID = db.Column(db.Integer, nullable=False)
    old_name = db.Column(db.String(200), nullable=False)
    new_name = db.Column(db.String(200), nullable=False)
    old_definition = db.Column(db.Text, nullable=True)
    new_definition = db.Column(db.Text, nullable=True)
    old_SPA = db.Column(db.Boolean, nullable=True)
    new_SPA = db.Column(db.Boolean, nullable=True)
    old_SPB = db.Column(db.Boolean, nullable=True)
    new_SPB = db.Column(db.Boolean, nullable=True)
    old_SPC = db.Column(db.Boolean, nullable=True)
    new_SPC = db.Column(db.Boolean, nullable=True)
    old_SPD = db.Column(db.Boolean, nullable=True)
    new_SPD = db.Column(db.Boolean, nullable=True)
    old_SPE = db.Column(db.Boolean, nullable=True)
    new_SPE = db.Column(db.Boolean, nullable=True)
    old_SPF = db.Column(db.Boolean, nullable=True)
    new_SPF = db.Column(db.Boolean, nullable=True)
    old_EFA = db.Column(db.Boolean, nullable=True)
    new_EFA = db.Column(db.Boolean, nullable=True)
    old_EFB = db.Column(db.Boolean, nullable=True)
    new_EFB = db.Column(db.Boolean, nullable=True)
    old_EFC = db.Column(db.Boolean, nullable=True)
    new_EFC = db.Column(db.Boolean, nullable=True)
    old_EFD = db.Column(db.Boolean, nullable=True)
    new_EFD = db.Column(db.Boolean, nullable=True)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/all_history')
def all_history():
    all_histories = IndicatorHistory.query.all()
    return render_template('all_history.html', histories=all_histories)

@app.route('/')
def home():
    indicators = Indicator.query.all()
    return render_template('index.html', indicators=indicators)

@app.route('/add', methods=['POST'])
def add_indicator():
    name = request.form['name']
    definition = request.form['definition']
    SPA = 'SPA' in request.form
    SPB = 'SPB' in request.form
    SPC = 'SPC' in request.form
    SPD = 'SPD' in request.form
    SPE = 'SPE' in request.form
    EFA = 'EFA' in request.form
    EFB = 'EFB' in request.form
    EFC = 'EFC' in request.form
    EFD = 'EFD' in request.form
    
    new_indicator = Indicator(
        name=name, 
        definition=definition, 
        SPA=SPA, 
        SPB=SPB, 
        SPC=SPC, 
        SPD=SPD, 
        SPE=SPE, 
        EFA=EFA, 
        EFB=EFB, 
        EFC=EFC, 
        EFD=EFD, 
    )
    db.session.add(new_indicator)
    db.session.commit()

    flash('Indicator added successfully!')
    return redirect(url_for('home'))

@app.route('/add', methods=['GET'])
def add_page():
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    indicator = Indicator.query.get(id)
    if request.method == 'POST':
        old_name = indicator.name
        old_definition = indicator.definition
        
        # Capture old SPs and EFs values
        old_SPA = indicator.SPA
        old_SPB = indicator.SPB
        old_SPC = indicator.SPC
        old_SPD = indicator.SPD
        old_SPE = indicator.SPE
        old_SPF = indicator.SPF
        old_EFA = indicator.EFA
        old_EFB = indicator.EFB
        old_EFC = indicator.EFC
        old_EFD = indicator.EFD
        
        # Update current indicator's SPs and EFs based on form data
        indicator.name = request.form['name']
        indicator.definition = request.form['definition']
        indicator.SPA = 'SPA' in request.form
        indicator.SPB = 'SPB' in request.form
        indicator.SPC = 'SPC' in request.form
        indicator.SPD = 'SPD' in request.form
        indicator.SPE = 'SPE' in request.form
        indicator.SPF = 'SPF' in request.form
        indicator.EFA = 'EFA' in request.form
        indicator.EFB = 'EFB' in request.form
        indicator.EFC = 'EFC' in request.form
        indicator.EFD = 'EFD' in request.form
        
        # Check if any field was updated, and if so, create a history record
        if (old_name != indicator.name or old_definition != indicator.definition or
            old_SPA != indicator.SPA or old_SPB != indicator.SPB or old_SPC != indicator.SPC or
            old_SPD != indicator.SPD or old_SPE != indicator.SPE or old_SPF != indicator.SPF or
            old_EFA != indicator.EFA or old_EFB != indicator.EFB or old_EFC != indicator.EFC or
            old_EFD != indicator.EFD):
            
            history = IndicatorHistory(
                indicator_ID=id,
                old_name=old_name,
                new_name=request.form['name'],
                old_definition=old_definition,
                new_definition=request.form['definition'],
                old_SPA=old_SPA, new_SPA=indicator.SPA,
                old_SPB=old_SPB, new_SPB=indicator.SPB,
                old_SPC=old_SPC, new_SPC=indicator.SPC,
                old_SPD=old_SPD, new_SPD=indicator.SPD,
                old_SPE=old_SPE, new_SPE=indicator.SPE,
                old_SPF=old_SPF, new_SPF=indicator.SPF,
                old_EFA=old_EFA, new_EFA=indicator.EFA,
                old_EFB=old_EFB, new_EFB=indicator.EFB,
                old_EFC=old_EFC, new_EFC=indicator.EFC,
                old_EFD=old_EFD, new_EFD=indicator.EFD
            )
            db.session.add(history)
        
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', indicator=indicator)

@app.route('/view/<int:id>', methods=['GET'])
def view(id):
    indicator = Indicator.query.get(id)
    return render_template('view.html', indicator=indicator)

@app.route('/history/<int:id>')
def history(id):
    histories = IndicatorHistory.query.filter_by(indicator_ID=id).all()
    return render_template('history.html', histories=histories)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('home'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('home'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        import_from_csv(filepath, db)
        flash('File successfully uploaded and processed')
        return redirect(url_for('home'))
    else:
        flash('Invalid file type')
        return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
