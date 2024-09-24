# Generated by Django 4.2.2 on 2024-09-24 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('encuesta', '0002_respuestaencuestaprivada_respuestaencuestapublica_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opcionpreguntaselectmultiple',
            name='pregunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opciones', to='encuesta.preguntaselectmultiple'),
        ),
        migrations.AlterField(
            model_name='respuestapreguntaselectmultiple',
            name='respuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opcion_respuesta_pregunta_selectMultiple', to='encuesta.opcionpreguntaselectmultiple'),
        ),
    ]