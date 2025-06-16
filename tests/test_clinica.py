import unittest
from datetime import datetime
import sys
import os

# Agregar el directorio src al path para importar los módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.modelo.paciente import Paciente
from src.modelo.medico import Medico
from src.modelo.especialidad import Especialidad
from src.modelo.turno import Turno
from src.modelo.receta import Receta
from src.modelo.historia_clinica import HistoriaClinica
from src.modelo.clinica import Clinica
from src.modelo.excepciones import (
    PacienteNoEncontradoException,
    MedicoNoDisponibleException,
    TurnoOcupadoException,
    RecetaInvalidaException
)


class TestClinica(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.clinica = Clinica()
        
        # Crear pacientes de prueba
        self.paciente1 = Paciente("Juan Pérez", "12345678", "15/03/1985")
        self.paciente2 = Paciente("María González", "87654321", "22/07/1990")
        
        # Crear médicos de prueba
        self.medico1 = Medico("Dr. García", "MED001")
        self.medico2 = Medico("Dra. López", "MED002")
        
        # Crear especialidades
        self.cardiologia = Especialidad("Cardiología", ["lunes", "miércoles", "viernes"])
        self.pediatria = Especialidad("Pediatría", ["martes", "jueves"])
        
        # Asignar especialidades a médicos
        self.medico1.agregar_especialidad(self.cardiologia)
        self.medico2.agregar_especialidad(self.pediatria)
    
    def test_agregar_paciente(self):
        """Test para verificar que se puede agregar un paciente correctamente"""
        self.clinica.agregar_paciente(self.paciente1)
        
        pacientes = self.clinica.obtener_pacientes()
        self.assertEqual(len(pacientes), 1)
        self.assertEqual(pacientes[0], self.paciente1)
        
        # Verificar que se creó la historia clínica
        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertIsNotNone(historia)
        self.assertEqual(historia._paciente, self.paciente1)
    
    def test_agregar_medico(self):
        """Test para verificar que se puede agregar un médico correctamente"""
        self.clinica.agregar_medico(self.medico1)
        
        medicos = self.clinica.obtener_medicos()
        self.assertEqual(len(medicos), 1)
        self.assertEqual(medicos[0], self.medico1)
    
    def test_obtener_medico_por_matricula(self):
        """Test para verificar que se puede obtener un médico por matrícula"""
        self.clinica.agregar_medico(self.medico1)
        
        medico_encontrado = self.clinica.obtener_medico_por_matricula("MED001")
        self.assertEqual(medico_encontrado, self.medico1)
    
    def test_obtener_medico_por_matricula_inexistente(self):
        """Test para verificar error al buscar médico inexistente"""
        with self.assertRaises(Exception):
            self.clinica.obtener_medico_por_matricula("MED999")
    
    def test_validar_existencia_paciente(self):
        """Test para verificar validación de existencia de paciente"""
        self.clinica.agregar_paciente(self.paciente1)
        
        # No debe lanzar excepción
        self.clinica.validar_existencia_paciente("12345678")
        
        # Debe lanzar excepción para paciente inexistente
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.validar_existencia_paciente("99999999")
    
    def test_validar_existencia_medico(self):
        """Test para verificar validación de existencia de médico"""
        self.clinica.agregar_medico(self.medico1)
        
        # No debe lanzar excepción
        self.clinica.validar_existencia_medico("MED001")
        
        # Debe lanzar excepción para médico inexistente
        with self.assertRaises(Exception):
            self.clinica.validar_existencia_medico("MED999")
    
    def test_obtener_dia_semana_en_espanol(self):
        """Test para verificar conversión de día de la semana al español"""
        # Lunes = 0, Domingo = 6
        fecha_lunes = datetime(2025, 6, 16)  # Lunes
        fecha_martes = datetime(2025, 6, 17)  # Martes
        fecha_miercoles = datetime(2025, 6, 18)  # Miércoles
        fecha_jueves = datetime(2025, 6, 19)  # Jueves
        fecha_viernes = datetime(2025, 6, 20)  # Viernes
        fecha_sabado = datetime(2025, 6, 21)  # Sábado
        fecha_domingo = datetime(2025, 6, 22)  # Domingo
        
        self.assertEqual(self.clinica.obtener_dia_semana_en_espanol(fecha_lunes), "lunes")
        self.assertEqual(self.clinica.obtener_dia_semana_en_espanol(fecha_martes), "martes")
        self.assertEqual(self.clinica.obtener_dia_semana_en_espanol(fecha_miercoles), "miércoles")
        self.assertEqual(self.clinica.obtener_dia_semana_en_espanol(fecha_jueves), "jueves")
        self.assertEqual(self.clinica.obtener_dia_semana_en_espanol(fecha_viernes), "viernes")
        self.assertEqual(self.clinica.obtener_dia_semana_en_espanol(fecha_sabado), "sábado")
        self.assertEqual(self.clinica.obtener_dia_semana_en_espanol(fecha_domingo), "domingo")
    
    def test_obtener_especialidad_disponible(self):
        """Test para verificar obtención de especialidad disponible"""
        especialidad_lunes = self.clinica.obtener_especialidad_disponible(self.medico1, "lunes")
        self.assertEqual(especialidad_lunes, "Cardiología")
        
        especialidad_martes = self.clinica.obtener_especialidad_disponible(self.medico1, "martes")
        self.assertIsNone(especialidad_martes)
    
    def test_validar_especialidad_en_dia(self):
        """Test para verificar validación de especialidad en día específico"""
        # No debe lanzar excepción para combinación válida
        self.clinica.validar_especialidad_en_dia(self.medico1, "Cardiología", "lunes")
        
        # Debe lanzar excepción para día no disponible
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.validar_especialidad_en_dia(self.medico1, "Cardiología", "martes")
        
        # Debe lanzar excepción para especialidad incorrecta
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.validar_especialidad_en_dia(self.medico1, "Pediatría", "lunes")
    
    def test_agendar_turno_exitoso(self):
        """Test para verificar agendamiento exitoso de turno"""
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        fecha_turno = datetime(2025, 6, 23, 10, 30)  # Lunes
        
        self.clinica.agendar_turno("12345678", "MED001", "Cardiología", fecha_turno)
        
        turnos = self.clinica.obtener_turnos()
        self.assertEqual(len(turnos), 1)
        
        turno = turnos[0]
        self.assertEqual(turno.obtener_medico(), self.medico1)
        self.assertEqual(turno.obtener_fecha_hora(), fecha_turno)
        
        # Verificar que se agregó a la historia clínica
        historia = self.clinica.obtener_historia_clinica("12345678")
        turnos_historia = historia.obtener_turnos()
        self.assertEqual(len(turnos_historia), 1)
    
    def test_agendar_turno_paciente_inexistente(self):
        """Test para verificar error al agendar turno con paciente inexistente"""
        self.clinica.agregar_medico(self.medico1)
        fecha_turno = datetime(2025, 6, 23, 10, 30)  # Lunes
        
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.agendar_turno("99999999", "MED001", "Cardiología", fecha_turno)
    
    def test_agendar_turno_medico_inexistente(self):
        """Test para verificar error al agendar turno con médico inexistente"""
        self.clinica.agregar_paciente(self.paciente1)
        fecha_turno = datetime(2025, 6, 23, 10, 30)  # Lunes
        
        with self.assertRaises(Exception):
            self.clinica.agendar_turno("12345678", "MED999", "Cardiología", fecha_turno)
    
    def test_agendar_turno_especialidad_no_disponible(self):
        """Test para verificar error al agendar turno en día no disponible"""
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        fecha_turno = datetime(2025, 6, 17, 10, 30)  # Martes (no disponible para cardiología)
        
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("12345678", "MED001", "Cardiología", fecha_turno)
    
    def test_agendar_turno_duplicado(self):
        """Test para verificar error al agendar turno duplicado"""
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_paciente(self.paciente2)
        self.clinica.agregar_medico(self.medico1)
        
        fecha_turno = datetime(2025, 6, 23, 10, 30)  # Lunes
        
        # Agendar primer turno
        self.clinica.agendar_turno("12345678", "MED001", "Cardiología", fecha_turno)
        
        # Intentar agendar segundo turno en mismo horario
        with self.assertRaises(TurnoOcupadoException):
            self.clinica.agendar_turno("87654321", "MED001", "Cardiología", fecha_turno)
    
    def test_emitir_receta_exitosa(self):
        """Test para verificar emisión exitosa de receta"""
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        medicamentos = ["Aspirina 100mg", "Atorvastatina 20mg"]
        
        self.clinica.emitir_receta("12345678", "MED001", medicamentos)
        
        # Verificar que se agregó a la historia clínica
        historia = self.clinica.obtener_historia_clinica("12345678")
        recetas = historia.obtener_recetas()
        self.assertEqual(len(recetas), 1)
        
        receta = recetas[0]
        self.assertEqual(receta._paciente, self.paciente1)
        self.assertEqual(receta._medico, self.medico1)
        self.assertEqual(receta._medicamentos, medicamentos)
    
    def test_emitir_receta_paciente_inexistente(self):
        """Test para verificar error al emitir receta con paciente inexistente"""
        self.clinica.agregar_medico(self.medico1)
        medicamentos = ["Aspirina 100mg"]
        
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.emitir_receta("99999999", "MED001", medicamentos)
    
    def test_emitir_receta_medico_inexistente(self):
        """Test para verificar error al emitir receta con médico inexistente"""
        self.clinica.agregar_paciente(self.paciente1)
        medicamentos = ["Aspirina 100mg"]
        
        with self.assertRaises(Exception):
            self.clinica.emitir_receta("12345678", "MED999", medicamentos)
    
    def test_emitir_receta_sin_medicamentos(self):
        """Test para verificar error al emitir receta sin medicamentos"""
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        with self.assertRaises(RecetaInvalidaException):
            self.clinica.emitir_receta("12345678", "MED001", [])
    
    def test_obtener_historia_clinica_paciente_inexistente(self):
        """Test para verificar error al obtener historia clínica de paciente inexistente"""
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.obtener_historia_clinica("99999999")
    
    def test_validar_turno_no_duplicado(self):
        """Test para verificar validación de turno no duplicado"""
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        fecha_turno = datetime(2025, 6, 23, 10, 30)  # Lunes
        
        # Primer turno - no debe lanzar excepción
        self.clinica.validar_turno_no_duplicado("MED001", fecha_turno)
        
        # Agendar turno
        self.clinica.agendar_turno("12345678", "MED001", "Cardiología", fecha_turno)
        
        # Segundo turno en mismo horario - debe lanzar excepción
        with self.assertRaises(TurnoOcupadoException):
            self.clinica.validar_turno_no_duplicado("MED001", fecha_turno)


if __name__ == '__main__':
    unittest.main()