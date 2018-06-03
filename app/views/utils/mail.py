import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate


def send_confirm_mail(from_addr, from_addr_pass, to_addr, token):
    '''email送信
    Args:
        from_addr:  送り元メールアドレス
        from_addr_pass:  送り元メールアドレスのパスワード
        to_addr:  送り先メールアドレス
        token:  仮登録のトークン
    '''
    # メッセージ作成
    message = _create_message(
        from_addr,
        to_addr,
        token
    )

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(from_addr, from_addr_pass)
    s.sendmail(from_addr, to_addr, message.as_string())
    s.close()

    return 0

def _create_message(
    from_addr,
    to_addr,
    token
):
    url = 'http://localhost:3000/?token=' + token

    body = '以下のURLにアクセスしてください\n\n' + url

    msg = MIMEText(body)
    # msg = MIMEText(body + url)
    msg['Subject'] = '学生2chの仮登録メールについて'
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()

    print("token", token)


    return msg