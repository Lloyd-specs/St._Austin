"""
Seed the SIH database with realistic sample data for St. Austin Hospital.
Usage: python manage.py seed_data
"""
import random
from datetime import date, time, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import Role, User
from apps.patients.models import EmergencyContact, Patient
from apps.appointments.models import Appointment, QueueEntry
from apps.medical_records.models import Consultation, VitalSign
from apps.prescriptions.models import Prescription, PrescriptionItem
from apps.pharmacy.models import Medication, Dispensation
from apps.inventory.models import Batch, StockMovement
from apps.laboratory.models import ImagingOrder, LabOrder, LabResult, LabTest
from apps.billing.models import Invoice, InvoiceItem, Payment


class Command(BaseCommand):
    help = 'Seed the database with realistic sample data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing old seed data...')
        self._clear_data()
        self.stdout.write('Seeding roles...')
        roles = self._seed_roles()
        self.stdout.write('Seeding staff users...')
        users = self._seed_users(roles)
        self.stdout.write('Seeding medications...')
        medications = self._seed_medications(users)
        self.stdout.write('Seeding inventory batches...')
        batches = self._seed_batches(medications, users)
        self.stdout.write('Seeding patients...')
        patients = self._seed_patients()
        self.stdout.write('Seeding appointments...')
        appointments = self._seed_appointments(patients, users)
        self.stdout.write('Seeding consultations & vitals...')
        consultations = self._seed_consultations(patients, users, appointments)
        self.stdout.write('Seeding lab orders...')
        self._seed_lab_orders(patients, users, consultations)
        self.stdout.write('Seeding prescriptions...')
        self._seed_prescriptions(patients, users, consultations, medications, batches)
        self.stdout.write('Seeding invoices & payments...')
        self._seed_billing(patients, consultations, users)
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def _clear_data(self):
        Payment.objects.all().delete()
        InvoiceItem.objects.all().delete()
        Invoice.objects.all().delete()
        Dispensation.objects.all().delete()
        PrescriptionItem.objects.all().delete()
        Prescription.objects.all().delete()
        LabResult.objects.all().delete()
        LabTest.objects.all().delete()
        LabOrder.objects.all().delete()
        ImagingOrder.objects.all().delete()
        VitalSign.objects.all().delete()
        Consultation.objects.all().delete()
        QueueEntry.objects.all().delete()
        Appointment.objects.all().delete()
        StockMovement.objects.all().delete()
        Batch.objects.all().delete()
        Dispensation.objects.all().delete()
        Medication.objects.all().delete()
        EmergencyContact.objects.all().delete()
        Patient.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

    def _seed_roles(self):
        role_data = [
            ('admin_systeme', 'Administrateur Systeme'),
            ('accueil', "Personnel d'Accueil"),
            ('medecin', 'Medecin'),
            ('infirmier', 'Infirmier'),
            ('pharmacien', 'Pharmacien'),
            ('directeur', 'Directeur'),
        ]
        roles = {}
        for name, desc in role_data:
            role, _ = Role.objects.get_or_create(name=name, defaults={'description': desc})
            roles[name] = role
        return roles

    def _seed_users(self, roles):
        users = {}

        # Fix superuser role if it exists with wrong role
        try:
            admin = User.objects.get(email='admin@staustin.cm')
            admin.role = roles['admin_systeme']
            admin.is_staff = True
            admin.is_superuser = True
            admin.must_change_password = False
            admin.employee_id = 'EMP-001'
            admin.save()
            users['admin'] = admin
        except User.DoesNotExist:
            users['admin'] = User.objects.create_superuser(
                email='admin@staustin.cm',
                password='Admin@2026',
                first_name='Admin',
                last_name='Systeme',
                role=roles['admin_systeme'],
                employee_id='EMP-001',
            )
            users['admin'].must_change_password = False
            users['admin'].save()

        staff_data = [
            # Doctors
            ('Dr. Jean', 'Mbarga', 'medecin', 'jean.mbarga@staustin.cm', 'EMP-100', '+237 6 77 12 34 56'),
            ('Dr. Marie', 'Nkoulou', 'medecin', 'marie.nkoulou@staustin.cm', 'EMP-101', '+237 6 99 88 77 66'),
            ('Dr. Paul', 'Fotso', 'medecin', 'paul.fotso@staustin.cm', 'EMP-102', '+237 6 55 44 33 22'),
            # Nurses
            ('Claudine', 'Atangana', 'infirmier', 'claudine.atangana@staustin.cm', 'EMP-200', '+237 6 11 22 33 44'),
            ('Brigitte', 'Eyenga', 'infirmier', 'brigitte.eyenga@staustin.cm', 'EMP-201', '+237 6 22 33 44 55'),
            # Receptionist
            ('Sandrine', 'Biyick', 'accueil', 'sandrine.biyick@staustin.cm', 'EMP-300', '+237 6 33 44 55 66'),
            ('Thomas', 'Essomba', 'accueil', 'thomas.essomba@staustin.cm', 'EMP-301', '+237 6 44 55 66 77'),
            # Pharmacists
            ('Alain', 'Tchinda', 'pharmacien', 'alain.tchinda@staustin.cm', 'EMP-400', '+237 6 55 66 77 88'),
            ('Rosalie', 'Kamga', 'pharmacien', 'rosalie.kamga@staustin.cm', 'EMP-401', '+237 6 66 77 88 99'),
            # Director
            ('Prof. Emmanuel', 'Ngo Bama', 'directeur', 'emmanuel.ngobama@staustin.cm', 'EMP-500', '+237 6 77 88 99 00'),
        ]

        for first, last, role_name, email, emp_id, phone in staff_data:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'role': roles[role_name],
                    'employee_id': emp_id,
                    'phone': phone,
                    'is_active': True,
                    'must_change_password': False,
                },
            )
            if created:
                user.set_password('Password@2026')
                user.save()
            users[email] = user

        return users

    def _seed_medications(self, users):
        pharmacist = User.objects.filter(role__name='pharmacien').first()
        meds_data = [
            ('MED-001', 'Paracetamol 500mg', 'Paracetamol', 'tablet', '500mg', 'Sanofi', 'Analgesique', 150),
            ('MED-002', 'Amoxicilline 500mg', 'Amoxicilline', 'capsule', '500mg', 'GSK', 'Antibiotique', 500),
            ('MED-003', 'Ibuprofene 400mg', 'Ibuprofene', 'tablet', '400mg', 'Cinpharm', 'Anti-inflammatoire', 200),
            ('MED-004', 'Metformine 850mg', 'Metformine', 'tablet', '850mg', 'Merck', 'Antidiabetique', 350),
            ('MED-005', 'Amlodipine 5mg', 'Amlodipine', 'tablet', '5mg', 'Pfizer', 'Antihypertenseur', 300),
            ('MED-006', 'Omeprazole 20mg', 'Omeprazole', 'capsule', '20mg', 'AstraZeneca', 'Antiulcereux', 250),
            ('MED-007', 'Ceftriaxone 1g', 'Ceftriaxone', 'injection', '1g', 'Roche', 'Antibiotique', 2500),
            ('MED-008', 'Diazepam 5mg', 'Diazepam', 'tablet', '5mg', 'Roche', 'Anxiolytique', 175),
            ('MED-009', 'Salbutamol 100mcg', 'Salbutamol', 'inhaler', '100mcg', 'GSK', 'Bronchodilatateur', 3500),
            ('MED-010', 'Artemether/Lumefantrine', 'Artemether', 'tablet', '20/120mg', 'Novartis', 'Antipaludeen', 1200),
            ('MED-011', 'Diclofenac Gel', 'Diclofenac', 'cream', '1%', 'Novartis', 'Anti-inflammatoire', 1500),
            ('MED-012', 'Chlorpheniramine 4mg', 'Chlorpheniramine', 'syrup', '4mg/5ml', 'Cinpharm', 'Antihistaminique', 800),
            ('MED-013', 'Ciprofloxacine 500mg', 'Ciprofloxacine', 'tablet', '500mg', 'Bayer', 'Antibiotique', 450),
            ('MED-014', 'Losartan 50mg', 'Losartan', 'tablet', '50mg', 'Merck', 'Antihypertenseur', 400),
            ('MED-015', 'Insuline Mixtard', 'Insuline', 'injection', '100UI/ml', 'Novo Nordisk', 'Antidiabetique', 8500),
        ]

        medications = {}
        for code, name, generic, form, strength, mfr, cat, price in meds_data:
            med, _ = Medication.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'generic_name': generic,
                    'form': form,
                    'strength': strength,
                    'manufacturer': mfr,
                    'category': cat,
                    'unit_price': Decimal(str(price)),
                    'reorder_level': 20,
                    'is_active': True,
                    'created_by': pharmacist,
                },
            )
            medications[code] = med
        return medications

    def _seed_batches(self, medications, users):
        pharmacist = User.objects.filter(role__name='pharmacien').first()
        batches = {}
        today = date.today()

        for code, med in medications.items():
            qty = random.randint(50, 500)
            batch = Batch.objects.create(
                medication=med,
                batch_number=f'LOT-{code[-3:]}-2026A',
                quantity_received=qty,
                quantity_remaining=qty,
                unit_cost=med.unit_price * Decimal('0.6'),
                supplier='Laborex Cameroun',
                received_date=today - timedelta(days=random.randint(5, 60)),
                expiry_date=today + timedelta(days=random.randint(180, 730)),
                is_verified=True,
            )
            batches[code] = batch

            StockMovement.objects.create(
                batch=batch,
                movement_type='entry',
                quantity=qty,
                reason='Reception stock initial',
                reference=f'BON-{code[-3:]}',
                performed_by=pharmacist,
            )

        return batches

    def _seed_patients(self):
        patients_data = [
            ('PAT-2026-0001', 'Amadou', 'Bello', '1985-03-15', 'M', '+237 6 70 11 22 33', 'Yaounde', 'Centre', 'A+', 'Penicilline', '', 'CNPS', 'CNPS-88001', '2027-12-31'),
            ('PAT-2026-0002', 'Fatima', 'Njoya', '1990-08-22', 'F', '+237 6 91 22 33 44', 'Douala', 'Littoral', 'O+', '', 'Hypertension arterielle', 'AXA Cameroun', 'AXA-55201', '2027-06-30'),
            ('PAT-2026-0003', 'Pierre', 'Mvondo', '1978-11-05', 'M', '+237 6 55 33 44 55', 'Yaounde', 'Centre', 'B+', '', 'Diabete type 2', '', '', None),
            ('PAT-2026-0004', 'Grace', 'Tabi', '2000-01-12', 'F', '+237 6 80 44 55 66', 'Bertoua', 'Est', 'O-', 'Aspirine', '', '', '', None),
            ('PAT-2026-0005', 'Martin', 'Ngono', '1965-07-30', 'M', '+237 6 72 55 66 77', 'Yaounde', 'Centre', 'AB+', '', 'Hypertension, Arthrose', 'BEAC Mutuelle', 'BM-33100', '2026-12-31'),
            ('PAT-2026-0006', 'Isabelle', 'Kouam', '1995-04-18', 'F', '+237 6 98 66 77 88', 'Bamenda', 'Nord-Ouest', 'A-', 'Sulfamides', '', '', '', None),
            ('PAT-2026-0007', 'Emmanuel', 'Tchatchoua', '1988-12-01', 'M', '+237 6 77 77 88 99', 'Bafoussam', 'Ouest', 'O+', '', '', 'Saar Assurances', 'SAAR-7720', '2027-03-31'),
            ('PAT-2026-0008', 'Beatrice', 'Akono', '2015-06-20', 'F', '+237 6 55 88 99 00', 'Yaounde', 'Centre', 'B-', '', 'Asthme', 'CNPS', 'CNPS-99222', '2027-12-31'),
            ('PAT-2026-0009', 'Rodrigue', 'Mbouda', '1972-09-08', 'M', '+237 6 66 99 00 11', 'Ebolowa', 'Sud', 'A+', '', 'Goutte', '', '', None),
            ('PAT-2026-0010', 'Christine', 'Ndam', '1998-02-25', 'F', '+237 6 90 00 11 22', 'Douala', 'Littoral', 'O+', '', '', 'Activa Assurances', 'ACT-4480', '2027-09-30'),
            ('PAT-2026-0011', 'Samuel', 'Owona', '1955-05-10', 'M', '+237 6 71 11 33 55', 'Yaounde', 'Centre', 'AB-', 'Codeine', 'Insuffisance cardiaque', 'CNPS', 'CNPS-11003', '2027-12-31'),
            ('PAT-2026-0012', 'Josephine', 'Biloa', '2003-10-30', 'F', '+237 6 82 22 44 66', 'Kribi', 'Sud', 'B+', '', '', '', '', None),
            ('PAT-2026-0013', 'Thierry', 'Mengueme', '1980-01-19', 'M', '+237 6 93 33 55 77', 'Yaounde', 'Centre', 'O+', '', 'Ulcere gastrique', '', '', None),
            ('PAT-2026-0014', 'Veronique', 'Essola', '1992-07-14', 'F', '+237 6 74 44 66 88', 'Douala', 'Littoral', 'A+', '', '', 'Beneficial Life', 'BL-6650', '2026-11-30'),
            ('PAT-2026-0015', 'Alain', 'Nkengfack', '1970-03-28', 'M', '+237 6 85 55 77 99', 'Maroua', 'Extreme-Nord', 'O-', 'Metoclopramide', 'Paludisme recurrent', '', '', None),
        ]

        patients = []
        for pid, first, last, dob, sex, phone, city, region, blood, allergies, chronic, ins_provider, ins_num, ins_exp in patients_data:
            exp_date = date.fromisoformat(ins_exp) if ins_exp else None
            patient = Patient.objects.create(
                unique_pid=pid,
                first_name=first,
                last_name=last,
                date_of_birth=date.fromisoformat(dob),
                sex=sex,
                phone_primary=phone,
                city=city,
                region=region,
                blood_type=blood,
                allergies=allergies,
                chronic_conditions=chronic,
                insurance_provider=ins_provider,
                insurance_number=ins_num,
                insurance_expiry=exp_date,
            )
            patients.append(patient)

        # Emergency contacts
        contacts = [
            (patients[0], 'Halima Bello', 'Epouse', '+237 6 70 99 88 77'),
            (patients[1], 'Ibrahim Njoya', 'Frere', '+237 6 91 88 77 66'),
            (patients[2], 'Anne Mvondo', 'Epouse', '+237 6 55 77 66 55'),
            (patients[3], 'Marcel Tabi', 'Pere', '+237 6 80 66 55 44'),
            (patients[4], 'Jeanne Ngono', 'Fille', '+237 6 72 55 44 33'),
            (patients[7], 'Marc Akono', 'Pere', '+237 6 55 44 33 22'),
            (patients[10], 'David Owona', 'Fils', '+237 6 71 33 22 11'),
        ]
        for patient, name, rel, phone in contacts:
            EmergencyContact.objects.create(patient=patient, name=name, relationship=rel, phone=phone)

        return patients

    def _seed_appointments(self, patients, users):
        doctors = list(User.objects.filter(role__name='medecin'))
        today = date.today()
        appointments = []

        departments = ['Medecine Generale', 'Cardiologie', 'Pediatrie', 'Gynecologie', 'Chirurgie']
        reasons = [
            'Consultation de routine',
            'Douleurs abdominales',
            'Suivi hypertension',
            'Fievre persistante',
            'Controle diabete',
            'Douleurs articulaires',
            'Vaccination enfant',
            'Bilan de sante',
            'Toux chronique',
            'Maux de tete recurrents',
        ]

        # Past appointments (completed)
        for i in range(20):
            apt_date = today - timedelta(days=random.randint(1, 30))
            apt = Appointment.objects.create(
                patient=random.choice(patients),
                doctor=random.choice(doctors),
                department=random.choice(departments),
                scheduled_date=apt_date,
                scheduled_time=time(hour=random.randint(8, 15), minute=random.choice([0, 15, 30, 45])),
                duration_minutes=30,
                status='completed',
                reason=random.choice(reasons),
            )
            appointments.append(apt)

        # Today's appointments
        statuses_today = ['checked_in', 'in_progress', 'completed', 'scheduled', 'confirmed']
        for i in range(8):
            apt = Appointment.objects.create(
                patient=patients[i % len(patients)],
                doctor=doctors[i % len(doctors)],
                department=random.choice(departments),
                scheduled_date=today,
                scheduled_time=time(hour=8 + i, minute=0),
                duration_minutes=30,
                status=statuses_today[i % len(statuses_today)],
                reason=random.choice(reasons),
            )
            appointments.append(apt)

        # Future appointments
        for i in range(10):
            apt = Appointment.objects.create(
                patient=random.choice(patients),
                doctor=random.choice(doctors),
                department=random.choice(departments),
                scheduled_date=today + timedelta(days=random.randint(1, 14)),
                scheduled_time=time(hour=random.randint(8, 15), minute=random.choice([0, 15, 30, 45])),
                duration_minutes=30,
                status='scheduled',
                reason=random.choice(reasons),
            )
            appointments.append(apt)

        # Queue entries for today
        receptionist = User.objects.filter(role__name='accueil').first()
        for i, apt in enumerate(appointments):
            if apt.scheduled_date == today and apt.status in ('checked_in', 'in_progress', 'completed'):
                q_status = 'waiting' if apt.status == 'checked_in' else ('serving' if apt.status == 'in_progress' else 'completed')
                QueueEntry.objects.create(
                    patient=apt.patient,
                    appointment=apt,
                    department=apt.department,
                    priority=random.choice([0, 0, 0, 1]),
                    ticket_number=f'T-{i + 1:03d}',
                    status=q_status,
                    served_by=apt.doctor if q_status != 'waiting' else None,
                )

        return appointments

    def _seed_consultations(self, patients, users, appointments):
        doctors = list(User.objects.filter(role__name='medecin'))
        nurses = list(User.objects.filter(role__name='infirmier'))
        consultations = []

        complaints = [
            ('Fievre et courbatures depuis 3 jours', 'Le patient presente une fievre a 39.2C avec des courbatures generalisees.', 'Temperature elevee, ganglions cervicaux sensibles', 'Paludisme probable', 'TDR paludisme + NFS. Traitement antipaludeen si positif.'),
            ('Douleurs thoraciques intermittentes', 'Douleurs precordiales depuis 1 semaine, irradiant vers le bras gauche.', 'TA 160/95, souffle systolique grade II', 'HTA non controlee, angor a eliminer', 'ECG + bilan lipidique. Ajuster traitement antihypertenseur.'),
            ('Toux productive depuis 2 semaines', 'Toux avec expectorations verdatres, dyspnee legere.', 'Rales crepitants base droite, SpO2 94%', 'Pneumonie communautaire', 'Radio thorax + CRP. Antibiotherapie empirique.'),
            ('Controle glycemie trimestriel', 'Patient diabetique type 2 sous metformine.', 'IMC 28.5, pieds sans lesions', 'Diabete type 2 equilibre', 'HbA1c + bilan renal. Poursuivre traitement.'),
            ('Douleurs epigastriques', 'Epigastralgies post-prandiales depuis 1 mois.', 'Sensibilite epigastrique, pas de defense', 'Gastrite probable', 'Test H. pylori. IPP pendant 4 semaines.'),
            ('Cephalees recurrentes', 'Cephalees frontales bilaterales, 3x/semaine depuis 2 mois.', 'Examen neurologique normal, TA normale', 'Cephalees de tension', 'Paracetamol a la demande. Gestion du stress.'),
            ('Eruption cutanee prurigineuse', 'Plaques erythemateuses sur les bras depuis 5 jours.', 'Plaques urticariennes, pas d\'oedeme', 'Urticaire allergique', 'Antihistaminique. Eviter les allergenes identifies.'),
            ('Douleurs articulaires genoux', 'Gonalgies bilaterales aggravees par la marche.', 'Crepitations rotuliens, pas d\'epanchement', 'Gonarthrose bilaterale', 'AINS + kinesitherapie. Radio si persistance.'),
        ]

        completed_apts = [a for a in appointments if a.status == 'completed']
        for i, apt in enumerate(completed_apts[:12]):
            c_data = complaints[i % len(complaints)]
            consult = Consultation.objects.create(
                patient=apt.patient,
                doctor=apt.doctor,
                appointment=apt,
                chief_complaint=c_data[0],
                history_present_illness=c_data[1],
                physical_examination=c_data[2],
                assessment=c_data[3],
                plan=c_data[4],
                follow_up_date=date.today() + timedelta(days=random.choice([7, 14, 30])),
            )
            consultations.append(consult)

            # Vital signs
            nurse = random.choice(nurses) if nurses else apt.doctor
            VitalSign.objects.create(
                patient=apt.patient,
                consultation=consult,
                recorded_by=nurse,
                temperature=Decimal(str(round(random.uniform(36.2, 39.5), 1))),
                blood_pressure_systolic=random.randint(110, 170),
                blood_pressure_diastolic=random.randint(65, 100),
                heart_rate=random.randint(60, 100),
                respiratory_rate=random.randint(14, 22),
                oxygen_saturation=Decimal(str(round(random.uniform(93.0, 99.5), 1))),
                weight=Decimal(str(round(random.uniform(50.0, 95.0), 1))),
                height=Decimal(str(round(random.uniform(155.0, 185.0), 1))),
            )

        return consultations

    def _seed_lab_orders(self, patients, users, consultations):
        doctors = list(User.objects.filter(role__name='medecin'))
        lab_tech = User.objects.filter(role__name='infirmier').first()

        test_catalog = [
            ('NFS', 'HEM-01', 'Hematologie'),
            ('Glycemie a jeun', 'BIO-01', 'Biochimie'),
            ('Creatinine', 'BIO-02', 'Biochimie'),
            ('Transaminases (ASAT/ALAT)', 'BIO-03', 'Biochimie'),
            ('TDR Paludisme', 'PAR-01', 'Parasitologie'),
            ('Goutte epaisse', 'PAR-02', 'Parasitologie'),
            ('ECBU', 'MIC-01', 'Microbiologie'),
            ('CRP', 'BIO-04', 'Biochimie'),
            ('HbA1c', 'BIO-05', 'Biochimie'),
            ('Bilan lipidique', 'BIO-06', 'Biochimie'),
        ]

        results_data = {
            'HEM-01': [('Hemoglobine', '13.5', 'g/dL', '12-16', False), ('Leucocytes', '8200', '/mm3', '4000-10000', False), ('Plaquettes', '245000', '/mm3', '150000-400000', False)],
            'BIO-01': [('Glycemie', '1.85', 'g/L', '0.70-1.10', True)],
            'BIO-02': [('Creatinine', '9.2', 'mg/L', '7-13', False)],
            'BIO-03': [('ASAT', '28', 'UI/L', '10-40', False), ('ALAT', '35', 'UI/L', '10-40', False)],
            'PAR-01': [('TDR Paludisme', 'Positif', '', 'Negatif', True)],
            'PAR-02': [('Densite parasitaire', '12500', 'p/uL', '<0', True)],
            'MIC-01': [('Leucocytes', '150000', '/mL', '<10000', True), ('Culture', 'E. coli', '', 'Sterile', True)],
            'BIO-04': [('CRP', '48', 'mg/L', '<6', True)],
            'BIO-05': [('HbA1c', '7.8', '%', '<7.0', True)],
            'BIO-06': [('Cholesterol total', '2.35', 'g/L', '<2.0', True), ('HDL', '0.45', 'g/L', '>0.40', False), ('LDL', '1.60', 'g/L', '<1.60', False)],
        }

        order_num = 1
        for consult in consultations[:8]:
            selected_tests = random.sample(test_catalog, k=random.randint(1, 3))
            status = random.choice(['completed', 'completed', 'in_progress', 'ordered'])

            order = LabOrder.objects.create(
                patient=consult.patient,
                consultation=consult,
                ordered_by=consult.doctor,
                order_number=f'LAB-2026-{order_num:04d}',
                status=status,
                priority=random.choice(['routine', 'routine', 'urgent']),
            )
            order_num += 1

            for test_name, test_code, category in selected_tests:
                lab_test = LabTest.objects.create(
                    order=order,
                    test_name=test_name,
                    test_code=test_code,
                    category=category,
                )

                if status == 'completed' and test_code in results_data:
                    for val_name, val, unit, ref, abnormal in results_data[test_code]:
                        LabResult.objects.create(
                            test=lab_test,
                            value=f'{val_name}: {val}' if len(results_data[test_code]) == 1 else val,
                            unit=unit,
                            reference_range=ref,
                            is_abnormal=abnormal,
                            performed_by=lab_tech,
                            validated_by=consult.doctor,
                        )
                        break  # one result per test

    def _seed_prescriptions(self, patients, users, consultations, medications, batches):
        pharmacist = User.objects.filter(role__name='pharmacien').first()
        med_list = list(medications.values())
        batch_list = list(batches.items())

        rx_num = 1
        for consult in consultations[:10]:
            status = random.choice(['signed', 'dispensed', 'dispensed', 'partially_dispensed'])
            rx = Prescription.objects.create(
                prescription_number=f'RX-2026-{rx_num:04d}',
                patient=consult.patient,
                consultation=consult,
                prescriber=consult.doctor,
                status=status,
                valid_until=date.today() + timedelta(days=30),
                notes='',
            )
            rx_num += 1

            num_items = random.randint(1, 4)
            chosen_meds = random.sample(med_list, k=min(num_items, len(med_list)))

            dosages = ['1 comprime', '2 comprimes', '5ml', '1 gelule', '1 injection']
            frequencies = ['3x/jour', '2x/jour', '1x/jour', 'matin et soir', 'toutes les 8h']
            durations = ['5 jours', '7 jours', '10 jours', '14 jours', '30 jours']

            for med in chosen_meds:
                qty = random.randint(6, 30)
                item = PrescriptionItem.objects.create(
                    prescription=rx,
                    medication=med,
                    dosage=random.choice(dosages),
                    frequency=random.choice(frequencies),
                    duration=random.choice(durations),
                    quantity=qty,
                    route='oral' if med.form in ('tablet', 'capsule', 'syrup') else 'iv' if med.form == 'injection' else 'topical',
                    instructions='A prendre pendant les repas' if med.form in ('tablet', 'capsule') else '',
                )

                # Dispense if status is dispensed
                if status in ('dispensed', 'partially_dispensed') and pharmacist:
                    batch_code = med.code
                    if batch_code in batches:
                        batch = batches[batch_code]
                        disp_qty = qty if status == 'dispensed' else qty // 2
                        Dispensation.objects.create(
                            prescription=rx,
                            prescription_item=item,
                            dispensed_by=pharmacist,
                            medication=med,
                            batch=batch,
                            quantity_dispensed=disp_qty,
                        )
                        batch.quantity_remaining = max(0, batch.quantity_remaining - disp_qty)
                        batch.save()

    def _seed_billing(self, patients, consultations, users):
        cashier = User.objects.filter(role__name='accueil').first()
        today = date.today()

        inv_num = 1
        for consult in consultations[:10]:
            consultation_fee = random.choice([5000, 7500, 10000, 15000])
            lab_fee = random.choice([0, 3000, 5000, 8000, 12000])
            med_fee = random.choice([2000, 5000, 8000, 15000, 25000])

            subtotal = consultation_fee + lab_fee + med_fee
            insurance_cov = Decimal('0')
            if consult.patient.insurance_provider:
                insurance_cov = Decimal(str(subtotal)) * Decimal('0.7')

            amount_due = Decimal(str(subtotal)) - insurance_cov
            status = random.choice(['paid', 'paid', 'pending', 'partially_paid'])

            invoice = Invoice.objects.create(
                invoice_number=f'FAC-2026-{inv_num:04d}',
                patient=consult.patient,
                consultation=consult,
                status=status,
                subtotal=Decimal(str(subtotal)),
                tax_amount=Decimal('0'),
                discount=Decimal('0'),
                total=Decimal(str(subtotal)),
                insurance_coverage=insurance_cov,
                amount_due=amount_due,
                currency='XAF',
                due_date=today + timedelta(days=30),
            )
            inv_num += 1

            # Invoice items
            InvoiceItem.objects.create(
                invoice=invoice,
                description='Consultation medicale',
                category='consultation',
                quantity=1,
                unit_price=Decimal(str(consultation_fee)),
                total_price=Decimal(str(consultation_fee)),
            )
            if lab_fee > 0:
                InvoiceItem.objects.create(
                    invoice=invoice,
                    description='Examens de laboratoire',
                    category='lab',
                    quantity=1,
                    unit_price=Decimal(str(lab_fee)),
                    total_price=Decimal(str(lab_fee)),
                )
            if med_fee > 0:
                InvoiceItem.objects.create(
                    invoice=invoice,
                    description='Medicaments',
                    category='medication',
                    quantity=1,
                    unit_price=Decimal(str(med_fee)),
                    total_price=Decimal(str(med_fee)),
                )

            # Payments
            if status in ('paid', 'partially_paid'):
                pay_amount = amount_due if status == 'paid' else amount_due * Decimal('0.5')
                Payment.objects.create(
                    invoice=invoice,
                    amount=pay_amount,
                    payment_method=random.choice(['cash', 'mtn_momo', 'orange_money', 'cash', 'cash']),
                    transaction_id=f'TXN-{random.randint(100000, 999999)}' if random.random() > 0.5 else '',
                    status='completed',
                    payment_date=timezone.now() - timedelta(days=random.randint(0, 14)),
                    received_by=cashier,
                )
