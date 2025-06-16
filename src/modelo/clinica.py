from datetime import datetime
from .paciente import Paciente
from .medico import Medico
from .turno import Turno
from .receta import Receta
from .historia_clinica import HistoriaClinica
from .especialidad import Especialidad
from .excepciones import (
    PacienteNoEncontradoException,
    MedicoNoDisponibleException,
    TurnoOcupadoException,
    RecetaInvalidaException
)


class Clinica:
    """
    Clase principal que representa el sistema de gestión de la clínica.
    """
    
    def __init__(self):
        self.__pacientes = {}  # DNI -> Paciente
        self.__medicos = {}    # Matrícula -> Medico
        self.__turnos = []     # Lista de turnos
        self.__historias_clinicas = {}  # DNI -> HistoriaClinica
        
    def agregar_paciente(self, paciente: Paciente):
        """Registra un paciente y crea su historia clínica."""
        if not isinstance(paciente, Paciente):
            raise ValueError("El parámetro debe ser una instancia de Paciente")
        
        dni = paciente.obtener_dni()
        if dni in self.__pacientes:
            raise ValueError(f"Ya existe un paciente con DNI {dni}")
        
        self.__pacientes[dni] = paciente
        self.__historias_clinicas[dni] = HistoriaClinica(paciente)
        
    def agregar_medico(self, medico: Medico):
        """Registra un médico."""
        if not isinstance(medico, Medico):
            raise ValueError("El parámetro debe ser una instancia de Medico")
        
        matricula = medico.obtener_matricula()
        if matricula in self.__medicos:
            raise ValueError(f"Ya existe un médico con matrícula {matricula}")
        
        self.__medicos[matricula] = medico
        
    def obtener_pacientes(self):
        """Devuelve todos los pacientes registrados."""
        return list(self.__pacientes.values())
        
    def obtener_medicos(self):
        """Devuelve todos los médicos registrados."""
        return list(self.__medicos.values())
        
    def obtener_medico_por_matricula(self, matricula: str):
        """Devuelve un médico por su matrícula."""
        if matricula not in self.__medicos:
            raise MedicoNoDisponibleException(f"No existe médico con matrícula {matricula}")
        return self.__medicos[matricula]
        
    def agendar_turno(self, dni: str, matricula: str, especialidad: str, fecha_hora: datetime):
        """Agenda un turno si se cumplen todas las condiciones."""
        # Validar existencia de paciente y médico
        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)
        
        paciente = self.__pacientes[dni]
        medico = self.__medicos[matricula]
        
        # Validar que no haya turno duplicado
        self.validar_turno_no_duplicado(matricula, fecha_hora)
        
        # Obtener día de la semana
        dia_semana = self.obtener_dia_semana_en_espanol(fecha_hora)
        
        # Validar especialidad en día
        self.validar_especialidad_en_dia(medico, especialidad, dia_semana)
        
        # Crear y agendar turno
        turno = Turno(paciente, medico, fecha_hora, especialidad)
        self.__turnos.append(turno)
        
        # Agregar a historia clínica
        self.__historias_clinicas[dni].agregar_turno(turno)
        
    def obtener_turnos(self):
        """Devuelve todos los turnos agendados."""
        return self.__turnos.copy()
        
    def emitir_receta(self, dni: str, matricula: str, medicamentos: list[str]):
        """Emite una receta para un paciente."""
        if not medicamentos:
            raise RecetaInvalidaException("La receta debe incluir al menos un medicamento")
        
        # Validar existencia de paciente y médico
        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)
        
        paciente = self.__pacientes[dni]
        medico = self.__medicos[matricula]
        
        # Crear receta
        receta = Receta(paciente, medico, medicamentos)
        
        # Agregar a historia clínica
        self.__historias_clinicas[dni].agregar_receta(receta)
        
    def obtener_historia_clinica(self, dni: str):
        """Devuelve la historia clínica completa de un paciente."""
        self.validar_existencia_paciente(dni)
        return self.__historias_clinicas[dni]
        
    def validar_existencia_paciente(self, dni: str):
        """Verifica si un paciente está registrado."""
        if dni not in self.__pacientes:
            raise PacienteNoEncontradoException(f"No existe paciente con DNI {dni}")
            
    def validar_existencia_medico(self, matricula: str):
        """Verifica si un médico está registrado."""
        if matricula not in self.__medicos:
            raise MedicoNoDisponibleException(f"No existe médico con matrícula {matricula}")
            
    def validar_turno_no_duplicado(self, matricula: str, fecha_hora: datetime):
        """Verifica que no haya un turno duplicado."""
        for turno in self.__turnos:
            if (turno.obtener_medico().obtener_matricula() == matricula and 
                turno.obtener_fecha_hora() == fecha_hora):
                raise TurnoOcupadoException(f"El médico ya tiene un turno agendado para {fecha_hora}")
                
    def obtener_dia_semana_en_espanol(self, fecha_hora: datetime) -> str:
        """Traduce un objeto datetime al día de la semana en español."""
        dias = {
            0: 'lunes',
            1: 'martes', 
            2: 'miércoles',
            3: 'jueves',
            4: 'viernes',
            5: 'sábado',
            6: 'domingo'
        }
        return dias[fecha_hora.weekday()]
        
    def obtener_especialidad_disponible(self, medico: Medico, dia_semana: str) -> str:
        """Obtiene la especialidad disponible para un médico en un día."""
        return medico.obtener_especialidad_para_dia(dia_semana)
        
    def validar_especialidad_en_dia(self, medico: Medico, especialidad_solicitada: str, dia_semana: str):
        """Verifica que el médico atienda esa especialidad ese día."""
        especialidad_disponible = medico.obtener_especialidad_para_dia(dia_semana)
        
        if especialidad_disponible is None:
            raise MedicoNoDisponibleException(f"El médico no atiende los días {dia_semana}")
            
        if especialidad_disponible.lower() != especialidad_solicitada.lower():
            raise MedicoNoDisponibleException(
                f"El médico no atiende {especialidad_solicitada} los días {dia_semana}. "
                f"Atiende {especialidad_disponible}"
            )