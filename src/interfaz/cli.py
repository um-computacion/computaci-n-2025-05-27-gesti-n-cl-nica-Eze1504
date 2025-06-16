"""
Interfaz de línea de comandos (CLI) para el sistema de gestión de clínica.
Proporciona un menú interactivo para todas las operaciones del sistema.
"""

from datetime import datetime
import sys
import os

# Agregar el directorio padre al path para importar el modelo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.modelo.clinica import Clinica
from src.modelo.paciente import Paciente
from src.modelo.medico import Medico
from src.modelo.especialidad import Especialidad
from src.modelo.excepciones import (
    PacienteNoEncontradoException,
    MedicoNoDisponibleException, 
    TurnoOcupadoException,
    RecetaInvalidaException
)


class CLI:
    """
    Interfaz de línea de comandos para el sistema de gestión de clínica.
    Maneja la interacción con el usuario y delega la lógica de negocio a la clase Clinica.
    """
    
    def __init__(self):
        """Inicializa la CLI con una nueva instancia de Clinica."""
        self.clinica = Clinica()
    
    def mostrar_menu(self):
        """Muestra el menú principal de opciones."""
        print("\n" + "="*50)
        print("       SISTEMA DE GESTIÓN DE CLÍNICA")
        print("="*50)
        print("1) Agregar paciente")
        print("2) Agregar médico") 
        print("3) Agendar turno")
        print("4) Agregar especialidad a médico")
        print("5) Emitir receta")
        print("6) Ver historia clínica")
        print("7) Ver todos los turnos")
        print("8) Ver todos los pacientes")
        print("9) Ver todos los médicos")
        print("0) Salir")
        print("="*50)
    
    def ejecutar(self):
        """
        Bucle principal de la aplicación.
        Muestra el menú y procesa las opciones del usuario.
        """
        while True:
            try:
                self.mostrar_menu()
                opcion = input("Seleccione una opción: ").strip()
                
                if opcion == "1":
                    self.agregar_paciente()
                elif opcion == "2":
                    self.agregar_medico()
                elif opcion == "3":
                    self.agendar_turno()
                elif opcion == "4":
                    self.agregar_especialidad_medico()
                elif opcion == "5":
                    self.emitir_receta()
                elif opcion == "6":
                    self.ver_historia_clinica()
                elif opcion == "7":
                    self.ver_todos_turnos()
                elif opcion == "8":
                    self.ver_todos_pacientes()
                elif opcion == "9":
                    self.ver_todos_medicos()
                elif opcion == "0":
                    print("\n¡Gracias por usar el sistema de gestión de clínica!")
                    break
                else:
                    print("\n❌ Opción inválida. Por favor, seleccione una opción del menú.")
                
                self.pausar()
                
            except KeyboardInterrupt:
                print("\n\n¡Hasta luego!")
                break
            except Exception as e:
                print(f"\n❌ Error inesperado: {e}")
                self.pausar()
    
    def agregar_paciente(self):
        """Solicita datos del paciente y lo registra en el sistema."""
        print("\n--- AGREGAR PACIENTE ---")
        try:
            nombre = input("Nombre completo: ").strip()
            if not nombre:
                print("❌ El nombre no puede estar vacío.")
                return
            
            dni = input("DNI: ").strip()
            if not dni:
                print("❌ El DNI no puede estar vacío.")
                return
            
            fecha_nacimiento = input("Fecha de nacimiento (dd/mm/aaaa): ").strip()
            if not fecha_nacimiento:
                print("❌ La fecha de nacimiento no puede estar vacía.")
                return
            
            # Validar formato de fecha
            try:
                datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
            except ValueError:
                print("❌ Formato de fecha inválido. Use dd/mm/aaaa")
                return
            
            paciente = Paciente(nombre, dni, fecha_nacimiento)
            self.clinica.agregar_paciente(paciente)
            print(f"✅ Paciente {nombre} registrado exitosamente.")
            
        except Exception as e:
            print(f"❌ Error al agregar paciente: {e}")
    
    def agregar_medico(self):
        """Solicita datos del médico y lo registra en el sistema."""
        print("\n--- AGREGAR MÉDICO ---")
        try:
            nombre = input("Nombre completo: ").strip()
            if not nombre:
                print("❌ El nombre no puede estar vacío.")
                return
            
            matricula = input("Matrícula: ").strip()
            if not matricula:
                print("❌ La matrícula no puede estar vacía.")
                return
            
            medico = Medico(nombre, matricula)
            
            # Agregar especialidades
            print("\nAhora agregue las especialidades del médico:")
            while True:
                especialidad_nombre = input("Nombre de especialidad (o 'fin' para terminar): ").strip()
                if especialidad_nombre.lower() == 'fin':
                    break
                
                if not especialidad_nombre:
                    print("❌ El nombre de especialidad no puede estar vacío.")
                    continue
                
                print("Días de atención (separados por comas):")
                print("Ejemplo: lunes, miércoles, viernes")
                dias_input = input("Días: ").strip()
                
                if not dias_input:
                    print("❌ Debe especificar al menos un día.")
                    continue
                
                dias = [dia.strip().lower() for dia in dias_input.split(",")]
                dias_validos = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
                
                # Validar días
                dias_invalidos = [dia for dia in dias if dia not in dias_validos]
                if dias_invalidos:
                    print(f"❌ Días inválidos: {', '.join(dias_invalidos)}")
                    print("Use: lunes, martes, miércoles, jueves, viernes, sábado, domingo")
                    continue
                
                especialidad = Especialidad(especialidad_nombre, dias)
                medico.agregar_especialidad(especialidad)
                print(f"✅ Especialidad {especialidad_nombre} agregada.")
            
            self.clinica.agregar_medico(medico)
            print(f"✅ Médico {nombre} registrado exitosamente.")
            
        except Exception as e:
            print(f"❌ Error al agregar médico: {e}")
    
    def agendar_turno(self):
        """Solicita datos del turno y lo agenda en el sistema."""
        print("\n--- AGENDAR TURNO ---")
        try:
            dni = input("DNI del paciente: ").strip()
            if not dni:
                print("❌ El DNI no puede estar vacío.")
                return
            
            matricula = input("Matrícula del médico: ").strip()
            if not matricula:
                print("❌ La matrícula no puede estar vacía.")
                return
            
            especialidad = input("Especialidad: ").strip()
            if not especialidad:
                print("❌ La especialidad no puede estar vacía.")
                return
            
            fecha_str = input("Fecha del turno (dd/mm/aaaa): ").strip()
            if not fecha_str:
                print("❌ La fecha no puede estar vacía.")
                return
            
            hora_str = input("Hora del turno (HH:MM): ").strip()
            if not hora_str:
                print("❌ La hora no puede estar vacía.")
                return
            
            # Combinar fecha y hora
            fecha_hora_str = f"{fecha_str} {hora_str}"
            try:
                fecha_hora = datetime.strptime(fecha_hora_str, "%d/%m/%Y %H:%M")
            except ValueError:
                print("❌ Formato de fecha u hora inválido. Use dd/mm/aaaa HH:MM")
                return
            
            self.clinica.agendar_turno(dni, matricula, especialidad, fecha_hora)
            print("✅ Turno agendado exitosamente.")
            
        except PacienteNoEncontradoException as e:
            print(f"❌ {e}")
        except MedicoNoDisponibleException as e:
            print(f"❌ {e}")
        except TurnoOcupadoException as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Error al agendar turno: {e}")
    
    def agregar_especialidad_medico(self):
        """Agrega una nueva especialidad a un médico existente."""
        print("\n--- AGREGAR ESPECIALIDAD A MÉDICO ---")
        try:
            matricula = input("Matrícula del médico: ").strip()
            if not matricula:
                print("❌ La matrícula no puede estar vacía.")
                return
            
            # Verificar que el médico existe
            try:
                medico = self.clinica.obtener_medico_por_matricula(matricula)
            except Exception as e:
                print(f"❌ {e}")
                return
            
            especialidad_nombre = input("Nombre de la nueva especialidad: ").strip()
            if not especialidad_nombre:
                print("❌ El nombre de especialidad no puede estar vacío.")
                return
            
            print("Días de atención (separados por comas):")
            print("Ejemplo: lunes, miércoles, viernes")
            dias_input = input("Días: ").strip()
            
            if not dias_input:
                print("❌ Debe especificar al menos un día.")
                return
            
            dias = [dia.strip().lower() for dia in dias_input.split(",")]
            dias_validos = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
            
            # Validar días
            dias_invalidos = [dia for dia in dias if dia not in dias_validos]
            if dias_invalidos:
                print(f"❌ Días inválidos: {', '.join(dias_invalidos)}")
                print("Use: lunes, martes, miércoles, jueves, viernes, sábado, domingo")
                return
            
            especialidad = Especialidad(especialidad_nombre, dias)
            medico.agregar_especialidad(especialidad)
            print(f"✅ Especialidad {especialidad_nombre} agregada al médico exitosamente.")
            
        except Exception as e:
            print(f"❌ Error al agregar especialidad: {e}")
    
    def emitir_receta(self):
        """Solicita datos y emite una receta médica."""
        print("\n--- EMITIR RECETA ---")
        try:
            dni = input("DNI del paciente: ").strip()
            if not dni:
                print("❌ El DNI no puede estar vacío.")
                return
            
            matricula = input("Matrícula del médico: ").strip()
            if not matricula:
                print("❌ La matrícula no puede estar vacía.")
                return
            
            print("Medicamentos (separados por comas):")
            medicamentos_input = input("Medicamentos: ").strip()
            if not medicamentos_input:
                print("❌ Debe especificar al menos un medicamento.")
                return
            
            medicamentos = [med.strip() for med in medicamentos_input.split(",")]
            medicamentos = [med for med in medicamentos if med]  # Filtrar vacíos
            
            if not medicamentos:
                print("❌ Debe especificar al menos un medicamento válido.")
                return
            
            self.clinica.emitir_receta(dni, matricula, medicamentos)
            print("✅ Receta emitida exitosamente.")
            
        except PacienteNoEncontradoException as e:
            print(f"❌ {e}")
        except RecetaInvalidaException as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Error al emitir receta: {e}")
    
    def ver_historia_clinica(self):
        """Muestra la historia clínica completa de un paciente."""
        print("\n--- VER HISTORIA CLÍNICA ---")
        try:
            dni = input("DNI del paciente: ").strip()
            if not dni:
                print("❌ El DNI no puede estar vacío.")
                return
            
            historia = self.clinica.obtener_historia_clinica(dni)
            print(f"\n📋 HISTORIA CLÍNICA")
            print("-" * 50)
            print(historia)
            
        except PacienteNoEncontradoException as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Error al obtener historia clínica: {e}")
    
    def ver_todos_turnos(self):
        """Muestra todos los turnos agendados en el sistema."""
        print("\n--- TODOS LOS TURNOS ---")
        try:
            turnos = self.clinica.obtener_turnos()
            if not turnos:
                print("📅 No hay turnos agendados.")
                return
            
            print(f"\n📅 TURNOS AGENDADOS ({len(turnos)} total)")
            print("-" * 80)
            for i, turno in enumerate(turnos, 1):
                print(f"{i}. {turno}")
                print("-" * 40)
                
        except Exception as e:
            print(f"❌ Error al obtener turnos: {e}")
    
    def ver_todos_pacientes(self):
        """Muestra todos los pacientes registrados."""
        print("\n--- TODOS LOS PACIENTES ---")
        try:
            pacientes = self.clinica.obtener_pacientes()
            if not pacientes:
                print("👥 No hay pacientes registrados.")
                return
            
            print(f"\n👥 PACIENTES REGISTRADOS ({len(pacientes)} total)")
            print("-" * 60)
            for i, paciente in enumerate(pacientes, 1):
                print(f"{i}. {paciente}")
                
        except Exception as e:
            print(f"❌ Error al obtener pacientes: {e}")
    
    def ver_todos_medicos(self):
        """Muestra todos los médicos registrados."""
        print("\n--- TODOS LOS MÉDICOS ---")
        try:
            medicos = self.clinica.obtener_medicos()
            if not medicos:
                print("👨‍⚕️ No hay médicos registrados.")
                return
            
            print(f"\n👨‍⚕️ MÉDICOS REGISTRADOS ({len(medicos)} total)")
            print("-" * 70)
            for i, medico in enumerate(medicos, 1):
                print(f"{i}. {medico}")
                print()
                
        except Exception as e:
            print(f"❌ Error al obtener médicos: {e}")
    
    def pausar(self):
        """Pausa la ejecución esperando que el usuario presione Enter."""
        input("\nPresione Enter para continuar...")


def main():
    """Función principal que inicia la aplicación CLI."""
    cli = CLI()
    cli.ejecutar()


if __name__ == "__main__":
    main()