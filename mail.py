import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#Email will be sent from MSPi Gmail account
fromEmail = 'mspismartcam@gmail.com'
#Ask me for Password (Nick)
fromEmailPassword = 'ENTER PASSWORD HERE'

# Email your email here for testing
toEmail = 'nicolas182@icloud.com'

# Function sends the image of the person detected on your porch
def sendEmail(image):
	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = 'MSPi Security Update'
	msgRoot['From'] = fromEmail
	msgRoot['To'] = toEmail
	msgRoot.preamble = 'MSPi camera update'

	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)
	msgText = MIMEText('Smart security cam found object')
	msgAlternative.attach(msgText)

	msgText = MIMEText('<img src="cid:image1">', 'html')
	msgAlternative.attach(msgText)

	msgImage = MIMEImage(image)
	msgImage.add_header('Content-ID', '<image1>')
	msgRoot.attach(msgImage)

	smtp = smtplib.SMTP('smtp.gmail.com', 587)
	smtp.starttls()
	smtp.login(fromEmail, fromEmailPassword)
	smtp.sendmail(fromEmail, toEmail, msgRoot.as_string())
	smtp.quit()
