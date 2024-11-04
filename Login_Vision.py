from tkinter import *
from tkinter import ttk
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import numpy as np
from PIL import Image, ImageTk
import ttkthemes

def registrar_usuario():
    usuario_info = usuario.get()
    contra_info = contra.get()

    archivo = open(usuario_info, "w")
    archivo.write(usuario_info + "\n")
    archivo.write(contra_info)
    archivo.close()

    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)
    
    # Notificaciones
    notification = Toplevel(pantalla1)
    notification.geometry("300x100")
    notification.title("")
    notification.config(bg='#2ecc71')
    
    Label(notification, 
          text="✓ Registro Exitoso", 
          fg="white", 
          bg='#2ecc71',
          font=("Helvetica", 12, "bold")).pack(pady=20)
    
    notification.after(2000, notification.destroy)

def registro_facial():
    cap = cv2.VideoCapture(0)
    while(True):
        ret,frame = cap.read()
        frame = cv2.flip(frame, 1)  # Ahora es espejo
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.putText(frame, 'Presione "Esc" para capturar', (20,50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
        cv2.imshow('Registro Facial',frame)
        if cv2.waitKey(1) == 27:
            break
    
    usuario_img = usuario.get()
    cv2.imwrite(usuario_img+".jpg",frame)
    cap.release()
    cv2.destroyAllWindows()

    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)
    
    # Notificación
    notification = Toplevel(pantalla1)
    notification.geometry("300x100")
    notification.title("")
    notification.config(bg='#2ecc71')
    
    Label(notification, 
          text="✓ Registro Facial Exitoso", 
          fg="white", 
          bg='#2ecc71',
          font=("Helvetica", 12, "bold")).pack(pady=20)
    
    notification.after(2000, notification.destroy)

    def reg_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC)
            cv2.imwrite(usuario_img+".jpg",cara_reg)
            pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = usuario_img+".jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    reg_rostro(img, caras)

def registro():
    global usuario
    global contra
    global usuario_entrada
    global contra_entrada
    global pantalla1
    
    pantalla1 = Toplevel(pantalla)
    pantalla1.title("Registro de Usuario")
    pantalla1.geometry("400x500")
    pantalla1.configure(bg='#f5f6fa')
    
    # Frame principal
    frame_main = ttk.Frame(pantalla1, style='Card.TFrame')
    frame_main.pack(pady=20, padx=40, fill="both", expand=True)
    
    # Estilo para el frame
    style = ttk.Style(frame_main)
    style.configure('Card.TFrame', background='white')
    
    # Header
    Label(frame_main, 
          text="Crear Cuenta", 
          font=("Helvetica", 20, "bold"),
          bg='white',
          fg='#2c3e50').pack(pady=20)
    
    usuario = StringVar()
    contra = StringVar()
    
    # Frame para el formulario
    frame_form = ttk.Frame(frame_main, style='Card.TFrame')
    frame_form.pack(pady=20, padx=20)
    
    # Campos de entrada con iconos
    Label(frame_form, 
          text="Usuario", 
          font=("Helvetica", 11),
          bg='white',
          fg='#7f8c8d').pack(anchor=W)
    usuario_entrada = ttk.Entry(frame_form, 
                              textvariable=usuario,
                              font=("Helvetica", 12),
                              width=30)
    usuario_entrada.pack(pady=(5,15))
    
    Label(frame_form, 
          text="Contraseña", 
          font=("Helvetica", 11),
          bg='white',
          fg='#7f8c8d').pack(anchor=W)
    contra_entrada = ttk.Entry(frame_form, 
                             textvariable=contra,
                             font=("Helvetica", 12),
                             width=30,
                             show="•")
    contra_entrada.pack(pady=5)
    
    # Frame para botones
    frame_buttons = ttk.Frame(frame_main, style='Card.TFrame')
    frame_buttons.pack(pady=30)
    
    # Estilo para botones
    style.configure('Accent.TButton',
                   font=("Helvetica", 11),
                   padding=10)
    
    # Botones
    ttk.Button(frame_buttons, 
               text="Registro Tradicional",
               style='Accent.TButton',
               command=registrar_usuario).pack(pady=10)
    
    ttk.Button(frame_buttons, 
               text="Registro Facial",
               style='Accent.TButton',
               command=registro_facial).pack(pady=10)

def verificacion_login():
    log_usuario = verificacion_usuario.get()
    log_contra = verificacion_contra.get()

    usuario_entrada2.delete(0, END)
    contra_entrada2.delete(0, END)

    lista_archivos = os.listdir()
    if log_usuario in lista_archivos:
        archivo2 = open(log_usuario, "r")
        verificacion = archivo2.read().splitlines()
        if log_contra in verificacion:
            notification = Toplevel(pantalla2)
            notification.geometry("300x100")
            notification.title("")
            notification.config(bg='#2ecc71')
            Label(notification, 
                  text="✓ Inicio de Sesión Exitoso", 
                  fg="white",
                  bg='#2ecc71',
                  font=("Helvetica", 12, "bold")).pack(pady=20)
            notification.after(2000, notification.destroy)
        else:
            notification = Toplevel(pantalla2)
            notification.geometry("300x100")
            notification.title("")
            notification.config(bg='#e74c3c')
            Label(notification, 
                  text="✕ Contraseña Incorrecta", 
                  fg="white",
                  bg='#e74c3c',
                  font=("Helvetica", 12, "bold")).pack(pady=20)
            notification.after(2000, notification.destroy)
    else:
        notification = Toplevel(pantalla2)
        notification.geometry("300x100")
        notification.title("")
        notification.config(bg='#e74c3c')
        Label(notification, 
              text="✕ Usuario no encontrado", 
              fg="white",
              bg='#e74c3c',
              font=("Helvetica", 12, "bold")).pack(pady=20)
        notification.after(2000, notification.destroy)

def login_facial():
    cap = cv2.VideoCapture(0)
    counter = 0  # Contador parpadeo del texto

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        # Fondo detrás del texto
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 20), (500, 70), (0, 0, 0), -1) 
        frame = cv2.addWeighted(overlay, 0.5, frame, 0.5, 0)      

        #Parpadeo del texto 
        text_color = (255, 255, 255) if (counter // 20) % 2 == 0 else (180, 180, 180)
        cv2.putText(frame, 'Presione "Esc" para capturar', (20, 50), 
                    cv2.FONT_HERSHEY_COMPLEX, 0.8, text_color, 2)

        cv2.imshow('Login Facial', frame)

        counter += 1  
        if cv2.waitKey(1) == 27:  
            break

    cap.release()
    cv2.destroyAllWindows()
            
    usuario_login = verificacion_usuario.get()
    cv2.imwrite(usuario_login+"LOG.jpg",frame)
    cap.release()
    cv2.destroyAllWindows()

    usuario_entrada2.delete(0, END)
    contra_entrada2.delete(0, END)
    
    def log_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC)
            cv2.imwrite(usuario_login+"LOG.jpg",cara_reg)
            return pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = usuario_login+"LOG.jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    log_rostro(img, caras)

    def orb_sim(img1,img2):
        orb = cv2.ORB_create()
        kpa, descr_a = orb.detectAndCompute(img1, None)
        kpb, descr_b = orb.detectAndCompute(img2, None)
        comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
        matches = comp.match(descr_a, descr_b)
        regiones_similares = [i for i in matches if i.distance < 70]
        if len(matches) == 0:
            return 0
        return len(regiones_similares)/len(matches)

    im_archivos = os.listdir()
    if usuario_login+".jpg" in im_archivos:
        rostro_reg = cv2.imread(usuario_login+".jpg",0)
        rostro_log = cv2.imread(usuario_login+"LOG.jpg",0)
        similitud = orb_sim(rostro_reg, rostro_log)
        if similitud >= 0.98:
            notification = Toplevel(pantalla2)
            notification.geometry("300x100")
            notification.title("")
            notification.config(bg='#2ecc71')
            Label(notification, 
                  text=f"✓ Bienvenido {usuario_login}\nCompatibilidad: {similitud:.2%}", 
                  fg="white",
                  bg='#2ecc71',
                  font=("Helvetica", 12, "bold")).pack(pady=20)
            notification.after(3000, notification.destroy)
        else:
            notification = Toplevel(pantalla2)
            notification.geometry("300x100")
            notification.title("")
            notification.config(bg='#e74c3c')
            Label(notification, 
                  text=f"✕ Rostro no compatible\nCompatibilidad: {similitud:.2%}", 
                  fg="white",
                  bg='#e74c3c',
                  font=("Helvetica", 12, "bold")).pack(pady=20)
            notification.after(3000, notification.destroy)
    else:
        notification = Toplevel(pantalla2)
        notification.geometry("300x100")
        notification.title("")
        notification.config(bg='#e74c3c')
        Label(notification, 
              text="✕ Usuario no encontrado", 
              fg="white",
              bg='#e74c3c',
              font=("Helvetica", 12, "bold")).pack(pady=20)
        notification.after(2000, notification.destroy)

def login():
    global pantalla2
    global verificacion_usuario
    global verificacion_contra
    global usuario_entrada2
    global contra_entrada2
    
    pantalla2 = Toplevel(pantalla)
    pantalla2.title("Iniciar Sesión")
    pantalla2.geometry("400x500")
    pantalla2.configure(bg='#f5f6fa')
    
    # Frame principal
    frame_main = ttk.Frame(pantalla2, style='Card.TFrame')
    frame_main.pack(pady=20, padx=40, fill="both", expand=True)
    
    # Header
    Label(frame_main, 
          text="Iniciar Sesión", 
          font=("Helvetica", 20, "bold"),
          bg='white',
          fg='#2c3e50').pack(pady=20)
    
    verificacion_usuario = StringVar()
    verificacion_contra = StringVar()
    
    # Frame para el formulario
    frame_form = ttk.Frame(frame_main, style='Card.TFrame')
    frame_form.pack(pady=20, padx=20)
    
    Label(frame_form, 
          text="Usuario", 
          font=("Helvetica", 11),
          bg='white',
          fg='#7f8c8d').pack(anchor=W)
    usuario_entrada2 = ttk.Entry(frame_form, 
                                textvariable=verificacion_usuario,
                                font=("Helvetica", 12),
                                width=30)
    usuario_entrada2.pack(pady=(5,15))
    
    Label(frame_form, 
          text="Contraseña", 
          font=("Helvetica", 11),
          bg='white',
          fg='#7f8c8d').pack(anchor=W)
    contra_entrada2 = ttk.Entry(frame_form, 
                               textvariable=verificacion_contra,
                               font=("Helvetica", 12),
                               width=30,
                               show="•")
    contra_entrada2.pack(pady=5)
    
    # Frame para botones
    frame_buttons = ttk.Frame(frame_main, style='Card.TFrame')
    frame_buttons.pack(pady=30)
    
    ttk.Button(frame_buttons, 
                text="Inicio de Sesión Tradicional",
                style='Accent.TButton',
                command=verificacion_login).pack(pady=10)

    ttk.Button(frame_buttons,
               text="Inicio de Sesión Facial",
               style='Accent.TButton',
               command=login_facial).pack(pady=10)

def pantalla_principal():
    global pantalla
    pantalla = Tk()
    pantalla.geometry("800x600")
    pantalla.title("Sistema de Login Inteligente")
    pantalla.configure(bg='#f5f6fa')
    
    style = ttkthemes.ThemedStyle(pantalla)
    style.set_theme("arc") 
    
    style.configure('Card.TFrame', background='white')
    style.configure('Accent.TButton',
                   font=("Helvetica", 11),
                   padding=10)
    
    main_frame = ttk.Frame(pantalla, style='Card.TFrame')
    main_frame.pack(expand=True, pady=50, padx=50)
    
    # Logo 
    title_frame = ttk.Frame(main_frame, style='Card.TFrame')
    title_frame.pack(pady=30)
    
    Label(title_frame, 
          text="SISTEMA DE LOGIN INTELIGENTE", 
          font=("Helvetica", 24, "bold"),
          bg='white',
          fg='#2c3e50').pack()
    
    Label(title_frame,
          text="Reconocimiento Facial + Autenticación Tradicional",
          font=("Helvetica", 12),
          bg='white',
          fg='#7f8c8d').pack(pady=10)
    
    # Frame para los botones
    button_frame = ttk.Frame(main_frame, style='Card.TFrame')
    button_frame.pack(pady=30)
    
    # Estilo para botones grandes
    style.configure('Large.Accent.TButton',
                   font=("Helvetica", 12, "bold"),
                   padding=15)
    
    # Botones principales
    ttk.Button(button_frame,
               text="INICIAR SESIÓN",
               style='Large.Accent.TButton',
               command=login).pack(pady=10, padx=20, ipadx=30)
    
    ttk.Button(button_frame,
               text="REGISTRARSE",
               style='Large.Accent.TButton',
               command=registro).pack(pady=10, padx=20, ipadx=30)
    
    # Footer
    footer_frame = ttk.Frame(main_frame, style='Card.TFrame')
    footer_frame.pack(pady=30)
    
    Label(footer_frame,
          text="© 2024 Sistema de Login Inteligente",
          font=("Helvetica", 9),
          bg='white',
          fg='#95a5a6').pack()
    
    Label(footer_frame,
          text="Desarrollado con Tecnología de Reconocimiento Facial",
          font=("Helvetica", 9),
          bg='white',
          fg='#95a5a6').pack()

    # Centrar la ventana en la pantalla
    pantalla.update_idletasks()
    width = pantalla.winfo_width()
    height = pantalla.winfo_height()
    x = (pantalla.winfo_screenwidth() // 2) - (width // 2)
    y = (pantalla.winfo_screenheight() // 2) - (height // 2)
    pantalla.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    pantalla.mainloop()

if __name__ == "__main__":
    pantalla_principal()