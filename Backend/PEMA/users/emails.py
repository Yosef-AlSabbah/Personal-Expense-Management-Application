from djoser.email import ActivationEmail


class CustomActivationEmail(ActivationEmail):
    template_name = 'email/activation.html'
