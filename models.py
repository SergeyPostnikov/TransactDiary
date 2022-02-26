from app import db, session, Base
from datetime import datetime
from datetime import timedelta

class User(Base):
	__tablename__ = 'users'
	user_id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(20), nullable=False)
	lastname = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(50), nullable=False, unique=True)
	psw = db.Column(db.String(500), nullable=False)

	def __init__(self, **kwargs):
		self.name = kwargs.get('name')
		self.email = kwargs.get('email')
		self.password = bcrypt.hash(kwargs.get('psw'))

	@classmethod
	def get_users(cls):
		return cls.query.all()

	@classmethod
	def get_user(cls, user_id=None, email=None):
		if bool(user_id) != bool(email):
			if not email:
				return cls.query.filter(cls.user_id==user_id).first()
			return cls.query.filter(cls.email==email).first()

	def update_user(self, **kwargs):
		for key, field in kwargs.items():
			setattr(self, key, field)
		session.commit()

	@classmethod
	def delete_user(cls, user_id):
		user = cls.get_user(user_id=user_id)
		session.delete(user)
		session.commit()
		return user

	def __repr__(self):
		return f'<user with id: {self.user_id}>'



class Transaction(Base):
	__tablename__ = 'transactions'
	tr_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete="CASCADE"))
	description = db.Column(db.String(50), nullable=True)
	amount = db.Column(db.Float(10, 2), nullable=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	
	def __repr__(self):
		return f'<Transaction with id: {self.tr_id}>'

	@classmethod
	def get_transactions(cls, user_id):
		return cls.query.filter(user_id==user_id).all()

	@classmethod
	def get_transaction(cls, tr_id):
		return cls.query.filter_by(tr_id=tr_id).first()

	def update_transaction(self, **kwargs):
		for key, field in kwargs.items():
			setattr(self, key, field)
		session.commit()
		return self

	@classmethod
	def delete_transaction(cls, tr_id):
		transaction = cls.get_transaction(tr_id=tr_id)
		session.delete(transaction)
		session.commit()
		return transaction
	

