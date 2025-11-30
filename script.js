// --- Patients ---
const patientForm = document.getElementById('patientForm');
const patientList = document.getElementById('patientList');

patientForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        name: document.getElementById('pname').value,
        age: document.getElementById('page').value,
        gender: document.getElementById('pgender').value,
        disease: document.getElementById('pdisease').value
    };
    await fetch('/patients', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    patientForm.reset();
    loadPatients();
});

async function loadPatients() {
    const res = await fetch('/patients');
    const patients = await res.json();
    patientList.innerHTML = '';
    patients.forEach(p => {
        const li = document.createElement('li');
        li.textContent = `${p.name} | Age: ${p.age} | Gender: ${p.gender} | Disease: ${p.disease}`;
        patientList.appendChild(li);
    });
}

// --- Doctors ---
const doctorForm = document.getElementById('doctorForm');
const doctorList = document.getElementById('doctorList');

doctorForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        name: document.getElementById('dname').value,
        specialization: document.getElementById('dspec').value
    };
    await fetch('/doctors', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    doctorForm.reset();
    loadDoctors();
});

async function loadDoctors() {
    const res = await fetch('/doctors');
    const doctors = await res.json();
    doctorList.innerHTML = '';
    doctors.forEach(d => {
        const li = document.createElement('li');
        li.textContent = `${d.name} | Specialization: ${d.specialization}`;
        doctorList.appendChild(li);
    });
}

// --- Medicines ---
const medicineForm = document.getElementById('medicineForm');
const medicineList = document.getElementById('medicineList');

medicineForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        name: document.getElementById('mname').value,
        price: parseFloat(document.getElementById('mprice').value)
    };
    await fetch('/medicines', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    medicineForm.reset();
    loadMedicines();
});

async function loadMedicines() {
    const res = await fetch('/medicines');
    const medicines = await res.json();
    medicineList.innerHTML = '';
    medicines.forEach(m => {
        const li = document.createElement('li');
        li.textContent = `${m.name} | Price: $${m.price}`;
        medicineList.appendChild(li);
    });
}

// Load data initially
loadPatients();
loadDoctors();
loadMedicines();
