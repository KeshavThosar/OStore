# Todos 
## TD_sql_model
Objective: Create a model for object to store metadata  
Start Date: 3 July, 2024  
End Date: 5 July, 2024  

### Implementations
Object { id, filename, hash, created_datetime }  

id: Primary key, auto-generated   
filename: Name of the uploaded file, provided by user  
hash: SHA256 hash of the uploaded file, actual file is stored with this name  
created_datetime: timestamp for time of upload  

## TD_upload_api
Objective: To create a CRUD endpoint for file uploads  
Start Date: 5 July, 2024  
End Date: 13 July, 2024  

### Considerations
Needs to be integrated with database  
Once implemented, this needs to be hooked with the authentication  

### Endpoints
/storage/add -> filename, file  
/storage/get -> id  
/storage/list  
/storage/replace  
/storage/remove  

## TD_auth_api
Objective: To create an authentication system for preventing unautorised access to storage api  
Start Date: 13 July, 2024  
End Date: 14 July, 2024  

### Considerations
Needs to be integrated with database  
Once implemented, this needs to be hooked with the storage api  
JWT for token exchange  
Access Token is passed as Bearer Token in any storage requests  

### Endpoints
/auth/register -> email, password  
/auth/login -> email, password : access_token  

### Utilities
is_token_valid(token) : checks if token is valid or expired  

## TD_frontend
Objective: To develop a very simple UI to display the functionality of the service  
Start Date: 14 July, 2024   
End Date:  

### Considerations
Basic Login and Register Page  
Dashboard display all uploaded files with option to upload, replace, remove files  

