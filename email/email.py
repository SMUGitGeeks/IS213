import sendgrid

sg = sendgrid.SendGridAPIClient('')
data = {
  "personalizations": [
    {
      "to": [
        {
          "email": "glenlow12374@gmail.com"
        }
      ],
      "subject": "Sending with SendGrid is Fun"
    }
  ],
  "from": {
    "email": "glen.low.2021@scis.smu.edu.sg"
  },
  "content": [
    {
      "type": "text/plain",
      "value": "and easy to do anywhere, even with Python"
    }
  ]
}
response = sg.client.mail.send.post(request_body=data)
print(response.status_code)
print(response.body)
print(response.headers)