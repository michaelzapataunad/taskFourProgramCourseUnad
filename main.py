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

class Client(Entity):
    """
    Clase que representa un cliente del sistema.
    Implementa validaciones robustas para los datos personales (nombre, email, teléfono).
    Demuestra encapsulación de datos mediante propiedades y validaciones estrictas.
    """

    def __init__(self, client_id, name, email, phone):
        """
        Inicializa un cliente con validaciones de datos.
        
        Args:
            client_id: Identificador único del cliente.
            name: Nombre completo del cliente (mínimo 3 caracteres, sin números).
            email: Correo electrónico válido.
            phone: Número de teléfono (mínimo 10 dígitos).
        
        Raises:
            ValidationError: Si alguno de los datos no cumple con las validaciones.
        """
        super().__init__(client_id)
        self.__name = None
        self.__email = None
        self.__phone = None

        self.name = name
        self.email = email
        self.phone = phone

    @property
    def name(self):
        """Obtiene el nombre del cliente."""
        return self.__name

    @name.setter
    def name(self, value):
        """Valida que el nombre no esté vacío y tenga una longitud mínima."""
        if not value or len(value.strip()) < 3:
            raise ValidationError("Client name must contain at least 3 characters.")
        self.__name = value.strip()

    @property
    def email(self):
        """Obtiene el correo del cliente."""
        return self.__email

    @email.setter
    def email(self, value):
        """Valida que el correo tenga un formato básico correcto."""
        if not value or "@" not in value or "." not in value:
            raise ValidationError("Client email is invalid.")
        self.__email = value.strip()

    @property
    def phone(self):
        """Obtiene el teléfono del cliente."""
        return self.__phone

    @phone.setter
    def phone(self, value):
        """Valida que el teléfono sea numérico y tenga al menos 7 dígitos."""
        if not value or not value.isdigit() or len(value) < 7:
            raise ValidationError("Client phone must be numeric and contain at least 7 digits.")
        self.__phone = value.strip()

    def get_summary(self):
        """Retorna un resumen legible del cliente."""
        return f"#{self.entity_id} - {self.name} | {self.email} | {self.phone}"
        
# ==============================
# APORTE FIN - Luz Yomaira Moreno
# ==============================


# ==============================

# APORTE INICIO - Luz Yomaira Moreno Viveros

# Rol: Clase abstracta Service y servicios derivados RoomBookingService y EquipmentRentalService.

# ==============================

class Service(Entity, ABC):

    """

    Clase abstracta Servicio.

    Define la estructura común de todos los servicios ofrecidos por Software FJ.

    """

 

    def __init__(self, entity_id, name, base_price, available=True):

        super().__init__(entity_id)

        self._name = name

        self._base_price = float(base_price)

        self._available = available

 

    @property

    def name(self):

        return self._name

 

    @property

    def base_price(self):

        return self._base_price

 

    @property

    def available(self):

        return self._available

 

    @abstractmethod

    def calculate_cost(self, duration, tax=0.0, discount=0.0):

        """

        Método con parámetros opcionales que simula sobrecarga.

        Permite calcular costo con impuestos, descuentos o sin ellos.

        """

        pass

 

    @abstractmethod

    def describe_service(self):

        """Describe el servicio especializado."""

        pass

 

    @abstractmethod

    def validate_parameters(self):

        """Valida parámetros propios del servicio especializado."""

        pass

 

    def get_summary(self):

        """Resumen general del servicio."""

        return f"#{self.entity_id} - {self.name} | Base price: ${self.base_price:,.2f}"

 

 

class RoomBookingService(Service):

    """Servicio especializado para reservas de salas."""

 

    def __init__(self, entity_id, name, base_price, room_capacity):

        super().__init__(entity_id, name, base_price)

        self.room_capacity = int(room_capacity)

 

    def validate_parameters(self):

        """Valida que la sala tenga capacidad positiva y precio válido."""

        if self.base_price <= 0:

            raise ValidationError("Room service base price must be greater than zero.")

        if self.room_capacity <= 0:

            raise ValidationError("Room capacity must be greater than zero.")

 

    def calculate_cost(self, duration, tax=0.0, discount=0.0):

        """Calcula el costo por duración, aplicando impuesto y descuento opcional."""

        subtotal = self.base_price * duration

        return subtotal + (subtotal * tax) - discount

 

    def describe_service(self):

        """Descripción polimórfica del servicio de sala."""

        return f"Room booking for up to {self.room_capacity} people."

 

 

class EquipmentRentalService(Service):

    """Servicio especializado para alquiler de equipos."""

 

    def __init__(self, entity_id, name, base_price, equipment_quantity):

        super().__init__(entity_id, name, base_price)

        self.equipment_quantity = int(equipment_quantity)

 

    def validate_parameters(self):

        """Valida cantidad de equipos y precio."""

        if self.base_price <= 0:

            raise ValidationError("Equipment rental price must be greater than zero.")

        if self.equipment_quantity <= 0:

            raise ValidationError("Equipment quantity must be greater than zero.")

 

    def calculate_cost(self, duration, tax=0.0, discount=0.0):

        """Calcula costo considerando duración y cantidad de equipos."""

        subtotal = self.base_price * duration * self.equipment_quantity

        return subtotal + (subtotal * tax) - discount

 

    def describe_service(self):

        """Descripción polimórfica del alquiler de equipos."""

        return f"Equipment rental including {self.equipment_quantity} item(s)."

# ==============================

# APORTE FIN - Luz Yomaira Moreno Viveros 

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

 

class SoftwareFJApp:

    """Aplicación gráfica principal desarrollada con Tkinter."""

 

    def __init__(self, root):

        self.root = root

        self.root.title("Software FJ - Client, Service and Reservation Management")

        self.root.geometry("1100x700")

        self.root.configure(bg="#f4f7fb")

 

        self.manager = SystemManager()

 

        self.create_styles()

        self.create_widgets()

        self.load_initial_services()

 

    def create_styles(self):

        """Configura estilos visuales básicos para la interfaz."""

        style = ttk.Style()

        style.theme_use("clam")

        style.configure("TButton", padding=6, font=("Arial", 10))

        style.configure("TLabel", background="#f4f7fb", font=("Arial", 10))

        style.configure("Title.TLabel", font=("Arial", 18, "bold"), background="#f4f7fb")

        style.configure("TNotebook", background="#f4f7fb")

        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

 

    def create_widgets(self):

        """Crea todos los elementos gráficos de la aplicación."""

        title = ttk.Label(

            self.root,

            text="Software FJ Management System",

            style="Title.TLabel"

        )

        title.pack(pady=10)

 

        self.notebook = ttk.Notebook(self.root)

        self.notebook.pack(fill="both", expand=True, padx=15, pady=10)

 

        self.client_tab = ttk.Frame(self.notebook)

        self.service_tab = ttk.Frame(self.notebook)

        self.reservation_tab = ttk.Frame(self.notebook)

        self.simulation_tab = ttk.Frame(self.notebook)

 

        self.notebook.add(self.client_tab, text="Clients")

        self.notebook.add(self.service_tab, text="Services")

        self.notebook.add(self.reservation_tab, text="Reservations")

        self.notebook.add(self.simulation_tab, text="Simulation")

 

        self.build_client_tab()

        self.build_service_tab()

        self.build_reservation_tab()

        self.build_simulation_tab()

 

    def build_client_tab(self):

        """Construye la pestaña de clientes."""

        form = ttk.LabelFrame(self.client_tab, text="Register Client")

        form.pack(fill="x", padx=20, pady=15)

 

        ttk.Label(form, text="Name:").grid(row=0, column=0, padx=8, pady=8)

        ttk.Label(form, text="Email:").grid(row=0, column=2, padx=8, pady=8)

        ttk.Label(form, text="Phone:").grid(row=0, column=4, padx=8, pady=8)

 

        self.client_name = ttk.Entry(form, width=25)

        self.client_email = ttk.Entry(form, width=25)

        self.client_phone = ttk.Entry(form, width=18)

 

        self.client_name.grid(row=0, column=1, padx=8, pady=8)

        self.client_email.grid(row=0, column=3, padx=8, pady=8)

        self.client_phone.grid(row=0, column=5, padx=8, pady=8)

 

        ttk.Button(form, text="Add Client", command=self.add_client_ui).grid(row=0, column=6, padx=8)

 

        self.client_tree = ttk.Treeview(

            self.client_tab,

            columns=("id", "name", "email", "phone"),

            show="headings"

        )

        self.client_tree.heading("id", text="ID")

        self.client_tree.heading("name", text="Name")

        self.client_tree.heading("email", text="Email")

        self.client_tree.heading("phone", text="Phone")

        self.client_tree.pack(fill="both", expand=True, padx=20, pady=10)

 

    def build_service_tab(self):

        """Construye la pestaña de servicios."""

        form = ttk.LabelFrame(self.service_tab, text="Create Service")

        form.pack(fill="x", padx=20, pady=15)

 

        ttk.Label(form, text="Type:").grid(row=0, column=0, padx=8, pady=8)

        ttk.Label(form, text="Name:").grid(row=0, column=2, padx=8, pady=8)

        ttk.Label(form, text="Base Price:").grid(row=0, column=4, padx=8, pady=8)

        ttk.Label(form, text="Extra Value:").grid(row=0, column=6, padx=8, pady=8)

 

        self.service_type = ttk.Combobox(

            form,

            values=["Room Booking", "Equipment Rental", "Specialized Consulting"],

            state="readonly",

            width=22

        )

        self.service_type.set("Room Booking")

        self.service_name = ttk.Entry(form, width=22)

        self.service_price = ttk.Entry(form, width=12)

        self.service_extra = ttk.Entry(form, width=12)

 

        self.service_type.grid(row=0, column=1, padx=8, pady=8)

        self.service_name.grid(row=0, column=3, padx=8, pady=8)

        self.service_price.grid(row=0, column=5, padx=8, pady=8)

        self.service_extra.grid(row=0, column=7, padx=8, pady=8)

 

        ttk.Button(form, text="Add Service", command=self.add_service_ui).grid(row=0, column=8, padx=8)

 

        self.service_tree = ttk.Treeview(

            self.service_tab,

            columns=("id", "type", "name", "price", "description"),

            show="headings"

        )

        self.service_tree.heading("id", text="ID")

        self.service_tree.heading("type", text="Type")

        self.service_tree.heading("name", text="Name")

        self.service_tree.heading("price", text="Base Price")

        self.service_tree.heading("description", text="Description")

        self.service_tree.pack(fill="both", expand=True, padx=20, pady=10)

 

    def build_reservation_tab(self):

        """Construye la pestaña de reservas."""

        form = ttk.LabelFrame(self.reservation_tab, text="Create Reservation")

        form.pack(fill="x", padx=20, pady=15)

 

        ttk.Label(form, text="Client:").grid(row=0, column=0, padx=8, pady=8)

        ttk.Label(form, text="Service:").grid(row=0, column=2, padx=8, pady=8)

        ttk.Label(form, text="Duration:").grid(row=0, column=4, padx=8, pady=8)

 

        self.client_combo = ttk.Combobox(form, state="readonly", width=30)

        self.service_combo = ttk.Combobox(form, state="readonly", width=35)

        self.duration_entry = ttk.Entry(form, width=10)

 

        self.client_combo.grid(row=0, column=1, padx=8, pady=8)

        self.service_combo.grid(row=0, column=3, padx=8, pady=8)

        self.duration_entry.grid(row=0, column=5, padx=8, pady=8)

 

        ttk.Button(form, text="Create Reservation", command=self.add_reservation_ui).grid(row=0, column=6, padx=8)

 

        self.reservation_tree = ttk.Treeview(

            self.reservation_tab,

            columns=("id", "client", "service", "duration", "status", "total"),

            show="headings"

        )

        self.reservation_tree.heading("id", text="ID")

        self.reservation_tree.heading("client", text="Client")

        self.reservation_tree.heading("service", text="Service")

        self.reservation_tree.heading("duration", text="Duration")

        self.reservation_tree.heading("status", text="Status")

        self.reservation_tree.heading("total", text="Total Cost")

        self.reservation_tree.pack(fill="both", expand=True, padx=20, pady=10)

 

    def build_simulation_tab(self):

        """Construye la pestaña para simular mínimo 10 operaciones completas."""

        info = ttk.Label(

            self.simulation_tab,

            text="Run a controlled simulation with valid and invalid operations.",

            font=("Arial", 11)

        )

        info.pack(pady=15)

 

        ttk.Button(

            self.simulation_tab,

            text="Run 10 Operations Simulation",

            command=self.run_simulation

        ).pack(pady=5)

 

        self.simulation_output = tk.Text(self.simulation_tab, height=25, width=120)

        self.simulation_output.pack(padx=20, pady=15, fill="both", expand=True)

 

    def load_initial_services(self):

        """Carga servicios iniciales válidos para facilitar la prueba del sistema."""

        examples = [

            ("Room Booking", "Executive Meeting Room", 45000, 12),

            ("Equipment Rental", "Laptop Rental", 25000, 2),

            ("Specialized Consulting", "Software Architecture Advice", 80000, 4)

        ]

 

        for service_type, name, price, extra in examples:

            try:

                self.manager.add_service(service_type, name, price, extra)

            except SoftwareFJException:

                pass

 

        self.refresh_all_tables()

 

    def add_client_ui(self):

        """Evento gráfico para registrar clientes desde la interfaz."""

        try:

            self.manager.add_client(

                self.client_name.get(),

                self.client_email.get(),

                self.client_phone.get()

            )

        except SoftwareFJException as error:

            messagebox.showerror("Error", str(error))

        else:

            messagebox.showinfo("Success", "Client registered successfully.")

            self.client_name.delete(0, tk.END)

            self.client_email.delete(0, tk.END)

            self.client_phone.delete(0, tk.END)

            self.refresh_all_tables()

 

    def add_service_ui(self):

        """Evento gráfico para crear servicios desde la interfaz."""

        try:

            self.manager.add_service(

                self.service_type.get(),

                self.service_name.get(),

                self.service_price.get(),

                self.service_extra.get()

            )

        except ValueError as error:

            logging.error(f"Invalid numeric value: {error}")

            messagebox.showerror("Error", "Base Price and Extra Value must be numeric.")

        except SoftwareFJException as error:

            messagebox.showerror("Error", str(error))

        else:

            messagebox.showinfo("Success", "Service created successfully.")

            self.service_name.delete(0, tk.END)

            self.service_price.delete(0, tk.END)

            self.service_extra.delete(0, tk.END)

            self.refresh_all_tables()

 

    def add_reservation_ui(self):

        """Evento gráfico para crear reservas desde la interfaz."""

        try:

            client_index = self.client_combo.current()

            service_index = self.service_combo.current()

 

            if client_index < 0 or service_index < 0:

                raise ReservationError("Please select a client and a service.")

 

            self.manager.add_reservation(

                self.manager.clients[client_index],

                self.manager.services[service_index],

                self.duration_entry.get()

            )

        except ValueError as error:

            logging.error(f"Invalid duration value: {error}")

            messagebox.showerror("Error", "Duration must be a numeric value.")

        except SoftwareFJException as error:

            messagebox.showerror("Error", str(error))

        else:

            messagebox.showinfo("Success", "Reservation created successfully.")

            self.duration_entry.delete(0, tk.END)

            self.refresh_all_tables()

 

    def refresh_all_tables(self):

        """Actualiza tablas y listas desplegables."""

        self.refresh_clients()

        self.refresh_services()

        self.refresh_reservations()

 

        self.client_combo["values"] = [client.get_summary() for client in self.manager.clients]

        self.service_combo["values"] = [service.get_summary() for service in self.manager.services]

 

    def refresh_clients(self):

        """Actualiza la tabla de clientes."""

        for item in self.client_tree.get_children():

            self.client_tree.delete(item)

 

        for client in self.manager.clients:

            self.client_tree.insert("", tk.END, values=(client.entity_id, client.name, client.email, client.phone))

 

    def refresh_services(self):

        """Actualiza la tabla de servicios."""

        for item in self.service_tree.get_children():

            self.service_tree.delete(item)

 

        for service in self.manager.services:

            self.service_tree.insert(

                "",

                tk.END,

                values=(

                    service.entity_id,

                    service.__class__.__name__,

                    service.name,

                    f"${service.base_price:,.2f}",

                    service.describe_service()

                )

            )

 

    def refresh_reservations(self):

        """Actualiza la tabla de reservas."""

        for item in self.reservation_tree.get_children():

            self.reservation_tree.delete(item)

 

        for reservation in self.manager.reservations:

            self.reservation_tree.insert(

                "",

                tk.END,

                values=(

                    reservation.entity_id,

                    reservation.client.name,

                    reservation.service.name,

                    reservation.duration,

                    reservation.status,

                    f"${reservation.total_cost:,.2f}"

                )

            )

 

    def write_simulation_line(self, text):

        """Escribe una línea en la salida de simulación."""

        self.simulation_output.insert(tk.END, text + "\n")

        self.simulation_output.see(tk.END)

 

    def run_simulation(self):

        """

        Ejecuta mínimo 10 operaciones completas.

        Incluye operaciones válidas e inválidas para demostrar la continuidad del sistema.

        """

        self.simulation_output.delete("1.0", tk.END)

        self.write_simulation_line("Starting simulation...")

 

        operations = [

            ("Valid client registration", lambda: self.manager.add_client("Michael Zapata", "michael@email.com", "3001234567")),

            ("Invalid client registration", lambda: self.manager.add_client("Lu", "bad-email", "abc")),

            ("Valid client registration", lambda: self.manager.add_client("Luz Yomaira Moreno", "luz@email.com", "3011234567")),

            ("Valid room service", lambda: self.manager.add_service("Room Booking", "Training Room", 60000, 20)),

            ("Invalid room service", lambda: self.manager.add_service("Room Booking", "Broken Room", -100, 0)),

            ("Valid equipment service", lambda: self.manager.add_service("Equipment Rental", "Video Beam Rental", 30000, 1)),

            ("Invalid consulting service", lambda: self.manager.add_service("Specialized Consulting", "Invalid Consulting", 50000, 9)),

            ("Successful reservation", lambda: self.manager.add_reservation(self.manager.clients[0], self.manager.services[0], 2)),

            ("Failed reservation by invalid duration", lambda: self.manager.add_reservation(self.manager.clients[0], self.manager.services[0], 0)),

            ("Successful reservation with tax calculation", lambda: self.manager.add_reservation(self.manager.clients[-1], self.manager.services[-1], 3)),

        ]

 

        for number, (description, operation) in enumerate(operations, start=1):

            try:

                result = operation()

            except Exception as error:

                # El error se captura para que el programa continúe estable.

                logging.error(f"Simulation operation {number} failed: {error}")

                self.write_simulation_line(f"Operation {number}: {description} -> ERROR: {error}")

            else:

                self.write_simulation_line(f"Operation {number}: {description} -> OK: {result.get_summary()}")

            finally:

                logging.info(f"Simulation operation {number} finished.")

 

        self.refresh_all_tables()

        self.write_simulation_line("Simulation finished. Check software_fj_logs.txt for logs.")

 

 

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
