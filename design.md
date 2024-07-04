# Object Store  

## Objective  
To create an object storage service where user can upload files via an API/UI  

## Additional Feature  
- Structing can be flat or nested (an object's location is mapped to a route)  
- Distributed system with backup and load balancing
- Object Router

## Tech Stack (Initial):  
- Backend: Python, Flask, SQLite  
- Frontend: Javascript  
- Infrastructure (Later): Docker  

## Todo
[x] Create a model for object to store metadata : TD_sql_model
[ ] Create a simple file upload api using Flask : TD_upload_api
[ ] Keep behind an auth token: TD_auth_api
[ ] Implement a File Finder for retrieving from multiple storage locations : TD_file_finder (Later)
[ ] Dockerize the software : TD_docker
[ ] Rollout multiple instances using K8S : TD_k8s
[ ] Put the system infront of load balancer: TD_load_balancer
[ ] Create Demo Video

