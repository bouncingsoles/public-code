#!/usr/bin/python3
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import sys
import configparser

#Function to download our PNG files
def download_file(url, headers, filename):
    local_filename = filename
    r = requests.get(url, headers=headers, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename

#Function to send our HTML email with embedded image
def send_email(from_email, to_email, smtp_server, filename1, filename2, filename3):
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Grafana Report'
    msgRoot['From'] = from_email
    msgRoot['To'] = to_email
    msgRoot.preamble = 'This is a multi-part message in MIME format.'
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)
    msgText = MIMEText(
        '<br><img src="cid:image1"><br> <br><img src="cid:image2"><br> <br><img src="cid:image3"><br>',
        'html')
    msgAlternative.attach(msgText)
    fp1 = open(filename1, 'rb')
    fp2 = open(filename2, 'rb')
    fp3 = open(filename3, 'rb')
    msgImage1 = MIMEImage(fp1.read())
    msgImage2 = MIMEImage(fp2.read())
    msgImage3 = MIMEImage(fp3.read())
    fp1.close()
    fp2.close()
    fp3.close()
    msgImage1.add_header('Content-ID', '<image1>')
    msgImage2.add_header('Content-ID', '<image2>')
    msgImage3.add_header('Content-ID', '<image3>')
    msgRoot.attach(msgImage1)
    msgRoot.attach(msgImage2)
    msgRoot.attach(msgImage3)
    # Send the email (this example assumes SMTP authentication is required)
    smtp = smtplib.SMTP()
    smtp.connect(smtp_server)
    smtp.sendmail(from_email, to_email, msgRoot.as_string())
    smtp.quit()

#Check to make sure they enter something for the config file
if len(sys.argv) == 1:
    print ("Please enter a config file to use with --config <filename>")
    exit()
if len(sys.argv) > 3:
    print ("Too many args passed.")
    exit()

##Read our config in.
config = configparser.ConfigParser()

#try:
#    if config['grafana']['server']:
#        print ("Valid config found %s" % config['grafana']['server'])
#    else:
#        print ("There was an issue with the config file")
#        quit(0)
#except KeyError:
#    print ("Config error.")

try:
    config.read(sys.argv[2])
except IndexError:
    print ("Please enter a config file to use with --config <filename>")
    exit(0)

####Our args need to be correct before we proceed.
headers = {'Authorization': 'Bearer %s' % config['grafana']['api_key']}
url = 'http://%s/render/dashboard/db/%s?orgId=1&from=now-1d&to=now&width=1000&height=500' % (config['grafana']['server'],config['grafana']['graph_name'])
filename1 = 'grafana_grab.png'
url2 = 'http://%s/render/dashboard/db/%s?orgId=1&from=now-7d&to=now&width=1000&height=500' % (config['grafana']['server'],config['grafana']['graph_name'])
filename2 = 'grafana_grab2.png'
url3 = 'http://%s/render/dashboard/db/%s?orgId=1&from=now-30d&to=now&width=1000&height=500' % (config['grafana']['server'],config['grafana']['graph_name'])
filename3 = 'grafana_grab3.png'

###Grab our PNG files
download_file(url, headers, filename1)
download_file(url2, headers, filename2)
download_file(url3, headers, filename3)

###Start of our mail function
send_email(config['email']['email_from'], config['email']['email_to'], config['email']['smtp_server'], filename1, filename2, filename3)
