from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Patient, Doctor, Medicine, MedicalRecord, Bill
import os

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'devkey'  # change for production

db.init_app(app)

# Initialize DB file if not exists
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    patients = Patient.query.count()
    doctors = Doctor.query.count()
    medicines = Medicine.query.count()
    return render_template('index.html', patients=patients, doctors=doctors, medicines=medicines)

# Patients
@app.route('/patients')
def patients():
    allp = Patient.query.all()
    return render_template('patients.html', patients=allp)

@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form.get('age') or None
        gender = request.form.get('gender')
        contact = request.form.get('contact')
        p = Patient(name=name, age=age, gender=gender, contact=contact)
        db.session.add(p)
        db.session.commit()
        flash('Patient added.')
        return redirect(url_for('patients'))
    return render_template('add_patient.html')

@app.route('/patients/delete/<int:id>')
def delete_patient(id):
    p = Patient.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    flash('Patient deleted.')
    return redirect(url_for('patients'))

# Doctors
@app.route('/doctors')
def doctors():
    docs = Doctor.query.all()
    return render_template('doctors.html', doctors=docs)

@app.route('/doctors/add', methods=['GET','POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        spec = request.form.get('specialization')
        contact = request.form.get('contact')
        d = Doctor(name=name, specialization=spec, contact=contact)
        db.session.add(d)
        db.session.commit()
        flash('Doctor added.')
        return redirect(url_for('doctors'))
    return render_template('add_doctor.html')

@app.route('/doctors/delete/<int:id>')
def delete_doctor(id):
    d = Doctor.query.get_or_404(id)
    db.session.delete(d)
    db.session.commit()
    flash('Doctor deleted.')
    return redirect(url_for('doctors'))

# Medicines
@app.route('/medicines')
def medicines():
    meds = Medicine.query.all()
    return render_template('medicines.html', medicines=meds)

@app.route('/medicines/add', methods=['GET','POST'])
def add_medicine():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form.get('price') or 0)
        stock = int(request.form.get('stock') or 0)
        m = Medicine(name=name, price=price, stock=stock)
        db.session.add(m)
        db.session.commit()
        flash('Medicine added.')
        return redirect(url_for('medicines'))
    return render_template('add_medicine.html')

@app.route('/medicines/delete/<int:id>')
def delete_medicine(id):
    m = Medicine.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    flash('Medicine deleted.')
    return redirect(url_for('medicines'))

# Medical Records (basic create & list)
@app.route('/records')
def records():
    recs = MedicalRecord.query.all()
    return render_template('records.html', records=recs)

@app.route('/records/add', methods=['GET','POST'])
def add_record():
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    if request.method == 'POST':
        patient_id = int(request.form['patient_id'])
        doctor_id = int(request.form.get('doctor_id') or 0) or None
        diagnosis = request.form.get('diagnosis')
        prescription = request.form.get('prescription')
        r = MedicalRecord(patient_id=patient_id, doctor_id=doctor_id, diagnosis=diagnosis, prescription=prescription)
        db.session.add(r)
        db.session.commit()
        flash('Medical record added.')
        return redirect(url_for('records'))
    return render_template('add_record.html', patients=patients, doctors=doctors)

# Billing - simple: choose patient, select medicines (comma-separated ids), compute total
@app.route('/billing', methods=['GET','POST'])
def billing():
    patients = Patient.query.all()
    medicines = Medicine.query.all()
    if request.method == 'POST':
        patient_id = int(request.form['patient_id'])
        med_ids = request.form.get('med_ids','').strip()
        if med_ids == '':
            flash('No medicines selected.')
            return redirect(url_for('billing'))
        med_list = [int(x.strip()) for x in med_ids.split(',') if x.strip().isdigit()]
        items = []
        total = 0.0
        for mid in med_list:
            med = Medicine.query.get(mid)
            if med:
                items.append(f"{med.name} (₹{med.price})")
                total += med.price
        details = '; '.join(items)
        bill = Bill(patient_id=patient_id, total=total, details=details)
        db.session.add(bill)
        db.session.commit()
        flash(f'Bill created. Total ₹{total:.2f}')
        return redirect(url_for('view_bill', bill_id=bill.id))
    return render_template('billing.html', patients=patients, medicines=medicines)

@app.route('/bill/<int:bill_id>')
def view_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    patient = Patient.query.get(bill.patient_id)
    return render_template('view_bill.html', bill=bill, patient=patient)

if _name_ == '_main_':
    app.run(debug=True)