from wtforms import Form, StringField, IntegerField, validators,TextField

class DoctorForm(Form):
	id = StringField('id')
	name = StringField('Name', [validators.Length(min=4, max=100)])
	email = StringField('Email Address', [validators.Email(message='Enter a valid email id')])
	phoneNumber = StringField('Phone Number', [validators.required()])
	description = TextField('Description')
	experience = IntegerField('Experience', [validators.required()])
	speciality = StringField('Speciality', [validators.required()])
	education = StringField("Education: ")

class ClinicForm(Form):
	#Clinic
	id = StringField('id')
	clinicName = StringField('Clinic Name', [validators.required()])
	locality = StringField('Locality', [validators.required()])
	city = StringField('City', [validators.required()])
	address = StringField('Address', [validators.required()])
	services = StringField('Services')