from django.db import migrations, models
class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_userfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfile',
            name='file_name',
        ),
        migrations.RemoveField(
            model_name='userfile',
            name='user',
        ),
        migrations.AddField(
            model_name='userfile',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='userfile',
            name='title',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userfile',
            name='username',
            field=models.CharField(default=' ', max_length=100),
            preserve_default=False,
        ),
    ]
