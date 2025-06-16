"""
Clase Turno para el sistema de gestión de clínica.
"""
from datetime import datetime
from .paciente import Paciente
from .medico import Medico
from .excepciones import DatosInvalidosException


class Turno:
    """
    Representa un turno médico entre un paciente y un médico.
    
    Atributos privados:
        __paciente (Paciente): Paciente que asiste al turno
        __medico (Medico): Médico asignado al turno
        __fecha_hora (datetime): Fecha y hora del turno
        __especialidad (str): Especialidad médica del turno
    """
    
    def __init__(self, paciente: Paciente, medico: Medico, fecha_hora: datetime, especialidad: str):
        """
        Inicializa un nuevo turno.
        
        Args:
            paciente (Paciente): Paciente del turno
            medico (Medico): Médico del turno
            fecha_hora (datetime): Fecha y hora del turno
            especialidad (str): Especialidad médica
            
        Raises:
            DatosInvalidosException: Si los datos son inválidos
        """
        self._validar_datos(paciente, medico, fecha_hora, especialidad)
        self.__paciente = paciente
        self.__medico = medico
        self.__fecha_hora = fecha_hora
        self.__especialidad = especialidad.strip()
    
    def _validar_datos(self, paciente: Paciente, medico: Medico, 
                      fecha_hora: datetime, especialidad: str) -> None:
        """
        Valida los datos del turno.
        
        Args:
            paciente (Paciente): Paciente a validar
            medico (Medico): Médico a validar
            fecha_hora (datetime): Fecha y hora a validar
            especialidad (str): Especialidad a validar
            
        Raises:
            DatosInvalidosException: Si algún dato es inválido
        """
        if paciente is None:
            raise DatosInvalidosException("El paciente no puede ser None")
        
        if medico is None:
            raise DatosInvalidosException("El médico no puede ser None")
        
        if fecha_hora is None:
            raise DatosInvalidosException("La fecha y hora no pueden ser None")
        
        if not especialidad or not especialidad.strip():
            raise DatosInvalidosException("La especialidad no puede estar vacía")
        
        # Validar que la fecha no sea en el pasado
        if fecha_hora < datetime.now():
            raise DatosInvalidosException("No se pueden agendar turnos en el pasado")
    
    def obtener_medico(self) -> Medico:
        """
        Devuelve el médico asignado al turno.
        
        Returns:
            Medico: Médico del turno
        """
        return self.__medico
    
    def obtener_fecha_hora(self) -> datetime:
        """
        Devuelve la fecha y hora del turno.
        
        Returns:
            datetime: Fecha y hora del turno
        """
        return self.__fecha_hora
    
    def __str__(self) -> str:
        """
        Representación legible del turno.
        
        Returns:
            str: Representación incluyendo paciente, médico, especialidad y fecha/hora
        """
        fecha_str = self.__fecha_hora.strftime("%d/%m/%Y %H:%M")
        return (f"Turno: {self.__paciente.obtener_dni()} con "
                f"Dr./Dra. {self.__medico.obtener_matricula()} "
                f"({self.__especialidad}) - {fecha_str}")