#!/usr/bin/env python3
"""
Punto de entrada principal del Sistema de Gestión de Clínica.
Ejecuta la interfaz de línea de comandos (CLI).
"""

import sys
import os

# Agregar el directorio actual al path para las importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.interfaz.cli import CLI


def main():
    """
    Función principal que inicia el sistema de gestión de clínica.
    """
    print("Iniciando Sistema de Gestión de Clínica...")
    print("=" * 50)
    
    try:
        # Crear e iniciar la interfaz CLI
        cli = CLI()
        cli.ejecutar()
        
    except KeyboardInterrupt:
        print("\n\n¡Sistema cerrado por el usuario!")
    except Exception as e:
        print(f"\n❌ Error crítico al iniciar el sistema: {e}")
        print("Por favor, verifique que todos los archivos del modelo estén presentes.")
        sys.exit(1)


if __name__ == "__main__":
    main()