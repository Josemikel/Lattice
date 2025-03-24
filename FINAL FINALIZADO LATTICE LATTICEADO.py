import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import numpy as np
from matplotlib.gridspec import GridSpec

xfig = 14
yfig = 8

def close_window (): 
     root.quit()
     root.destroy()

def plot():
     global ax, ax2  # ax y ax2 son globales
     ax.clear()  
     ax2.clear()  # Borra lo que esté graficado en ax y ax2

     time = int(time_entry.get())  # Toma los valores de entrada de los cuadros de texto
     z2 = float(z2_entry.get())
     z3 = float(z3_entry.get())
     vo = float(vo_entry.get())
     Da = float(da_entry.get())
     Db = float(db_entry.get())
     Va = float(va_entry.get())
     Vb = float(vb_entry.get())

     vlines = [0, Da, Da + Db]  # Organiza las divisiones de los medios
     speed = [300, 100]

     dem = z2 + z3  # Calcula los coeficientes alfa y beta
     alfa21 = -1
     beta21 = 0
     alfa34 = 1
     beta34 = 2
     alfa23 = (z3 - z2) / dem
     beta23 = 2 * z3 / dem
     alfa32 = (z2 - z3) / dem
     beta32 = 2 * z2 / dem

     ylim = time  # Ajusta el tamaño del gráfico
     xlim = vlines[2] + vlines[2] / 5

     color = ["c", "r", "g"]

     ratio_fig = (yfig / ylim) / (
          xfig / xlim
     )  # Ajusta la proporción para la rotación del texto

     dist = [x - y for x, y in zip(vlines[1:], vlines[:-1])]  # Distancias entre los medios
     drop = [
          int(x / y) for x, y in zip(dist, speed)
     ]  # "Drop" o tiempo de propagación

     text_size = 7
     tiempo = drop[0]

     v_pu = 1
     trans_z1 = np.zeros(
          500
     )  # Inicializa los vectores para los datos de voltaje en cada punto
     ref_z1 = np.zeros(500)
     trans_z2 = np.zeros(500)
     ref_z2 = np.zeros(500)
     voltaje_final = np.zeros(500)
     voltaje_acum = np.zeros(500)

     trans_z1[0] = v_pu
     trans_z2[tiempo] = v_pu * beta23
     ref_z1[tiempo] = v_pu * alfa23

     while tiempo < time:
          if trans_z1[tiempo] != 0:
               if ref_z2[tiempo + drop[0] - drop[1]] == 0:
                    ref_z1[tiempo + drop[0]] = trans_z1[tiempo] * alfa23
                    trans_z2[tiempo + drop[0]] = trans_z1[tiempo] * beta23
               else:
                    temp = ref_z2[tiempo + drop[0] - drop[1]]
                    ref_z1[tiempo + drop[0]] = (trans_z1[tiempo] * alfa23) + (temp * beta32)
                    trans_z2[tiempo + drop[0]] = (trans_z1[tiempo] * beta23) + (
                         temp * alfa32
                    )

          if ref_z2[tiempo] != 0:
               if trans_z1[tiempo + drop[1] - drop[0]] == 0:
                    trans_z2[tiempo + drop[1]] = ref_z2[tiempo] * alfa32
                    ref_z1[tiempo + drop[1]] = ref_z2[tiempo] * beta32
               else:
                    temp = trans_z1[tiempo + drop[1] - drop[0]]
                    trans_z2[tiempo + drop[1]] = (ref_z2[tiempo] * alfa32) + (temp * beta23)
                    ref_z1[tiempo + drop[1]] = (ref_z2[tiempo] * beta32) + (temp * alfa23)

          if ref_z1[tiempo] != 0:
               trans_z1[tiempo + drop[0]] = ref_z1[tiempo] * alfa21

          if trans_z2[tiempo] != 0:
               ref_z2[tiempo + drop[1]] = trans_z2[tiempo] * alfa34
               voltaje_final[tiempo + drop[1]] = trans_z2[tiempo] * beta34

          tiempo = tiempo + 1

     acum = 0
     for i in range(time):
          acum = acum + voltaje_final[i]
          voltaje_acum[i] = acum

     tiempo = 0

     for i in range(len(vlines)):
          ax.axvline(
               x=vlines[i],
               color="black",
               label="axvline - full height",
               linestyle="dashed",
          )

     while tiempo < time:
          if trans_z1[tiempo] != 0:
               x0, y0 = [vlines[0], vlines[1]], [tiempo, tiempo + drop[0]]
               ax.plot(x0, y0, color=color[0])
               ax.text(vlines[0], tiempo, str(round(trans_z1[tiempo], 4)), rotation=-np.arctan(ratio_fig * (drop[0] / dist[0])) * 180 / np.pi, size=text_size)

          if ref_z1[tiempo] != 0:
               x1, y1 = [vlines[1], vlines[0]], [tiempo, tiempo + drop[0]]
               ax.plot(x1, y1, color=color[0])
               ax.text(vlines[1] - dist[0] / 10, tiempo, str(round(ref_z1[tiempo], 4)), rotation=np.arctan(ratio_fig * (drop[0] / dist[0])) * 180 / np.pi, size=text_size)

          if trans_z2[tiempo] != 0:
               x0, y0 = [vlines[1], vlines[2]], [tiempo, tiempo + drop[1]]
               ax.plot(x0, y0, color=color[1])
               ax.text((vlines[1]), tiempo, str(round(trans_z2[tiempo], 4)), rotation=-np.arctan(ratio_fig * (drop[1] / dist[1])) * 180 / np.pi, size=text_size)

          if ref_z2[tiempo] != 0:
               x1, y1 = [vlines[2], vlines[1]], [tiempo, tiempo + drop[1]]
               ax.plot(x1, y1, color=color[1])
               ax.text((vlines[2]) - dist[1] / 10, tiempo, str(round(ref_z2[tiempo], 4)), rotation=np.arctan(ratio_fig * (drop[1] / dist[1])) * 180 / np.pi, size=text_size)

          if voltaje_final[tiempo] != 0:
               x2, y2 = [vlines[2], vlines[2] + vlines[2] / 20], [tiempo, tiempo]
               ax.plot(x2, y2, color=color[2])
               ax.text(vlines[2] + vlines[2] / 20, tiempo, str(round(voltaje_final[tiempo], 4)), size=text_size)
               ax.text(vlines[2] + vlines[2] / 10, tiempo, str(round(voltaje_acum[tiempo], 4)), size=text_size)

          tiempo = tiempo + 1

     #ax.text(xlim, time/2, "Voltaje acumulado", size=10, rotation=90)
     ax.set_ylim([0, ylim])  # Configura los ejes
     ax.set_xlim([0, xlim])
     ax.invert_yaxis()
     ax.set_title("Diagrama de Lattice")
     ax.set_xlabel("Distancia (m)")
     ax.set_ylabel("Tiempo (us)")

     # Nuevo gráfico para voltaje_final y voltaje_acum vs tiempo
     ax2.plot(range(time), voltaje_final[:time], label="Voltaje Final", color="blue")
     ax2.plot(range(time), voltaje_acum[:time], label="Voltaje Acumulado", color="orange")
     ax2.set_title("Voltaje vs Tiempo")
     ax2.set_xlabel("Tiempo (us)")
     ax2.set_ylabel("Voltaje")
     ax2.legend()

     canvas.draw()  # Redibuja el lienzo para mostrar los gráficos actualizados

# Ajustar diseño
root = tk.Tk()
root.title("Simulación de Lattice")  # Agrega un título a la ventana
root.protocol("WM_DELETE_WINDOW", close_window)

# Abre la ventana en estado maximizado
root.state("zoomed")  

# Aumentar el tamaño de la figura para asegurarse de que todo encaje
xfig = 16  # Figura ligeramente más ancha
yfig = 9   # Figura ligeramente más alta

# GridSpec para personalizar el diseño de los gráficos
fig = plt.figure(figsize=(xfig, yfig))
gs = GridSpec(2, 3, figure=fig)  # Divide la figura en una cuadrícula de 2x3
ax = fig.add_subplot(gs[:, 0:2])  # El gráfico izquierdo ocupa las dos primeras columnas
ax2 = fig.add_subplot(gs[0, 2])  # El gráfico superior derecho ocupa la esquina superior derecha

# Crea un frame para los widgets dentro de la cuadrícula de matplotlib
widgets_frame = tk.Frame(root)
canvas = FigureCanvasTkAgg(fig, master=widgets_frame)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Agrega la barra de herramientas para poder hacer zoom en el gráfico
toolbar_frame = tk.Frame(master=widgets_frame)
toolbar_frame.pack(side=tk.TOP, fill=tk.X)
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
toolbar.update()

# Marco para los parámetros (widgets) dentro de la celda inferior derecha de la cuadrícula
params_frame = tk.Frame(master=canvas.get_tk_widget(), bg="lightgray", relief=tk.RAISED, bd=2)
params_frame.place(relx=0.82, rely=0.6, anchor="n")  # Mover un poco más hacia la izquierda

# título para la sección de widgets
tk.Label(params_frame, text="Parámetros", bg="lightgray", font=("Arial", 12, "bold")).grid(
row=0, column=0, columnspan=6, pady=10
)

# Entradas para los parámetros
#cada uno organizado en una fila y columna dentro del frame
tk.Label(params_frame, text="Tiempo:", bg="lightgray").grid(row=1, column=0, sticky="w", padx=5, pady=5)
time_entry = tk.Entry(params_frame)
time_entry.insert(0, "100")
time_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(params_frame, text="Vo:", bg="lightgray").grid(row=2, column=0, sticky="w", padx=5, pady=5)
vo_entry = tk.Entry(params_frame)
vo_entry.insert(0, "1")
vo_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(params_frame, text="Za:", bg="lightgray").grid(row=1, column=2, sticky="w", padx=5, pady=5)
z2_entry = tk.Entry(params_frame)
z2_entry.insert(0, "400")
z2_entry.grid(row=1, column=3, padx=5, pady=5)

tk.Label(params_frame, text="Zb:", bg="lightgray").grid(row=1, column=4, sticky="w", padx=5, pady=5)
z3_entry = tk.Entry(params_frame)
z3_entry.insert(0, "40")
z3_entry.grid(row=1, column=5, padx=5, pady=5)

tk.Label(params_frame, text="Da:", bg="lightgray").grid(row=2, column=2, sticky="w", padx=5, pady=5)
da_entry = tk.Entry(params_frame)
da_entry.insert(0, "3000")
da_entry.grid(row=2, column=3, padx=5, pady=5)

tk.Label(params_frame, text="Db:", bg="lightgray").grid(row=2, column=4, sticky="w", padx=5, pady=5)
db_entry = tk.Entry(params_frame)
db_entry.insert(0, "100")
db_entry.grid(row=2, column=5, padx=5, pady=5)

tk.Label(params_frame, text="Va:", bg="lightgray").grid(row=3, column=2, sticky="w", padx=5, pady=5)
va_entry = tk.Entry(params_frame)
va_entry.insert(0, "300")
va_entry.grid(row=3, column=3, padx=5, pady=5)

tk.Label(params_frame, text="Vb:", bg="lightgray").grid(row=3, column=4, sticky="w", padx=5, pady=5)
vb_entry = tk.Entry(params_frame)
vb_entry.insert(0, "100")
vb_entry.grid(row=3, column=5, padx=5, pady=5)

# Botón de ejecutar
tk.Button(params_frame, text="Ejecutar", command=plot, height=2, width=20, bg="lightblue", font=("Arial", 10, "bold")).grid(
row=4, column=0, columnspan=6, pady=10
)

# Empaquetar el marco de widgets
widgets_frame.pack(fill=tk.BOTH, expand=True)

#la ventana de Tkinter cambia de tamaño dinámicamente para ajustar todos los elementos
root.geometry(f"{int(xfig * 80)}x{int(yfig * 80)}")  # Establece dinámicamente el tamaño de la ventana basado en el tamaño de la figura
root.minsize(1200, 800)  # Establece un tamaño mínimo para evitar que se corten elementos

root.mainloop()