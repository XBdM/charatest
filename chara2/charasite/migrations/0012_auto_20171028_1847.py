# Generated by Django 2.0a1 on 2017-10-28 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charasite', '0011_auto_20171028_1811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.RemoveField(
            model_name='book',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='bookinstance',
            name='book',
        ),
        migrations.RemoveField(
            model_name='bookinstance',
            name='borrower',
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(help_text='Enter the name of your project', max_length=200),
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.DeleteModel(
            name='BookInstance',
        ),
    ]
