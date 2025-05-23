import imaplib
import email
import re

from data import imap_server, email_address, password

# Connect to IMAP and login
imap = imaplib.IMAP4_SSL(imap_server)
imap.login(email_address, password)
imap.select('"[Gmail]/All Mail"')

# Search for recent messages
status, msgnums = imap.search(None, 'SINCE', '01-Jan-2023')
if status == "OK":
    msg_ids = msgnums[0].split()[::-1]  # reverse to get latest first

    unsubscribe_messages = []
    found_unsubscribe_links = set()  # Keep track of all unsubscribe links found so far

    for msgnum in msg_ids:
        if len(unsubscribe_messages) >= 100:
            break  # Stop after finding 10 unique messages with unsubscribe links

        _, data = imap.fetch(msgnum, "(RFC822)")
        message = email.message_from_bytes(data[0][1])

        found_links = []

        # Check List-Unsubscribe header
        unsubscribe_header = message.get("List-Unsubscribe")
        if unsubscribe_header:
            links = re.findall(r'<(http[s]?://[^>]+)>', unsubscribe_header)
            for link in links:
                if link not in found_unsubscribe_links:
                    found_links.append(link)

        # Check in plain text body
        if not found_links:
            for part in message.walk():
                if part.get_content_type() == "text/plain" and part.get_content_disposition() != "attachment":
                    body = part.get_payload(decode=True)
                    if body:
                        text = body.decode(part.get_content_charset() or "utf-8", errors="ignore")
                        body_links = re.findall(r'https?://\S+', text)
                        for link in body_links:
                            if "unsubscribe" in link.lower() and link not in found_unsubscribe_links:
                                found_links.append(link)
                    break

        # Only add the message if there are new unsubscribe links that were not found before
        if found_links:
            unsubscribe_messages.append((msgnum.decode(), message, found_links))
            for link in found_links:
                found_unsubscribe_links.add(link)  # Mark these links as found

    # Print results
    for msgnum, message, links in unsubscribe_messages:
        print(f"\nMessage #{msgnum}")
        print(f"From: {message.get('From')}")
        print(f"Subject: {message.get('Subject')}")
        for link in links:
            print(f"Unsubscribe Link: {link}")
        print("-" * 60)

imap.close()
imap.logout()

