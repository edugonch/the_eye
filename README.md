# The Eye

## Conclutions

1) Application should respond quick, even is there are erros on the payload, the user interaction can't be delayed b/c a process error or delayed on the backend
2) Add a token authentication so the eye can be sure this is a trusted client, the token can be created on the django admin backend, linked to an user.
3) I took the example use cases, I tryied to make a modular architecture, so in case of adding more use cases I can have the flexibility to do this

## Requirements

1) The database use the default SQLite, so you won't need to install a server db
2) You will need a redis instance running on port 6379
