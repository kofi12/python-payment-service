## How to run the service/test

### Docker Container

- this service is dockarized and pushed to docker hub
- you can run this container with the following command in terminal provided you've downloaded the docker CLI
- docker run -p 8000:8000 akhaizel/payment_service:test
- run the test version rather than "latest", the only difference is the test provides a small client to make testing easier
- testing with curl or postman may lead to CORS related issues
- IMPORTANT, please open the link in Safari, if you still have an issue remove '0.0.0.0' in the url for 'localhost'
- behaviour is less predictable on other browsers, CORS issues ect.


### Testing Locally

- you must have python 3.11 installed on your machine
- afterwards, install poetry(used to manage dependencies in python) with the command `pip install poetry`
- run the command `poetry shell` this should create a virtualenvironment
- run the command `poetry install` poetry will install dependencies in the pyproject.toml file
- now that the dependencies are installed you can run the service with the command `poetry run uvicorn main:app --reload`


### Test cases

- because this backend is built using the FastApi framework documentation is provided by default
- to access the docs, once the server is running go to 'http://localhost:8000/docs'
- you can test the end points there as well