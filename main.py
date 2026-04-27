"""
Proyecto: Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas
Curso: Programación - UNAD
Lenguaje: Python
Interfaz gráfica: Tkinter

IMPORTANTE:
- Toda la interfaz gráfica está en inglés, como solicita la actividad.
- Los comentarios y explicaciones del código están en español.
- El sistema no usa base de datos; trabaja con objetos y listas internas.
- Se usa archivo de logs para registrar eventos y errores.
"""

# ==============================
# APORTE INICIO - Michael Zapata
# Rol: Integración general, ventana principal, estructura base, gestor del sistema y ejecución.
# ==============================

import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
from datetime import datetime
import logging


# Configuración del archivo de logs.
# Este archivo registra eventos relevantes y errores controlados del sistema.
logging.basicConfig(
    filename="software_fj_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class SoftwareFJException(Exception):
    """Excepción base personalizada para errores del sistema Software FJ."""
    pass


class ValidationError(SoftwareFJException):
    """Excepción personalizada para errores de validación de datos."""
    pass


class ServiceUnavailableError(SoftwareFJException):
    """Excepción personalizada para servicios no disponibles."""
    pass


class ReservationError(SoftwareFJException):
    """Excepción personalizada para errores relacionados con reservas."""
    pass


class Entity(ABC):
    """
    Clase abstracta general.
    Representa una entidad base del sistema y obliga a implementar el método get_summary.
    """

    def __init__(self, entity_id):
        self._entity_id = entity_id

    @property
    def entity_id(self):
        """Encapsulación del identificador de la entidad."""
        return self._entity_id

    @abstractmethod
    def get_summary(self):
        """Método abstracto que debe ser implementado por las clases derivadas."""
        pass


class SystemManager:
    """
    Clase gestora del sistema.
    Administra listas internas de clientes, servicios y reservas sin usar base de datos.
    """

    def __init__(self):
        self.clients = []
        self.services = []
        self.reservations = []
        self.next_client_id = 1
        self.next_service_id = 1
        self.next_reservation_id = 1

    def add_client(self, name, email, phone):
        """
        Registra un cliente válido en la lista interna.
        Usa try/except/else/finally para demostrar manejo robusto de excepciones.
        """
        try:
            client = Client(self.next_client_id, name, email, phone)
        except ValidationError as error:
            logging.error(f"Client registration failed: {error}")
            raise
        else:
            self.clients.append(client)
            self.next_client_id += 1
            logging.info(f"Client registered: {client.get_summary()}")
            return client
        finally:
            logging.info("Client registration process finished.")

    def add_service(self, service_type, name, base_price, extra_value=0):
        """
        Crea servicios especializados de acuerdo con el tipo seleccionado.
        Aplica polimorfismo porque cada servicio calcula costos y descripciones diferente.
        """
        try:
            if service_type == "Room Booking":
                service = RoomBookingService(self.next_service_id, name, base_price, extra_value)
            elif service_type == "Equipment Rental":
                service = EquipmentRentalService(self.next_service_id, name, base_price, extra_value)
            elif service_type == "Specialized Consulting":
                service = SpecializedConsultingService(self.next_service_id, name, base_price, extra_value)
            else:
                raise ValidationError("Invalid service type selected.")

            service.validate_parameters()
        except SoftwareFJException as error:
            logging.error(f"Service creation failed: {error}")
            raise
        else:
            self.services.append(service)
            self.next_service_id += 1
            logging.info(f"Service created: {service.get_summary()}")
            return service
        finally:
            logging.info("Service creation process finished.")

    def add_reservation(self, client, service, duration):
        """Crea una reserva integrando cliente, servicio, duración y estado."""
        try:
            reservation = Reservation(self.next_reservation_id, client, service, duration)
            reservation.process()
        except ReservationError as error:
            logging.error(f"Reservation failed: {error}")
            raise
        else:
            self.reservations.append(reservation)
            self.next_reservation_id += 1
            logging.info(f"Reservation created: {reservation.get_summary()}")
            return reservation
        finally:
            logging.info("Reservation process finished.")


# ==============================
# APORTE FIN - Michael Zapata
# ==============================


# ==============================
# APORTE INICIO - Luz Yomaira Moreno
# Rol: Clase Cliente, validaciones robustas y encapsulación de datos personales.
# ==============================

# ==============================
# APORTE FIN - Luz Yomaira Moreno
# ==============================


# ==============================
# APORTE INICIO - Juan Rodriguez
# Rol: Clase abstracta Service y servicios derivados RoomBookingService y EquipmentRentalService.
# ==============================

# ==============================
# APORTE FIN - Juan Rodriguez
# ==============================


# ==============================
# APORTE INICIO - Luis Carlos Salas
# Rol: Servicio SpecializedConsultingService y clase Reservation con confirmación/cancelación/procesamiento.
# ==============================

# ==============================
# APORTE FIN - Luis Carlos Salas
# ==============================


# ==============================
# APORTE INICIO - Nicolas Valencia
# Rol: Interfaz gráfica Tkinter, simulación de operaciones y conexión visual con el sistema.
# ==============================

# ==============================
# APORTE FIN - Nicolas Valencia
# ==============================


# ==============================
# APORTE INICIO - Michael Zapata
# Rol: Punto de entrada del programa y ejecución final del proyecto.
# ==============================

def main():
    """Función principal que inicializa la ventana Tkinter."""
    root = tk.Tk()
    app = SoftwareFJApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# ==============================
# APORTE FIN - Michael Zapata
# ==============================