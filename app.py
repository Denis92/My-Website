from flask import Flask, request, render_template
from flask_mail import Mail, Message
from flask_script import Manager, Server
from threading import Thread

from flask_sslify import SSLify

from config import Config

app = Flask(__name__)
# context = ('homepi76.ru.crt', 'homepi76.ru.key')
# sslify = SSLify(app)
manager = Manager(app)

manager.add_command("runserver", Server(use_debugger=True, host="127.0.0.1", port="843",
                                            ssl_crt='homepi76.ru.crt', ssl_key='homepi76.ru.key'))


def async_send_mail(app, msg, mail):
    with app.app_context():
        mail.send(msg)


def send_email(email_sender,text, topic):
    print(f"{email_sender} {text} {topic}")
    config_app = Config()
    mail = Mail(app)
    app.config['MAIL_SERVER'] = config_app.MAIL_SERVER
    app.config['MAIL_PORT'] = config_app.MAIL_PORT
    app.config['MAIL_USE_TLS'] = config_app.MAIL_USE_TLS
    app.config['MAIL_USERNAME'] = config_app.MAIL_USERNAME
    app.config['MAIL_DEFAULT_SENDER'] = config_app.MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = config_app.MAIL_PASSWORD
    message = Message(topic, recipients=[email_sender])
    message.html = render_template("email.html", text=text)
    mail.send(message)
    # async_send_mail(app, message, mail)
    # thr = Thread(target=async_send_mail,  args=[app,  message, mail])
    # thr.start()
    # return thr

@app.route('/mail', methods=["POST"])
def mail():
    email_sender = request.form["email"]
    topic = request.form["topic"]
    message_text = request.form["message-text"]
    send_email(email_sender=email_sender, text=message_text, topic=topic)
    return 'Hello World!'


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == '__main__':
    # app.debug = True
    # context = ('homepi76.ru.crt', 'homepi76.ru.key')
    # app.run(port=8433, ssl_context=context )
    manager.run()
