"""
Clase Especialidad para el sistema de gestión de clínica.
"""
from .excepciones import DatosInvalidosException


class Especialidad:
    """
    Representa una especialidad médica junto con los días de atención.
    
    Atributos privados:
        __tipo (str): Nombre de la especialidad
        __dias (list[str]): Lista de días de atención en minúsculas
    """
    
    def __init__(self, tipo: str, dias: list[str]):
        """
        Inicializa una nueva especialidad.
        
        Args:
            tipo (str): Nombre de la especialidad
            dias (list[str]): Lista de días de atención
            
        Raises:
            DatosInvalidosException: Si los datos son inválidos
        """
        self._validar_datos(tipo, dias)
        self.__tipo = tipo.strip()
        self.__dias = [dia.lower().strip() for dia in dias]
    
    def _validar_datos(self, tipo: str, dias: list[str]) -> None:
        """
        Valida los datos de la especialidad.
        
        Args:
            tipo (str): Tipo de especialidad a validar
            dias (list[str]): Días a validar
            
        Raises:
            DatosInvalidosException: Si los datos son inválidos
        """
        if not tipo or not tipo.strip():
            raise DatosInvalidosException("El tipo de especialidad no puede estar vacío")
        
        if not dias or len(dias) == 0:
            raise DatosInvalidosException("Debe especificar al menos un día de atención")
        
        dias_validos = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        for dia in dias:
            if dia.lower().strip() not in dias_validos:
                raise DatosInvalidosException(f"'{dia}' no es un día válido")
        
        # Verificar que no haya días duplicados
        dias_normalizados = [dia.lower().strip() for dia in dias]
        if len(dias_normalizados) != len(set(dias_normalizados)):
            raise DatosInvalidosException("No se pueden repetir días de atención")
    
    def obtener_especialidad(self) -> str:
        """
        Devuelve el nombre de la especialidad.
        
        Returns:
            str: Nombre de la especialidad
        """
        return self.__tipo
    
    def verificar_dia(self, dia: str) -> bool:
        """
        Verifica si la especialidad está disponible en el día proporcionado.
        
        Args:
            dia (str): Día a verificar (no sensible a mayúsculas/minúsculas)
            
        Returns:
            bool: True si está disponible, False en caso contrario
        """
        return dia.lower().strip() in self.__dias
    
    def __str__(self) -> str:
        """
        Representación legible de la especialidad.
        
        Returns:
            str: Cadena con el nombre y días de atención
        """
        dias_str = ", ".join(self.__dias)
        return f"{self.__tipo} (Días: {dias_str})"