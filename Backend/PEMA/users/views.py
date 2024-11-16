from django.shortcuts import render


def activate_account(request, uid, token):
    # Pass uid and token to the template
    context = {
        'uid': uid,
        'token': token,
        'activation_url': '/auth/users/activation/'
    }
    return render(request, 'users/EmailVerificationPage.html', context)
