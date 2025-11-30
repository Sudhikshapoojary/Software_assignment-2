from flask import Blueprint, request, jsonify
from models import db, Patient, Doctor, Medicine

hospital_bp = Blueprint('hospital', __name__)

# ---- Patient Routes ----
@hospital_bp.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    patient = Patient(name=data['name'], age=data['age'], gender=data['gender'], disease=data['disease'])
    db.session.add(patient)
    db.session.commit()
    return jsonify({"message": "Patient added successfully!"})

@hospital_bp.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify([{"id": p.id, "name": p.name, "age": p.age, "gender": p.gender, "disease": p.disease} for p in patients])

# ---- Doctor Routes ----
@hospital_bp.route('/doctors', methods=['POST'])
def add_doctor():
    data = request.json
    doctor = Doctor(name=data['name'], specialization=data['specialization'])
    db.session.add(doctor)
    db.session.commit()
    return jsonify({"message": "Doctor added successfully!"})

@hospital_bp.route('/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify([{"id": d.id, "name": d.name, "specialization": d.specialization} for d in doctors])

# ---- Medicine Routes ----
@hospital_bp.route('/medicines', methods=['POST'])
def add_medicine():
    data = request.json
    medicine = Medicine(name=data['name'], price=data['price'])
    db.session.add(medicine)
    db.session.commit()
    return jsonify({"message": "Medicine added successfully!"})

@hospital_bp.route('/medicines', methods=['GET'])
def get_medicines():
    medicines = Medicine.query.all()
    return jsonify([{"id": m.id, "name": m.name, "price": m.price} for m in medicines])

