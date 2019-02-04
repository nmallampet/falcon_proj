A simple API service (built using Falcon) that lets user create useraccounts and tasks. 

Techstack:
	- Backend:
		- Python2.7
			- Falcon
		- PostgresSQL 
		
API rest format: {Hostname}:/api/{version}/{name}/{action}
Project Heirarchy 
	- src
		- api 
			- uauth (user authentication and creation api service)
			- pm (task creation authentication and creation)
		- db 
			- init_db (script to create appropriate db and tables in postgres)



			
		
			
			