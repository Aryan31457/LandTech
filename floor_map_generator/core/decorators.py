from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def admin_required(function):
    def check_admin(user):
        return user.is_authenticated and user.user_type == 'admin'
    
    decorated_view = user_passes_test(check_admin, login_url='/')(function)
    return decorated_view