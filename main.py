
import tkinter as tk
from tkinter import ttk
from csv_formatter import csv_format_tool
from num2words import num2words


# Diccionario de colindancias
colindancias = {
    "ac": "área común",
    "dp": "Departamento número",
    "edp": "Estacionamiento de Departmento número",
    "et": "Estacionamiento No.",
    "tdp": "Terraza de Departamento número",
    "lc": "Local Comercial número",
    "b": "Bodega número",
    "t": "Terraza número",
    "pf": "Propiedad que es o fue"
}

# Lista para almacenar el historial
historial = []

ERROR_TEXTO = "Ingresar el siguiente formato: [<m>.<cm>.<colindancia>]"

csvtool = csv_format_tool()


def focus_next(event):
    event.widget.tk_focusNext().focus()
    return "break"


def focus_prev(event):
    event.widget.tk_focusPrev().focus()
    return "break"


def formatear_medida(medida):
    m_cm_c = medida.split(".") 
    m = int(m_cm_c[0])
    cm = int(m_cm_c[1]) if len(m_cm_c) == 3 else 0
    colindancia = m_cm_c[len(m_cm_c) - 1]
    return m, cm, colindancia


def actualizar_medida(*args):
    try:
        m, cm, c = formatear_medida(entry_medida.get())
        metros = m
        centimetros = cm
        colindancia = c

        metros_txt = num2words(metros, lang='es') + " metros"
        centimetros_txt = num2words(centimetros, lang='es') + " centímetros"

        if metros == 1:
            metros_txt = "un metro"
        elif metros == 0:
            metros_txt = ""
        if centimetros == 1:
            centimetros_txt = "un centímetro"
        elif centimetros == 0:
            centimetros_txt = ""
        if "uno" in metros_txt:
            metros_txt = metros_txt.replace("uno", "un")
        if "uno" in centimetros_txt:
            centimetros_txt = centimetros_txt.replace("uno", "un")

        numero = ''.join(filter(str.isdigit, colindancia))

        clave_dict = colindancia.replace(f"{numero}", "")
        numero_txt = num2words(numero, lang="es") if numero else ""

        if clave_dict in colindancias:
            colindancia_formateada = f"{colindancias[clave_dict]} ({numero}) {numero_txt}"
        else:
            colindancia_formateada = f"{colindancia}"

        medida = f"{metros}.{centimetros:02d} m ({metros_txt} {centimetros_txt})"
        if metros_txt == "":
            medida = f"{metros}.{centimetros:02d} m ({centimetros_txt})"
        if centimetros_txt == "":
            medida = f"{metros}.{centimetros:02d} m ({metros_txt})"

        if colindancia_formateada:
            medida += f" con {colindancia_formateada}"

        label_resultado.config(text=medida, justify="left")
    except Exception as e:
        label_resultado.config(text=ERROR_TEXTO)


def limpiar_campos():
    entry_medida.delete(0, tk.END)
    entry_medida.focus()


def copiar_medida(event=None):
    if label_resultado.cget("text") != ERROR_TEXTO:
        medida = label_resultado.cget("text")
        root.clipboard_clear()
        root.clipboard_append(medida + ".")
        label_copiado.config(text="Medida copiada al portapapeles")
        root.after(3000, lambda: label_copiado.config(text=""))

        if medida not in historial:
            historial.insert(0, medida)  # Insertar al inicio de la lista
            if len(historial) > 100:  # Limitar el historial a 100 elementos
                historial.pop()
        actualizar_historial()
        limpiar_campos()
    else:
        return

def copiar_area(event=None):
    area = label_resultado.cget("text")
    root.clipboard_clear()
    root.clipboard_append(area)
    label_copiado.config(text="Descripcion de area copiada al portapapeles")
    root.after(3000, lambda: label_copiado.config(text=""))

    # Aregar la medida al historial
    if area not in historial:
        historial.insert(0, area)  
        if len(historial) > 100:  
            historial.pop()
    actualizar_historial()
    limpiar_campos()


def formatear_superficie(m2, cm2, c):
    colindancia = c
    comun = False
    m2_txt = num2words(m2, lang='es') + " metros"
    cm2_txt = num2words(cm2, lang='es') + " centímetros cuadrados"

    if m2 == 1:
        m2_txt = "un metro"
    elif m2 == 0:
        m2_txt = ""
    if cm2 == 1:
        cm2_txt = "un centímetro cuadrado"
    elif cm2 == 0:
        cm2_txt = ""
    if "uno" in m2_txt:
        m2_txt = m2_txt.replace("uno", "un")
    if "uno" in cm2_txt:
        cm2_txt = cm2_txt.replace("uno", "un")

    numero = ''.join(filter(str.isdigit, colindancia))
    global clave_dict
    clave_dict = colindancia.replace(f"{numero}", "")
    if clave_dict == "ac":
        comun = True
    numero_txt = num2words(numero, lang="es") if numero else ""
    if clave_dict in colindancias:
        colindancia_formateada = f"{colindancias[clave_dict]} ({numero}) {numero_txt}"
    else:
        colindancia_formateada = f"{colindancia}"
    tipo_area = "área común" if comun else "área privativa"
    return colindancia_formateada, tipo_area, m2_txt, cm2_txt


def desc_area(event=None):
    try:
        el_o_la = "El"
        m, cm, c = formatear_medida(entry_medida.get() if entry_medida.get() else "0")
        m2 = m
        cm2 = cm
        c = c
        colindancia_formateada, tipo_area, m2_txt, cm2_txt = formatear_superficie(m2, cm2, c)
        if clave_dict in ("t", "tdp", "b"):
            el_o_la = "La"
        area = (f"El {colindancia_formateada}, cuenta con una superficie de área común total de {m2}.{cm2:02d} m2"
                f" ({m2_txt} {cm2_txt}) los cuales todos están techados, con las siguientes medidas y colindancias:")
        if m2 == 0:
            area = (f"El {colindancia_formateada}, cuenta con una superficie de área común total de {m2}.{cm2:02d} m2"
                    f" ({cm2_txt}) los cuales todos están techados, con las siguientes medidas y colindancias:")
        elif cm2 == 0:
            area = (f"El {colindancia_formateada}, cuenta con una superficie de área común total de {m2}.{cm2:02d} m2"
                    f" ({m2_txt} cuadrados) los cuales todos están techados, con las siguientes medidas y colindancias:")


        if tipo_area == "área privativa":
            area = (f"{el_o_la} {colindancia_formateada}, cuenta con una superficie de área privativa total de {m2}"
                f".{cm2:02d} m2 ({m2_txt} {cm2_txt}) los cuales todos están techados y un indiviso de %.")
            if m2 == 0:
                area = (f"{el_o_la} {colindancia_formateada}, cuenta con una superficie de área privativa total de {m2}"
                        f".{cm2:02d} m2 ({cm2_txt}) los cuales todos están techados y un indiviso de %.")
            elif cm2 == 0:
                area = (f"{el_o_la} {colindancia_formateada}, cuenta con una superficie de área privativa total de {m2}"
                        f".{cm2:02d} m2 ({m2_txt} cuadrados) los cuales todos están techados y un indiviso de %.")

        label_resultado.config(text=area)
        copiar_area()
    except Exception as e:
        label_resultado.config(text=ERROR_TEXTO)


def abrir_ventana_areas(event=None):

    # Crear una nueva ventana
    ventana_areas = tk.Toplevel(root)
    ventana_areas.title("Superficies Techada y No Techada")
    ventana_areas.geometry("350x150")

    # Crear y ubicar etiquetas y entradas
    ttk.Label(ventana_areas, text="Sup. Techada (m²):").grid(row=0, column=0, padx=5, pady=5)
    entry_techada_m = ttk.Entry(ventana_areas)
    entry_techada_m.bind("<Return>", focus_next)
    entry_techada_m.bind("<Down>", focus_next)
    entry_techada_m.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(ventana_areas, text="Sup. Techada (cm²):").grid(row=1, column=0, padx=5, pady=5)
    entry_techada_cm = ttk.Entry(ventana_areas)
    entry_techada_cm.bind("<Return>", focus_next)
    entry_techada_cm.bind("<Up>", focus_prev)
    entry_techada_cm.grid(row=1, column=1, padx=5, pady=5)
    entry_techada_m.focus()

    def desc_area_tnt(*args):
        try:
            el_o_la = "El"
            m, cm, c = formatear_medida(entry_medida.get() if entry_medida.get() else "0")
            m2 = m
            cm2 = cm
            colindancia_formateada, tipo_area, m2_txt, cm2_txt = formatear_superficie(m2, cm2, c)
            if clave_dict in ("t", "tdp", "b"):
                el_o_la = "La"
            area = (f"El {colindancia_formateada} (nombre), cuenta con una superficie de área común total de {m2}.{cm2:02d} m2"
                    f" ({m2_txt} {cm2_txt}) ")
            if tipo_area == "área privativa":
                area = (f"{el_o_la} {colindancia_formateada}, cuenta con una superficie de área privativa total de {m2}"
                        f".{cm2:02d} m2 ({m2_txt} {cm2_txt}) ")

            return area
        except Exception as e:
            label_resultado.config(text=ERROR_TEXTO)

    def guardar_areas():
        try:
            m, cm, c = formatear_medida(entry_medida.get() if entry_medida.get() else "0")
            m2 = (int(entry_techada_m.get()) if entry_techada_m.get() else 0)
            cm2 = (int(entry_techada_cm.get()) if entry_techada_cm.get() else 0)
            colindancia_formateada, tipo_area, m2_txt, cm2_txt = formatear_superficie(m2, cm2, c)
            area_techada = f"de los cuales {m2}.{cm2:02d} m2 ({m2_txt} {cm2_txt}) están techados"
            ventana_areas.destroy()
            area = desc_area_tnt()
            if tipo_area == "área privativa":
                area_techada += " y un indiviso de %."
            else:
                area_techada += ", con las siguientes medidas y colindancias:"
            label_resultado.config(text=area+area_techada)


            copiar_area()
        except Exception as e:
            label_resultado.config(text=ERROR_TEXTO)

    boton_guardar = ttk.Button(ventana_areas, text="Guardar", command=guardar_areas)
    boton_guardar.grid(row=2, column=0, columnspan=2, pady=10)
    boton_guardar.bind("<Return>", lambda event: boton_guardar.invoke())


def actualizar_historial():
    historial_tree.delete(*historial_tree.get_children())
    for i, item in enumerate(historial):
        historial_tree.insert("", "end", values=(i + 1, item))


def usar_historial(event):
    selection = historial_tree.selection()
    if selection:
        item = historial_tree.item(selection[0])
        medida_seleccionada = item['values'][1]
        label_resultado.config(text=medida_seleccionada)
        root.clipboard_clear()
        root.clipboard_append(medida_seleccionada)
        label_copiado.config(text="Medida del historial copiada")
        root.after(3000, lambda: label_copiado.config(text=""))


def copiar_historial_entero(event=None):
    if historial:
        historial_formateado = ", ".join(historial)
        historial_formateado += "."
        root.clipboard_clear()
        root.clipboard_append(historial_formateado)
        label_copiado.config(text="Historial completo copiado")
        root.after(3000, lambda: label_copiado.config(text=""))
    else:
        label_copiado.config(text="El historial está vacío")
        root.after(3000, lambda: label_copiado.config(text=""))


def borrar_historial(event=None):
    global historial
    historial = []
    actualizar_historial()
    label_copiado.config(text="Historial borrado")
    root.after(3000, lambda: label_copiado.config(text=""))


def ventana_csv(event=None):
    ventana = tk.Toplevel(root)
    ventana.title("Subir Csv")
    ventana.geometry("275x250")
    

    label = ttk.Label(ventana, text="Especifica la ubicacion del archivo .csv")
    label.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

    entry = ttk.Entry(ventana)
    entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

    label_excepcion = ttk.Label(ventana, text="")
    label_excepcion.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
    
    def copiar_plantilla():
        try:
            with open("template.txt") as t:
                plantilla = t.read()
                root.clipboard_clear()
                root.clipboard_append(plantilla)
                label_excepcion.config(text="Plantilla copiada al portapapeles", foreground="green")
                ventana.after(3000, lambda : label_excepcion.config(text="", foreground="#ffffff"))
        except Exception as e:
            label_excepcion.config(text="No se encontro la plantilla", foreground="red")
            ventana.after(3000, lambda : label_excepcion.config(text="", foreground="#ffffff"))
            return
            

    def subir_csv():
        try:    
            ubicacion = entry.get()
            csvtool.upload_csv(file_path=ubicacion)
            label_excepcion.config(text="Plantilla generada con exito")
        
        except Exception as e:
            label_excepcion.config(text="Ubicacion del archivo .csv invalida", foreground="red")
            ventana.after(3000, lambda : label_excepcion.config(text="", foreground="#ffffff"))
            return
    
    def mostrar_plantilla():
        try:
            with open("template.txt") as t:
                    plantilla = t.read()
                    
                    wintxt = tk.Tk()
                    wintxt.title("Plantilla")
                    wintxt.geometry("500x600")
 
                    frame_txt = ttk.Frame(wintxt)
                    frame_txt.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
                    
                    vbar = ttk.Scrollbar(frame_txt)
                    vbar.pack(side=tk.RIGHT, fill=tk.Y)

                    txt = tk.Text(frame_txt, background="#333333", foreground="#ffffff")
                    txt.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

                    txt.configure(yscrollcommand=vbar.set)
                    vbar.configure(command=txt.yview)

                    txt.insert(tk.END, plantilla)
                            
                    wintxt.mainloop()
                    
        except Exception as e:
            label_excepcion.config(text="No se encontro la plantilla", foreground="red")
            ventana.after(3000, lambda : label_excepcion.config(text="", foreground="#ffffff"))
            return
        
    
    subirbtn = ttk.Button(ventana, text="Subir", command=subir_csv) 
    subirbtn.grid(row=3, columnspan=1, sticky=(tk.W, tk.E), padx=5, pady=5)
    
    copiar = ttk.Button(ventana, text="Copiar Plantilla", command=copiar_plantilla) 
    copiar.grid(row=4, columnspan=1, sticky=(tk.W, tk.E), padx=5, pady=5)
    
    mostrar = ttk.Button(ventana, text="Ver Plantilla", command=mostrar_plantilla) 
    mostrar.grid(row=5, columnspan=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    
# Crear la ventana principal con tema
root = tk.Tk()
root.title("AutoMD v1.0")
root.geometry("650x750")


#Binds
root.bind('<Return>', copiar_medida)
root.bind('<Control-d>', desc_area)
root.bind('<Control-t>', abrir_ventana_areas)
root.bind('<Control-s>', copiar_historial_entero)
root.bind('<Control-f>', borrar_historial)

root.tk.call('source', 'azure.tcl')
root.tk.call("set_theme", "dark")

# Frame principal
main_frame = ttk.Frame(root, padding="20")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)

# Crear y ubicar etiquetas y entradas
ttk.Label(main_frame, text="Colindancia/Descripcion:", justify="center").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
entry_medida = ttk.Entry(main_frame)
entry_medida.grid(row=1, columnspan=1, sticky=(tk.W, tk.E), padx=5, pady=5)
entry_medida.focus_set()

# Label para mostrar el resultado
label_resultado = ttk.Label(main_frame, text=ERROR_TEXTO, wraplength=600, justify="center")
label_resultado.grid(row=3, columnspan=1, sticky=(tk.W, tk.E), padx=5, pady=10)

# Botón para copiar la medida
boton_copiar = ttk.Button(main_frame, text="(ENTER) Medida", command=copiar_medida)
boton_copiar.grid(row=4, column=0, sticky=(tk.W, tk.E), pady= 5)

# Boton para sacar la descripcion del area
boton_area = ttk.Button(main_frame, text="(Ctrl+D) Descripcion Area", command=desc_area)
boton_area.grid(row=5, column=0, sticky=(tk.W, tk.E), pady= 5)

# Botón "Desc Area T/NT"
boton_desc_area_tnt = ttk.Button(main_frame, text="(Ctrl+T) Desc Area T/NT", command=abrir_ventana_areas)
boton_desc_area_tnt.grid(row=6, column=0, sticky=(tk.W, tk.E), pady= 5)

boton_csv = ttk.Button(main_frame, text="Generar Plantilla", command=ventana_csv)
boton_csv.grid(row=7, column=0, sticky=(tk.W, tk.E), pady= 5)

# Label para mostrar el mensaje de copiado
label_copiado = ttk.Label(main_frame, text="", foreground="green")
label_copiado.grid(row=8, columnspan=1, sticky=(tk.W, tk.E), padx=5, pady=5)

# Frame para el historial
historial_frame = ttk.Frame(main_frame)
historial_frame.grid(row=9, columnspan=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
historial_frame.columnconfigure(0, weight=1)

ttk.Label(historial_frame, text="Historial:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

# Crear y configurar el Treeview para el historial
historial_tree = ttk.Treeview(historial_frame, columns=("num", "medida"), show="headings", height=10)
historial_tree.heading("num", text="#")
historial_tree.heading("medida", text="Medida/Descripcion")
historial_tree.column("num", width=50)
historial_tree.column("medida", width=550)
historial_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
historial_tree.bind('<Double-1>', usar_historial)

# Scrollbar para el Treeview
scrollbar = ttk.Scrollbar(historial_frame, orient="vertical", command=historial_tree.yview)
scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
historial_tree.configure(yscrollcommand=scrollbar.set)

# Frame para los botones de historial
botones_frame = ttk.Frame(main_frame)
botones_frame.grid(row=10, columnspan=1, sticky=(tk.W, tk.E), padx=5, pady=5)
botones_frame.columnconfigure(0, weight=1)
botones_frame.columnconfigure(1, weight=1)

# Botones para copiar historial entero y borrar historial
boton_copiar_historial = ttk.Button(botones_frame, text="(Ctrl+S) Copiar Historial Completo", command=copiar_historial_entero)
boton_copiar_historial.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

boton_borrar_historial = ttk.Button(botones_frame, text=" (Ctrl+F) Borrar Historial", command=borrar_historial)
boton_borrar_historial.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

# Conectar las entradas a la función de actualización
entry_metros_var = tk.StringVar()
entry_centimetros_var = tk.StringVar()
entry_colindancia_var = tk.StringVar()

entry_metros_var.trace_add("write", actualizar_medida)
entry_centimetros_var.trace_add("write", actualizar_medida)
entry_colindancia_var.trace_add("write", actualizar_medida)

entry_medida.config(textvariable=entry_metros_var)

# Configurar el grid para que sea expansible
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Ejecutar el bucle principal
root.mainloop()
