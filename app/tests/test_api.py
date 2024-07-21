# Use pytest to run the unit tests
import os
import requests
from dotenv import load_dotenv

load_dotenv()

response: requests.Response = requests.post(
  url=f"http://localhost:{os.environ['PORT']}/auth/login",
  data={'email': os.environ['test_user'], 'password': os.environ['test_pass']}
  )

dir_path = os.path.dirname(os.path.realpath(__file__))
test_file_name =  'test_upload.txt'
test_file = os.path.join(dir_path, test_file_name)

access_token = response.json()['access_token']
auth_header = {'Authorization': 'Bearer ' + access_token}
api_url = f"http://localhost:{os.environ['PORT']}"

def test_auth():
  response = requests.post(
    url=api_url + '/auth/login',
    data={'email': os.environ['test_user'], 'password': os.environ['test_pass']}
  )
  assert response.ok

def test_storage():
  f = open(test_file, 'rb')
  response = requests.post(
    url=api_url + '/storage/add',
    headers=auth_header,
    data={'filename': test_file_name},
    files={'file':f}
  )
  f.close()

  upload_ok = response.ok

  response = requests.get(
    url=api_url + '/storage/list',
    headers=auth_header
  )

  res = response.json()
  files = list(filter(lambda x: x['name'] == test_file_name, res))

  list_ok = len(files) == 1

  test_file_identifier = files[0]['identifier']

  response = requests.delete(
    url=api_url + '/storage/remove?id='+test_file_identifier,
    headers=auth_header
  )

  delete_ok = response.ok

  assert upload_ok and list_ok and delete_ok