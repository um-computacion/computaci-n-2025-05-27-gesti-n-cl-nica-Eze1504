"""
Tests de integración para el Sistema de Gestión de Clínica.

Estos tests verifican el funcionamiento conjunto de todos los componentes
del sistema, simulando flujos completos de trabajo.
"""

import unittest
from datetime import datetime, timedelta
import sys
import os

# Agregar el directorio src al path para importar los módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.modelo.clinica import Clinica
from src.modelo.paciente import Paciente
from src.modelo.medico import Medico
from src.modelo.especialidad import Especialidad
from src.modelo.turno import Turno
from src.modelo.receta import Receta
from src.modelo.historia_clinica import HistoriaClinica
from src.modelo.excepciones import (
    PacienteNoEncontradoException,
    MedicoNoDisponibleException,
    TurnoOcupadoException,
    RecetaInvalidaException
)


class TestIntegracion(unittest.TestCase):
    """Tests de integración que verifican el funcionamiento completo del sistema."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.clinica = Clinica()
        
        # Crear pacientes de prueba
        self.paciente1 = Paciente("Juan Pérez", "12345678", "15/03/1990")
        self.paciente2 = Paciente("María García", "87654321", "22/07/1985")
        
        # Crear especialidades
        self.pediatria = Especialidad("Pediatría", ["lunes", "miércoles", "viernes"])
        self.cardiologia = Especialidad("Cardiología", ["martes", "jueves"])
        self.traumatologia = Especialidad("Traumatología", ["lunes", "martes", "miércoles"])
        
        # Crear médicos de prueba
        self.medico1 = Medico("Dr. Carlos Rodríguez", "MP001")
        self.medico1.agregar_especialidad(self.pediatria)
        self.medico1.agregar_especialidad(self.cardiologia)
        
        self.medico2 = Medico("Dra. Ana López", "MP002")
        self.medico2.agregar_especialidad(self.traumatologia)
        
        # Registrar en la clínica
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_paciente(self.paciente2)
        self.clinica.agregar_medico(self.medico1)
        self.clinica.agregar_medico(self.medico2)

    def test_flujo_completo_atencion_medica(self):
        """Test del flujo completo: registro, turno, atención y receta."""
        
        # 1. Verificar que los pacientes y médicos están registrados
        pacientes = self.clinica.obtener_pacientes()
        medicos = self.clinica.obtener_medicos()
        
        self.assertEqual(len(pacientes), 2)
        self.assertEqual(len(medicos), 2)
        
        # 2. Agendar un turno para pediatría en lunes
        fecha_turno = datetime(2025, 6, 23, 10, 0)  # Lunes
        
        self.clinica.agendar_turno(
            "12345678", 
            "MP001", 
            "Pediatría", 
            fecha_turno
        )
        
        # 3. Verificar que el turno se agendó correctamente
        turnos = self.clinica.obtener_turnos()
        self.assertEqual(len(turnos), 1)
        
        turno = turnos[0]
        self.assertEqual(turno.obtener_medico().obtener_matricula(), "MP001")
        self.assertEqual(turno.obtener_fecha_hora(), fecha_turno)
        
        # 4. Emitir una receta después del turno
        medicamentos = ["Paracetamol 500mg", "Ibuprofeno 400mg"]
        self.clinica.emitir_receta("12345678", "MP001", medicamentos)
        
        # 5. Verificar la historia clínica completa
        historia = self.clinica.obtener_historia_clinica("12345678")
        
        turnos_historia = historia.obtener_turnos()
        recetas_historia = historia.obtener_recetas()
        
        self.assertEqual(len(turnos_historia), 1)
        self.assertEqual(len(recetas_historia), 1)
        
        # Verificar detalles de la receta
        receta = recetas_historia[0]
        self.assertEqual(len(receta._medicamentos), 2)
        self.assertIn("Paracetamol 500mg", receta._medicamentos)

    def test_multiples_turnos_mismo_paciente(self):
        """Test de múltiples turnos para el mismo paciente con diferentes médicos."""
        
        # Turno 1: Pediatría con Dr. Rodríguez (lunes)
        fecha1 = datetime(2025, 6, 23, 10, 0)  # Lunes
        self.clinica.agendar_turno("12345678", "MP001", "Pediatría", fecha1)
        
        # Turno 2: Traumatología con Dra. López (martes)
        fecha2 = datetime(2025, 6, 24, 14, 0)  # Martes
        self.clinica.agendar_turno("12345678", "MP002", "Traumatología", fecha2)
        
        # Turno 3: Cardiología con Dr. Rodríguez (jueves)
        fecha3 = datetime(2025, 6, 26, 16, 0)  # Jueves
        self.clinica.agendar_turno("12345678", "MP001", "Cardiología", fecha3)
        
        # Verificar que todos los turnos se agendaron
        turnos = self.clinica.obtener_turnos()
        self.assertEqual(len(turnos), 3)
        
        # Verificar historia clínica
        historia = self.clinica.obtener_historia_clinica("12345678")
        turnos_historia = historia.obtener_turnos()
        self.assertEqual(len(turnos_historia), 3)
        
        # Verificar que cada turno tiene la especialidad correcta
        especialidades = [turno._especialidad for turno in turnos_historia]
        self.assertIn("Pediatría", especialidades)
        self.assertIn("Traumatología", especialidades)
        self.assertIn("Cardiología", especialidades)

    def test_validaciones_cruzadas_turnos(self):
        """Test de validaciones entre turnos y disponibilidad médica."""
        
        fecha_lunes = datetime(2025, 6, 23, 10, 0)  # Lunes
        
        # 1. Agendar turno válido
        self.clinica.agendar_turno("12345678", "MP001", "Pediatría", fecha_lunes)
        
        # 2. Intentar agendar turno duplicado (mismo médico, misma fecha/hora)
        with self.assertRaises(TurnoOcupadoException):
            self.clinica.agendar_turno("87654321", "MP001", "Pediatría", fecha_lunes)
        
        # 3. Intentar agendar especialidad no disponible ese día
        fecha_domingo = datetime(2025, 6, 22, 10, 0)  # Domingo
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("87654321", "MP001", "Pediatría", fecha_domingo)
        
        # 4. Intentar agendar especialidad que el médico no tiene
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("87654321", "MP001", "Traumatología", fecha_lunes)

    def test_flujo_recetas_multiples_medicos(self):
        """Test de emisión de recetas por diferentes médicos para el mismo paciente."""
        
        # Agendar turnos previos
        fecha1 = datetime(2025, 6, 23, 10, 0)  # Lunes - Pediatría
        fecha2 = datetime(2025, 6, 24, 14, 0)  # Martes - Traumatología
        
        self.clinica.agendar_turno("12345678", "MP001", "Pediatría", fecha1)
        self.clinica.agendar_turno("12345678", "MP002", "Traumatología", fecha2)
        
        # Emitir recetas de diferentes médicos
        medicamentos_pediatria = ["Paracetamol infantil", "Jarabe para la tos"]
        medicamentos_traumatologia = ["Antiinflamatorio", "Relajante muscular"]
        
        self.clinica.emitir_receta("12345678", "MP001", medicamentos_pediatria)
        self.clinica.emitir_receta("12345678", "MP002", medicamentos_traumatologia)
        
        # Verificar historia clínica
        historia = self.clinica.obtener_historia_clinica("12345678")
        recetas = historia.obtener_recetas()
        
        self.assertEqual(len(recetas), 2)
        
        # Verificar que las recetas tienen los médicos correctos
        matriculas_medicos = [receta._medico.obtener_matricula() for receta in recetas]
        self.assertIn("MP001", matriculas_medicos)
        self.assertIn("MP002", matriculas_medicos)

    def test_gestion_especialidades_dinamica(self):
        """Test de agregar especialidades dinámicamente y su impacto en turnos."""
        
        # Crear nuevo médico
        medico3 = Medico("Dr. Luis Martínez", "MP003")
        neurologia = Especialidad("Neurología", ["miércoles", "viernes"])
        medico3.agregar_especialidad(neurologia)
        
        self.clinica.agregar_medico(medico3)
        
        # Agendar turno con la nueva especialidad
        fecha_miercoles = datetime(2025, 6, 25, 11, 0)  # Miércoles
        self.clinica.agendar_turno("87654321", "MP003", "Neurología", fecha_miercoles)
        
        # Verificar que el turno se agendó correctamente
        turnos = self.clinica.obtener_turnos()
        turno_neurologia = next(
            (t for t in turnos if t._especialidad == "Neurología"), 
            None
        )
        
        self.assertIsNotNone(turno_neurologia)
        self.assertEqual(turno_neurologia._medico.obtener_matricula(), "MP003")
        
        # Intentar agendar en día no disponible para neurología
        fecha_lunes = datetime(2025, 6, 23, 11, 0)  # Lunes
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("87654321", "MP003", "Neurología", fecha_lunes)

    def test_casos_limite_validaciones(self):
        """Test de casos límite y validaciones extremas."""
        
        # 1. Intentar operaciones con paciente inexistente
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.agendar_turno("99999999", "MP001", "Pediatría", datetime.now())
        
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.emitir_receta("99999999", "MP001", ["Medicamento"])
        
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.obtener_historia_clinica("99999999")
        
        # 2. Intentar operaciones con médico inexistente
        with self.assertRaises(Exception):  # Podría ser MedicoNoEncontradoException
            self.clinica.agendar_turno("12345678", "MP999", "Pediatría", datetime.now())
        
        # 3. Intentar emitir receta sin medicamentos
        with self.assertRaises(RecetaInvalidaException):
            self.clinica.emitir_receta("12345678", "MP001", [])
        
        # 4. Verificar que las historias clínicas se crean automáticamente
        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertIsNotNone(historia)
        self.assertEqual(historia._paciente.obtener_dni(), "12345678")

    def test_integridad_datos_historias_clinicas(self):
        """Test de integridad de datos en historias clínicas."""
        
        # Crear un flujo completo de atención
        fecha_turno = datetime(2025, 6, 23, 10, 0)  # Lunes
        
        # Agendar turno
        self.clinica.agendar_turno("12345678", "MP001", "Pediatría", fecha_turno)
        
        # Emitir receta
        medicamentos = ["Medicamento A", "Medicamento B"]
        self.clinica.emitir_receta("12345678", "MP001", medicamentos)
        
        # Obtener historia clínica
        historia = self.clinica.obtener_historia_clinica("12345678")
        
        # Verificar que los datos están relacionados correctamente
        turnos = historia.obtener_turnos()
        recetas = historia.obtener_recetas()
        
        self.assertEqual(len(turnos), 1)
        self.assertEqual(len(recetas), 1)
        
        # Verificar que turno y receta pertenecen al mismo paciente
        turno = turnos[0]
        receta = recetas[0]
        
        self.assertEqual(turno._paciente.obtener_dni(), "12345678")
        self.assertEqual(receta._paciente.obtener_dni(), "12345678")
        
        # Verificar que las listas devueltas son copias (no referencias)
        turnos_originales = historia.obtener_turnos()
        turnos_copia = historia.obtener_turnos()
        
        # Modificar una copia no debe afectar la otra
        turnos_copia.clear()
        self.assertEqual(len(turnos_originales), 1)

    def test_flujo_multiples_pacientes_simultaneos(self):
        """Test de manejo simultáneo de múltiples pacientes."""
        
        # Crear fechas diferentes para evitar conflictos
        fecha1 = datetime(2025, 6, 23, 10, 0)  # Lunes 10:00
        fecha2 = datetime(2025, 6, 23, 11, 0)  # Lunes 11:00
        fecha3 = datetime(2025, 6, 24, 10, 0)  # Martes 10:00
        
        # Agendar turnos para diferentes pacientes
        self.clinica.agendar_turno("12345678", "MP001", "Pediatría", fecha1)
        self.clinica.agendar_turno("87654321", "MP001", "Pediatría", fecha2)
        self.clinica.agendar_turno("12345678", "MP002", "Traumatología", fecha3)
        
        # Emitir recetas
        self.clinica.emitir_receta("12345678", "MP001", ["Med A", "Med B"])
        self.clinica.emitir_receta("87654321", "MP001", ["Med C"])
        self.clinica.emitir_receta("12345678", "MP002", ["Med D", "Med E"])
        
        # Verificar historias clínicas individuales
        historia1 = self.clinica.obtener_historia_clinica("12345678")
        historia2 = self.clinica.obtener_historia_clinica("87654321")
        
        # Paciente 1: 2 turnos, 2 recetas
        self.assertEqual(len(historia1.obtener_turnos()), 2)
        self.assertEqual(len(historia1.obtener_recetas()), 2)
        
        # Paciente 2: 1 turno, 1 receta
        self.assertEqual(len(historia2.obtener_turnos()), 1)
        self.assertEqual(len(historia2.obtener_recetas()), 1)
        
        # Verificar totales del sistema
        self.assertEqual(len(self.clinica.obtener_turnos()), 3)

    def test_consistencia_fechas_y_horarios(self):
        """Test de consistencia en el manejo de fechas y horarios."""
        
        # Crear fechas con diferentes formatos y verificar consistencia
        fecha_base = datetime(2025, 6, 23, 14, 30)  # Lunes 14:30
        
        # Agendar turno
        self.clinica.agendar_turno("12345678", "MP001", "Pediatría", fecha_base)
        
        # Verificar que la fecha se mantiene exacta
        turnos = self.clinica.obtener_turnos()
        turno = turnos[0]
        
        self.assertEqual(turno.obtener_fecha_hora(), fecha_base)
        self.assertEqual(turno.obtener_fecha_hora().hour, 14)
        self.assertEqual(turno.obtener_fecha_hora().minute, 30)
        
        # Verificar conversión de día de la semana
        dia_semana = self.clinica.obtener_dia_semana_en_espanol(fecha_base)
        self.assertEqual(dia_semana, "lunes")
        
        # Emitir receta y verificar que la fecha es automática y actual
        tiempo_antes = datetime.now()
        self.clinica.emitir_receta("12345678", "MP001", ["Medicamento"])
        tiempo_despues = datetime.now()
        
        historia = self.clinica.obtener_historia_clinica("12345678")
        recetas = historia.obtener_recetas()
        fecha_receta = recetas[0]._fecha
        
        # La fecha de la receta debe estar entre los tiempos de antes y después
        self.assertTrue(tiempo_antes <= fecha_receta <= tiempo_despues)


if __name__ == '__main__':
    # Configuración para ejecutar los tests
    unittest.main(verbosity=2)