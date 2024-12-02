from tkinter import *
from tkinter import ttk, simpledialog
import cv2
import os
import numpy as np
import ttkthemes
from deepface import DeepFace

# Función para registrar un nuevo usuario con fotos y contraseña
def registrar_usuario():
    # Crear ventana de registro
    ventana_registro = Toplevel(pantalla)
    ventana_registro.geometry("400x300")
    ventana_registro.title("Registrar Usuario")
    
    # Aplicar tema con ttkthemes
    style = ttkthemes.ThemedStyle(ventana_registro)
    style.set_theme("arc")

    # Labels y campos de entrada para el registro
    Label(ventana_registro, text="Nombre de Usuario:", font=("Helvetica", 12)).pack(pady=10)
    entrada_usuario = Entry(ventana_registro, font=("Helvetica", 12), width=25)
    entrada_usuario.pack(pady=10)

    Label(ventana_registro, text="Contraseña:", font=("Helvetica", 12)).pack(pady=10)
    entrada_contraseña = Entry(ventana_registro, font=("Helvetica", 12), show="*", width=25)
    entrada_contraseña.pack(pady=10)

    # Función para capturar la foto y registrar al usuario
    def registrar_con_foto():
        usuario_nombre = entrada_usuario.get()
        contraseña = entrada_contraseña.get()

        if not usuario_nombre or not contraseña:
            mostrar_notificacion("Por favor complete todos los campos", "#e74c3c")
            return

        os.makedirs(f"usuarios/{usuario_nombre}", exist_ok=True)

        # Iniciar captura de imágenes
        cap = cv2.VideoCapture(0)
        detector = DeepFace

        fotos_capturadas = 0
        while fotos_capturadas < 3:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            cv2.imshow(f'Registro Facial ({fotos_capturadas+1}/3)', frame)

            if cv2.waitKey(1) == 27:  # Captura foto con "Esc"
                ruta_foto = f"usuarios/{usuario_nombre}/foto_{fotos_capturadas+1}.jpg"
                cv2.imwrite(ruta_foto, frame)

                fotos_capturadas += 1
                mostrar_notificacion(f"Foto {fotos_capturadas}/3 guardada", "#2ecc71")

        mostrar_notificacion(f"Usuario {usuario_nombre} registrado con éxito", "#2ecc71")
        cap.release()
        cv2.destroyAllWindows()

        # Cerrar la ventana de registro después de guardar los datos
        ventana_registro.destroy()

    # Botón para iniciar el registro con la foto
    ttk.Button(ventana_registro, text="Registrar con Reconocimiento Facial", command=registrar_con_foto).pack(pady=20)

# Función para mostrar notificaciones en la interfaz
def mostrar_notificacion(mensaje, color):
    notificacion = Toplevel(pantalla)
    notificacion.geometry("300x100")
    notificacion.title("Notificación")
    notificacion.config(bg=color)
    
    # Aplicando estilo con ttkthemes en la ventana de notificación
    style = ttkthemes.ThemedStyle(notificacion)
    style.set_theme("arc")
    style.configure('Card.TFrame', background='white')

    # Etiqueta para mostrar el mensaje
    Label(notificacion, 
          text=mensaje, 
          fg="white", 
          bg=color, 
          font=("Helvetica", 12, "bold")).pack(pady=30)

    notificacion.after(2000, notificacion.destroy)

# Función para la pantalla principal
def pantalla_principal():
    global pantalla
    pantalla = Tk()
    pantalla.geometry("800x600")
    pantalla.title("Sistema de Registro e Inicio Facial")
    pantalla.configure(bg='#f5f6fa')

    # Estilo con ttkthemes
    style = ttkthemes.ThemedStyle(pantalla)
    style.set_theme("arc")

    style.configure('Card.TFrame', background='white')
    style.configure('Accent.TButton', font=("Helvetica", 11), padding=10)

    main_frame = ttk.Frame(pantalla, style='Card.TFrame')
    main_frame.pack(expand=True, pady=50, padx=50)

    # Logo y título
    title_frame = ttk.Frame(main_frame, style='Card.TFrame')
    title_frame.pack(pady=30)

    Label(title_frame, 
          text="SISTEMA DE REGISTRO E INICIO FACIAL", 
          font=("Helvetica", 24, "bold"),
          bg='white',
          fg='#2c3e50').pack()

    Label(title_frame,
          text="Autenticación usando Reconocimiento Facial",
          font=("Helvetica", 12),
          bg='white',
          fg='#7f8c8d').pack(pady=10)

    # Botones
    button_frame = ttk.Frame(main_frame, style='Card.TFrame')
    button_frame.pack(pady=30)

    ttk.Button(button_frame, text="REGISTRAR USUARIO", style='Accent.TButton', command=registrar_usuario).pack(pady=20, ipadx=30)
    ttk.Button(button_frame, text="INICIAR SESIÓN", style='Accent.TButton').pack(pady=20, ipadx=30)

    # Footer
    footer_frame = ttk.Frame(main_frame, style='Card.TFrame')
    footer_frame.pack(pady=30)

    Label(footer_frame, text="© 2024 Sistema de Inicio Facial", font=("Helvetica", 9), bg='white', fg='#95a5a6').pack()

    pantalla.mainloop()

# Iniciar la aplicación
if __name__ == "__main__":
    os.makedirs("usuarios", exist_ok=True)
    pantalla_principal()





