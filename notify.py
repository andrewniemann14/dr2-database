# carrier email addresses:
# https://www.digitaltrends.com/mobile/how-to-send-a-text-from-your-email-account/

import smtplib
from email.message import Message

classes = {
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
  
  sender = 'DR2.0 Dashboard <dr2@niemann.app>'
  # in future, pull recipients from subscribers table in DB, loop this function for each recipient
  # changing this to email, not text, since that doesn't work anyway
  recipient = 'andrewniemann14@gmail.com'

  alert0 = classes[challenges[0]["vehicle_class"]] + " in " + challenges[0]["country"][1:] + " (" + challenges[0]["stage"] + ")"
  alert1 = classes[challenges[1]["vehicle_class"]] + " in " + challenges[1]["country"][1:] + " (" + challenges[1]["stage"] + ")"

  msg = Message()
  msg['From'] = sender
  msg['To'] = recipient
  msg['Subject'] = "Today's Challenges"
  msg.set_payload('\n{}\n{}'.format(alert0, alert1))

  try:
    smtp = smtplib.SMTP('mail.niemann.app', 587) # 465 for SSL, 587 for non-SSL

    smtp.login('dr2@niemann.app', '}p}et-3s[9)4')
    smtp.ehlo('mail.niemann.app')
    # smtp.sendmail(sender, recipients, msg)
    smtp.send_message(msg)
    smtp.quit()
  except smtplib.SMTPException as e:
    print("err:",e.strerror)