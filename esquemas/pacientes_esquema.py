from pydantic import BaseModel, Field, field_validator

class PacienteAltaEsquema(BaseModel):

    nombre: str = Field(..., min_length=2)
    apellido: str = Field(..., min_length=2)
    genero: str
    fecha_nacimiento: str

    @field_validator('genero')
    def validar_genero(cls, v):
        if v.lower() not in ['masculino', 'femenino', 'otro']:
            raise ValueError('Género no permitido')
        return v.lower()

    def serializar(self):
        """Convierte el objeto Pydantic a un diccionario para MongoDB"""
        return self.model_dump()