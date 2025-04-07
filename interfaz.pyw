import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import threading
import ProcesarFoto as pf
from RedNeuronalArtificial import RedNeuronalArtificial

#variables globales
dataset = []
dataset_dict = {}  # Para facilitar el manejo con checkboxes
escala = 0.1
foto_ancho = 600
foto_alto = 800
tamanio_entrada = foto_ancho * foto_alto
capas_ocultas_total = 2
capas_ocultas_arreglo = [100, 50]
tamanio_salida = 1
funcion_activacion = 'sigmoide'
epochs = 100
tasa_aprendizaje = 0.1

fotos_prueba = []

nn = 0

def cargafoto():
    mostrar_aviso("Cargando imágenes...", spinner=True)
    root.after(100)
    file_paths = filedialog.askopenfilenames(
        title="Seleccionar imágenes",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
    )
    for path in file_paths:
        img = Image.open(path).convert('L')
        dataset.append((path, 1))  # Agregar inicialmente como seleccionado
        dataset_dict[path] = tk.IntVar(value=1)
        show_image(img, path)
    mostrar_aviso("Imágenes cargadas exitosamente ✅")

def cargafotoTest():
    mostrar_aviso("Cargando imagen para test...", spinner=True)
    root.after(100)
    file_paths = filedialog.askopenfilenames(
        title="Seleccionar imagen",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
    )
    for path in file_paths:
        img = Image.open(path).convert('L')
        fotos_prueba.append(path)  
        show_image_test(img, path)
    mostrar_aviso("Imagenes cargada exitosamente ✅")


def actualizar_dataset(path, var):
    for i, (ruta, estado) in enumerate(dataset):
        if ruta == path:
            dataset[i] = (ruta, var.get())
            break

def show_image(img, path):
    width, height = img.size
    resized_img = img.resize((int(width * escala), int(height * escala)), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(resized_img)

    img = ttk.Frame(scrollable_frame, padding=5)
    img.pack(side="left", padx=5, pady=10)

    canvas = tk.Canvas(img, width=resized_img.width, height=resized_img.height)
    canvas.create_image(0, 0, anchor="nw", image=img_tk)
    canvas.image = img_tk
    canvas.pack()

    # Título de la imagen (solo el nombre del archivo)
    titulo_img = os.path.basename(path)
    label_path = ttk.Label(img, text=titulo_img, font=("Helvetica", 8))
    label_path.pack(pady=2)

    # Checkbox
    checkbox = ttk.Checkbutton(
        img,
        text="Seleccionar",
        variable=dataset_dict[path],
        command=lambda: actualizar_dataset(path, dataset_dict[path]),
        bootstyle="success"
    )
    checkbox.pack()
    print(dataset)

def show_image_test(img, path):
    width, height = img.size
    resized_img = img.resize((int(width * 0.5), int(height * 0.5)), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(resized_img)

    img = ttk.Frame(scrollable_frameI, padding=5)
    img.pack(side="left", padx=5, pady=10)

    canvas = tk.Canvas(img, width=resized_img.width, height=resized_img.height)
    canvas.create_image(0, 0, anchor="nw", image=img_tk)
    canvas.image = img_tk
    canvas.pack()

    # Título de la imagen (solo el nombre del archivo)
    titulo_img = os.path.basename(path)
    label_path = ttk.Label(img, text=titulo_img, font=("Helvetica", 8))
    label_path.pack(pady=2)

    

def mostrar_aviso(texto, spinner=False):
    aviso_label.config(text=texto)
    if spinner:
        aviso_spinner.start()
    else:
        aviso_spinner.stop()

def mostrar_consola():
    print('hola mundo')

def actualizar_escala(valor):
    global escala, foto_ancho, foto_alto, tamanio_entrada
    escala = float(valor)
    foto_ancho = int(600 * escala)
    foto_alto = int(800 * escala)
    tamanio_entrada = foto_ancho * foto_alto
    mostrar_aviso(f"Escala actual: {escala*100:.0f}% - Entrada: {tamanio_entrada} px")

def configurar_scroll(padre, hijo, elemento):
    padre.configure(scrollregion=padre.bbox("all"))
    padre.itemconfig(hijo, width=elemento.winfo_reqwidth())

def actualizar_ventana(event):
    ancho_ventana = root.winfo_width()
    alto_ventana = root.winfo_height()

    cabecera_ancho = int(ancho_ventana)
    cabecera_alto = int(alto_ventana*0.10)

    nb_ancho = int(ancho_ventana * 0.65)
    nb_alto = int(alto_ventana)

    avisos_ancho = int(ancho_ventana * 0.32)
    avisos_alto = int(alto_ventana)

    # Posicionar los cuadros
    cabecera.place(x=0,y=0, width=cabecera_ancho, height=cabecera_alto)
    nb.place(x=0, y=cabecera_alto, width=nb_ancho, height=nb_alto)
    avisos_c.place(x=nb_ancho, y=cabecera_alto, width=avisos_ancho, height=avisos_alto)

def configurar_frame_entrenar(event):
    configurar_scroll(frame_entrenar,canvas_interior_entrenar,scrollable_frame_entrenar)

def actualizar_epoch():
    global epochs
    epochs = var_epoch.get()
    mostrar_aviso(f"Épocas: {epochs}")
    print(epochs)

def actualizar_salida():
    global tamanio_salida
    tamanio_salida = var_salida.get()
    mostrar_aviso(f"Tamaño salida: {tamanio_salida}")
    print(tamanio_salida)

def actualizar_tasa():
    global tasa_aprendizaje
    tasa_aprendizaje = var_ts.get()
    mostrar_aviso(f"Tasa de aprendizaje: {tasa_aprendizaje}")
    print(tasa_aprendizaje)

def actualizar_funcion_activacion(event):
    global funcion_activacion
    funcion_activacion = cb_funciones.get()
    mostrar_aviso(f"Función de activación seleccionada: {funcion_activacion} ✅")

def actualizar_total_capas():
    global capas_ocultas_total, capas_ocultas_arreglo
    capas_ocultas_total = var_total_capas.get()
    
    # Asegura que el arreglo tenga la cantidad correcta de elementos
    while len(capas_ocultas_arreglo) < capas_ocultas_total:
        capas_ocultas_arreglo.append(10)  # valor por defecto
    capas_ocultas_arreglo = capas_ocultas_arreglo[:capas_ocultas_total]
    
    actualizar_canvas_capas()
    mostrar_aviso(f"Capas ocultas totales: {capas_ocultas_total}")

# Función que dibuja los spinbox de cada capa
def actualizar_canvas_capas():
    for widget in frame_capas_canvas.winfo_children():
        widget.destroy()
    
    for idx in range(capas_ocultas_total):
        frame = ttk.LabelFrame(frame_capas_canvas, text=f'Capa {idx+1}')
        frame.pack(side='left', padx=5, pady=5)

        label = ttk.Label(frame, text='tamaño de capa: ', font=("Helvetica", 8))
        label.pack(fill='x')

        var = tk.IntVar(value=capas_ocultas_arreglo[idx])

        def generar_callback(i, var_ref):
            def callback():
                capas_ocultas_arreglo[i] = var_ref.get()
                mostrar_aviso(f"Capas ocultas actualizadas: {capas_ocultas_arreglo}")
            return callback

        spin = ttk.Spinbox(
            frame,
            from_=1,
            to=1000,
            increment=10,
            textvariable=var,
            command=generar_callback(idx, var)
        )
        spin.pack(padx=5, pady=5)

def entrenar_modelo():
    entrenar_hilo = threading.Thread(target=tread_entrenar)
    entrenar_hilo.start()
    activar_desactivar_controles('disabled')
    

def tread_entrenar():
    global dataset,escala,tamanio_entrada,capas_ocultas_arreglo,tamanio_salida,funcion_activacion,epochs,tasa_aprendizaje,nn
    X = [pf.cargar_foto(url, foto_ancho, foto_alto) for url, objetivo in dataset]
    y = [[objetivo] for url, objetivo in dataset]
    nn = RedNeuronalArtificial(tamanio_entrada,capas_ocultas_arreglo,tamanio_salida,funcion_activacion)
    nn.entrenar(X, y, epochs, tasa_aprendizaje)
    print('hola mundo')
    activar_desactivar_controles('normal')


def testear_modelo():
    global fotos_prueba
    activar_desactivar_controles('disabled')
    for url in fotos_prueba:
        result = nn.propagacion(pf.cargar_foto(url, foto_ancho, foto_alto))
        pred = "MISMA persona" if result[0] > 0.8 else "DIFERENTE persona"
        mostrar_aviso(f"{url} → {pred} ({result[0]*100:.0f}%)")
        print(f"{url} → {pred} ({result[0]*100:.0f}%)")
    activar_desactivar_controles('normal')

def activar_desactivar_controles(valor):
    btn_cargar_foto.config(state=valor)
    btn_entrenar.config(state=valor)
    btn_cargar_foto_test.config(state=valor)
    btn_test.config(state=valor)
    slider_escala.configure(state=valor)
    epocas_sb.configure(state=valor)
    salida_sb.configure(state=valor)
    ts_sb.configure(state=valor)
    cb_funciones.configure(state=valor)
    spin_total_capas.configure(state=valor)



# Crear ventana principal
root = ttk.Window(themename="superhero")
root.title("Red Neuronal Artificial")
root.state("zoomed")

root.bind("<Configure>", actualizar_ventana)

#frame principal
contenido = ttk.Frame(root, padding=10)
contenido.pack(pady=5, padx=5, fill="both", expand=True)

cabecera = ttk.Frame(contenido)
cabecera.pack(fill='both')

tituloPrincipal = ttk.Label(cabecera, bootstyle="info", text="Red Neuronal Artificial", font=("Helvetica", 20, "bold"))
tituloPrincipal.pack(pady=5, padx=10)

subtituloPrincipal = ttk.Label(cabecera, bootstyle="info", text="Reconocimiento facial", font=("Helvetica", 16))
subtituloPrincipal.pack(pady=2, padx=10)

# crear un Notebook para las pestañas de entrenar y testear
nb = ttk.Notebook(contenido)
nb.pack(side='left',pady=5, padx=5, fill="both", expand=True)

##pestaña entrenar
frame_entrenar = tk.Canvas(nb)

#scroll para la pestaña entrenar
scrollbar_entrenar_y = ttk.Scrollbar(frame_entrenar, orient="vertical", command=frame_entrenar.yview, bootstyle="primary-round")
frame_entrenar.configure(yscrollcommand=scrollbar_entrenar_y.set)
scrollable_frame_entrenar = ttk.Frame(frame_entrenar)
canvas_interior_entrenar = frame_entrenar.create_window((0, 0), window=scrollable_frame_entrenar, anchor="nw")


scrollable_frame_entrenar.bind("<Configure>", configurar_frame_entrenar)
    
scrollbar_entrenar_y.pack(side="right", fill="y")

#contenido pestaña entrenar
entrenar = ttk.LabelFrame(frame_entrenar, text="Entrenar", padding=5)
entrenar.pack(pady=2, fill="both", padx=2, expand=True)

cabecera_entrenar = ttk.Frame(entrenar)
cabecera_entrenar.pack( pady=2)

#cargar fotos para entrenar
label = ttk.Label(cabecera_entrenar, text='Imágenes para entrenamiento: ', font=("Helvetica", 12))
label.pack(side='left',pady=5, padx=15)
#boton para cargar foto
btn_cargar_foto = ttk.Button(cabecera_entrenar, text='Cargar', bootstyle=('primary', 'outline'), command=cargafoto)
btn_cargar_foto.pack(side='left',padx=5, pady=5)

btn_entrenar = ttk.Button(cabecera_entrenar, text='Entrenar', bootstyle=('success', 'outline'), command=entrenar_modelo)
btn_entrenar.pack(side='left',padx=5, pady=5)


#opciones para entrenar

opciones = ttk.LabelFrame(entrenar,  text='Opciones de entrenamiento', padding=2)
opciones.pack( padx=5, fill='both')

opciones_general = ttk.Frame(opciones)
opciones_general.pack(padx=5, pady=5, fill='x')
##modificar el tamaño a entrenar n%
label_escala = ttk.LabelFrame(opciones_general, text="Tamaño de visualización")
label_escala.pack(pady=5,padx=5, fill='x')

slider_escala = ttk.Scale(
    label_escala,
    from_=0.1,
    to=1.0,
    orient="horizontal",
    value=escala,
    command=actualizar_escala
)
slider_escala.pack(fill='x', padx=10, pady=5)
# Etiquetas debajo del slider
frame_etiquetas = tk.Frame(label_escala)
frame_etiquetas.pack(fill='x', padx=10, pady=(0, 5))

label_min = tk.Label(frame_etiquetas, text="10%")
label_min.pack(side="left")

label_centro = tk.Label(frame_etiquetas, text="50%")
label_centro.pack(side="left", expand=True)

label_max = tk.Label(frame_etiquetas, text="100%")
label_max.pack(side="right")

##epocas para entrenar
epocas = ttk.LabelFrame(opciones_general, text='epochs')
epocas.pack(pady=5,padx=5,side='left')


var_epoch = ttk.IntVar(value=epochs)

epocas_sb = ttk.Spinbox(
    epocas,
    from_=1,            # Valor mínimo
    to=1000000,         # Valor máximo
    increment=10,       # Paso
    textvariable=var_epoch,
    command=actualizar_epoch
)
epocas_sb.pack(pady=5,padx=5)

##salida
salida = ttk.LabelFrame(opciones_general, text='salida')
salida.pack(pady=5,padx=5,side='left')


var_salida = ttk.IntVar(value=tamanio_salida)

salida_sb = ttk.Spinbox(
    salida,
    from_=1,            # Valor mínimo
    to=1000000,         # Valor máximo
    increment=1,        # Paso
    textvariable=var_salida,
    command=actualizar_salida
)
salida_sb.pack(pady=5,padx=5)


##tasa de aprendizaje
ts = ttk.LabelFrame(opciones_general, text='Tasa de Aprendizaje')
ts.pack(pady=5,padx=5,side='left')



var_ts = ttk.DoubleVar(value=tasa_aprendizaje)

ts_sb = ttk.Spinbox(
    ts,
    from_=0.0,            # Valor mínimo
    to=1,         # Valor máximo
    increment=0.01,       # Paso
    textvariable=var_ts,
    command=actualizar_tasa
)
ts_sb.pack(pady=5,padx=5)

#funciones de activacion para entrenar (capas ocultas)
labeld2 = ttk.LabelFrame(opciones_general, text='Función de activación')
labeld2.pack(pady=5, padx=5, side='left')
cb_funciones = ttk.Combobox(labeld2, state="readonly")
cb_funciones['values'] = ['sigmoide', 'relu', 'lineal', 'tanh']
cb_funciones.set(funcion_activacion)
cb_funciones.pack(pady=5, padx=5)
cb_funciones.bind("<<ComboboxSelected>>", actualizar_funcion_activacion)


##capas ocultas
capas_ocultas = ttk.Frame(opciones)
capas_ocultas.pack(padx=5,pady=5, fill='x')

co = ttk.LabelFrame(capas_ocultas, text='Total capas ocultas')
co.pack(pady=5,padx=5, fill='both')

var_total_capas = ttk.IntVar(value=capas_ocultas_total)

spin_total_capas = ttk.Spinbox(
    co,
    from_=1,
    to=10,
    textvariable=var_total_capas,
    command=actualizar_total_capas
)
spin_total_capas.pack(padx=5, pady=5)


frame_capas = ttk.LabelFrame(co, text="Capas Ocultas", padding=5)
frame_capas.pack(pady=5, fill="both", padx=5)

# Frame donde se colocarán los Spinbox de cada capa oculta
frame_canvas_oculta = tk.Canvas(frame_capas)

scrollbar_x_fcc = ttk.Scrollbar(frame_canvas_oculta, orient="horizontal", command=frame_canvas_oculta.xview, bootstyle="light-round")
frame_canvas_oculta.configure(xscrollcommand=scrollbar_x_fcc.set)
scrollable_frame_fcc = ttk.Frame(frame_canvas_oculta)
canvas_interior_fcc = frame_canvas_oculta.create_window((0, 0), window=scrollable_frame_fcc, anchor="nw")

def configurar_scroll_fcc(event):
    configurar_scroll(frame_canvas_oculta,canvas_interior_fcc,scrollable_frame_fcc)

scrollable_frame_fcc.bind("<Configure>", configurar_scroll_fcc)

frame_canvas_oculta.pack(fill='both', expand=True)
frame_capas_canvas = ttk.Frame(frame_canvas_oculta)
frame_capas_canvas.pack(side="left", padx=5)



lista_capas = []

if capas_ocultas_total > 0:
    print(capas_ocultas_total)
    n=0
    for capa in capas_ocultas_arreglo:
        lista_capas.append({'capa':n, 'tamanio_capa':capa})
        n+=1

actualizar_canvas_capas()


#lienzo para visualizar las fotos cargadas
canvas_train = ttk.Frame(entrenar)
canvas_train.pack(fill="both", expand=True)

canvas_padre = tk.Canvas(canvas_train)
scrollbar_x = ttk.Scrollbar(canvas_train, orient="horizontal", command=canvas_padre.xview, bootstyle="light-round")
scrollbar_y = ttk.Scrollbar(canvas_train, orient="vertical", command=canvas_padre.yview, bootstyle="light-round")
canvas_padre.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

scrollable_frame = ttk.Frame(canvas_padre)
canvas_interior = canvas_padre.create_window((0, 0), window=scrollable_frame, anchor="nw")

def configurar_scroll_fotos_entrenar(event):
    configurar_scroll(canvas_padre,canvas_interior,scrollable_frame)

scrollable_frame.bind("<Configure>", configurar_scroll_fotos_entrenar)


canvas_padre.pack(fill='both', expand=True)
scrollbar_y.pack(side="right", fill='y')
scrollbar_x.pack(side="bottom", fill='both')






###################

avisos_c = ttk.Frame(contenido, padding=10)
avisos_c.pack(side="right", fill="both", expand=True)

aviso_label = ttk.Label(avisos_c, text="Listo ✅", font=("Helvetica", 12, "bold"), bootstyle="info")
aviso_label.pack(pady=20)

aviso_spinner = ttk.Progressbar(avisos_c, mode='indeterminate', bootstyle="info-striped")
aviso_spinner.pack(pady=10, padx=10, fill="x")


#############################
#pestaña testear
frame_testear = tk.Canvas(nb)
frame_testear.pack(fill="both", expand=True)

#contenido pestaña testear
testear = ttk.LabelFrame(frame_testear, text="Testear", padding=5)
testear.pack(pady=2, fill="both", padx=2, expand=True)

cabecera_testear = ttk.Frame(testear)
cabecera_testear.pack( pady=2)

#cargar fotos para testear
label_test = ttk.Label(cabecera_testear, text='Imágenes para Testear: ', font=("Helvetica", 12))
label_test.pack(side='left',pady=5, padx=15)

#boton para cargar foto de testeo
btn_cargar_foto_test = ttk.Button(cabecera_testear, text='Cargar', bootstyle=('primary', 'outline'), command=cargafotoTest)
btn_cargar_foto_test.pack(side='left',padx=5, pady=5)

btn_test = ttk.Button(cabecera_testear, text='Testear', bootstyle=('success', 'outline'), command=testear_modelo)
btn_test.pack(side='left',padx=5, pady=5)

canvas_test = ttk.Frame(testear)
canvas_test.pack()

canvas_padreI = tk.Canvas(canvas_test)
scrollbar_xI = ttk.Scrollbar(canvas_test, orient="horizontal", command=canvas_padreI.xview)
scrollbar_yI = ttk.Scrollbar(canvas_test, orient="vertical", command=canvas_padreI.yview)
canvas_padreI.configure(xscrollcommand=scrollbar_xI.set, yscrollcommand=scrollbar_yI.set)

scrollable_frameI = ttk.Frame(canvas_padreI)
canvas_interiorI = canvas_padreI.create_window((0, 0), window=scrollable_frameI, anchor="nw")

scrollable_frameI.bind(
    "<Configure>",
    lambda e: canvas_padreI.configure(scrollregion=canvas_padreI.bbox("all"))
)

canvas_padreI.pack( fill="both", expand=True)
scrollbar_yI.pack(side='right',fill='y')
scrollbar_xI.pack(fill='both', side='bottom')

nb.add(frame_entrenar, text='Entrenar')
nb.add(frame_testear, text='Testear')

root.mainloop()
