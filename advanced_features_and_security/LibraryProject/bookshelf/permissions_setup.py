from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Book

@receiver(post_migrate)
def create_custom_permissions_and_groups(sender, **kwargs):
    ct = ContentType.objects.get_for_model(Book)

    perms = [
        ("can_view_book", "Can view book"),
        ("can_create_book", "Can create book"),
        ("can_edit_book", "Can edit book"),
        ("can_delete_book", "Can delete book"),
    ]

    created_perms = []
    for codename, name in perms:
        perm, _ = Permission.objects.get_or_create(
            codename=codename,
            name=name,
            content_type=ct,
        )
        created_perms.append(perm)

    # Map codename to permission for quick access
    perm_map = {perm.codename: perm for perm in created_perms}

    editors, _ = Group.objects.get_or_create(name='Editors')
    viewers, _ = Group.objects.get_or_create(name='Viewers')
    admins, _ = Group.objects.get_or_create(name='Admins')

    editors.permissions.set([
        perm_map['can_view_book'],
        perm_map['can_create_book'],
        perm_map['can_edit_book'],
    ])
    viewers.permissions.set([perm_map['can_view_book']])
    admins.permissions.set([
        perm_map['can_view_book'],
        perm_map['can_create_book'],
        perm_map['can_edit_book'],
        perm_map['can_delete_book'],
    ])