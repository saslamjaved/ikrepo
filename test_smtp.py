import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('iksaangroups@gmail.com', 'osbd qdsl jqrl envs')
    print("Connection successful")
    server.quit()
except Exception as e:
    print(f"Error: {e}")
