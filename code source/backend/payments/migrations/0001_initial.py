from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_payment_intent', models.CharField(max_length=255, unique=True)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('currency', models.CharField(default='usd', max_length=10)),
                ('status', models.CharField(default='created', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=models.CASCADE, related_name='payments', to='orders.order')),
            ],
        ),
    ]
