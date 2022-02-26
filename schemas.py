from marshmallow import Schema, validate, fields

class UserSchema(Schema):
	user_id = fields.Integer(dump_only=True)
	firstname = fields.String(required=True, validate=[validate.Length(max=50)])
	lastname = fields.String(required=True, validate=[validate.Length(max=50)])
	email = fields.String(required=True, validate=[validate.Length(max=50)])
	psw = fields.String(required=True, validate=[validate.Length(max=255)], load_only=True)


class TransactionSchema(Schema):
	tr_id = fields.Integer(dump_only=True)
	user_id = fields.Integer(required=True)
	description = fields.String(required=True, validate=[validate.Length(max=50)])
	amount = fields.Decimal(required=True)
	created_at = fields.DateTime(dump_only=True)
