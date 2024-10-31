from tkinter import *
from tkinter import filedialog
import os
import cv2
from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN
import numpy as np

# Función de registro
def registro():
    global usuario, contra, usuario_entrada, contra_entrada, pantalla1
    pantalla1 = Toplevel(pantalla)
    pantalla1.title("Registro")
    pantalla1.geometry("300x300")
    
    usuario = StringVar()
    contra = StringVar()
    
    Label(pantalla1, text="Registro facial: debe de asignar un usuario:").pack()
    Label(pantalla1, text="Registro tradicional: debe asignar usuario y contraseña:").pack()
    Label(pantalla1, text="Usuario * ").pack()
    usuario_entrada = Entry(pantalla1, textvariable=usuario)
    usuario_entrada.pack()
    
    Label(pantalla1, text="Contraseña * ").pack()
    contra_entrada = Entry(pantalla1, textvariable=contra, show='*')
    contra_entrada.pack()

    Button(pantalla1, text="Registro Tradicional", width=15, height=1, command=registrar_usuario).pack()
    Button(pantalla1, text="Registro Facial (Desde Cámara)", width=20, height=1, command=registro_facial).pack()
    Button(pantalla1, text="Registro Facial (Desde Archivo)", width=20, height=1, command=registro_foto).pack()

# Registro de usuario
def registrar_usuario():
    usuario_info = usuario.get()
    contra_info = contra.get()
    
    if os.path.exists(usuario_info + ".jpg"):
        Label(pantalla1, text="El usuario ya existe", fg="red", font=("Calibri", 11)).pack()
        return

    with open(usuario_info + ".txt", "w") as archivo:
        archivo.write(usuario_info + "\n")
        archivo.write(contra_info)

    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)
    Label(pantalla1, text="Registro Convencional Exitoso", fg="green", font=("Calibri", 11)).pack()

# Registro facial
def registro_facial():
    captura_foto()

def captura_foto():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Captura de Foto - Presiona 'Esc' para tomar la foto")

    for i in range(3):
        while True:
            ret, frame = cap.read()
            if not ret:
                Label(pantalla1, text="Error al capturar la imagen", fg="red", font=("Calibri", 11)).pack()
                break
            
            cv2.imshow("Captura de Foto - Presiona 'Esc' para tomar la foto", frame)

            key = cv2.waitKey(1)
            if key == 27:  # Tecla Esc
                usuario_img = f"{usuario.get()}_{i+1}.jpg"
                cv2.imwrite(usuario_img, frame)
                Label(pantalla1, text=f"Foto {i+1} registrada", fg="green", font=("Calibri", 11)).pack()
                break

    cap.release()
    cv2.destroyAllWindows()

def registro_foto():
    for i in range(3):
        usuario_img = f"{usuario.get()}_{i+1}.jpg"
        file_path = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            cv2.imwrite(usuario_img, cv2.imread(file_path))
            Label(pantalla1, text=f"Foto {i+1} registrada", fg="green", font=("Calibri", 11)).pack()
            img = usuario_img
            pixeles = plt.imread(img)
            detector = MTCNN()
            caras = detector.detect_faces(pixeles)
            reg_rostro(img, caras)

def reg_rostro(img, lista_resultados):
    data = plt.imread(img)
    for resultado in lista_resultados:
        x1, y1, ancho, alto = resultado['box']
        x2, y2 = x1 + ancho, y1 + alto
        cara_reg = data[y1:y2, x1:x2]
        cara_reg = cv2.resize(cara_reg, (150, 200), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(img, cara_reg)
        plt.imshow(data[y1:y2, x1:x2])
    plt.show()

# Verificación de login
def verificacion_login():
    imagenes_registradas = [f for f in os.listdir() if f.endswith('.jpg')]
    
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Presiona 'Esc' para tomar la foto")

    while True:
        ret, frame = cap.read()
        if not ret:
            Label(pantalla2, text="Error al capturar la imagen", fg="red", font=("Calibri", 11)).pack()
            break
        
        cv2.imshow("Presiona 'Esc' para tomar la foto", frame)

        key = cv2.waitKey(1)
        if key == 27:  # Tecla Esc
            break

    cap.release()
    cv2.destroyAllWindows()

    pixeles = frame
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)

    if len(caras) == 0:
        Label(pantalla2, text="No se detectó rostro", fg="red", font=("Calibri", 11)).pack()
        return

    similitud_mayor = 0
    usuario_detectado = ""

    for usuario_img in imagenes_registradas:
        rostro_reg = cv2.imread(usuario_img, 0)
        rostro_log = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        similitud = orb_sim(rostro_reg, rostro_log)

        print(f"Comparando con {usuario_img[:-4]}: {similitud:.2f}")

        if similitud > similitud_mayor:
            similitud_mayor = similitud
            usuario_detectado = usuario_img[:-4]

    if similitud_mayor >= 0.98:
        Label(pantalla2, text=f"Inicio de Sesión Exitoso como: {usuario_detectado}", fg="green", font=("Calibri", 11)).pack()
    else:
        Label(pantalla2, text="Incompatibilidad de rostros", fg="red", font=("Calibri", 11)).pack()

# Función de login
def login():
    global pantalla2
    pantalla2 = Toplevel(pantalla)
    pantalla2.title("Login")
    pantalla2.geometry("300x250")
    
    Label(pantalla2, text="Login facial: no es necesario ingresar un usuario.").pack()
    
    Button(pantalla2, text="Iniciar sesión con rostro", width=20, height=1, command=verificacion_login).pack()

def orb_sim(img1, img2):
    orb = cv2.ORB_create()
    kpa, descr_a = orb.detectAndCompute(img1, None)
    kpb, descr_b = orb.detectAndCompute(img2, None)
    if descr_a is None or descr_b is None:
        return 0
    comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = comp.match(descr_a, descr_b)
    regiones_similares = [i for i in matches if i.distance < 70]
    return len(regiones_similares) / len(matches) if matches else 0

# Función principal
pantalla = Tk()
pantalla.geometry("300x250")
pantalla.title("Sistema de Login")
Label(pantalla, text="Sistema de Login con Reconocimiento Facial", font=("Calibri", 13)).pack()
Button(pantalla, text="Login", height="2", width="30", command=login).pack()
Button(pantalla, text="Registro", height="2", width="30", command=registro).pack()

pantalla.mainloop()
