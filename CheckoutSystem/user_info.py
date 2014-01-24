def user_info(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            is_admin = True
            is_monitor = True
        else:
            is_admin = False
            is_monitor = request.user.groups.filter(name="Monitor")
    else:
        is_admin = False
        is_monitor = False

    return {
        'is_admin': is_admin,
        'is_monitor': is_monitor
    }