import rebound
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from datetime import datetime, timedelta


#EN ESTE CÓDIGO EL USUARIO PODRÁ VISUALIZAR LA EVOLUCION DE LA PRIMERA SIMULACIÓN PROPUESTA MEDIANTE UN VIDEO, DONDE PARTICIPA LA PARTICULA, EL SOL Y JÚPITER (MASA NORMAL)


print("Nota: Escriba a continuación 'L4' o 'L5' ")
eleccion_L4_L5 = input("Elija ver L4 o L5 en el sistema: ")
print("Nota: Escriba a continuación el tiempo en números enteros positivos ")
pasos_tiempo = int(input("Introduzca el tiempo en años: "))

# Crear la simulación
sim = rebound.Simulation()

# Definir las unidades de la simulación (antes de añadir las partículas)
sim.units = ('AU', 'yr', 'Msun')

# Parámetros del sistema
m_sun = 1.0          # Masa del Sol en masas solares
m_jupiter = 0.0009543 # Masa de Júpiter en masas solares
m_particula = 1e-15   # Masa de la partícula (despreciable)
r_jupiter = 5.2       # Distancia de Júpiter al Sol en AU
G = 4 * np.pi**2      # Constante gravitacional en AU^3 / (yr^2 M_sol)

# Añadir el Sol
sim.add(m=m_sun)

# Añadir Júpiter
sim.add(m=m_jupiter, a=r_jupiter)

# Velocidad angular de Júpiter
omega = np.sqrt(G * m_sun / r_jupiter**3)  # Omega en radianes por año

# Posición de la partícula en L4 o L5 (coordenadas x, y respecto al Sol)
if eleccion_L4_L5 == "L4":
    x_L4 = r_jupiter * np.cos(np.pi/3)  # 60 grados = pi/3 radianes
    y_L4 = r_jupiter * np.sin(np.pi/3)

    # Velocidades iniciales para la partícula en L4
    v_L4 = omega * r_jupiter  # Velocidad tangencial
    vx_L4 = -v_L4 * np.sin(np.pi/3)  # Componente en x
    vy_L4 = v_L4 * np.cos(np.pi/3)   # Componente en y

elif eleccion_L4_L5 == "L5":
    x_L4 = r_jupiter * np.cos(-np.pi/3)  # -60 grados = -pi/3 radianes
    y_L4 = r_jupiter * np.sin(-np.pi/3)

    # Velocidades iniciales para la partícula en L5
    v_L4 = omega * r_jupiter  # Velocidad tangencial
    vx_L4 = -v_L4 * np.sin(-np.pi/3)  # Componente en x
    vy_L4 = v_L4 * np.cos(-np.pi/3)   # Componente en y

# Añadir la partícula
sim.add(m=m_particula, x=x_L4, y=y_L4, vx=vx_L4, vy=vy_L4)

# Configurar la figura para la animación
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-6, 6)  # Limitar las dimensiones del gráfico
ax.set_ylim(-6, 6)
ax.set_xlabel('Posición X (AU)')
ax.set_ylabel('Posición Y (AU)')
ax.set_title(f'Evolución de las Órbitas de Júpiter y Partícula en L{4 if eleccion_L4_L5 == "L4" else 5}')
ax.grid(True)

# Añadir un objeto de texto para mostrar la fecha en la animación
date_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=10, verticalalignment='top')

# Inicialización de los objetos de la animación
jupiter_line, = ax.plot([], [], 'r-', label='Órbita de Júpiter')
particle_line, = ax.plot([], [], 'b-', label=f"Órbita de Partícula L{4 if eleccion_L4_L5 == 'L4' else 5}")
sun_scatter = ax.scatter(0, 0, color='yellow', label='Sol')  # Sol en el centro
jupiter_scatter = ax.scatter([], [], color='red', s=50)  # Punto para Júpiter
particle_scatter = ax.scatter([], [], color='blue', s=50)  # Punto para la partícula

ax.legend()

# Listas para almacenar las posiciones
jupiter_x_positions = []
jupiter_y_positions = []
particle_x_positions = []
particle_y_positions = []

# Parámetros de la animación
frames = 100  # Número total de frames
total_time = pasos_tiempo  # Tiempo total en años
time_per_frame = total_time / frames  # Tiempo que avanza por cada frame

# Función de inicialización para la animación
def init():
    jupiter_line.set_data([], [])
    particle_line.set_data([], [])
    jupiter_scatter.set_offsets(np.array([[], []]).T)
    particle_scatter.set_offsets(np.array([[], []]).T)
    date_text.set_text('')  # Inicializar el texto de la fecha
    return jupiter_line, particle_line, jupiter_scatter, particle_scatter, date_text

# Función de actualización para cada frame de la animación
def update(frame):
    sim.integrate(sim.t + time_per_frame)  # Integrar el tiempo correspondiente por frame
    
    jupiter = sim.particles[1]  # Índice 1 para Júpiter
    particle = sim.particles[2]  # Índice 2 para la partícula en L4/L5
    
    # Guardar posiciones
    jupiter_x_positions.append(jupiter.x)
    jupiter_y_positions.append(jupiter.y)
    particle_x_positions.append(particle.x)
    particle_y_positions.append(particle.y)
    
    # Actualizar datos de la línea y el punto
    jupiter_line.set_data(jupiter_x_positions, jupiter_y_positions)
    particle_line.set_data(particle_x_positions, particle_y_positions)
    jupiter_scatter.set_offsets([jupiter.x, jupiter.y])
    particle_scatter.set_offsets([particle.x, particle.y])
    
    # Actualizar el texto de la fecha
    current_date = frame * time_per_frame  # Calcular el tiempo actual en años
    date_text.set_text(f'Tiempo: {current_date:.2f} años')
    
    return jupiter_line, particle_line, jupiter_scatter, particle_scatter, date_text

# Crear la animación
ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, repeat=False, interval=100)

# Mostrar la animación
plt.show()

