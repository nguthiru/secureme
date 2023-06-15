def send_approval_email(user):
    pass

from django.template.context import Context
from django.template.loader import render_to_string
from django.core.mail import send_mail


def send_validation_email(user):
    from users.models import ValidationEmailCodes

    import random
    number = random.randint(1000000,9999999)
    reset_password = ValidationEmailCodes.objects.create(user=user,code=number)

    context = Context({'code':number})
    html_message = render_to_string('email_validate.html',{'code':number})
    message = f"Hello your Account Activation is \n {number}. Ignore if you did not make a request"
    send_mail(
          subject= "SecureMe Account Activation",
          message=message,
          from_email='nguthiruedwin@gmail.dom',
          html_message=html_message,
          recipient_list=[user.email],
          fail_silently= False)
    if send_mail ==0:
        return False
    else:
        return True



def send_reset_email(user):
    from users.models import PasswordReset

    import random
    number = random.randint(1000000,9999999)
    reset_password = PasswordReset.objects.create(user=user,reset_code=number)

    context = Context({'code':number})
    html_message = render_to_string('email_reset.html',{'code':number})
    message = f"Hello your password reset code is \n {number}. Ignore if you did not make a request"
    send_mail(
          subject= "SecureMe Password Reset",
          message=message,
          from_email='nguthiruedwin',
          html_message=html_message,
          recipient_list=[user.email],
          fail_silently= False)
    if send_mail ==0:
        return False
    else:
        return True