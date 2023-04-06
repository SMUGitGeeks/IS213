# 1. Open the link below in a browser to get an authorization code and copy it
# https://www.dropbox.com/oauth2/authorize?client_id=slittbfjy2ckrmn&token_access_type=offline&response_type=code
# client_id is our app_key as shown below

# 2. replace authorization code placeholder below with the code from step #1. 
# 3. run the following python code 
import requests

app_key = "slittbfjy2ckrmn"
app_secret = "v4qvy9gam785dvy"

# build the authorization URL:
authorization_url = "https://www.dropbox.com/oauth2/authorize?client_id=%s&response_type=code" % app_key

# send the user to the authorization URL:
print('Go to the following URL and allow access:')
print(authorization_url)

# get the authorization code from the user:
authorization_code = 'Authorization code here'
# authorization_code = 'GBTvNZzMglYAAAAAAAAADbfRe0aAgawHcjhiNp6hW9c'


# exchange the authorization code for an access token:
token_url = "https://api.dropboxapi.com/oauth2/token"
params = {
    "code": authorization_code,
    "grant_type": "authorization_code",
    "client_id": app_key,
    "client_secret": app_secret
}
r = requests.post(token_url, data=params)
print(r.text)

# 4. copy text in access_token from the printed r.text
# it should be long string starting with sl. 

# 5. go to apply_ui_vue.html, replace this copied access_token in the placeholder in const headers authorisation : <token>
