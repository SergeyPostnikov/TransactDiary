from app import client
from models import Transaction, User
import unittest
from string_generator import string_generator
from random import randint

class TransactionTestCase(unittest.TestCase):
	def test_get_transactions(self):
		data = {'user_id': 1}
		result = client.get('/user/transactions', json=data)
		self.assertEqual(result.status_code, 200)
		self.assertEqual(len(result.get_json()), len(Transaction.query.all()))

	def test_create_transaction(self):
		data = {
			'user_id': 1,
			'description': string_generator(10),
			'amount': randint(-400, 1000)
			}		
		result = client.post('/user/transaction', json=data)		
		self.assertEqual(result.status_code, 200)
		self.assertEqual(result.get_json()['description'], data['description'])

	def test_update_transaction(self):
		data = {
			'user_id': 1,
			'description': string_generator(10),
			'amount': randint(-400, 1000)
			}
		transaction = Transaction.query.order_by(Transaction.tr_id.desc()).first()
		result = client.put(f'/user/transaction/{transaction.tr_id}', json=data)
		self.assertEqual(result.status_code, 200)
		self.assertEqual(result.get_json()['description'], data['description'])

	def test_delete_transaction(self):
		transaction = Transaction.query.order_by(Transaction.tr_id.desc()).first()
		tr_id = transaction.tr_id
		result = client.delete(f'/user/transaction/{transaction.tr_id}')
		self.assertEqual(result.status_code, 200)
		self.assertIsNone(Transaction.query.filter_by(tr_id=tr_id).first())


if __name__ == '__main__':
	def suite():
		tests = ['test_get_transactions', 'test_create_transaction', 
		'test_update_transaction', 'test_delete_transaction']
		return unittest.TestSuite(map(TransactionTestCase, tests))

	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite())
