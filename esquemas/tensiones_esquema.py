from pydantic import BaseModel, Field
from datetime import datetime

class TensionEsquema(BaseModel):
    id_paciente: str
    valoracion: str
    estado: str = "final"
    fecha: datetime = Field(default_factory=datetime.now)

    def serializar(self):
        return self.model_dump()