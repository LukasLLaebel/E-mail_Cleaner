# E-mail_Cleaner
Clean up the subscribed email newsletters

E-mail cleaner is made to make your life easier.
first tough you need to do some simple tasks:
1. Go to [google account, security](https://myaccount.google.com/intro/security)
2. login and setup 2 factor auth
3. next go to search for "App passwords"
4. here you need to login again.
5. Now generate new app password
6. take the password you get and copy that
7. Now make a file called ´data.py´ in same location as your main py file
8. your data.py need to include:
   - imap_server : what server to call for gmail its: imap.gmail.com if you use another mail search for "imap server for ´my mail´"
   - email_address : here you add your email address
   - password : here add the password you just generated
   - REMINDER ALL OF THEM NEEDS TO BE A STRING MEANS : "imap.gmail.com","email@gmail.com", "ajtv jkol wosl lpla"
