# IS213
## Enterprise Solution Development Project

### First Setup
#### 1. Change the environment variables accordingly on the compose files
Compose files: docker-compose.yml, docker-compose-student.yml, kong/docker-compose.yml
#### 2. Create the required databases and run the sql files
#### 3. Run the following commands
Kong: 

`docker-compose -f kong/docker-compose.yml up`

Student: 

`docker-compose -f docker-compose-student.yml up`

Everything else: 

`docker-compose -f docker-compose.yml up`

#### 4. Get API key for dropbox
a. Generate an access code from [Dropbox Access Code Generator](https://www.dropbox.com/oauth2/authorize?client_id=slittbfjy2ckrmn&token_access_type=offline&response_type=code)

b. Paste access code into line 21 of apply_job/oauth.py

`authorization_code = '<code>''`

c. Run the following command

`python apply_job/oauth.py`

d. Copy the access token and paste it into line 159 of apply_ui_vue.html

`'Authorization': '<token>',`


### Environment Variables:
#### Create Job URL
`environ.get('createJobURL')`

#### Student URL
`environ.get('studentURL')`

#### Job URL
`environ.get('jobURL')`

#### Module URL
`environ.get('moduleURL')`

#### Error URL
`environ.get('errorURL')`

#### Database URL
`environ.get('dbURL')`

#### Sendgrid API Key
`environ.get('sendgridAPIKey')`

