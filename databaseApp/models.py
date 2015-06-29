from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey,Table
from database import Base
from sqlalchemy.orm import relationship, backref

class DocClinic(Base):
	__tablename__ = 'DocClinic'
	id = Column(Integer, primary_key = True)
	doctor_id = Column(Integer, ForeignKey('doctor.id'))
	clinic_id = Column(Integer, ForeignKey('clinic.id'))
	fees = Column(Integer, nullable = True)
	timings = Column(String(100), nullable = False)
	def __init__(self, fees, timings):
		self.timings = timings
		self.fees = fees

class Doctor(Base):
	__tablename__ = 'doctor'
	id = Column(Integer, primary_key = True)
	name = Column(String(100), nullable = False)
	email = Column(String(200), nullable = False)
	description = Column(String(500), nullable = True)
	experience = Column(Integer, nullable = False)
	education = Column(String(300), nullable = True)
	recommendations = Column(Integer, nullable = True)
	phoneNumber = Column(String, nullable = True)
	speciality = Column(String(200), nullable = False, index = True)
	docClinics = relationship('DocClinic', backref = backref('doctors'), lazy = 'dynamic')

	def __init__(self, name, experience = None, education = None, phoneNumber = None, description = None, email = None, speciality = None):
		self.name = name
		self.experience = experience
		self.education = education
		self.phoneNumber = phoneNumber
		self.description = description
		self.email = email
		self.speciality = speciality

	def __repr__(self):
		return '%s'%(self.name)

class Clinic(Base):
	__tablename__ = 'clinic'
	id = Column(Integer, primary_key = True)
	clinicName = Column(String(100), nullable = False)
	locality = Column(String(100), nullable = False,index = True)
	city = Column(String(100), nullable = False)
	address = Column(String(300), nullable = False)
	services = Column(String(400), nullable = True)
	docClinics = relationship('DocClinic', backref = 'clinics',lazy = 'dynamic')

	def __init__(self, clinicName, locality, city, address, services = None):
		self.clinicName = clinicName
		self.locality = locality
		self.address = address
		self.services = services
		self.city = city

	def __repr__(self):
		return '%s'%(self.clinicName)
