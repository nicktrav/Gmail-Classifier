# import libraries
import imaplib, re, os, sys

def main():
    # get the username and password from file
    abspath = '/Users/nick/Documents/pwd'
    if not os.path.exists(abspath):
        print 'Password file does not exist!'
        return
    
    # get the username and passowrd from the file
    f = open(abspath)
    items = f.read().split(';')
    username = items[0]
    password = items[1]
    
    # establish the connection
    conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    conn.login(username, password)
    
    # get the unread count
    unreadCount = int(re.search("UNSEEN (\d+)", conn.status("INBOX", "(UNSEEN)")[1][0]).group(1))
    print 'You have %d unread messages ... ' % unreadCount
    
    print 'Selecting the INBOX ... '
    conn.select('INBOX')
    typ, data = conn.search(None, 'ALL')
    
    # for each message in the inbox
    for num in data[0].split():        
        typ, data = conn.fetch(num, '(BODY[HEADER.FIELDS (SUBJECT FROM)])')
        # create an instance of the email
        print 'Message: %s\nData:\n%s' % (num, data[0][1])
        
    # close the connection
    conn.close()
    conn.logout()
    

if __name__ == '__main__':
    main()