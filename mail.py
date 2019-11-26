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
import settings

#Email will be sent from MSPi Gmail account
fromEmail = 'mspismartcam@gmail.com'
#Ask me for Password (Nick)
fromEmailPassword = 'MspiCamera4398'



db = firestore.client()
bucket = storage.bucket()




# Function sends the image of the person detected on your porch
def sendEmail(people):
   
    doc_ref = db.collection(u'users').document(settings.userID)
    doc = None
    try:
        doc = doc_ref.get()
        
    except google.cloud.exceptions.NotFound:
        print(u'No such document!')

    
    if len(people) > 0:
        if len(people) == 1:
            htmlTxt = '''
            <html>
                <div style=' align-items: center; text-align: center; font-family: sans-serif; background-color: white'>
                    <div width:100%'>
                        <div>
                            <img src="cid:image2" style='width:15%'> 
                        </div>
                        <div  style='display:inline;'>
                        <h1>MSPi Has Detected A Person:</h1>
                        </div>
                    </div>
                    <div style='display: block'>
                        <h2>''' + people[0] + '''</h2>
                    </div>    
                    <div>
                        <img src="cid:image1" style='border:1px solid black ;margin-left:150px;'>
                    </div>
                </div>

            </html>
            '''
        if len(people) == 2:
            htmlTxt = '''
            <html>
                <div style=' align-items: center; text-align: center; font-family: sans-serif; background-color: white'>
                    <div width:100%'>
                        <div>
                            <img src="cid:image2" style='width:15%'> 
                        </div>
                        <div  style='display:inline;'>
                        <h1>MSPi Has Detected A Person:</h1>
                        </div>
                    </div>
                    <div style='display: block'>
                        <h2>''' + people[0] + ''', and ''' +  people[1] + '''</h2>
                    </div>    
                    <div>
                        <img src="cid:image1" style='border:1px solid black ;margin-left:150px;'>
                    </div>
                </div>

            </html>
            '''
        if len(people) == 3:
            htmlTxt = '''
            <html>
                <div style=' align-items: center; text-align: center; font-family: sans-serif; background-color: white'>
                    <div width:100%'>
                        <div>
                            <img src="cid:image2" style='width:15%'> 
                        </div>
                        <div  style='display:inline;'>
                        <h1>MSPi Has Detected A Person:</h1>
                        </div>
                    </div>
                    <div style='display: block'>
                        <h2>''' + people[0] + ''', ''' +  people[1] + ''', and ''' + people[2] + '''</h2>
                    </div>    
                    <div>
                        <img src="cid:image1" style='border:1px solid black ;margin-left:150px;'>
                    </div>
                </div>

            </html>
            '''
        if len(people) > 3:
            htmlTxt = '''
            <html>
                <div style=' align-items: center; text-align: center; font-family: sans-serif; background-color: white'>
                    <div width:100%'>
                        <div>
                            <img src="cid:image2" style='width:15%'> 
                        </div>
                        <div  style='display:inline;'>
                        <h1>MSPi Has Detected A Person:</h1>
                        </div>
                    </div>
                    <div style='display: block'>
                        <h2>''' + people[0] + ''', and ''' +  people[1] + '''</h2>
                    </div>    
                    <div>
                        <img src="cid:image1" style='border:1px solid black ;margin-left:150px;'>
                    </div>
                </div>

            </html>
            '''
    else:
        htmlTxt = '''
        <html>
            <div style=' align-items: center; text-align: center; font-family: sans-serif; background-color: white'>
                <div width:100%'>
                    <div>
                        <img src="cid:image2" style='width:15%'> 
                    </div>
                    <div  style='display:inline;'>
                    <h1>MSPi Has Detected A Person:</h1>
                    </div>
                </div>
                <div style='display: block'>
                    <h2>No Faces Detected</h2>
                </div>    
                <div>
                    <img src="cid:image1" style='border:1px solid black ;margin-left:150px;'>
                </div>
            </div>

        </html>
        '''
        
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
    
    


    msgText = MIMEText(htmlTxt, 'html')
    msgAlternative.attach(msgText)

    
    fp = open('/home/pi/Desktop/CameraSoftware/WhoDat.jpg', 'rb')
    #fp = open('/Users/nick/Desktop/cameraRepo/CameraSoftware/WhoDat.jpg', 'rb')
    fp2 = open('/home/pi/Desktop/CameraSoftware/mspi.png', 'rb')
    msgImage2 = MIMEImage(fp2.read())
    msgImage2.add_header('Content-ID', '<image2>')
    msgRoot.attach(msgImage2)
    msgImage = MIMEImage(fp.read())
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(fromEmail, fromEmailPassword)
    smtp.sendmail(fromEmail, toEmail, msgRoot.as_string())
    smtp.quit()


