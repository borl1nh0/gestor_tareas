from django.core.management.base import BaseCommand
from faker import Faker 
from tareas.models import *

class Command (BaseCommand):
    help = 'Generadno datos usando Faker'
   
   
    def handle(self, *arg, **kwargs):
        fake = Faker('es_ES')
    
    
        for _ in range (10):
            Usuario.objects.create(
                nombre = fake.name() ,
                correo = fake.unique.email(),
                contrasena = fake.password(),
            )
            
            
        self.stdout.write(self.style.SUCCESS('dATOS GENERADOS CORRECTAMENTE'))