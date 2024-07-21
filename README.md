# OStore
An open-source, end to end, object/file storage solution

## Introduction
OStore is a free open source file/object storage api service that could be used to easily store, download and modify files on a server.  
The service is implemented using the following technologies:   
- Flask (For handling http requests)
- SQLite (For storing user and file data)  

## Installation and Usage
To install, clone the repository
```
git clone https://github.com/KeshavThosar/OStore.git
cd OStore
```

To install all the required dependencies
```
pip install -r requirements.txt
```
**Recommended: Use a virtual environment for better isolation. You can create one using the venv module**

To run the server
```
python app/app.py
```

You can access a testing frontend on `http://localhost:5000`

## Endpoints
### Authentication
| Endpoint  | Method | Parameters | Description |
| --- | --- | --- |---  |
| **/auth/register**  |  POST |  email, password | register to the service using an email  |
| **/auth/login**  | POST | email, password  | retrieve access token using email and password |

### Storage

| Endpoint  | Method | Parameters | Description |
| --- | --- | --- |---  |
| **/storage/add** | POST | filename, file | upload a file |
| **/storage/download** | GET | id | download a file by using the file identifier |
| **/storage/list** | GET | - | list all the files in the store |
| **/storage/get** | GET | id |  get information for a file by using the file identifier |
| **/storage/replace** | PUT | id, file | update a specific file uploaded by the same user |
| **/storage/remove** | DELETE | id | remove a file from the store |

**Remember: To use the service, you need to first login using the auth api and pass the access_token as the Bearer token in the Authorization header for each request**
 
 

