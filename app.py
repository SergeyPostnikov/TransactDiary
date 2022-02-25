from flask import Flask, jsonify, request

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from flask_apispec import use_kwargs, marshal_with
from schemas import UserSchema, TransactionSchema, AuthSchema
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

client = app.test_client()
engine = create_engine('mysql://root:1234@localhost/wallet')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

docs = FlaskApiSpec()
docs.init_app(app)

from models import *
Base.metadata.create_all(bind=engine)



@app.route('/users', methods=['GET'])
@marshal_with(UserSchema(many=True))
def get_users():
	users = User.get_users()
	return users


@app.route('/users', methods=['POST'])
@use_kwargs(UserSchema)
@marshal_with(UserSchema)
def create_user(**kwargs):
	user = User(**kwargs)
	session.add(user)
	session.commit()
	return user


@app.route('/register', methods=['POST'])
@use_kwargs(UserSchema)
@marshal_with(AuthSchema)	
def register(**kwargs):
	user = User(**kwargs)
	session.add(user)
	session.commit()
	token = user.get_token()
	return jsonify({'access_token': token})


@app.route('/login', methods=['POST'])
@use_kwargs(AuthSchema)
@marshal_with(AuthSchema)	
def login(**kwargs):
	user = User.auth(**kwargs)
	token = user.get_token()
	return jsonify({'access_token': token})	


@app.route('/user/<int:user_id>', methods=['PUT'])
@use_kwargs(UserSchema)
@marshal_with(UserSchema)
def update_user(user_id, **kwargs):
	user = User.get_user(user_id=user_id)

	if not user:
		return f'have no user with id {user_id}', 400
	
	user.update_user(**kwargs)
	return user



@app.route('/user/<int:user_id>', methods=['DELETE'])
@marshal_with(UserSchema)
def delete_user(user_id):
	user = User.delete_user(user_id=user_id)
	return user



@app.route('/user/transactions', methods=['GET'])
@marshal_with(TransactionSchema(many=True))
def get_transactions():
	user_id = get_jwt_identity()
	return Transaction.get_transactions(user_id=user_id)


@app.route('/user/transaction', methods=['POST'])
@use_kwargs(TransactionSchema)
@marshal_with(TransactionSchema)
def create_transaction(**kwargs):
	user_id = get_jwt_identity()
	transaction = Transaction(user_id=user_id, **kwargs)
	session.add(transaction)
	session.commit()
	return transaction


@app.route('/user/transaction/<int:id>', methods=['PUT'])
@use_kwargs(TransactionSchema)
@marshal_with(TransactionSchema)
def update_transaction(id, **kwargs):
	transaction = Transaction.get_transaction(tr_id=id)
	transaction.update_transaction(tr_id=id, **kwargs)
	return transaction


@app.route('/user/transaction/<int:id>', methods=['DELETE'])
@marshal_with(TransactionSchema)
def delete_transaction(id):
		return Transaction.delete_transaction(tr_id=id)


@app.teardown_appcontext
def shutdown_session(*args, **kwargs):
	session.remove()


docs.register(get_users)
docs.register(create_user)
docs.register(update_user)
docs.register(delete_user)
docs.register(login)

# docs.register(get_transactions)
# docs.register(create_transaction)
# docs.register(update_transaction)
# docs.register(delete_transactio)



if __name__ == '__main__':
	app.run(debug = True)