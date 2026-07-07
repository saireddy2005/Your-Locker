from django.db import migrations, models
class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_remove_userfile_file_name_remove_userfile_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='account_locked_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='failed_attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255),
        ),
    ]
