# Generated by Django 2.0 on 2019-05-10 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='icon',
            field=models.CharField(default='images/tx1.jpg', max_length=150, verbose_name='头像'),
        ),
    ]