from flask import Flask, request, render_template, redirect, url_for, make_response
from flask_mail import Mail, Message
from flask_script import Manager, Server
from threading import Thread
import os
# import requests
from requests.auth import HTTPBasicAuth


from config import Config, ProductionConfig, DevelopmentConfig

app = Flask(__name__)
config_app = Config()
app.config['MAIL_SERVER'] = config_app.MAIL_SERVER
app.config['MAIL_PORT'] = config_app.MAIL_PORT
app.config['MAIL_USE_TLS'] = config_app.MAIL_USE_TLS
app.config['MAIL_USERNAME'] = config_app.MAIL_USERNAME
app.config['MAIL_DEFAULT_SENDER'] = config_app.MAIL_DEFAULT_SENDER
app.config['MAIL_PASSWORD'] = config_app.MAIL_PASSWORD
PORT = config_app.PORT_APP
INSTALLATION = config_app.INSTALLATION
if INSTALLATION == "PROD":
    HOST = ProductionConfig.HOST
    DEBUG = False
else:
    HOST = DevelopmentConfig.HOST
    DEBUG = True
manager = Manager(app)

manager.add_command("runserver", Server(use_debugger=DEBUG, host=HOST, port=PORT,
                                            ssl_crt='homepi76.ru.crt', ssl_key='homepi76.ru.key'))


def async_send_mail(app, msg, mail):
    with app.app_context():
        mail.send(msg)


def send_email(email_sender, text, topic):
    mail = Mail(app)
    message = Message(topic, recipients=[config_app.MAIL_USERNAME])
    message.html = render_template("email.html", text=text, email_sender=email_sender)
    async_send_mail(app, message, mail)
    thr = Thread(target=async_send_mail,  args=[app,  message, mail])
    thr.start()
    return thr


@app.route('/mail', methods=["POST"])
def mail():
    email_sender = request.form["email"]
    topic = request.form["topic"]
    message_text = request.form["message-text"]
    send_email(email_sender=email_sender, text=message_text, topic=topic)
    resp = make_response(redirect('/'))
    resp.set_cookie("message", "OK", max_age=3)
    return resp


@app.route('/', methods=["GET", "POST"])
def index():
    show_message = False
    if request.cookies.get("message") == "OK":
        show_message = True
    pic_list = os.listdir(os.path.join(os.getcwd(), "static", "img", "certificates"))
    link_pic_list = [os.path.join("..", "static", "img", "certificates", pic_item) for pic_item in pic_list]
    pic_name_list = [pic_item[:-4] for pic_item in pic_list]
    user_name = request.cookies.get("user_name", "пользователь")
    render = render_template("index.html",
                           link_pic=link_pic_list,
                           pic_name_list=pic_name_list,
                           count_pic_cert=len(pic_list),
                           show_message=show_message,
                            user_name=user_name)
    if request.method == "POST":
        user_name = request.form["name"]
        print(user_name)
        resp = make_response(redirect("/"))
        resp.set_cookie("user_name", user_name, max_age=60*60*24*31)
        return resp
    return render


if __name__ == '__main__':
    manager.run()

