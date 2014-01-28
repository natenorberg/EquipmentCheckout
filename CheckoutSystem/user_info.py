def user_info(request):
    if request.user.is_authenticated():
        # Site permissions
        if request.user.is_superuser:
            # Admins should also have monitor priviledges
            is_admin = True
            is_monitor = True
        else:
            is_admin = False
            is_monitor = request.user.groups.filter(name="Monitor")

        # Checkout permissions
        is_music_ed = request.user.groups.filter(name="Music Education")
        is_pre_gate = request.user.groups.filter(name="Pre-Music Tech")
        is_post_gate = request.user.groups.filter(name="Music Tech")
        is_staff = request.user.groups.filter(name="Staff")
    else:
        is_admin = False
        is_monitor = False
        is_music_ed = False
        is_pre_gate = False
        is_post_gate = False
        is_staff = False

    return {
        'is_admin': is_admin,
        'is_monitor': is_monitor,
        'is_music_ed': is_music_ed,
        'is_pre_gate': is_pre_gate,
        'is_post_gate': is_post_gate,
        'is_staff': is_staff
    }