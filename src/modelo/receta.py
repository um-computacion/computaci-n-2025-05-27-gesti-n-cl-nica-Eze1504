"""
Clase Receta para el sistema de gestión de clínica.
"""
from datetime import datetime
from .paciente import Paciente
from .medico import Medico
from .excepciones import DatosInvalidosException, RecetaInvalidaException


class Receta:
    """
    Representa una receta médica emitida por un médico a un paciente.
    
    Atributos privados:
        __paciente (Paciente): Paciente al que se le emite la receta
        __medico (Medico): Médico que emite la receta
        __medicamentos (list[str]): Lista de medicamentos recetados
        __fecha (datetime): Fecha de emisión de la receta
    """
    
    def __init__(self, paciente: Paciente, medico: Medico, medicamentos: list[str]):
        """
        Inicializa una nueva receta.
        
        Args:
            paciente (Paciente): Paciente de la receta
            medico (Medico): Médico que emite la receta
            medicamentos (list[str]): Lista de medicamentos
            
        Raises:
            RecetaInvalidaException: Si los datos de la receta son inválidos
        """
        self._validar_datos(paciente, medico, medicamentos)
        self.__paciente = paciente
        self.__medico = medico
        self.__medicamentos = [med.strip() for med in medicamentos if med.strip()]
        self.__fecha = datetime.now()
    
    def _validar_datos(self, paciente: Paciente, medico: Medico, 
                      medicamentos: list[str]) -> None:
        """
        Valida los datos de la receta.
        
        Args:
            paciente (Paciente): Paciente a validar
            medico (Medico): Médico a validar
            medicamentos (list[str]): Medicamentos a validar
            
        Raises:
            RecetaInvalidaException: Si los datos son inválidos
        """
        if paciente is None:
            raise RecetaInvalidaException("El paciente no puede ser None")
        
        if medico is None:
            raise RecetaInvalidaException("El médico no puede ser None")
        
        if not medicamentos or len(medicamentos) == 0:
            raise RecetaInvalidaException("Debe especificar al menos un medicamento")
        
        # Validar que los medicamentos no estén vacíos
        medicamentos_validos = [med.strip() for med in medicamentos if med.strip()]
        if len(medicamentos_validos) == 0:
            raise RecetaInvalidaException("Debe especificar al menos un medicamento válido")
    
    def __str__(self) -> str:
        """
        Representación en cadena de la receta.
        
        Returns:
            str: Representación legible de la receta
        """
        fecha_str = self.__fecha.strftime("%d/%m/%Y %H:%M")
        medicamentos_str = ", ".join(self.__medicamentos)
        
        return (f"Receta para {self.__paciente.obtener_dni()} "
                f"por Dr./Dra. {self.__medico.obtener_matricula()} "
                f"({fecha_str}) - Medicamentos: {medicamentos_str}")