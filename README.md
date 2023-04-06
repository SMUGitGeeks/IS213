# IS213

## Enterprise Solution Development Project

### First Setup

#### 1. Change the environment variables accordingly on the compose files

Compose files: docker-compose.yml, docker-compose-student.yml, kong/docker-compose.yml

#### 2. Create the required databases and run the sql files

#### 3. Run the following commands

Kong:<br>
`docker-compose -f kong/docker-compose.yml up`

Student:<br>
`docker-compose -f docker-compose-student.yml up`

Everything else:<br>
`docker-compose -f docker-compose.yml up`

#### 4. Get API key for dropbox

a. Generate an access code
from [Dropbox Access Code Generator](https://www.dropbox.com/oauth2/authorize?client_id=slittbfjy2ckrmn&token_access_type=offline&response_type=code)

b. Paste access code into line 20 of apply_job/oauth.py<br>
`authorization_code = '<code>''`

c. Run the following command<br>
`python apply_job/oauth.py`

d. Copy the access token and paste it into line 163 of apply_ui_vue.html<br>
`'Authorization': '<token>',`

#### 5. Setup Kong

a. Visit http://localhost:1337/

b. Create account and login

c. Fill in the fields<br>
Name: `default`<br>
Kong Admin URL: `http://kong:8001`<br>
Create connection

d. Click on Services and Add New Service <br>
Name: `create_job_api`<br>
Protocol: `http`<br>
Host: `createjob`<br>
Port: `5007`<br>
Path: `/create_job`<br>
Submit Changes

e. Click onto the newly created Service and click on Routes<br>
Add New Route<br>
Paths: `/api/v1/createjob`<br>
Methods: `POST`<br>

f. Click onto Consumers and Create Consumer
Username: `admin`

g. Add group to admin consumer
Groups: `Admins`

h. Add credential API Key to admin consumer

i. Go to plugins and install acl plugin
Whitelist: `Admins`



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

