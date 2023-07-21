
from time import sleep
import requests
import json

requests.packages.urllib3.disable_warnings()

class Mail:
    def __init__(self, obj):
        if obj is None:
            return
        self.id = obj["id"]
        self._from = obj["from"]
        self.subject = obj["subject"]
        self.attachments = obj['attachments']
        self.body = obj['body']
        self.txtbody = obj['textBody']

class MailAdress:
    def __init__(self, emailrep : str):
        if emailrep is None or len(emailrep) <= 0:
            emailrep = requests.post("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").text
        self.em = json.loads(emailrep.strip())
        if (len(self.em) < 1):
            raise Exception("Error while getting new mail from api")
        # print(self.em)
        # print(f"resp : {self.em}")
        self.em = self.em[0]
        self.email = self.em.split("@")
        self.adress = self.email[0]
        self.domain = self.email[1]
        self.url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={self.adress}&domain={self.domain}"
        self.mails = {}
        self.readMails = []

    def is_mail_read(self, id):
        return id in self.readMails

    def read_mail(self, id):
        if id in self.mails.keys():
            if id not in self.readMails:
                self.readMails.append(id)
            return (self.mails[id])
        return Mail(None)

    def count_unread_mails(self):
        return len(self.mails) - len(self.readMails)

    def get_new_mail(self):
        _mails = []
        for x in self.mails:
            if (x not in self.readMails):
                _mails.append(self.mails[x])
                self.readMails(x)
        return _mails
    def get_all_mails(self):
        return self.mails

    def fetch_mail(self, callback = None):
        i = 0
        r = requests.get(self.url)
        parsed = json.loads(r.text)
        try:
            if 'id' in parsed[0]:
                for mail in parsed:
                    subject = mail['subject']
                    id = mail["id"]
                    if id in self.mails.keys():
                        return
                    print(f"""
Subject : {subject}
                        """)
                    url2 = f"https://www.1secmail.com/api/v1/?action=readMessage&login={self.adress}&domain={self.domain}&id={id}"
                    response = requests.get(url2)
                    response.raise_for_status()
                    print(f"response : {response.text}")
                    jsonResponse = response.json()
                    if (len(jsonResponse.items()) > 0):
                        self.mails[id] = Mail(jsonResponse)
                    i+=1
                    if callback is not None:
                        callback(self.mails[id])
                    
        except:
            return -1
        return i

    def get_new_mail():
        r = requests.post("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
        mail = MailAdress(r.text)
        return mail
