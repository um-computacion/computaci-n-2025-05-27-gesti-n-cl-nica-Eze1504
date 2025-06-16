"""
Excepciones personalizadas para el sistema de gestión de clínica.
"""


class PacienteNoEncontradoException(Exception):
    """Excepción lanzada cuando un paciente no existe en el sistema."""
    pass


class MedicoNoEncontradoException(Exception):
    """Excepción lanzada cuando un médico no existe en el sistema."""
    pass


class MedicoNoDisponibleException(Exception):
    """Excepción lanzada cuando un médico no está disponible para un turno."""
    pass


class TurnoOcupadoException(Exception):
    """Excepción lanzada cuando se intenta agendar un turno en un horario ocupado."""
    pass


class RecetaInvalidaException(Exception):
    """Excepción lanzada cuando los datos de una receta son inválidos."""
    pass


class PacienteDuplicadoException(Exception):
    """Excepción lanzada cuando se intenta registrar un paciente con DNI duplicado."""
    pass


class MedicoDuplicadoException(Exception):
    """Excepción lanzada cuando se intenta registrar un médico con matrícula duplicada."""
    pass


class EspecialidadDuplicadaException(Exception):
    """Excepción lanzada cuando se intenta agregar una especialidad duplicada a un médico."""
    pass


class DatosInvalidosException(Exception):
    """Excepción lanzada cuando los datos proporcionados son inválidos."""
    pass
