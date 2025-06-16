"""
Clase HistoriaClinica para el sistema de gestión de clínica.
"""
from .paciente import Paciente
from .turno import Turno
from .receta import Receta
from .excepciones import DatosInvalidosException


class HistoriaClinica:
    """
    Almacena la información médica de un paciente: turnos y recetas.
    
    Atributos privados:
        __paciente (Paciente): Paciente al que pertenece la historia clínica
        __turnos (list[Turno]): Lista de turnos agendados del paciente
        __recetas (list[Receta]): Lista de recetas emitidas para el paciente
    """
    
    def __init__(self, paciente: Paciente):
        """
        Inicializa una nueva historia clínica.
        
        Args:
            paciente (Paciente): Paciente propietario de la historia clínica
            
        Raises:
            DatosInvalidosException: Si el paciente es None
        """
        if paciente is None:
            raise DatosInvalidosException("El paciente no puede ser None")
        
        self.__paciente = paciente
        self.__turnos = []
        self.__recetas = []
    
    def agregar_turno(self, turno: Turno) -> None:
        """
        Agrega un nuevo turno a la historia clínica.
        
        Args:
            turno (Turno): Turno a agregar
            
        Raises:
            DatosInvalidosException: Si el turno es None
        """
        if turno is None:
            raise DatosInvalidosException("El turno no puede ser None")
        
        self.__turnos.append(turno)
    
    def agregar_receta(self, receta: Receta) -> None:
        """
        Agrega una receta médica a la historia clínica.
        
        Args:
            receta (Receta): Receta a agregar
            
        Raises:
            DatosInvalidosException: Si la receta es None
        """
        if receta is None:
            raise DatosInvalidosException("La receta no puede ser None")
        
        self.__recetas.append(receta)
    
    def obtener_turnos(self) -> list[Turno]:
        """
        Devuelve una copia de la lista de turnos del paciente.
        
        Returns:
            list[Turno]: Copia de la lista de turnos
        """
        return self.__turnos.copy()
    
    def obtener_recetas(self) -> list[Receta]:
        """
        Devuelve una copia de la lista de recetas del paciente.
        
        Returns:
            list[Receta]: Copia de la lista de recetas
        """
        return self.__recetas.copy()
    
    def __str__(self) -> str:
        """
        Representación textual de la historia clínica.
        
        Returns:
            str: Historia clínica completa incluyendo turnos y recetas
        """
        resultado = f"=== Historia Clínica de {self.__paciente} ===\n\n"
        
        resultado += f"TURNOS ({len(self.__turnos)}):\n"
        if self.__turnos:
            for i, turno in enumerate(self.__turnos, 1):
                resultado += f"{i}. {turno}\n"
        else:
            resultado += "No hay turnos registrados.\n"
        
        resultado += f"\nRECETAS ({len(self.__recetas)}):\n"
        if self.__recetas:
            for i, receta in enumerate(self.__recetas, 1):
                resultado += f"{i}. {receta}\n"
        else:
            resultado += "No hay recetas registradas.\n"
        
        return resultado