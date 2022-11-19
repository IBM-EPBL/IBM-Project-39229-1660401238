
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
def sendgridmail(user,TEXT):
    sg = sendgrid.SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    from_email = Email("nehanthkg@gmail.com")  
    to_email = To(user)  
    subject = "Registered Successfully"
    content = Content("text/plain",TEXT)
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()
    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)


if __name__ == '__main__':
    sendgridmail('ssquarecsquare@gmail.com', "Registered Successfully")
    