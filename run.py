from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from databaseApp.database import init_db, db_session
from databaseApp.models import Doctor, Clinic, DocClinic
from databaseApp.forms import DoctorForm, ClinicForm
import json
import newrelic.agent
from sqlalchemy import func,sql,desc,asc
init_db()
newrelic.agent.initialize("newrelic.ini")

def case(name):
	return func.lower(name)

def lCase(name):
	return name.lower()


app = Flask(__name__)
app.secret_key = "123456789"

@app.route('/search', methods = ['GET','POST'])
def search():
	doctors = Doctor.query.all()
	specialities = [doc.speciality for doc in doctors]
	clinics = Clinic.query.all()
	locations = [clnc.locality for clnc in clinics]
	return render_template('search.html')# listOfSpecialities = json.dumps(list(set(specialities))), listOfClinics = json.dumps(list(set(locations))))

@app.route('/doctor/<doctor_id>')
@app.route('/doctor/<doctor_id>/')
def getDoctor(doctor_id):
	doctor = Doctor.query.get(int(doctor_id))
	result = {}
	if doctor:
		result['name'] = doctor.name
		result['email'] = doctor.email
		result['education'] = doctor.education
		result['phone'] = doctor.phoneNumber
	return jsonify(results = result)

@app.route('/search/<location>/<specialization>/', methods = ['GET','POST'])
@app.route('/search/<location>/<specialization>', methods = ['GET', 'POST'])
@app.route('/search/<location>/<specialization>/<int:page>', methods = ['GET', 'POST'])
def results(location, specialization, page = 1):
	pageSize = 5
	queryResults = db_session.query(DocClinic).join(Doctor).join(Clinic).filter(case(Clinic.locality).like('%'+str(lCase(location))+'%')).filter(case(Doctor.speciality).like('%'+str(lCase(specialization))+'%')).filter(Doctor.id == DocClinic.doctor_id).filter(Clinic.id == DocClinic.clinic_id).offset(int((page-1)*pageSize)).limit(int(pageSize+1)).all()
	results,more,exJson = [],{},[]
	for x in queryResults:
		results.append((x.doctors,x.clinics,x.fees,x.timings))
		exJson.append({"name" : x.doctors.name,"speciality":x.doctors.speciality, "id" :x.doctors.id})
	if queryResults:
		location = queryResults[0].clinics.locality
		specialization = queryResults[0].doctors.speciality
	if len(results) > pageSize:
		more['hasMore'] = True
		results = results[:len(results)-1]
		more['nextLink'] = str(page + 1)
	else:
		more['hasMore'] = False
	if page > 1:
		more['prevLink'] = str(page - 1)

	isblank=False
	if(len(results) == 0):
		isblank=True
	print exJson
	return jsonify(results = exJson)
	#return render_template("resultsPage.html", results = results, job = specialization, address = location, num = len(results), more = more, page = page )

@app.route('/',methods = ['GET','POST'])
def home():
	doctors = Doctor.query.all()[:200]
	form = DoctorForm(request.form)
	if request.method == 'POST':
		if form.validate():
			#flash ('Form Validated')
			if form.id.data == '':
				doc = Doctor(name = form.name.data, email = form.email.data, phoneNumber = form.phoneNumber.data, description = form.description.data, education = form.education.data, experience = form.experience.data, speciality = form.speciality.data)
				db_session.add(doc)
				db_session.commit()
				doctors = Doctor.query.all()
		else:
			flash ('Form Validation unsuccessful. Please enter valid data')
			return render_template("addDoctor.html",form = form)
	return render_template("home.html", doctors = doctors, form = form)

@app.route('/addDoctor')
def addDoctor():
	form = DoctorForm(request.form)
	return render_template("addDoctor.html", form = form)

@app.route('/editDoctor/<doctor_id>', methods = ['GET','POST'])
def editDoctor(doctor_id):
	try:
		doc = Doctor.query.get(int(doctor_id))
		form = DoctorForm(request.form)
		#return render_template("editDoctor.html",form=form,doctor=doc)
	except AttributeError:
		return render_template("home.html", errMsg = "No Such Doctor")
	if request.method == 'POST':
		if form.validate():
			doc.name = form.name.data
			doc.email = form.email.data
			doc.phoneNumber = form.phoneNumber.data
			doc.description = form.description.data
			doc.education = form.education.data
			doc.experience = form.experience.data
			db_session.commit()
			doctors = Doctor.query.all()
			return render_template("home.html", doctors = doctors)
		else:
			flash("Invalid data entered!!")
			doctors = Doctor.query.all()
			return render_template('editDoctor.html', doctor = doc, form = form)
	else:
		return render_template("editDoctor.html", doctor = doc, form = form)

@app.route('/delete/<doctor_id>', methods = ['GET','POST'])
def deleteDoctor(doctor_id):
	try:
		doc = Doctor.query.get(int(doctor_id))
	except AttributeError:
		return render_template("home.html", errMsg = "No Such doctor")
	DocClinic.query.filter_by(doctor_id = doctor_id).delete()
	Doctor.query.filter_by(id = doctor_id).delete()
	db_session.commit()
	doctors = Doctor.query.all()
	return render_template("home.html", doctors = doctors)

@app.route('/addClinic/<doctor_id>', methods = ['GET','POST'])
def addClinic(doctor_id):
	form = ClinicForm(request.form)
	doctor = Doctor.query.get(int(doctor_id))
	doctors = Doctor.query.all()
	if request.method == 'POST':
		if form.validate():
			clinic = Clinic.query.filter_by(clinicName = form.clinicName.data, locality = form.locality.data, city = form.city.data, address = form.address.data).first()
			docclinic = DocClinic(request.form['fees'], request.form['timings'])
			db_session.add(docclinic)
			if clinic:
				docclinicAll = DocClinic.query.filter_by(doctor_id = doctor.id, clinic_id = clinic.id).first()
				if docclinicAll:
					return render_template("home.html", errMsg = "Already added for this doctor", doctors = doctors)
				doctor.docClinics.append(docclinic)
				clinic.docClinics.append(docclinic)
				db_session.commit()
			else:
				clinic = Clinic(clinicName = form.clinicName.data, locality = form.locality.data, city = form.city.data, address = form.address.data, services = form.services.data)
				db_session.add(clinic)
				doctor.docClinics.append(docclinic)
				clinic.docClinics.append(docclinic)
				db_session.commit()
		else:
			flash ('Form Validation unsuccessful. Please enter valid data')
		return render_template("home.html", doctors = doctors)
	else:
		return render_template("addClinic.html", form = form, doctor = doctor)

@app.route('/viewAllClinics')
def viewAllClinics():
	clinics = Clinic.query.all()
	if len(clinics) > 500:
		clinics = clinics[:300]
	return render_template("clinics.html", clinics = clinics)

@app.route('/viewClinics/<doctor_id>')
def clinics(doctor_id):
	doctor = Doctor.query.get(int(doctor_id))
	clinicList = [x.clinics  for x in doctor.docClinics]
	return render_template("clinics.html", clinics = clinicList)

@app.route('/deleteClinic/<clinic_id>', methods = ['GET','POST'])
def deleteClinic(clinic_id):
	try:
		clinic = Clinic.query.get(int(clinic_id))
	except AttributeError:
		doctors = Doctor.query.all()
		return render_template("home.html", doctors = doctors, errMsg = "No Such clinic")
	DocClinic.query.filter_by(clinic_id = clinic_id).delete()
	doctors = Doctor.query.all()
	return render_template("home.html", doctors = doctors)

@app.route('/editClinic/<clinic_id>', methods = ['GET','POST'])
def editClinic(clinic_id):
	try:
		clinic = Clinic.query.get(int(clinic_id))
	except AttributeError:
		doctors = Doctor.query.all()
		return render_template("home.html", doctors = doctors, errMsg = "No Such clinic")
	form = ClinicForm(request.form)
	if request.method == 'POST':
		if form.validate():
			clinic.clinicName = form.clinicName.data
			clinic.locality = form.locality.data
			clinic.city = form.city.data
			clinic.address = form.address.data
			clinic.services = form.services.data
			db_session.commit()
		else:
			flash("Invalid data entered. Please verify and try again.")
		doctors = Doctor.query.all()
		return render_template("home.html", doctors = doctors)
	else:
		return render_template("editClinics.html", form = form, clnc = clinic)

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"),404

if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0')
