import requests, re, random, time, sys
from random import getrandbits
from time import sleep
import urllib2

url = 'https://visitnorthhills.us4.list-manage.com/subscribe/post' #url of raffle
API_KEY = '' #2captcha api key
site_key = '6LcN9xoUAAAAAHqSkoJixPbUldBoHojA_GCp6Ims' #google recaptcha sitekey
email_head = ''

word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain" #dictionary site
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

#create list of words to use in email head
response = urllib2.urlopen(word_site)
txt = response.read()
WORDS = txt.splitlines() 

def main(limit):
    f = open('emails.txt','a')
    for n in range(limit):
        word=random.choice(WORDS)
        email = '{}{}@optumtech.me'.format(word, getrandbits(10)) #random email plus cathcall domain

        s = requests.Session()

        # here we post site key to 2captcha to get captcha ID (and we parse it here too)
        captcha_id = s.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(API_KEY, site_key, url)).text.split('|')[1]
        # then we parse gresponse from 2captcha response
        recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
        print("solving ref captcha...")
        while 'CAPCHA_NOT_READY' in recaptcha_answer:
            sleep(5)
            recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
        print(recaptcha_answer)
        recaptcha_answer = recaptcha_answer.split('|')[1]

        payload ={
            'u': '98aba7d0141269a44537b7a58',
            'amp;id': '5e3e8d54ab',
            'g-recaptcha-response' : recaptcha_answer,
            'EMAIL' : email

        }
        resp = requests.post(url, data = payload, headers = headers) #post request to fill out form
        if any(re.findall(r'Your entry to our contest has been confirmed', str(resp.text), re.IGNORECASE)):
            print "success with {}".format(email)
        else:
            print(email)
            print "failed"
            print resp.content
            exit()
    f.close()
main(100)
exit()
