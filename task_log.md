# Todos 
## TD_sql_model
Objective: Create a model for object to store metadata 
Start Date: 3 July, 2024
End Date: 

### Implementations
Object { id, filename, hash, created_datetime }

id: Primary key, auto-generated  
filename: Name of the uploaded file, provided by user  
hash: SHA256 hash of the uploaded file, actual file is stored with this name
created_datetime: timestamp for time of upload

