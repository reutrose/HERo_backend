from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    @receiver(post_save, sender='auth.User')
    def perform_add_user_to_users_group(sender, instance, created, **kwargs):
        from django.contrib.auth.models import Group, User
        from api.models import UserProfile
        from rest_framework.authtoken.models import Token

        group_names = ["Users", "Moderators", "Admins"]
        for group_name in group_names:
            Group.objects.get_or_create(name=group_name)
        
        if not created:
            return
        
        group, _ = Group.objects.get_or_create(name='Users')
        instance.groups.add(group)
        instance.save()
        
        UserProfile.objects.get_or_create(user=instance)
        Token.objects.get_or_create(user=instance)
        print(f'User {instance.username} added to the group {group.name}')