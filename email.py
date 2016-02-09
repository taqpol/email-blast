from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import getpass
import imaplib
import re 
import email
import sys


'''opens an imap connection to gmail using provided gmail credentials. 
   if a non-gmail address is used, an exception is raised. '''
   
   
def inbox_open():
    successful_open = False
    while_exit = False

    '''searches inbox for a chosen phrase. if no emails are returned, user is 
    prompted that there are no matches, and can search again or quit. returns a
    set object containing all email addresses from the inbox that sent an email to
    the user containing the entered search term. '''


    def inbox_scrape(z):
        address_bank = []
        while True:
            passphrase = input('enter term that script will'
                               ' use to search through emails in '
                               'the selected inbox: ')
            return_value, email_count = z.search(None, '(BODY "{}")'.format(passphrase))
            if len(email_count[0].decode('utf-8')) < 1:
                retry = input('Nothing found that matched search terms. try again?'
                              '(y/n)')
                while retry not in ('y', 'n'):
                    retry = input('input not recognized. retry inbox search? (y/n)')
                else:
                    if retry.lower() == 'y':
                        continue
                    elif retry.lower() == 'n':
                        z.logout()
                        return
            else:
                break
        
        while True:                
            for email_num in email_count[0].split():
                return_value, email_raw = z.fetch(email_num, '(RFC822)')
                if return_value != 'OK':
                    retry = input('error fetching messages. retry? (y/n)')
                while retry not in ('y', 'n'):
                    retry = input('input not recognized. retry email fetch? '
                                  '(y/n)')
                else:
                    if retry == 'y':
                        continue
                    elif retry == 'n':
                        z.logout()
                        break
                        
                messages = email.message_from_string(email_raw[0][1].decode('utf-8'))
                address = re.search('\<.+\>', messages['FROM'])
                address = address.group(0).lstrip('<').rstrip('>')
                address_bank.append(address)
        
        address_bank = set(address_bank) - user
        
        return address_bank        
            
    while not while_exit:
        user = input('enter email address: ')
        z = imaplib.IMAP4_SSL('imap.gmail.com')
        try:
            z.login(user, getpass.getpass('enter password: '))
        except imaplib.IMAP4.error:
            continue_bool = input("login failed. retry? (y/n)")
            while continue_bool.lower() not in ('y', 'n'):
                continue_bool = input("input not recognized. retry? "
                                      "(y/n)").lower()
            else:
                if continue_bool == 'n':
                    z.logout()
                    return
                elif continue_bool == 'y':
                    continue
        else:
            return_value, mailboxes = z.list()
            print("select which mailbox to search for emails: ")
            box_list = [re.search('\"\w+\"', boxes.decode('utf-8')) for boxes 
                        in mailboxes]
            for boxes in box_list:
                if boxes != None:
                    print(boxes.group(0))
            while not successful_open:
                search_box = input('enter box name here: ')
                try:
                    z.select(search_box)
                except imaplib.IMAP4.error:
                    continue_bool2 = input("couldn't open that box. either box" 
                                           " does not exist or name was "
                                           "misspelled. try again? (y/n)").lower()
                    if continue_bool2 not in ('y','n'):
                        continue_bool2 = input('response not recognized. continue'
                                           ' with reading process? (y/n)')
                    else:
                        if continue_bool2 == 'y':
                            continue
                        elif continue_bool2 == 'n':
                            z.logout()
                            return
                else:
                    print('mailbox opened: {}'.format(search_box))
                    successful_open, while_exit = True, True
                    
    if successful_open:
        address_bank = inbox_scrape(z)
    z.logout()
                                  
    return successful_open, user, address_bank 
    
            
'''opens an SMTP connection that takes information from the inbox_open() 
function and sends emails one at a time to all emails scraped from the inbox.
'''

           
def smtp_send(user, address_bank):
    with smtplib.SMTP('smtp.gmail.com', port = 587) as smtp:
        
        '''smtp_login ensures that no email can be sent if no connection can
        be established with the smtp server. '''
        
        
        def smtp_login(smtp):
            while True:
                try:
                    smtp.login(user, getpass.getpass("enter password again"
                                                     "(don't worry, your "
                                                     "password isn't stored."
                                                     "the IMAP and SMTP "
                                                     "protocols require a "
                                                     "different connection "
                                                     "and subsequent "
                                                     "reauthorization of said"
                                                     "connection): "))
                except smtplib.SMTPException:
                    continue_bool = input("login failed. retry? (y/n)")
                    while continue_bool.lower() not in ('y', 'n'):
                        continue_bool = input("input not recognized. retry? "
                                              "(y/n)")
                    else:
                        if continue_bool.lower() == 'n':
                            smtp.quit()
                            return
                        elif continue_bool.lower() == 'y':
                            continue
                else:
                    break
                    
        smtp.starttls()
        smtp_login(smtp)
        message = MIMEMultipart()
        message['From'] = user
        message['Subject'] = input('email subject here:')
        message_body = input('email body here:')
        message.attach(MIMEText(message_body))
        print('this is a preview of your message: '
              '\n "From: {}" \n "To: {}" \n "Subject: {}" \n "Contents: \n{}"'
              .format(message['From'], address_bank, message['Subject'], 
              message_body))
        warning_prompt = input('you are about to send a large amount of emails'
                               ' to these addresses. verify that you want to '
                               "send by typing 'confirm'. if you want to quit,"
                               " type 'quit': ")
        while warning_prompt not in ('confirm', 'quit'):
            warning_prompt = input("input not recognized. type 'confirm' to "
                                   "confirm sending of emails, or type 'quit'"
                                   ' to exit this prompt: ')
        else: 
            if warning_prompt.lower() == 'quit':
                smtp.quit()
                return
            elif warning_prompt.lower() == 'confirm':
                for addresses in address_bank:
                    message['To'] = addresses
                    smtp.sendmail(user, addresses, message.as_string())            
    
    
if __name__ == '__main__':
    successful_open, user, address_bank = inbox_open()
    if not successful_open or address_bank == {}:
        sys.exit()
    else:
        smtp_send(user, address_bank)
    
