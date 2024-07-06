'''
API definitions for the storage api
Currently supported endpoints:
/storage/add - upload a file
/storage/download - download a file by using the file identifier
/storage/list - list all the files in the store
/storage/get -  download information for a file by using the file identifier
/storage/replace - update a specific file uploaded by the same user
/storage/remove - remove a file from the store
'''

import os
import hashlib
import uuid

from .handler import EndpointHandler
from flask import request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from database.models import User, StoreObject

class Storage(EndpointHandler):
	def __init__(self, db: SQLAlchemy):
		super().__init__({
			'add': self.add_item,
			'list': self.list_items,
			'get': self.get_item,
			'download': self.download_item,
			'replace': self.replace_item,
			'remove': self.remove_item
		})

		self.db: SQLAlchemy = db
		dir_path = os.path.dirname(os.path.realpath(__file__))
		self.storage = os.path.join(dir_path, '..', 'storage') # storage location


	def add_item(self):
		response = {}
		if request.method == 'POST':
			file_identifier = str(uuid.uuid4())
			file_path = os.path.join(self.storage, file_identifier)
			sh256 = hashlib.sha256()
			fname = secure_filename(request.form['filename'])

			db_session = self.db.session

			file_in_store = db_session.execute(
				self.db.select(StoreObject).filter_by(file_name=fname)
				).scalar_one_or_none()
			
			if file_in_store is not None:
				response['message'] = 'File already exists!'
				return jsonify(response), 409 # Conflict
			
			f = request.files['file']	
			f.save(file_path)
			f.close()

			with open(file_path, 'rb') as f:
				sh256.update(f.read())
			
			file_hash = sh256.hexdigest()

			storeObject = StoreObject(
				file_name = fname,
				file_hash = file_hash,
				file_identifier = file_identifier,
				user_id = 1 # for testing
			)

			db_session.add(storeObject)
			db_session.commit()

			response['message'] = 'File uploaded successfully'
			response['name'] = fname
			response['hash'] = file_hash
			response['identifier'] = file_identifier

		return jsonify(response), 201 # Created

	def list_items(self):
		db_session = self.db.session
		storeObjects = db_session.execute(self.db.select(StoreObject)).scalars().all()
		files = map(lambda x: {
			'name': x.file_name, 
			'identifier': x.file_identifier, 
			'hash': x.file_hash,
			'created_on': x.creation_datetime
			}, storeObjects)
		
		return jsonify(list(files)), 200

	def check_for_file(self, identifier):
		db_session = self.db.session
		file_fetch = db_session.execute(
			self.db.select(StoreObject).filter_by(file_identifier=identifier)
			).scalar_one_or_none()
		return file_fetch

	def get_item(self):
		file_identifier = request.args.get('id')
		file_fetch = self.check_for_file(file_identifier)
		response = {}
		if file_fetch is None:
			response['message'] = 'no file exists for the provided id'
			return jsonify(response), 404
		
		return jsonify({
			'message': 'file information retrieved successfully',
			'name': file_fetch.file_name, 
			'identifier': file_fetch.file_identifier, 
			'hash': file_fetch.file_hash,
			'created_on': file_fetch.creation_datetime
		}), 200

	def replace_item(self):
		response = {}
		identifier = request.args.get('id', None)
		if request.method == 'PUT':
			pass

			if identifier is None:
				response['message'] = 'file identifier (id) not provided or is invalid'
				return jsonify(response), 406 # Unacceptable
			
			file_fetch()

		

		return jsonify(response), 200
	
	def download_item(self):
		identifier = request.args.get('id', None)
		response = {}
		if identifier is None:
			response['message'] = 'file identifier (id) not provided or is invalid'
			return jsonify(response), 406 # Unacceptable
		
		file_fetch = self.check_for_file(identifier)
		if file_fetch is None:
			response['message'] = 'no file exists for the provided id'
			return jsonify(response), 404
		
		file_to_send = os.path.join(self.storage, file_fetch.file_identifier)
		return send_file(file_to_send, download_name=file_fetch.file_name), 200
		
	def remove_item(self):
		response = {}
		if request.method == 'DELETE':
			identifier = request.args.get('id', None)
			if identifier is None:
				response['message'] = 'file identifier (id) not provided or is invalid'
				return jsonify(response), 406 # Unacceptable
			
			file_fetch = self.check_for_file(identifier)
			if file_fetch is None:
				response['message'] = 'no file exists for the provided id'
				return jsonify(response), 404
			
			db_session = self.db.session
			db_session.delete(file_fetch)
			db_session.commit()

			response['message'] = 'file was deleted successfully'

		else:
			response['message'] = 'file can be removed only using DELETE request'
			return jsonify(response), 405
				
		return jsonify(response), 200

   