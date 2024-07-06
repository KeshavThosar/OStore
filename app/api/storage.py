'''
API definitions for the storage api
Currently supported endpoints:
/storage/add - upload a file
/storage/get - download a file by using the file identifier
/storage/list - list all the files in the store
/storage/replace - update a specific file uploaded by the same user
/storage/remove - remove a file from the store
'''

import os
import hashlib
import uuid

from .handler import EndpointHandler
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from database.models import User, StoreObject

class Storage(EndpointHandler):
	def __init__(self, db: SQLAlchemy):
		super().__init__({
			'add': self.add_item,
			'list': self.list_items,
			'replace': self.replace_item,
			'remove': self.remove_item
		})

		self.db: SQLAlchemy = db
		dir_path = os.path.dirname(os.path.realpath(__file__))
		self.storage = os.path.join(dir_path, '..', 'storage')


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

	def replace_item(self):
		return 'OK'

	def remove_item(self):
		return 'OK'

   