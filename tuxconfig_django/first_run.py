from django.contrib.auth.models import Group, Permission

new_group, created = Group.objects.get_or_create(name='github')
permissions_list =  Permission.objects.all()
new_group.permissions.set(permissions_list)


new_group, created = Group.objects.get_or_create(name='vetting')
permissions_list =  Permission.objects.all()
new_group.permissions.set(permissions_list)