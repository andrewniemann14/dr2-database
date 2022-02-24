# carrier email addresses:
# https://www.digitaltrends.com/mobile/how-to-send-a-text-from-your-email-account/

import smtplib
from email.message import Message
import scraper # remove when done developing

classes = {
  # vehicle classes
  "eRallyH1FwdCaps": "H1 FWD",
  "eRallyH2FwdCaps": "H2 FWD",
  "eRallyH2RwdCaps": "H2 RWD",
  "eRallyH3FwdCaps": "H3 FWD",
  "eRallyH3RwdCaps": "H3 RWD",
  "eRallyGrpBRwdCaps": "Grp B RWD",
  "eRallyGrpB4wdCaps": "Grp B 4WD",
  "eRallyGrpACaps": "Grp A",
  "eRallyR2Caps": "R2",
  "eRallyNr4R4Caps": "NR4/R4",
  "eRallyR5Caps": "R5",
  "eRallyRGtCaps": "R-GT"
}

def notify(challenges):
  
  sender = 'DR2 Dashboard <dr2@niemann.app>'
  # in future, pull recipients from subscribers table in DB, loop this function for each recipient
  recipient = '8312363828@vtext.com'

  alert0 = classes[challenges[0]["vehicle_class"]] + " in " + challenges[0]["country"][1:]
  alert1 = classes[challenges[1]["vehicle_class"]] + " in " + challenges[1]["country"][1:]

  msg = Message()
  msg['From'] = sender
  msg['To'] = recipient
  msg['Subject'] = "Today's Challenges"
  msg.set_payload('\n\nsent at 13:40:00')
  print(msg.items())
  print(msg.get_payload())


  try:
    smtp = smtplib.SMTP('mail.niemann.app', 587) # 465 for SSL, 587 for non-SSL

    smtp.login('dr2@niemann.app', '}p}et-3s[9)4')
    # smtp.ehlo('mail.niemann.app') # remove this?
    # smtp.sendmail(sender, recipients, msg)
    smtp.send_message(msg)
    smtp.quit()
  except smtplib.SMTPException as e:
    print("err:",e.strerror)



notify(scraper.get_today())