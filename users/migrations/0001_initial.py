from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'user_type',
                    models.CharField(
                        choices=[('aluno', 'Aluno'), ('professor', 'Professor'), ('admin', 'Admin')],
                        max_length=10,
                    ),
                ),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('bio', models.TextField(blank=True)),
                ('avatar_url', models.URLField(blank=True)),
                (
                    'user',
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
    ]
