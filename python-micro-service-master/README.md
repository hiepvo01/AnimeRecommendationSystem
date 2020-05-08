## Up and Running

Install dependencies and enable the code in place.
```bash
$ pipenv install
$ pipenv run pip install --editable . --upgrade

set GOOGLE APPLICATION ENV:
 - use command:
  	-Windows: $env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\Andrew\OneDrive\Desktop\ds320-project2\python-micro-service-master\src\delivery\api\microservice\animebot-cbaheo-0c67109ae56b.json"
	-Linux : export GOOGLE_APPLICATION_CREDENTIALS="[PATH to client Json 
		(InspirationalQuote Json file)]"

$ pipenv install requests
$ pipenv install dialogflow
$ pipenv run uvicorn --reload delivery.api.microservice:app
```
