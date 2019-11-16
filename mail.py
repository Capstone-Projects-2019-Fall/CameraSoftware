import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.image import MIMEImage
import firebase_admin
from firebase import firebase
from firebase_admin import credentials
from firebase_admin import storage
from google.cloud import firestore
from firebase_admin import firestore

#Email will be sent from MSPi Gmail account
fromEmail = 'mspismartcam@gmail.com'
#Ask me for Password (Nick)
fromEmailPassword = 'MspiCamera4398'



db = firestore.client()
bucket = storage.bucket()




# Function sends the image of the person detected on your porch
def sendEmail():
   
    doc_ref = db.collection(u'users').document(u'SD3qcbNMAjTx7ComsRGTXFji22d2')
    doc = None
    try:
        doc = doc_ref.get()
        
    except google.cloud.exceptions.NotFound:
        print(u'No such document!')


    print(doc.to_dict()['email'])
    # Email your email here for testing
    toEmail = doc.to_dict()['email']
    #toEmail = "nicolas182@icloud.com"
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'MSPi Security Update'
    msgRoot['From'] = fromEmail
    msgRoot['To'] = toEmail
    msgRoot.preamble = 'MSPi camera update'
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    msgText = MIMEText('MSPi security detected a person')
    msgAlternative.attach(msgText)

    msgText = MIMEText('<img src="cid:image1">', 'html')
    msgAlternative.attach(msgText)

    
    fp = open('/home/pi/Desktop/CameraSoftware/WhoDat.jpg', 'rb')
    #fp = open('/Users/nick/Desktop/cameraRepo/CameraSoftware/WhoDat.jpg', 'rb')
    
    msgImage = MIMEImage(fp.read())
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(fromEmail, fromEmailPassword)
    smtp.sendmail(fromEmail, toEmail, msgRoot.as_string())
    smtp.quit()
