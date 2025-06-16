"""
Clase Medico para el sistema de gestión de clínica.
"""
from .especialidad import Especialidad
from .excepciones import DatosInvalidosException, EspecialidadDuplicadaException


class Medico:
    """
    Representa a un médico del sistema con sus especialidades y matrícula.
    
    Atributos privados:
        __nombre (str): Nombre completo del médico
        __matricula (str): Matrícula profesional (clave única)
        __especialidades (list[Especialidad]): Lista de especialidades
    """
    
    def __init__(self, nombre: str, matricula: str):
        """
        Inicializa un nuevo médico.
        
        Args:
            nombre (str): Nombre completo del médico
            matricula (str): Matrícula profesional
            
        Raises:
            DatosInvalidosException: Si los datos son inválidos
        """
        self._validar_datos(nombre, matricula)
        self.__nombre = nombre.strip()
        self.__matricula = matricula.strip()
        self.__especialidades = []
    
    def _validar_datos(self, nombre: str, matricula: str) -> None:
        """
        Valida los datos del médico.
        
        Args:
            nombre (str): Nombre a validar
            matricula (str): Matrícula a validar
            
        Raises:
            DatosInvalidosException: Si los datos son inválidos
        """
        if not nombre or not nombre.strip():
            raise DatosInvalidosException("El nombre del médico no puede estar vacío")
        
        if not matricula or not matricula.strip():
            raise DatosInvalidosException("La matrícula del médico no puede estar vacía")
    
    def agregar_especialidad(self, especialidad: Especialidad) -> None:
        """
        Agrega una especialidad a la lista del médico.
        
        Args:
            especialidad (Especialidad): Especialidad a agregar
            
        Raises:
            EspecialidadDuplicadaException: Si la especialidad ya existe
            DatosInvalidosException: Si la especialidad es None
        """
        if especialidad is None:
            raise DatosInvalidosException("La especialidad no puede ser None")
        
        # Verificar si ya existe la especialidad
        for esp in self.__especialidades:
            if esp.obtener_especialidad().lower() == especialidad.obtener_especialidad().lower():
                raise EspecialidadDuplicadaException(
                    f"El médico ya tiene la especialidad {especialidad.obtener_especialidad()}"
                )
        
        self.__especialidades.append(especialidad)
    
    def obtener_matricula(self) -> str:
        """
        Devuelve la matrícula del médico.
        
        Returns:
            str: Matrícula del médico
        """
        return self.__matricula
    
    def obtener_especialidad_para_dia(self, dia: str) -> str | None:
        """
        Devuelve el nombre de la especialidad disponible en el día especificado.
        
        Args:
            dia (str): Día de la semana a consultar
            
        Returns:
            str | None: Nombre de la especialidad o None si no atiende ese día
        """
        for especialidad in self.__especialidades:
            if especialidad.verificar_dia(dia):
                return especialidad.obtener_especialidad()
        return None
    
    def __str__(self) -> str:
        """
        Representación legible del médico.
        
        Returns:
            str: Representación incluyendo matrícula y especialidades
        """
        especialidades_str = ""
        if self.__especialidades:
            especialidades_list = [str(esp) for esp in self.__especialidades]
            especialidades_str = f" - Especialidades: {'; '.join(especialidades_list)}"
        
        return f"Dr./Dra. {self.__nombre} (Matrícula: {self.__matricula}){especialidades_str}"