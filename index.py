from tkinter import *
from tkinter import ttk 
from tkinter import messagebox
import os
import sys
import sqlite3

class Sistema:

        db_name ='database.db'

        def __init__ (self, window):
                self.wind = window
                self.wind.title('SISTEMA DE DESPACHO')
                # self.wind.geometry('900x900')
    
                barraMenu=Menu(window)
                window.config(menu=barraMenu)

                ordencompraMenu=Menu(barraMenu, tearoff=0)
                ordencompraMenu.add_command(label="Agregar Orden Compra", command=self.agregar_pedidos)
                ordencompraMenu.add_command(label="Modificar Orden Compra", command=self.modificar_pedido)
                ordencompraMenu.add_command(label="Borrar Orden Compra", command=self.eliminar_pedidos)

                #transporteMenu=Menu(barraMenu, tearoff=0)
                #transporteMenu.add_command(label="Crear Transporte")
                #transporteMenu.add_command(label="Actualizar Transporte")
                #transporteMenu.add_command(label="Revisar Transportes")
                #transporteMenu.add_command(label="Borrar Transportes")

                salirMenu=Menu(barraMenu, tearoff=0)
                salirMenu.add_command(label="Salir", command=self.salir)

                barraMenu.add_cascade(label="Ordenes de Compra", menu=ordencompraMenu)
                #barraMenu.add_cascade(label="Transportes", menu=transporteMenu)
                barraMenu.add_cascade(label="Salir", menu=salirMenu)

                #------------------------------Frame Superior---------------------------

                FrameSuperior = Frame(window)
                FrameSuperior.grid(row=0, column= 0, columnspan=2, pady = 10)

                botonTransportistas=Button(FrameSuperior, text="Transportistas", command=self.ver_transportes)
                botonTransportistas.grid(row=1, column=0, sticky="e", pady=10)

                botonOrdenesAsignadas=Button(FrameSuperior, text="Ordenes Pendientes", command=self.ver_ordenes_pendientes)
                botonOrdenesAsignadas.grid(row=1, column=1, sticky="e", pady=10)

                botonOrdenesTransportistas=Button(FrameSuperior, text="Orden por Camión", command=self.ver_ordenes_por_camion)
                botonOrdenesTransportistas.grid(row=1, column=2, sticky="e", pady=10)

                botonOrdenesFinalizadas=Button(FrameSuperior, text="Ordenes Finalizadas", command=self.ver_ordenes_finalizadas)
                botonOrdenesFinalizadas.grid(row=1, column=3, sticky="e", pady=10)
                botonTodaslasOrdenes=Button(FrameSuperior, text='Todas las ordenes', command=self.ver_todos_pedidos)
                botonTodaslasOrdenes.grid(row=2, column =0, columnspan=4, sticky='we')


                #------------------------------TABLA---------------------------
     
                self.tree=ttk.Treeview(height=15, columns=('Fecha', 'Nro Orden', 'Dirección', 'Comuna', 'Nro Despacho', #'Cod Transporte'))
                ))

                self.tree.grid(row=5, column=0, columnspan=2)
                scrolbary=ttk.Scrollbar(window, orient="vertical", command=self.tree.yview)
                scrolbarx=ttk.Scrollbar(window, orient="horizontal", command=self.tree.xview)
                scrolbary.grid(row=5, column=1, sticky="NSE")
                scrolbarx.grid(row=6, column=0, sticky="WE")
                self.tree.configure(yscrollcommand=scrolbary.set)
                self.tree.configure(xscrollcommand=scrolbarx.set)

                self.tree.heading('#0', text = "Fecha")
                self.tree.column("#0",minwidth=100,width=100, stretch=True)
                self.tree.heading('#1', text = "Nro Orden Compra")
                self.tree.column("#1",minwidth=100,width=100, stretch=True)
                self.tree.heading('#2', text = "Direccion")
                self.tree.column("#2",minwidth=100,width=200, stretch=True)
                self.tree.heading('#3', text = "Comuna")
                self.tree.column("#3",minwidth=100,width=100, stretch=True)
                self.tree.heading('#4', text = "Estado")
                self.tree.column("#4",minwidth=100,width=100, stretch=True)
                self.tree.heading('#5', text = "Cod. Transporte" )
                self.tree.column("#5",minwidth=100,width=120, stretch=True)

                #------------------------Botones INFERIORES----------------
                FrameInferior = Frame(window)
                FrameInferior.grid(row=7, column=0, columnspan=3)

                botonAgregarInfoEnvio=Button(FrameInferior, text="Agregar información de envío", command=self.agregar_informacion_envio)
                botonAgregarInfoEnvio.grid(sticky = W+E, pady=20)

                self.bbdd_existente()
                             
                self.ver_todos_pedidos()

#---------------------FUNCIONES DE AGREGAR MODIFICAR O BORRAR PEDIDOS--------------#

        

        def agregar_pedidos(self):
                self.ventana_pedidos = Toplevel()
                self.ventana_pedidos.title = ("Agregar Ordenes de Compra")

                Label(self.ventana_pedidos, text='').grid(row=0, pady=5)
                Label(self.ventana_pedidos, text='Fecha (Formato 29-03-2019)').grid(row=1, column=1)
                fecha=Entry(self.ventana_pedidos)
                fecha.grid(row=1, column=2)
                fechaIngresada = fecha.get()

                Label(self.ventana_pedidos, text='Número de Orden').grid(row=2, column=1)
                orden=Entry(self.ventana_pedidos)
                orden.grid(row=2, column=2)

                Label(self.ventana_pedidos, text='Dirección').grid(row=3, column=1)
                direccion=Entry(self.ventana_pedidos)
                direccion.grid(row=3, column=2)

                Label(self.ventana_pedidos, text='Comuna').grid(row=4, column=1)
                comuna=Entry(self.ventana_pedidos)
                comuna.grid(row=4, column=2)


                boton=ttk.Button(self.ventana_pedidos, text='Agregar Orden', command= lambda: self.agregar_orden_clic(fecha.get(), orden.get(), direccion.get(), comuna.get()))
                boton.grid(row=6, column=1, columnspan=2, pady=10)
                
        def agregar_orden_clic(self, fecha, orden, direccion, comuna):
                InfoFecha=self.info_fecha(fecha)
                EncontroCodigo = self.info_Orden(orden)
                datos_llenos = self.validar_pedido(fecha, orden,direccion, comuna)

                if InfoFecha == False:
                        messagebox.showinfo('Error', 'Fecha mal Ingresada, respetar formato por favor. \n\n\t\tEjemplo: dd/mm/aaaa')
                if EncontroCodigo:
                        messagebox.showinfo('Error','El codigo de pedido debe ser unico' )
                if datos_llenos == False:
                        messagebox.showinfo('Error', 'Debe completar todos los datos solicitados')
                
                if InfoFecha == True and EncontroCodigo == False and datos_llenos == True:
                        query='INSERT INTO PEDIDOS VALUES (NULL, ?, ?, ?, ?, "Pendiente", "")'
                        parametros = fecha, orden, direccion, comuna
                        self.run_query(query, parametros)
                        self.ventana_pedidos.destroy()
                        self.ver_todos_pedidos()
                
        def info_fecha(self, fecha):
                cantidad = fecha.count('-')
                digitos = len(fecha)
                if cantidad == 2:
                        valor = False
                        if digitos ==10:
                                valor = True
                else:
                        valor = False

                return valor
            
        def info_Orden(self, orden):
                query= 'SELECT DISTINCT NRO_ORDEN FROM PEDIDOS'
                parametros = orden
                valor = self.ver_repetido(query, parametros)
                return valor
                
        def validar_pedido(self,fecha, orden, direccion, comuna):
                return len(fecha)!= 0 and len(orden) != 0 and len(direccion) != 0 and len(comuna)!=0

        def eliminar_pedidos(self):

                try: 
                        self.tree.item(self.tree.selection())['values'][0]
                except IndexError as e:
                        messagebox.showinfo('Advertencia', 'Favor seleccionar un registro')
                        return
                valor = messagebox.askquestion('Borrar registro', '¿Esta seguro de Borrar este Pedido?')

                if valor == 'yes':
                        codigo = self.tree.item(self.tree.selection())['values'][0]
                        query= 'DELETE FROM PEDIDOS WHERE NRO_ORDEN = ?'

                        self.run_query(query, (codigo, ))
                        messagebox.showinfo('Éxito', 'El registro ha sido borrado exitosamente')
                        self.ver_todos_pedidos()

        def modificar_pedido(self):
                try: 
                        self.tree.item(self.tree.selection())['values'][0]
                except IndexError as e:
                        messagebox.showinfo('Advertencia', 'Favor seleccionar un registro')
                        return
                valor = messagebox.askquestion('Modificar registro', '¿Esta seguro de Modificar este Pedido?')

                fecha_pedido = self.tree.item(self.tree.selection())['text']
                codigo_pedido = self.tree.item(self.tree.selection())['values'][0]
                direccion_pedido = self.tree.item(self.tree.selection())['values'][1]
                comuna_pedido = self.tree.item(self.tree.selection())['values'][2]

                if valor == 'yes':
                        self.ventana_modificar_pedidos = Toplevel()
                        self.ventana_modificar_pedidos.title = 'Editar Orden de Pedido'

                        Label(self.ventana_modificar_pedidos, text='Datos de Solo Lectura').grid(row=0, columnspan=3,pady=10)
                        Label(self.ventana_modificar_pedidos, text='Fecha Pedido').grid(row=1, column=1)
                        Entry(self.ventana_modificar_pedidos, textvariable = StringVar(self.ventana_modificar_pedidos, value=fecha_pedido), state = "readonly").grid(row=1, column=2)

                        Label(self.ventana_modificar_pedidos, text='Codigo Pedido').grid(row=2, column=1)
                        Entry(self.ventana_modificar_pedidos, textvariable = StringVar(self.ventana_modificar_pedidos, value=codigo_pedido), state = "readonly").grid(row=2, column=2)

                        Label(self.ventana_modificar_pedidos, text='Datos a Modificar').grid(row=3, columnspan=3,pady=10)

        
                        Label(self.ventana_modificar_pedidos, text='Dirección').grid(row=4, column=1)
                        direccion_nueva=Entry(self.ventana_modificar_pedidos, textvariable = StringVar(self.ventana_modificar_pedidos, value=direccion_pedido))
                        direccion_nueva.grid(row=4, column=2)

                        Label(self.ventana_modificar_pedidos, text='Comuna').grid(row=5, column=1)
                        comuna_nueva=Entry(self.ventana_modificar_pedidos, textvariable = StringVar(self.ventana_modificar_pedidos, value=comuna_pedido))
                        comuna_nueva.grid(row=5, column=2)

                        ttk.Button(self.ventana_modificar_pedidos, text='Aceptar', command=lambda: self.click_modificar_orden_pedido(direccion_nueva.get(), comuna_nueva.get(), codigo_pedido)).grid(row=6, columnspan=3, pady=10)

        def click_modificar_orden_pedido (self, direccion, comuna, nro_orden):
                query= 'UPDATE PEDIDOS SET DIRECCION = ?, COMUNA=? WHERE NRO_ORDEN = ?'
                parametros=(direccion, comuna, nro_orden)
                self.run_query(query,parametros)
                self.ventana_modificar_pedidos.destroy()
                self.ver_todos_pedidos()
                        
               
#-------------------------FUNCIONES PEDIDOS------------------#

        def ver_ordenes_por_camion(self):
                records = self.tree.get_children()

                for element in records:
                        self.tree.delete(element)

                query = 'SELECT * FROM PEDIDOS ORDER BY CODIGO_TRANSPORTE ASC'
                db_rows = self.run_query(query)

                for row in db_rows:
                        if len(row[6]) != 0:
                                self.tree.insert('', 0, text=row[1], values =(row[2],row[3], row[4], row[5], row[6]))

        def ver_todos_pedidos(self):
                records = self.tree.get_children()

                for element in records:
                        self.tree.delete(element)

                query = 'SELECT * FROM PEDIDOS ORDER BY ID DESC'
                db_rows = self.run_query(query)

                for row in db_rows:
                        self.tree.insert('', 0, text=row[1], values =(row[2],row[3], row[4], row[5], row[6]))

        def ver_ordenes_finalizadas(self):
                records = self.tree.get_children()

                for element in records:
                        self.tree.delete(element)

                query = 'SELECT * FROM PEDIDOS WHERE ESTADO ="Finalizado" ORDER BY ID ASC'
                db_rows = self.run_query(query)

                for row in db_rows:
                        self.tree.insert('', 0, text=row[1], values =(row[2],row[3], row[4], row[5], row[6]))

        def ver_ordenes_pendientes(self):
                records = self.tree.get_children()

                for element in records:
                        self.tree.delete(element)

                query = 'SELECT * FROM PEDIDOS WHERE ESTADO ="Pendiente" ORDER BY ID ASC'
                db_rows = self.run_query(query)

                for row in db_rows:
                        self.tree.insert('', 0, text=row[1], values =(row[2],row[3], row[4], row[5], row[6]))
                
        def agregar_informacion_envio(self):
                try: 
                        self.tree.item(self.tree.selection())['text'][0]
                except IndexError as e:
                        messagebox.showinfo("Advertencia", "debe seleccionar un registro")
                        return
                orden = self.tree.item(self.tree.selection())['values'][0]

                self.agregar_ventana = Toplevel()
                self.agregar_ventana.title='Agrega la informacion de Envío'
                
                Label(self.agregar_ventana, text='Orden de despacho').grid(row=1, column=1)
                Entry(self.agregar_ventana, textvariable=StringVar(self.agregar_ventana, value = orden), state="readonly").grid(row=1, column = 2)

                Label(self.agregar_ventana, text='Estado').grid(row=2, column=1)

                #CB Estado
                self.estado = ttk.Combobox(self.agregar_ventana, postcommand=self.dropdown_opened, state="readlonly")
                self.estado.bind("<<ComboboxSelected>>", self.selection_changed)
                self.estado["values"]=["Pendiente", "Enviado", "Finalizado"]
                self.estado.set('Enviado')
                #estado.place(x=50, y=50)
                self.estado.grid(row=2, column=2)


                #Obtener Registro ya Existente
                query='SELECT ESTADO FROM PEDIDOS WHERE NRO_ORDEN = ?'
                parametros = orden
                estado=self.run_query(query, (parametros,))
                for i in estado:
                        estado=i
                self.estado.set(estado)
                Encontro_Finalizado='Finalizado' in estado
                if Encontro_Finalizado:
                        desea_modificar=messagebox.askquestion('Finalizado', 'Pedido ya esta finalizado, ¿Desea Modifcar?')
                else:
                        desea_modificar = 'yes'

                Label(self.agregar_ventana, text='Cod. Transporte').grid(row=3, column=1)


                #CB Codigos
                #OBTENGO LOS CODIGOS CON LA QUERY Y METODO
                codigos=self.codigo_transportes_existente()
                self.codigosCB=ttk.Combobox(self.agregar_ventana, postcommand=self.dropdown_opened, state="readonly")
                self.codigosCB.bind("<<ComboboxSelected>>", self.selection_changed)
                #Relleno los codigos de
                for element in codigos:
                        values = list(self.codigosCB["values"])
                        self.codigosCB['values']=values+[element]
                
                #OBTENER REGISTRO YA EXISTENTE
                query='SELECT CODIGO_TRANSPORTE FROM PEDIDOS WHERE NRO_ORDEN = ?'
                parametros= orden
                codigo_transporte_obtenido = self.run_query(query, (parametros, ))
                for i in codigo_transporte_obtenido:
                        codigo_transporte_obtenido=i

                if codigo_transporte_obtenido != ('',):
                        self.codigosCB.set(codigo_transporte_obtenido)
                #print(codigo_transporte_obtenido)
                self.codigosCB.grid(row=3, column=2)


                if desea_modificar == 'yes':
                        Button(self.agregar_ventana, text='Modificar',command= lambda: self.agregar_informacion_click(orden, self.estado.get(), self.codigosCB.get())).grid(row=4, column=0, columnspan=3, pady=15)
                else:
                        self.agregar_ventana.destroy()

        def agregar_informacion_click(self, orden, estado, codigo_transporte):
                valor=self.validar_codigos()
                if valor:
                        query='UPDATE PEDIDOS SET ESTADO = ?, CODIGO_TRANSPORTE = ? WHERE NRO_ORDEN = ?'
                        messagebox.showinfo("Exito", "Información agregada exitosamente")
                        parametros=(estado, codigo_transporte, orden)
                        self.run_query(query,parametros)
                        self.agregar_ventana.destroy()
                        self.ver_todos_pedidos()
                else:
                        messagebox.showinfo("Error", "Debe completar todos los datos para actualizar")

        def validar_codigos(self):
                return len(self.codigosCB.get()) != 0  and len(self.codigosCB.get()) !=0

        def selection_changed(self, event):
                #print("Nuevo elemento seleccionado:", self.estado.get())
                #print("Nuevo elemento seleccionado:", self.codigosCB.get())
                #print(len(self.estado.get()))
                pass
        def dropdown_opened(self):
                #print("Lista desplegada.")
                pass

        def codigo_transportes_existente(self):
                query='SELECT CODIGO_TRANSPORTE FROM TRANSPORTES'
                codigos=self.run_query(query)
                return codigos

#--------------------------Funciones Generales-----------#

        def bbdd_existente(self):
                try:    
                        query = 'SELECT * FROM PEDIDOS'
                        resultado = self.run_query(query)
                        
                except :
                        valor = messagebox.askquestion("Error", "La BBDD No Existe \n¿Desea crear la Base de Datos?\nEsto es necesario para continuar la ejecución de programa")

                        if valor =="yes":
                                self.crear_bbdd()
                        else:
                                window.destroy()
                        
                                
        def crear_bbdd(self):
                try:
                        query1=('''
                        CREATE TABLE PEDIDOS (
                        ID	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        FECHA	TEXT NOT NULL,
                        NRO_ORDEN	TEXT NOT NULL,
                        DIRECCION	TEXT NOT NULL,
                        COMUNA	TEXT NOT NULL,
                        ESTADO	TEXT,
                        CODIGO_TRANSPORTE	INTEGER)
                        ''')
                        
                        self.run_query(query1)

                        query2=('''
                        CREATE TABLE TRANSPORTES (
                        ID	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        CODIGO_TRANSPORTE	TEXT NOT NULL,
                        NOMBRE_TRANSPORTE	TEXT NOT NULL,
                        RESPONSABLE_TRANSPORTE	TEXT NOT NULL,
                        FONO_TRANSPORTE	INTEGER NOT NULL)
                        ''')
                        self.run_query(query2)

                        self.crear_datos_demostracion()

                except:
                        messagebox.showwarning("¡Atención!", "La BBDD ya existe")

        def crear_datos_demostracion(self):
                query=('''
                INSERT INTO PEDIDOS VALUES
                (NULL, "21-02-2019","P01", "pasaje 23 184", "La Florida", "Pendiente", ""),
                (NULL, "21-02-2019","P02", "gabriela poniente 192", "Puente Alto", "Pendiente", ""),
                (NULL, "22-02-2019","P03", "pasaje lo barnechea 16550", "Maipu", "Pendiente", ""),
                (NULL, "21-02-2019","P04", "pasaje raimundo 284", "Maipu", "Pendiente", ""),
                (NULL, "20-02-2019","P05", "san ignacio de loyola 75", "Santiago Centro", "Pendiente", ""),
                (NULL, "23-02-2019","P06", "san alfonso 183", "Estacion Central", "Pendiente", ""),
                (NULL, "12-02-2019","P07", "arsenal 25", "Quilicura", "Finalizado", "T01"),
                (NULL, "10-02-2019","P08", "san francisco 23", "La Pintana", "Finalizado", "T02"),
                (NULL, "09-02-2019","P09", "San Francisco 87", "El Bosque", "Finalizado", "T02")
                ''')
                self.run_query(query)
                query2=('''
                INSERT INTO TRANSPORTES VALUES
                (NULL, "T01", "TRANSPORTES UNO", "Juan Gallardo", 3345678),
                (NULL, "T02", "TRANSPORTES DOS", "Juan Perez", 3345678),
                (NULL, "T03", "TRANSPORTES UNO", "Juan Fernandez", 3345678)
                ''')
                self.run_query(query2)

                self.restart_program()

        def restart_program(self):
                """Restarts the current program.
                Note: this function does not return. Any cleanup action (like
                saving data) must be done before calling this function."""
                python = sys.executable
                os.execl(python, python, * sys.argv)


        def ver_repetido(self, querycomp, numero_a_comparar):
                        #query='SELECT DISTINCT CODIGO_TRANSPORTE FROM TRANSPORTES'
                
                with sqlite3.connect(self.db_name) as conn:
                        cursor = conn.cursor()
                        resultado = cursor.execute(querycomp)
                        conn.commit()
                        prueba=cursor.fetchall()
                verdad=False

                for element in prueba:
                        if numero_a_comparar in element:
                                verdad= True
               
                return verdad

        def salir(self):
                valor= messagebox.askquestion("Salir", "¿Esta seguro de salir de la aplicación")
                
                if valor =="yes":
                        window.destroy()

        def run_query(self, query, parametros =()):
                with sqlite3.connect(self.db_name) as conn:
                        cursor = conn.cursor()
                        resultado = cursor.execute(query, parametros)
                        conn.commit()
                return resultado

        def validar_transporte(self):
                return len(self.codTransporte.get()) != 0
        

#----------------FUNCIONES TRANSPORTE--------#

        def ver_transportes(self):
              
                self.edit_wind=Toplevel()
                self.edit_wind.title = 'Transportistas'

                self.treeT=ttk.Treeview(self.edit_wind, height=5, columns=('Código Tranpsorte', 'Nombre Transporte', 'Nombre Responsable'))
                self.treeT.grid(row=0, column=0)

                scrolbary=ttk.Scrollbar(self.edit_wind, orient="vertical", command=self.treeT.yview)
                scrolbary.grid(row=0, column=1, sticky="NSE")
                self.treeT.configure(yscrollcommand=scrolbary.set)
                self.treeT.heading('#0', text='Código')
                self.treeT.heading('#1', text='Nombre')
                self.treeT.heading('#2', text='Responsable')
                self.treeT.heading('#3', text='Teléfono')
                self.listado_transporte()

                #----------FRAME TRANSPORTE-------------
                frameBT=LabelFrame(self.edit_wind, text="Crear Nuevo Transporte")
                frameBT.grid(row=1, column = 0, columnspan = 5, pady=10)

                #Codigo Transporte
                Label(frameBT, text='Codigo Transporte').grid(row=1, column=0)
                self.codTransporte=Entry(frameBT)
                self.codTransporte.focus()
                self.codTransporte.grid(row=1, column=1, columnspan=2)
                
                #Nombre Transporte
                Label(frameBT, text='Nombre Transporte').grid(row=2, column=0)
                self.nomTransporte=Entry(frameBT)
                self.nomTransporte.grid(row=2, column=1, columnspan=2)
                
                #Nombre Responsable
                Label(frameBT, text='Nombre Responsable').grid(row=3, column=0)
                self.nomResponsable=Entry(frameBT)
                self.nomResponsable.grid(row=3, column=1, columnspan=2)
                #Telefono Responsable
                Label(frameBT, text='Nro. Teléfono').grid(row=4, column=0)
                self.numTransporte=Entry(frameBT)
                self.numTransporte.grid(row=4, column=1, columnspan=2)

                ttk.Button(frameBT, text="Agregar Tranportista", command=self.agregar_transporte).grid(row=5, column=0, pady=10, sticky=W+E)

                ttk.Button(frameBT, text="Eliminar Transportista", command=self.borrar_transporte).grid(row=5, column=1, pady=10, sticky=W+E)

                ttk.Button(frameBT, text="Modificar Transporte", command=self.mod_transporte).grid(row=5, column=2, pady=10, sticky=W+E)


        def mod_transporte(self):
                try:
                        self.treeT.item(self.treeT.selection())['text'][0]
                except IndexError as e:
                        valor=messagebox.showinfo("Advertencia", "debe seleccionar un registro")
                        return
                cod = self.treeT.item(self.treeT.selection())['text']
                nomTra = self.treeT.item(self.treeT.selection())['values'][0]
                nomRes=self.treeT.item(self.treeT.selection())['values'][1]
                nroTel=self.treeT.item(self.treeT.selection())['values'][2]

                self.editar_wind = Toplevel()
                self.editar_wind.title = 'Editar Transporte'

                #CODIGO ANTERIOR
                Label(self.editar_wind, text= 'Código a Modificar').grid(row=0, column=1)
                Entry(self.editar_wind, textvariable = StringVar(self.editar_wind, value = cod), state= "readonly").grid(row =0, column =2)

                #Label(self.editar_wind, text='Nuevo Código').grid(row=1, column=1)
                #new_cod = Entry(self.editar_wind)
                #new_cod.grid(row=1, column =2)

                #NOMBRE ANTERIOR
                Label(self.editar_wind, text='Nombre Anterior').grid(row=2, column=1)
                Entry(self.editar_wind, textvariable = StringVar(self.editar_wind, value = nomTra), state = "readonly").grid(row=2, column=2)

                Label(self.editar_wind, text='Nombre Nuevo').grid(row=3, column=1)
                new_name = Entry(self.editar_wind)
                new_name.grid(row=3, column=2)

                #RESPONSABLE ANTERIOR
                Label(self.editar_wind, text='Responsable Anterior').grid(row=4, column=1)
                Entry(self.editar_wind, textvariable=StringVar(self.editar_wind, value = nomRes), state="readonly").grid(row=4, column=2)

                Label(self.editar_wind, text='Responsable Nuevo').grid(row=5, column=1)
                new_responsable=Entry(self.editar_wind)
                new_responsable.grid(row=5, column=2)

                #TELEFONO ANTERIOR
                Label(self.editar_wind, text='Telefono Anterior').grid(row=6, column=1)
                Entry(self.editar_wind, textvariable=StringVar(self.editar_wind, value=nroTel), state='readonly').grid(row=6, column=2)

                Label(self.editar_wind, text='Telefono Nuevo').grid(row=7, column=1)
                new_fono=Entry(self.editar_wind)
                new_fono.grid(row=7, column=2)

                
                Button(self.editar_wind, text='Modificar', command= lambda: self.edit_recordsTransporte( new_name.get(), new_responsable.get(), new_fono.get(), cod, nomTra,nomRes, nroTel)).grid(row=8, column=1, sticky=W+E, pady=15, padx=5)

                Button(self.editar_wind, text='Cancelar', command= lambda:self.editar_wind.destroy()).grid(row= 8, column=2, sticky = W+E, pady=15, padx=5)

        def agregar_transporte(self):
                if self.validar_transporte():
                        
                        query= 'INSERT INTO TRANSPORTES VALUES(NULL, ?,?,?,?)'
                        parametros = (self.codTransporte.get(), self.nomTransporte.get(), self.nomResponsable.get(), self.numTransporte.get())

                        querycomp= 'SELECT DISTINCT CODIGO_TRANSPORTE FROM TRANSPORTES'
                        numero_a_comparar=self.codTransporte.get()
                        valor = self.ver_repetido(querycomp, numero_a_comparar)

                        if valor:
                                messagebox.showinfo('Error', 'El codigo no se puede repetir')
                                self.codTransporte.delete(0, END)
    
                        else:
                                self.run_query(query, parametros)
                                messagebox.showinfo("Éxito", 'Transportista agregado correctamente')
                       
                                self.codTransporte.delete(0, END)
                                self.nomTransporte.delete(0, END)
                                self.nomResponsable.delete(0, END)
                                self.numTransporte.delete(0, END)

                                self.listado_transporte()
                else:
                        messagebox.showinfo("Advertencia", 'Todos los campos son requeridos')

        def borrar_transporte(self):
                
                try:
                        self.treeT.item(self.treeT.selection())['text'][0]
                except IndexError as e:
                        valor= messagebox.showinfo("Advertencia", "debe seleccionar un registro")
                        return
                seguro = messagebox.askquestion('Desea Borrar', 'Esta seguro de querer borrar el transporte')
                if seguro =="yes":

                        codigo= self.treeT.item(self.treeT.selection())['text']
                        query = 'DELETE FROM TRANSPORTES WHERE CODIGO_TRANSPORTE = ?'
                        self.run_query(query, (codigo, ))
                        valor=messagebox.showinfo('Éxito', 'Ha sido eliminado exitosamente')
                else:
                        return
                self.listado_transporte()

        #----------OBTENER LISTADO DE TRANSPORTE
        def listado_transporte(self):
                records=self.treeT.get_children()

                for element in records:
                        self.treeT.delete(element)
                query = 'SELECT * FROM TRANSPORTES ORDER BY ID DESC'
                db_rows = self.run_query(query)

                for row in db_rows:
                        self.treeT.insert('', 0, text = row[1], values = (row[2], row[3], row[4] ))

        def edit_recordsTransporte(self, new_name, new_responsable, new_fono, cod, nomTra, nomRes, nroTel):
                query= 'UPDATE TRANSPORTES set NOMBRE_TRANSPORTE = ?,  RESPONSABLE_TRANSPORTE = ?, FONO_TRANSPORTE = ? WHERE CODIGO_TRANSPORTE = ? AND NOMBRE_TRANSPORTE = ? AND RESPONSABLE_TRANSPORTE = ? AND FONO_TRANSPORTE = ?'
                parametros= (new_name, new_responsable, new_fono, cod, nomTra, nomRes,nroTel)

                querycomp= 'SELECT DISTINCT CODIGO_TRANSPORTE FROM TRANSPORTES'
                
                self.run_query(query, parametros)
                self.editar_wind.destroy()
                valor= messagebox.showinfo('Actualizado', 'Registro actualizado con éxito')
                self.listado_transporte()
  
if __name__ == '__main__':
    window = Tk()
    application = Sistema(window) 
    window.mainloop()