import poplib
from email.parser import Parser


def get_info(msg):
    if msg.is_multipart():
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            return get_info(part)
    if not msg.is_multipart():
        content_type = msg.get_content_type()
        if content_type == 'text/plain':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            return content


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def check_for_code(email, password):
    print('check mail',email)
    mail = poplib.POP3_SSL('pop-mail.outlook.com')
    mail.user(email)
    mail.pass_(password)
    num_messages = len(mail.list()[1])
    resp, lines, octets = mail.retr(num_messages)
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    msg = Parser().parsestr(msg_content)

    message = get_info(msg)
    if 'facebook' in msg_content.lower():
        for line in message.split('\n'):
            # if 'confirmemail.php' in line:
            #     print(line)
            line = line.strip()
            if len(line) == 5 and line.isdigit():
                return line
    return None
