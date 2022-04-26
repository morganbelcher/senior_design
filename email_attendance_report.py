import os
import yagmail
import datetime

receiver = "prof@kennesaw.edu"
body = "Attendance File"
date_time = datetime.datetime.now()
filename = "Attendance "+.os.sep+"Attendance_"+date_time+".csv"

yag = yagmail.SMIP("email@gmail.com", "email_password")

yag.send (
    to = receiver,
    subject = "Attendance Report "+date_time,
    contents = body,
    attachments = filemane,
    )
