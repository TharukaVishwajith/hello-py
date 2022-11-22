FROM python:3-alpine

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY . .

EXPOSE 5000
CMD [ "gunicorn","-w","2","-b","0.0.0.0:5000","app:create_app(test_config=None,env='PROD')"]