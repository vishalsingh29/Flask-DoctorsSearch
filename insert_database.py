from databaseApp.database import db_session, init_db
from databaseApp.models import Doctor, Clinic,DocClinic
from random import randint
from faker import Factory
init_db()
fake = Factory.create('en_US')

for _ in range(200):
	print _
	loct = ['BTM','Whitefield','JP Nagar','Jayanagar','Koramangala','Indira Nagar','Pratap Nagar','Gandhi Nagar','Hiran Magri','Yeshwantpur','Marathalli']
	clinic = Clinic(fake.street_name(),loct[int(randint(1,1000)%len(loct))],fake.city(),fake.address(),"Many Services")
	db_session.add(clinic)
	db_session.commit()

allClinics = Clinic.query.all()

for _ in range(1000):
	print _
	years = randint(1,20)
	spclts = ['Dentist','Cardiologist','Surgeon','Heart Specialist','Neurologist','Dermatologist','Brain Surgeon','Urologist','Psychologist','Psychiatrist']
	costs = [200,500,300,220,1239,233,2424,2324,1000]
	name = fake.name()
	name1 = name.split()[0]
	desc = fake.text()
	doc = Doctor(name,years,desc[:100],fake.phone_number(),"DESCRIPTION",name1+"@example.com",spclts[int(randint(1,1000)%len(spclts))])
	db_session.add(doc)
	
	dc = DocClinic(costs[int(randint(20,300)%len(costs))],"Monday to Friday, 8:00am to 10:00am")
	dc2 = DocClinic(randint(1,2000),"Monday to Thursday, 9:10am to 12:10pm")
	db_session.add(dc)
	db_session.add(dc2)
	x = randint(1,2000000)%200
	y = randint(1,2000000)%200
	clinic = allClinics[y]
	clinic.docClinics.append(dc)
	doc.docClinics.append(dc)
	if x != y:
		clinic2 = allClinics[x]
		doc.docClinics.append(dc2)
		clinic2.docClinics.append(dc2)
	db_session.commit()
