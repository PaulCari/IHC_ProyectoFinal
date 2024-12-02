from tkinter import *
from tkinter import ttk, simpledialog
import cv2
import os
import numpy as np
import ttkthemes
from deepface import DeepFace

# Función para registrar un nuevo usuario con fotos
def registrar_usuario():
    cap = cv2.VideoCapture(0)
    detector = DeepFace  # Usamos DeepFace para la verificación facial

    usuario_nombre = simpledialog.askstring("Registro", "Ingrese su nombre de usuario:")
    if not usuario_nombre:
        mostrar_notificacion("Registro cancelado", "#e74c3c")
        cap.release()
        return

    os.makedirs(f"usuarios/{usuario_nombre}", exist_ok=True)

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

# Función para iniciar sesión usando reconocimiento facial
def iniciar_sesion_facial():
    cap = cv2.VideoCapture(0)
    
    usuario_autenticado = False
    while not usuario_autenticado:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.imshow('Inicio de Sesión Facial', frame)

        if cv2.waitKey(1) == 27:  # Presiona "Esc" para capturar
            captura_sesion = "captura_sesion.jpg"
            cv2.imwrite(captura_sesion, frame)

            # Comparación con DeepFace
            pixeles = cv2.imread(captura_sesion)
            for usuario in os.listdir("usuarios"):
                coincidencias = 0
                for foto in os.listdir(f"usuarios/{usuario}"):
                    foto_registrada = f"usuarios/{usuario}/{foto}"

                    # Usamos DeepFace para comparar la imagen capturada con las fotos del usuario
                    try:
                        resultado = DeepFace.verify(captura_sesion, foto_registrada, enforce_detection=False)
                        if resultado["verified"]:
                            coincidencias += 1
                    except Exception as e:
                        print(f"Error en la comparación: {e}")

                if coincidencias >= 2:  # Dos de tres fotos deben coincidir
                    usuario_autenticado = True
                    mostrar_notificacion(f"Inicio de Sesión Exitoso: {usuario}", "#2ecc71")
                    break

            if not usuario_autenticado:
                mostrar_notificacion("No se reconoció la cara", "#e74c3c")

            break

    cap.release()
    cv2.destroyAllWindows()

# Función para mostrar notificaciones en la interfaz con estilo de ttkthemes
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
    ttk.Button(button_frame, text="INICIAR SESIÓN", style='Accent.TButton', command=iniciar_sesion_facial).pack(pady=20, ipadx=30)

    # Footer
    footer_frame = ttk.Frame(main_frame, style='Card.TFrame')
    footer_frame.pack(pady=30)

    Label(footer_frame, text="© 2024 Sistema de Inicio Facial", font=("Helvetica", 9), bg='white', fg='#95a5a6').pack()

    pantalla.mainloop()

# Iniciar la aplicación
if __name__ == "__main__":
    os.makedirs("usuarios", exist_ok=True)
    pantalla_principal()







