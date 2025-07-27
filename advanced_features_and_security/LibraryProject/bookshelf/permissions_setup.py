from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.dispatch import receiver

@receiver(post_migrate)
def create_custom_permissions_and_groups(sender, **kwargs):
    Book = apps.get_model('bookshelf', 'Book')
    content_type = ContentType.objects.get_for_model(Book)

    permissions = [
        ("can_view_userprofile", "Can view user profile"),
        ("can_create_userprofile", "Can create user profile"),
        ("can_edit_userprofile", "Can edit user profile"),
        ("can_delete_userprofile", "Can delete user profile"),
    ]

    for codename, name in permissions:
        Permission.objects.get_or_create(codename=codename, name=name, content_type=content_type)

    group, created = Group.objects.get_or_create(name='Librarian')
    group.permissions.set(Permission.objects.filter(codename__in=[p[0] for p in permissions]))
