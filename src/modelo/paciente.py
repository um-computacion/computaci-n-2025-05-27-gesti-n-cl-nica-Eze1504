"""
Clase Paciente para el sistema de gestión de clínica.
"""
from datetime import datetime
from .excepciones import DatosInvalidosException


class Paciente:
    """
    Representa a un paciente de la clínica.
    
    Atributos privados:
        __nombre (str): Nombre completo del paciente
        __dni (str): DNI del paciente (identificador único)
        __fecha_nacimiento (str): Fecha de nacimiento en formato dd/mm/aaaa
    """
    
    def __init__(self, nombre: str, dni: str, fecha_nacimiento: str):
        """
        Inicializa un nuevo paciente.
        
        Args:
            nombre (str): Nombre completo del paciente
            dni (str): DNI del paciente
            fecha_nacimiento (str): Fecha de nacimiento en formato dd/mm/aaaa
            
        Raises:
            DatosInvalidosException: Si algún dato es inválido
        """
        self._validar_datos(nombre, dni, fecha_nacimiento)
        self.__nombre = nombre.strip()
        self.__dni = dni.strip()
        self.__fecha_nacimiento = fecha_nacimiento.strip()
    
    def _validar_datos(self, nombre: str, dni: str, fecha_nacimiento: str) -> None:
        """
        Valida los datos del paciente.
        
        Args:
            nombre (str): Nombre a validar
            dni (str): DNI a validar
            fecha_nacimiento (str): Fecha de nacimiento a validar
            
        Raises:
            DatosInvalidosException: Si algún dato es inválido
        """
        if not nombre or not nombre.strip():
            raise DatosInvalidosException("El nombre del paciente no puede estar vacío")
        
        if not dni or not dni.strip():
            raise DatosInvalidosException("El DNI del paciente no puede estar vacío")
        
        if not fecha_nacimiento or not fecha_nacimiento.strip():
            raise DatosInvalidosException("La fecha de nacimiento no puede estar vacía")
        
        # Validar formato de fecha dd/mm/aaaa
        try:
            datetime.strptime(fecha_nacimiento.strip(), "%d/%m/%Y")
        except ValueError:
            raise DatosInvalidosException("La fecha de nacimiento debe estar en formato dd/mm/aaaa")
    
    def obtener_dni(self) -> str:
        """
        Devuelve el DNI del paciente.
        
        Returns:
            str: DNI del paciente
        """
        return self.__dni
    
    def __str__(self) -> str:
        """
        Representación en texto del paciente.
        
        Returns:
            str: Representación legible del paciente
        """
        return f"Paciente: {self.__nombre} (DNI: {self.__dni}, Nacimiento: {self.__fecha_nacimiento})"