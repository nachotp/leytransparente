from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from pathlib import Path


def send_email(subject, mail, context, to):
    """
    Email Message Wrapper
    :param subject: Asunto del correo
    :param mail: nombre de la template
    :param context: diccionario de info para render
    :param to: Destinatario
    :return: Exito del envío
    """
    path = Path("emails") / f'{mail}.html'

    subject = '[LEY-TP] '+subject
    if type(to) == str:
        to = [to]

    message = render_to_string(path.resolve(), context)
    msg = EmailMessage(subject, message, to=to)
    msg.content_subtype = "html"
    return msg.send()
