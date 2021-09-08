import sys
from datetime import datetime
from Funciones04 import *
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import urllib.request

#Diccionario Area
sqlArea="SELECT Descripción_Área,Cod_Área FROM TAB_SOC_010_Áreas_de_la_empresa"
#Diccionario Moneda
sqlMoneda="SELECT Descrip_moneda, Cod_moneda FROM TAB_SOC_008_Monedas"

class Consultar(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("ERP_PSOLP_001_01.ui",self)

        self.pbGrabar.clicked.connect(self.Grabar)
        self.pbAprobar.clicked.connect(self.Aprobar)
        self.pbRechazar.clicked.connect(self.Rechazar)
        self.pbSalir.clicked.connect(self.close)

        global dict_estadoPosicion
        dict_estadoPosicion = {}

    def datosGenerales(self, codSoc, empresa, usuario, Num_Solp):
        global Cod_Soc, Nom_Soc, Cod_Usuario, Año, Numero_Solp

        Cod_Soc = codSoc
        Nom_Soc = empresa
        Cod_Usuario = usuario
        Numero_Solp = Num_Solp

        now = datetime.now()
        Año=str(now.year)

        cargarLogo(self.lbLogo_Mp, 'multiplay')
        cargarLogo(self.lbLogo_Soc, Cod_Soc)
        cargarIcono(self, 'erp')
        cargarIcono(self.pbNuevaSOLP,'nuevo')
        cargarIcono(self.pbSeleccionar,'buscar')
        cargarIcono(self.pbGrabar,'grabar')
        cargarIcono(self.pbModificar,'modificar')
        cargarIcono(self.pbDarBaja,'darbaja')
        cargarIcono(self.pbLiberar_SOLP,'liberar')
        cargarIcono(self.pbAprobar,'activar')
        cargarIcono(self.pbRechazar,'cerrar')
        cargarIcono(self.pbSalir,'salir')

        self.Inicio()

    def Inicio(self):
        global dicArea,dicMoneda

        area=consultarSql(sqlArea)
        dicArea={}
        for a in area:
            dicArea[a[1]]=a[0]

        moneda=consultarSql(sqlMoneda)
        dicMoneda={}
        for m in moneda:
            dicMoneda[m[1]]=m[0]

        sqlTipoSolp="SELECT Descrip_Tip_Solp,Tipo_Solp FROM `TAB_SOLP_003_Solicitud Pedido`"
        tip=consultarSql(sqlTipoSolp)
        tipos={}
        for t in tip:
            tipos[t[1]]=t[0]
        insertarDatos(self.cbTipo_SOLP, tip)
        self.cbTipo_SOLP.setCurrentIndex(-1)

        #Diccionario tipo de estados de documento
        estadosDoc={'1':'Activo','2':'-','3':'Para Aprobación','4':'Anulado','5':'Aprobado','6':'Proceso de invitacion','7':'--','8':'Prov. Cotizo','9':'Concluido'}
        for k,v in estadosDoc.items():
            self.cbEstado_SOLP.addItem(v)
            self.cbEstado_SOLP.setCurrentIndex(-1)

        #Insertar datos en los ComboBox de la cabecera
        insertarDatos(self.cbArea, area)
        insertarDatos(self.cbMoneda, moneda)
        #Inicializar los combo box de la cabecera en blanco
        self.cbArea.setCurrentIndex(-1)
        self.cbMoneda.setCurrentIndex(-1)

        sqlSolicitante="SELECT Nom_usuario,Cod_usuario FROM TAB_SOC_005_Usuarios WHERE Cod_Soc='%s'"%(Cod_Soc)
        data=consultarSql(sqlSolicitante)
        usuario={}
        for dato in data:
            usuario[dato[1]]=dato[0]
        insertarDatos(self.cbSolicitante, data)
        self.cbSolicitante.setCurrentIndex(-1)

        sqlcabeceraSOLP='''SELECT b.Descrip_Tip_Solp, c.Descripción_Área, d.Nom_usuario, a.Fecha_Solp, a.Estado_Solp, e.Texto, SUM(f.Cant_Mat_Serv*f.Precio_ref), g.Descrip_moneda FROM TAB_SOLP_001_Cabecera_Solicitud_Pedido a LEFT JOIN `TAB_SOLP_003_Solicitud Pedido` b ON a.Tipo_solp=b.Tipo_Solp LEFT JOIN TAB_SOC_010_Áreas_de_la_empresa c ON a.Area_Solp=c.Cod_Área LEFT JOIN TAB_SOC_005_Usuarios d ON a.Cod_Soc=d.Cod_Soc AND a.Solicita_Solp=d.Cod_usuario LEFT JOIN TAB_SOC_019_Texto_Proceso e ON e.Cod_Soc=a.Cod_Soc AND e.Año=a.Año AND e.Tipo_Proceso='1' AND e.Nro_Doc=a.Nro_Solp AND e.Item_Doc='0' LEFT JOIN TAB_SOLP_002_Detalle_Solicitud_Pedido f ON f.Cod_Soc=a.Cod_Soc AND f.Año=a.Año AND f.Nro_Solp=a.Nro_Solp AND f.Estado_Item!='4' LEFT JOIN TAB_SOC_008_Monedas g ON f.Moneda=g.Cod_moneda WHERE a.Cod_Soc='%s' AND a.Año='%s' AND a.Nro_Solp='%s' GROUP BY a.Nro_Solp'''%(Cod_Soc, Año, Numero_Solp)
        listcabecera=convlist(sqlcabeceraSOLP)

        sqldetalleSOLP="SELECT a.Estado_Item,a.Item_Solp,a.Cod_Mat,c.Descrip_Mat,c.Uni_Base,k.Descrip_Marca,a.Cant_Mat_Serv,a.Precio_ref,a.Fecha_Requerimiento,d.Nom_Soc_Largo,e.Nomb_Planta,f.Nomb_Alm,g.Nom_usuario,h.Descripción_Área FROM TAB_SOLP_002_Detalle_Solicitud_Pedido a LEFT JOIN TAB_MAT_001_Catalogo_Materiales c ON a.Cod_Soc=c.Cod_Soc AND a.Cod_Mat=c.Cod_Mat LEFT JOIN TAB_SOC_001_Sociedad d ON a.Cod_Soc=d.Cod_soc LEFT JOIN TAB_SOC_002_Planta e ON a.Cod_Soc=e.Cod_soc AND a.Centro=e.Cod_Planta LEFT JOIN TAB_SOC_003_Almacén f ON a.Cod_Soc=f.Cod_Soc AND a.Centro=f.Cod_Planta AND a.Almacen=f.Cod_Alm LEFT JOIN TAB_SOC_005_Usuarios g ON a.Cod_Soc=g.Cod_Soc AND a.Solicitante=g.Cod_usuario LEFT JOIN TAB_SOC_010_Áreas_de_la_empresa h ON a.Area_gestora=h.Cod_Área LEFT JOIN TAB_MAT_010_Marca_de_Producto k ON a.Cod_Mat=c.Cod_Mat AND c.Marca=k.Cod_Marca WHERE a.Cod_Soc='%s' AND a.Año='%s' AND a.Nro_Solp='%s' ORDER BY a.Item_Solp;" %(Cod_Soc, Año, Numero_Solp)

        actualizarSOLP(self,self.tbwRegistro_SOLP,sqldetalleSOLP,estadosDoc,Cod_Soc,Numero_Solp,Año)

        self.leNro_SOLP.setText(Numero_Solp)
        self.cbTipo_SOLP.setCurrentText(listcabecera[0])

        FechaSOLP=formatearFecha(listcabecera[3])
        self.leFecha_SOLP.setText(FechaSOLP)
        self.cbSolicitante.setCurrentText(listcabecera[2])
        self.cbArea.setCurrentText(listcabecera[1])
        self.cbEstado_SOLP.setCurrentIndex(int(listcabecera[4])-1)

        if listcabecera[5]!=None:
            self.teTexto_Cabecera.setText(listcabecera[5])
        else:
            print('Sin texto Cabecera')
            # mensajeDialogo("informacion", "Informacion", "Texto de Cabecera no registrado. Verifique")


        monto=formatearDecimal(listcabecera[6],'2')
        self.leMonto_SOLP.setText(monto)
        self.leMonto_SOLP.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)

        self.cbMoneda.setCurrentText(listcabecera[7])

        self.leNro_SOLP.setEnabled(False)
        self.cbMoneda.setEnabled(False)
        self.leMonto_SOLP.setEnabled(False)
        self.cbTipo_SOLP.setEnabled(False)
        self.cbArea.setEnabled(False)
        self.teTexto_Cabecera.setEnabled(False)
        self.cbSolicitante.setEnabled(False)
        self.leFecha_SOLP.setEnabled(False)
        self.cbEstado_SOLP.setEnabled(False)
        self.pbModificar.setEnabled(False)
        self.pbDarBaja.setEnabled(False)
        self.pbLiberar_SOLP.setEnabled(False)
        self.pbSeleccionar.setEnabled(False)
        self.pbNuevaSOLP.setEnabled(False)

    def Aprobar(self):
        try:
            # Fecha=datetime.now().strftime("%Y-%m-%d")
            # Hora=datetime.now().strftime("%H:%M:%S.%f")
            estado_Item=self.tbwRegistro_SOLP.item(self.tbwRegistro_SOLP.currentRow(),0).text()
            Item_Solp=self.tbwRegistro_SOLP.item(self.tbwRegistro_SOLP.currentRow(),1).text()

            if len(estado_Item)!=0:
                if estado_Item!='Aprobado':
                    reply = mensajeDialogo("pregunta", "Pregunta","¿Realmente desea Aprobar Item?")
                    if reply == 'Yes':
                        k = Item_Solp
                        v = '5'
                        dict_temp = {}
                        dict_temp.setdefault(k,v)
                        dict_estadoPosicion.update(dict_temp)
                        print(dict_estadoPosicion)
                        # Estado_Item=5
                        # sqlAprobar="UPDATE TAB_SOLP_002_Detalle_Solicitud_Pedido SET Estado_Item='%s',Fecha_Mod='%s',Hora_Mod='%s',Usuario_Mod='%s' WHERE Cod_Soc='%s'AND Año='%s'AND Nro_Solp='%s'AND Item_Solp='%s'"%(Estado_Item,Fecha,Hora,Cod_Usuario,Cod_Soc,Año,Numero_Solp,Item_Solp)
                        # respuesta=ejecutarSql(sqlAprobar)
                        # if respuesta['respuesta']=='correcto':
                        #     mensajeDialogo("informacion", "Informacion", "Item fue Aprobado")
            #--------------------------------------------------
                        Estado_Item=QTableWidgetItem("Aprobado")
                        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                        Estado_Item.setFlags(flags)
                        Estado_Item.setTextAlignment(QtCore.Qt.AlignCenter)
                        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
                        brush.setStyle(QtCore.Qt.SolidPattern)
                        Estado_Item.setForeground(brush)
                        self.tbwRegistro_SOLP.setItem(self.tbwRegistro_SOLP.currentRow(),0, Estado_Item)
                        self.tbwRegistro_SOLP.resizeColumnToContents(0)
                        # elif respuesta['respuesta']=='incorrecto':
                        #     mensajeDialogo("error", "Error", "No se pudo Aprobar a Item")

                else:
                    mensajeDialogo("error", "Error", "Item ya fue Aprobado")
                # elif Estado_Item=="Anulado":
                #     mensajeDialogo("error", "Error", "Item Anulado sin acceso a Aprobar")

            else:
                mensajeDialogo("error", "Error", "Seleccione fila con datos")

        except Exception as e:
            mensajeDialogo("error", "Error", "Seleccione una fila")
            print(e)

    def Rechazar(self):
        try:
            # Fecha=datetime.now().strftime("%Y-%m-%d")
            # Hora=datetime.now().strftime("%H:%M:%S.%f")
            estado_Item=self.tbwRegistro_SOLP.item(self.tbwRegistro_SOLP.currentRow(),0).text()
            Item_Solp=self.tbwRegistro_SOLP.item(self.tbwRegistro_SOLP.currentRow(),1).text()

            if len(estado_Item)!=0:
                if estado_Item!='Rechazado':
                    reply = mensajeDialogo("pregunta", "Pregunta","¿Realmente desea Rechazar el Item?")
                    if reply == 'Yes':
                        k = Item_Solp
                        v = '4'
                        dict_temp = {}
                        dict_temp.setdefault(k,v)
                        dict_estadoPosicion.update(dict_temp)
                        print(dict_estadoPosicion)
                        # Estado_Item=4
                        # sqlAprobar="UPDATE TAB_SOLP_002_Detalle_Solicitud_Pedido SET Estado_Item='%s',Fecha_Mod='%s',Hora_Mod='%s',Usuario_Mod='%s' WHERE Cod_Soc='%s'AND Año='%s'AND Nro_Solp='%s'AND Item_Solp='%s'"%(Estado_Item,Fecha,Hora,Cod_Usuario,Cod_Soc,Año,Numero_Solp,Item_Solp)
                        # respuesta=ejecutarSql(sqlAprobar)
                        # if respuesta['respuesta']=='correcto':
                        #     mensajeDialogo("informacion", "Informacion", "Item fue Anulado")
            #--------------------------------------------------
                        Estado_Item=QTableWidgetItem("Rechazado")
                        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                        Estado_Item.setFlags(flags)
                        Estado_Item.setTextAlignment(QtCore.Qt.AlignCenter)
                        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
                        brush.setStyle(QtCore.Qt.SolidPattern)
                        Estado_Item.setForeground(brush)
                        self.tbwRegistro_SOLP.setItem(self.tbwRegistro_SOLP.currentRow(),0, Estado_Item)
                        self.tbwRegistro_SOLP.resizeColumnToContents(0)
                        # elif respuesta['respuesta']=='incorrecto':
                        #     mensajeDialogo("error", "Error", "No se pudo Anular a Item")

                else:
                    mensajeDialogo("error", "Error", "Item ya fue Rechazado")
                # elif Estado_Item=="Aprobado":
                #     mensajeDialogo("error", "Error", "Item Aprobado, sin acceso a Anular")

            else:
                mensajeDialogo("error", "Error", "Seleccione fila con datos")

        except Exception as e:
            mensajeDialogo("error", "Error", "Seleccione una fila")
            print(e)

    def Grabar(self):
        rows=self.tbwRegistro_SOLP.rowCount()
        EstadoSolp=self.cbEstado_SOLP.currentText()
        lista_estado=[]
        for row in range(rows):
            Estado_Item=self.tbwRegistro_SOLP.item(row,0).text()
            lista_estado.append(Estado_Item)

        Ap=lista_estado.count('Aprobado')
        An=lista_estado.count('Rechazado')

        if EstadoSolp!='Aprobado'and EstadoSolp!='Anulado':
            Fecha=datetime.now().strftime("%Y-%m-%d")
            Hora=datetime.now().strftime("%H:%M:%S.%f")
            if Ap!=0:
                Estado_SOLP=5
                sqlEstadoSolp="UPDATE TAB_SOLP_001_Cabecera_Solicitud_Pedido SET Estado_Solp='%s',Aprobado_Por='%s',Fecha_Mod='%s',Hora_Mod='%s',Usuario_Mod='%s' WHERE Cod_Soc='%s'AND Año='%s'AND Nro_Solp='%s'"%(Estado_SOLP,Cod_Usuario,Fecha,Hora,Cod_Usuario,Cod_Soc,Año,Numero_Solp)
                respuesta=ejecutarSql(sqlEstadoSolp)
                sqlAprobar="UPDATE TAB_SOLP_002_Detalle_Solicitud_Pedido SET Estado_Item='%s',Fecha_Mod='%s',Hora_Mod='%s',Usuario_Mod='%s' WHERE Cod_Soc='%s'AND Año='%s'AND Nro_Solp='%s'AND Item_Solp='%s'"%(Estado_Item,Fecha,Hora,Cod_Usuario,Cod_Soc,Año,Numero_Solp,Item_Solp)
                respuesta=ejecutarSql(sqlAprobar)
                if respuesta['respuesta']=='correcto':
                    mensajeDialogo("informacion", "Informacion", "Requerimiento se grabo correctamente, paso a Estado Aprobado")
                    self.cbEstado_SOLP.setCurrentIndex(4)
                elif respuesta['respuesta']=='incorrecto':
                    mensajeDialogo("error", "Error", "Requerimiento no cambio de Estado")

            elif An==rows:
                Estado_SOLP=4
                sqlEstadoSolp="UPDATE TAB_SOLP_001_Cabecera_Solicitud_Pedido SET Estado_Solp='%s',Fecha_Mod='%s',Hora_Mod='%s',Usuario_Mod='%s' WHERE Cod_Soc='%s'AND Año='%s'AND Nro_Solp='%s'"%(Estado_SOLP,Fecha,Hora,Cod_Usuario,Cod_Soc,Año,Numero_Solp)
                respuesta=ejecutarSql(sqlEstadoSolp)
                if respuesta['respuesta']=='correcto':
                    mensajeDialogo("informacion", "Informacion", "Requerimiento se grabo correctamente, paso a Estado Anulado")
                    self.cbEstado_SOLP.setCurrentIndex(3)
                elif respuesta['respuesta']=='incorrecto':
                    mensajeDialogo("error", "Error", "Requerimiento no cambio de Estado")

            else:
                mensajeDialogo("error", "Error", "Para Grabar Apruebe o Rechace uno o mas Items")

        else:
            mensajeDialogo("error", "Error", "Requerimiento ya fue grabado")

    def TextoPosicion(self):
        try:
            fila=self.tbwRegistro_SOLP.currentRow()
            NroSolPedido=self.leNro_SOLP.text()
            Item_Solp=self.tbwRegistro_SOLP.item(fila,1).text()
            TextoPosicion(NroSolPedido,Item_Solp).exec_()
            actualizarboton(self,self.tbwRegistro_SOLP,Cod_Soc,Año,Numero_Solp,Item_Solp,fila)

        except:
            mensajeDialogo("error", "Error", "Complete los Campos")

class TextoPosicion(QDialog):
    def __init__(self,NroSolPedido,Item_Solp):
        QDialog.__init__(self)
        uic.loadUi('ERP_REQ_P002_Texto_Posicion.ui',self)

        global NroDoc,ItemDoc

        NroDoc=NroSolPedido
        ItemDoc=Item_Solp

        self.pbGrabarDetalle.clicked.connect(self.Grabar)
        self.pbModificarDetalle.clicked.connect(self.Modificar)

        sqlText="SELECT Texto FROM TAB_SOC_019_Texto_Proceso WHERE Cod_Soc='%s'AND Año='%s' AND Tipo_Proceso='1' AND Nro_Doc='%s' AND Item_Doc='%s'"%(Cod_Soc,Año,NroDoc,ItemDoc)
        text= consultarSql(sqlText)
        if text!=[]:
            self.teDetalle.setText(text[0][0])
            font = QtGui.QFont()
            font.setPointSize(12)
            self.teDetalle.setFont(font)
            self.teDetalle.setEnabled(False)
            self.pbGrabarDetalle.setEnabled(False)
        elif text==[]:
            self.pbModificarDetalle.setEnabled(False)

        cargarIcono(self.pbGrabarDetalle,'grabar')
        cargarIcono(self.pbModificarDetalle,'modificar')

    def Grabar(self):

        Texto=self.teDetalle.toPlainText()
        if len(Texto)!=0:
            Fecha=datetime.now().strftime("%Y-%m-%d")
            Hora=datetime.now().strftime("%H:%M:%S.%f")

            sqlTex="SELECT Texto FROM TAB_SOC_019_Texto_Proceso WHERE Cod_Soc='%s'AND Año='%s' AND Tipo_Proceso='1' AND Nro_Doc='%s' AND Item_Doc='%s'"%(Cod_Soc,Año,NroDoc,ItemDoc)
            tex= consultarSql(sqlTex)

            if tex==[]:
                sqlTexto="INSERT INTO TAB_SOC_019_Texto_Proceso(Cod_Soc, Año, Tipo_Proceso, Nro_Doc, Item_Doc, Texto, Fecha_Reg, Hora_Reg, Usuario_Reg) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(Cod_Soc,Año,1,NroDoc,ItemDoc,Texto,Fecha,Hora,Cod_Usuario)
                respuesta=ejecutarSql(sqlTexto)
                if respuesta['respuesta']=='correcto':
                    mensajeDialogo("informacion", "Informacion", "Texto grabado con éxito")
                    self.pbGrabarDetalle.setEnabled(False)
                    self.pbModificarDetalle.setEnabled(True)
                    self.teDetalle.setEnabled(False)

                elif respuesta['respuesta']=='incorrecto':
                    mensajeDialogo("error", "Error", "El Texto no se pudo grabar")

            elif tex!=[]:
                sqlTexto="UPDATE TAB_SOC_019_Texto_Proceso SET Texto='%s',Fecha_Mod='%s',Hora_Mod='%s',Usuario_Mod='%s' WHERE Cod_Soc='%s' AND Año='%s' AND Tipo_Proceso='1' AND Nro_Doc='%s' AND Item_Doc='%s' "%(Texto,Fecha,Hora,Cod_Usuario,Cod_Soc,Año,NroDoc,ItemDoc)
                respuesta=ejecutarSql(sqlTexto)
                if respuesta['respuesta']=='correcto':
                    mensajeDialogo("informacion", "Informacion", "Texto modificado con éxito")
                    self.pbGrabarDetalle.setEnabled(False)
                    self.pbModificarDetalle.setEnabled(True)
                    self.teDetalle.setEnabled(False)
                elif respuesta['respuesta']=='incorrecto':
                    mensajeDialogo("error", "Error", "El Texto no se pudo modificar")

        else:
            mensajeDialogo("error", "Error", "¡No se puede Grabar texto vacio!")

    def Modificar(self):
        self.teDetalle.setEnabled(True)
        self.pbGrabarDetalle.setEnabled(True)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    _main=Consultar()
    _main.showMaximized()
    app.exec_()
