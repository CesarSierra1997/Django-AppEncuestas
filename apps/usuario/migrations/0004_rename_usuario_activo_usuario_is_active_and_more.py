# Generated by Django 4.2.2 on 2024-09-16 00:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_usuario_groups_usuario_is_superuser_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='usuario_activo',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='usuario_administrador',
            new_name='is_staff',
        ),
    ]
