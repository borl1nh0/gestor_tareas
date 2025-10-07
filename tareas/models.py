from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    nombre = models.CharField(max_length=150)
    correo = models.CharField(max_length=200, unique=True)
    contrasena = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(default=timezone.now)
    
    def __str__(self): 
        return self.nombre

class Proyecto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    duracion_estimada = models.FloatField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    # Creador (muchos proyectos -> un usuario)
    creador = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='proyectos_creados')
    # Colaboradores (muchos a muchos)
    colaboradores = models.ManyToManyField('Usuario', related_name='proyectos_asignados', blank=True)
    
    def __str__(self): 
        return self.nombre

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self): 
        return self.nombre

class Tarea(models.Model):
    ESTADOS = (
        ('Pendiente','Pendiente'), 
        ('Progreso','Progreso'), 
        ('Completada','Completada'))
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    prioridad = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS)
    completada = models.BooleanField()
    fecha_creacion = models.DateField()
    hora_vencimiento = models.TimeField(null=True, blank=True)
    # Creador (muchas tareas -> un usuario)
    creador = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='tareas_creadas')
    # Proyecto (muchas tareas -> un proyecto)
    proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE, related_name='tareas')
    # Etiquetas (muchos - muchos)
    etiquetas = models.ManyToManyField('Etiqueta', related_name='tareas', blank=True)
    # Usuarios asignados vía tabla intermedia
    asignados = models.ManyToManyField('Usuario', through='AsignacionTarea', related_name='tareas_asignadas', blank=True)
    
    def __str__(self): 
        return self.titulo

class AsignacionTarea(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='asignaciones')
    tarea = models.ForeignKey('Tarea', on_delete=models.CASCADE, related_name='asignaciones')
    observaciones = models.TextField()
    fecha_asignacion = models.DateTimeField(default=timezone.now)
    
    def __str__(self): 
        return f"{self.usuario} -> {self.tarea}"

class Comentario(models.Model):
    contenido = models.TextField()
    fecha_comentario = models.DateTimeField(default=timezone.now)
    autor = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='comentarios')
    tarea = models.ForeignKey('Tarea', on_delete=models.CASCADE, related_name='comentarios')
    
    def __str__(self): 
        return f"Comentario de {self.autor} en {self.tarea}"
