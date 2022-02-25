from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin


class Config:
	SECRET_KEY = '7a317056db2f472abe2b010dc2c98336'
	APISPEC_SPEC = APISpec(
		title='wallet',
		version='v1',
		openapi_version='3.0.1',
		plugins=[MarshmallowPlugin()],)

	APISPEC_SWAGGER_URL = '/swagger/'