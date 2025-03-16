from users.models import UserInfo

def get_user_info(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = UserInfo.objects.get(pk=user_id)
        except UserInfo.DoesNotExist:
            user = None
    else:
        user = None
    return {'current_user': user}
