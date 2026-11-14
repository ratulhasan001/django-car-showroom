from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0004_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='image',
            field=models.ImageField(upload_to='cars/'),
        ),
    ]
