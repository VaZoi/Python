import pandas as pd
import smtplib
from email.mime.text import MIMEText

subject = "Test Email"
body = """
Dear valued customer,

We hope this message finds you well.

At RecipesBook, we are passionate about providing you with the best culinary experiences. As part of our commitment to excellence, we are excited to introduce a new collection of mouthwatering recipes tailored to tantalize your taste buds and inspire your culinary adventures.

Whether you're a seasoned chef or an aspiring home cook, our recipes are crafted with care to ensure that every dish is not only delicious but also easy to prepare. From comforting classics to innovative creations, there's something for everyone in our diverse selection.

To get started, simply visit our website or app, where you'll find an array of recipes ranging from hearty mains to delectable desserts. We've also included helpful tips and tricks to elevate your cooking skills and make every meal a memorable occasion.

Thank you for choosing RecipesBook as your culinary partner. We're thrilled to embark on this flavorful journey with you.

Happy cooking!

Warm regards,
RecipesBook
"""

sender = "vazodevelopment@gmail.com"
password = input("What is your password? \n")

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

recipients_df = pd.read_excel('emails.xlsx')
recipients_list = recipients_df['Email'].tolist()

send_email(subject, body, sender, recipients_list, password)
