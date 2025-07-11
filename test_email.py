
import smtplib
# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.starttls()
# Authentication
s.login("iksaangroups@gmail.com", "osbd qdsl jqrl envs")
# message to be sent
message = "Message_you_need_to_send"
# sending the mail
s.sendmail("iksaangroups@gmail.com", "sdaslamjaveed@gmail.com", message)
# terminating the session
s.quit()
