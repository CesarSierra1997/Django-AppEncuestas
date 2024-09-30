# Generated by Django 4.2.2 on 2024-09-30 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('encuesta', '0003_encuesta_fechamodificacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpcionesPregunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opcion_1', models.CharField(max_length=100, verbose_name='Digite la opción 1')),
                ('opcion_2', models.CharField(max_length=100, verbose_name='Digite la opción 2')),
                ('opcion_3', models.CharField(max_length=100, verbose_name='Digite la opción 3')),
                ('opcion_4', models.CharField(max_length=100, verbose_name='Digite la opción 4')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opciones', to='encuesta.pregunta')),
            ],
        ),
        migrations.AlterField(
            model_name='encuesta',
            name='estado',
            field=models.BooleanField(default=True, verbose_name='Estado de la encuesta'),
        ),
        migrations.DeleteModel(
            name='OpcionPregunta',
        ),
    ]
