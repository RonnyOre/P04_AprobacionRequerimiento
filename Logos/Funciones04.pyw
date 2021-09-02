import requests
import re
import sys
import time
from decimal import Decimal
from datetime import date, datetime, timedelta
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
import urllib.request
from PyQt5 import*

url = 'http://www.multiplay.com.pe/consultas/consulta-prueba.php'

#--------------------------------PROGRAMA N°1----------------------------------

def ejecutarSql(sql):
    datos = {'accion':'ejecutar','sql': sql}
    x = requests.post(url, data = datos)
    if x.text!="":
        respuesta=x.json()
        if respuesta!=[]:
            print(respuesta)
    else:
        print("respuesta vacía")
    return respuesta

def consultarSql(sql):
    datos = {'accion':'leer','sql': sql}
    x = requests.post(url, data=datos)
    respuesta=x.json()
    myresult=[]
    if respuesta!=[]:
        for datos in respuesta:
            contenido=[]
            for k,dato in datos.items():
                contenido.append(dato)
            myresult.append(contenido)

    return myresult

def cargarLogo(lb, codSoc):
    try:
        if codSoc == 'multiplay':
            codSoc = 'Mp_st'
        folderLogo = '''Logos/Logo'''+ codSoc +'.png'
        logoSoc = QPixmap(folderLogo)
        ratio = QtCore.Qt.KeepAspectRatio
        logoSoc = logoSoc.scaled(250, 35, ratio)
        lb.setPixmap(logoSoc)
    except:
        ""

def cargarIcono(obj, tipoIcono):
    try:
        iconos = {
        'añadir': "add",
        'texto': "articulo",
        'banco':"banco",
        'copiar': "copy",
        'deposito':"deposit",
        'registrar': "clipboard",
        'guardar': "diskette",
        'grabar': "diskette",
        'documentos': "documents",
        'editar': "edit",
        'modificar': "edit",
        'nuevo':"file",
        'finalizar': "finalizar",
        'imagen': "imagen",
        'direccion':"location",
        'salir': "logout",
        'buscar': "loupe",
        'erp': "organization",
        'pdf': "pdf",
        'imprimir': "printer",
        'compra':"purchasing",
        'material': "router",
        'cargar': "sand-clock",
        'usuario': "user",
        'verificar': "verify",
        'visualizar': "visualizar",
        'darbaja': "x-button"}
        icono = iconos[tipoIcono]
        folderIcono = '''IconosLocales/'''+ icono +'.png'
        icon = QPixmap(folderIcono)
        if tipoIcono != 'erp':
            obj.setIcon(QIcon(icon))
        else:
            obj.setWindowIcon(QIcon(icon))
    except:
        ""

#--------------------------------PROGRAMA N°2----------------------------------

def actualizar(tw,sql):
    tw.clearContents()
    informacion=consultarSql(sql)
    flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    row=0
    for fila in informacion:
        col=0
        for i in fila:
            if i!=fila[3]:
                item=QTableWidgetItem(i)
                item.setFlags(flags)
                if tw.rowCount()<=row:
                    tw.insertRow(tw.rowCount())
                tw.setItem(row, col, item)
                col += 1
        if fila[3]=="1":
            C4=QTableWidgetItem(str("ACTIVO"))
            C4.setFlags(flags)
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            tw.setItem(row, 4, C4)
        else:
            C4=QTableWidgetItem(str("BAJA"))
            C4.setFlags(flags)
            font = QtGui.QFont()
            font.setPointSize(12)
            C4.setFont(font)
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            C4.setForeground(brush)
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            tw.setItem(row, 4, C4)
        row+=1

def convlist(sql):
    informacion=consultarSql(sql)
    lista = []
    for info in informacion:
        for elemento in info:
            lista.append(elemento)
    return lista

def insertarDatos(cb, Datos):
    cb.clear()
    for dato in Datos:
        cb.addItem(dato[0])

def NombreUbigeo(CodPais,CodDepartamento,CodProvincia,CodDistrito,TablaUbigeo):
    NombreUBI={}
    try:
        NombreUBI["Pais"]=TablaUbigeo[CodPais+"-0-0-0"]
    except:
        NombreUBI["Pais"]=""
    if NombreUBI["Pais"]=="Peru":
        try:
            if CodDepartamento!="0":
                NombreUBI["Departamento"]=TablaUbigeo[CodPais+"-"+CodDepartamento+"-0-0"]
            else:
                NombreUBI["Departamento"]=""
        except:
            NombreUBI["Departamento"]=""
        try:
            if CodProvincia!="0" and CodDepartamento!="0":
                NombreUBI["Provincia"]=TablaUbigeo[CodPais+"-"+CodDepartamento+"-"+CodProvincia+"-0"]
            else:
                NombreUBI["Provincia"]=""
        except:
            NombreUBI["Provincia"]=""
        try:
            if CodDistrito!="0" and CodProvincia!="0" and CodDepartamento!="0":
                NombreUBI["Distrito"]=TablaUbigeo[CodPais+"-"+CodDepartamento+"-"+CodProvincia+"-"+CodDistrito]
            else:
                NombreUBI["Distrito"]=""
        except:
            NombreUBI["Distrito"]=""
    else:
        try:
            if CodDepartamento!="0":
                NombreUBI["Departamento"]=TablaUbigeo[CodPais+"-"+CodDepartamento+"-0-0"]
            else:
                NombreUBI["Departamento"]=""
        except:
            NombreUBI["Departamento"]=""
        NombreUBI["Provincia"]=""
        NombreUBI["Distrito"]=""
    return NombreUBI

def TablaUbigeo(sql):
    ubicacion=consultarSql(sql)
    tablaUbigeo={}
    for item in ubicacion:
        tablaUbigeo[item[0]+"-"+item[1]+"-"+item[2]+"-"+item[3]]=item[4]
    return tablaUbigeo

#---------------------------------PROGRAMA N°3----------------------------------

def actualizarInter(tw,sql,Tipo_Inter,dicTipoInter):
    tw.clearContents()
    informacion=consultarSql(sql)
    if informacion!=[]:
        rows=tw.rowCount()
        for r in range(rows):
            tw.removeRow(1)
        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        row=0
        for fila in informacion:
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            cb = QComboBox(tw)
            tw.setCellWidget(row, 0, cb)
            insertarDatos(cb,Tipo_Inter)
            cb.setEditable(True)
            for k,v in dicTipoInter.items():
                if fila[0]==k:
                    tw.cellWidget(row, 0).setEditText(v)
            font = QtGui.QFont()
            font.setPointSize(12)
            cb.setFont(font)
            # font = QFont('Times', 12)
            le = cb.lineEdit()
            le.setFont(font)
            tw.resizeColumnToContents(0)
            tw.cellWidget(row, 0).setEnabled(False)

            col=1
            for i in fila:
                if i!=fila[0] and i!=fila[7]:
                    item=QTableWidgetItem(i)
                    item.setFlags(flags)
                    if tw.rowCount()<=row:
                        tw.insertRow(tw.rowCount())
                    tw.setItem(row, col, item)
                    col += 1

            if fila[7]=="1":
                C7=QTableWidgetItem(str("ACTIVO"))
                C7.setFlags(flags)
                if tw.rowCount()<=row:
                    tw.insertRow(tw.rowCount())
                tw.setItem(row, 7, C7)
            else:
                C7=QTableWidgetItem(str("BAJA"))
                C7.setFlags(flags)
                font = QtGui.QFont()
                font.setPointSize(12)
                C7.setFont(font)
                brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                C7.setForeground(brush)
                if tw.rowCount()<=row:
                    tw.insertRow(tw.rowCount())
                tw.setItem(row, 7, C7)
            row+=1
    else:
        cb = QComboBox(tw)
        tw.setCellWidget(0, 0, cb)
        insertarDatos(cb,Tipo_Inter)
        cb.setCurrentIndex(-1)
        font = QtGui.QFont()
        font.setPointSize(12)
        cb.setFont(font)
        tw.resizeColumnToContents(0)

        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        item=QTableWidgetItem()
        item.setFlags(flags)
        tw.setItem(0,7, item)

def actualizarBan(self,tw,sql,datos,TCta,dicbanco,banco,dicmoneda,mon):
    tw.clearContents()

    informacion=consultarSql(sql)

    if informacion!=[]:
        rows=tw.rowCount()
        for r in range(rows):
            tw.removeRow(1)
        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        row=0
        for fila in informacion:
            C0=QTableWidgetItem(fila[0])
            C0.setFlags(flags)
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            tw.setItem(row,0, C0)
            tw.resizeColumnToContents(0)

            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            cb1 = QComboBox(tw)
            # cb1.setEditable(True)
            tw.setCellWidget(row, 1, cb1)
            llenarPais(datos,cb1)
            cb1.setCurrentIndex(int(fila[1])-1)
            # tw.cellWidget(row, 1).setEditText(fila[1])
            font = QtGui.QFont()
            font.setPointSize(12)
            cb1.setFont(font)
            tw.resizeColumnToContents(1)
            tw.cellWidget(row, 1).setEnabled(False)
            cb1.activated.connect(self.cargarDepartamento)

            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            cb2 = QComboBox(tw)
            # cb2.setEditable(True)
            tw.setCellWidget(row, 2, cb2)
            Paisx=fila[1]
            llenarDepartamento(datos,cb2,Paisx)
            cb2.setCurrentIndex(int(fila[2])-1)
            # tw.cellWidget(row, 2).setEditText(fila[2])
            font = QtGui.QFont()
            font.setPointSize(12)
            cb2.setFont(font)
            tw.resizeColumnToContents(2)
            tw.cellWidget(row, 2).setEnabled(False)

            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            cb3 = QComboBox(tw)
            # cb3.setEditable(True)
            tw.setCellWidget(row, 3, cb3)
            insertarDatos(cb3,banco)
            cb3.setCurrentIndex(int(fila[3])-1)
            # tw.cellWidget(row, 3).setEditText(fila[3])
            font = QtGui.QFont()
            font.setPointSize(12)
            cb3.setFont(font)
            tw.resizeColumnToContents(3)
            tw.cellWidget(row, 3).setEnabled(False)


            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            cb4 = QComboBox(tw)
            # cb4.setEditable(True)
            tw.setCellWidget(row, 4, cb4)
            for k,v in TCta.items():
                cb4.addItem(k)
            if fila[4]=="CA":
                cb4.setCurrentIndex(0)
            elif fila[4]=="CC":
                cb4.setCurrentIndex(1)
            font = QtGui.QFont()
            font.setPointSize(12)
            cb4.setFont(font)
            tw.resizeColumnToContents(4)
            tw.cellWidget(row,4).setEnabled(False)

            C5=QTableWidgetItem(fila[5])
            C5.setFlags(flags)
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            tw.setItem(row,5, C5)

            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            cb6 = QComboBox(tw)
            # cb6.setEditable(True)
            tw.setCellWidget(row, 6, cb6)
            insertarDatos(cb6,mon)

            cb6.setCurrentIndex(int(fila[6])-1)
            # tw.cellWidget(row, 8).setEditText(fila[6])
            font = QtGui.QFont()
            font.setPointSize(12)
            cb6.setFont(font)
            tw.resizeColumnToContents(6)
            tw.cellWidget(row, 6).setEnabled(False)

            C7=QTableWidgetItem(fila[7])
            C7.setFlags(flags)
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            tw.setItem(row,7, C7)

            if fila[8]=="1":
                C8=QTableWidgetItem(str("ACTIVO"))
                C8.setFlags(flags)
                if tw.rowCount()<=row:
                    tw.insertRow(tw.rowCount())
                tw.setItem(row,8, C8)
            else:
                C8=QTableWidgetItem(str("BAJA"))
                C8.setFlags(flags)
                font = QtGui.QFont()
                font.setPointSize(12)
                C8.setFont(font)
                brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                C8.setForeground(brush)
                if tw.rowCount()<=row:
                    tw.insertRow(tw.rowCount())
                tw.setItem(row, 8, C8)
            row+=1
    else:
        cb0 = QComboBox(tw)
        tw.setCellWidget(0, 1, cb0)
        for k,v in datos.items():
            codigo=k.split("-")
            if "-".join(codigo[1:])=="0-0-0":
                cb0.addItem(v)
        cb0.setCurrentIndex(-1)
        # cb0.setStyleSheet("background-color: rgb(255,255,255);")
        font = QtGui.QFont()
        font.setPointSize(12)
        cb0.setFont(font)
        tw.resizeColumnToContents(1)
        cb0.activated.connect(self.cargarDepartamento)

        #creacion combo departamento...
        cb1 = QComboBox(tw)
        tw.setCellWidget(0, 2, cb1)
        cb1.setCurrentIndex(-1)
        # cb1.setStyleSheet("background-color: rgb(255,255,255);")
        font = QtGui.QFont()
        font.setPointSize(12)
        cb1.setFont(font)
        tw.resizeColumnToContents(2)

        #creacion combo tipo de banco...
        cb2 = QComboBox(tw)
        tw.setCellWidget(0, 3, cb2)
        insertarDatos(cb2,banco)
        cb2.setCurrentIndex(-1)
        # cb2.setStyleSheet("background-color: rgb(255,255,255);")
        font = QtGui.QFont()
        font.setPointSize(12)
        cb2.setFont(font)
        tw.resizeColumnToContents(3)

        #creacion combo tipo de cuenta...
        cb3 = QComboBox(tw)
        tw.setCellWidget(0, 4, cb3)
        for k,v in TCta.items():
            cb3.addItem(k)
        cb3.setCurrentIndex(-1)
        # cb3.setStyleSheet("background-color: rgb(255,255,255);")
        font = QtGui.QFont()
        font.setPointSize(12)
        cb3.setFont(font)
        tw.resizeColumnToContents(4)

        cb4 = QComboBox(tw)
        tw.setCellWidget(0, 6, cb4)
        insertarDatos(cb4,mon)
        cb4.setCurrentIndex(-1)
        # cb4.setStyleSheet("background-color: rgb(255,255,255);")
        font = QtGui.QFont()
        font.setPointSize(12)
        cb4.setFont(font)
        tw.resizeColumnToContents(6)

        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        Nro=QTableWidgetItem("1")
        Nro.setFlags(flags)
        tw.setItem(0,0, Nro)

        item=QTableWidgetItem()
        item.setFlags(flags)
        tw.setItem(0,8, item)
        tw.resizeColumnToContents(0)

def actualizarComp(tw,sql):
    tw.clearContents()
    informacion=consultarSql(sql)
    if informacion!=[]:
        rows=tw.rowCount()
        for r in range(rows):
            tw.removeRow(1)
        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        row=0
        for fila in informacion:
            tw.resizeColumnToContents(0)
            tw.resizeColumnToContents(5)
            col=0
            for i in fila:
                item=QTableWidgetItem(i)
                item.setFlags(flags)
                # item.setTextAlignment(QtCore.Qt.AlignHCenter)
                if tw.rowCount()<=row:
                    tw.insertRow(tw.rowCount())
                tw.setItem(row, col, item)
                # tw.resizeColumnToContents(col)
                col += 1
            row+=1
    else:
        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        Nro=QTableWidgetItem("1")
        Nro.setFlags(flags)
        tw.setItem(0,0, Nro)
        tw.resizeColumnToContents(0)
        tw.resizeColumnToContents(5)

def consultaRucLE(RUC,self): #NUEVO
    try:
        r = requests.get("https://api.sunat.cloud/ruc/" + str(RUC))
        data=r.json()
        if not data:
            QMessageBox.information(self, "Consulta RUC", "No se encontró el RUC " + str(RUC), QMessageBox.Discard)
            self.close()
            return;
        RazonSocial=data["razon_social"]
        NombreComercial=data["nombre_comercial"]
        Direccion=data["domicilio_fiscal"]
        Estado=data["contribuyente_estado"]
        RepresentanteLegal=data["representante_legal"]
        return [RazonSocial, NombreComercial, Direccion, Estado, RepresentanteLegal]

    except requests.exceptions.ConnectionError:

        payload = {'ruc': str(RUC)}
        r = requests.get("http://www.multiplay.com.pe/consultas/sunat.php",params=payload, verify=False, timeout=5)
        data=r.json()
        if not data:
            QMessageBox.information(self, "Consulta RUC", "No se encontró el RUC " + str(RUC), QMessageBox.Discard)
            return;
        RazonSocial=data["nombre_o_razon_social"]
        NombreComercial="-"
        Direccion=data["direccion"]
        Estado=data["estado_del_contribuyente"]
        return [RazonSocial, NombreComercial, Direccion, Estado]

def extrdata(self):
    data=[]
    NumCol=self.columnCount()
    for col in range(NumCol):
        if col!=1:
            item=self.item(self.currentRow(),col).text()
            data.append(item)
    return data

def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield (key, value)
            yield from recursive_items(value)
        else:
            yield (key, value)

def llenarPais(TablaUbigeo,cbPais):  #Codigo pais va 0
    for ubigeo,nombre in TablaUbigeo.items():
        au=ubigeo.find("-")
        bu=ubigeo.find("-",au+1)
        cu=ubigeo.find("-",bu+1)
        if ubigeo[au+1:]=="0-0-0":
            cbPais.addItem(nombre)

def llenarDepartamento(TablaUbigeo,cbDepartamento,codigoPais):  #Codigo pais va 0
    for ubigeo,nombre in TablaUbigeo.items():
        au=ubigeo.find("-")
        bu=ubigeo.find("-",au+1)
        cu=ubigeo.find("-",bu+1)
        if ubigeo[:au]==codigoPais and ubigeo[au+1:]!="0-0-0" and ubigeo[bu+1:]=="0-0":
            cbDepartamento.addItem(nombre)

def llenarDep(TablaUbigeo,cbDepartamento,codigoPais):  #Codigo pais va 0
    cbDepartamento.clear()
    for ubigeo,nombre in TablaUbigeo.items():
        au=ubigeo.find("-")
        bu=ubigeo.find("-",au+1)
        cu=ubigeo.find("-",bu+1)
        if ubigeo[:au]==codigoPais and ubigeo[au+1:]!="0-0-0" and ubigeo[bu+1:]=="0-0":
            cbDepartamento.addItem(ubigeo[au+1:bu]+" - "+nombre)
            cbDepartamento.setCurrentIndex(-1)

def verificarTIP(tw):
    TIP=[]
    A=tw.rowCount()
    B=tw.currentRow()
    for fila in range(A-(A-B)):
        item=tw.cellWidget(fila, 0).currentText()
        TIP.append(item)
    return TIP

#--------------------------------PROGRAMA N°4----------------------------------
def Cargar(self,tw,sql,dicArea,dicSoli,Inicio,Final,Fec_Inicial,Fec_Final,Cod_Soc):
    tw.clearContents()
    informacion=consultarSql(sql)
    if informacion!=[]:
        rows=tw.rowCount()
        for r in range(rows):
            tw.removeRow(1)
        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        row=0
        for fila in informacion:
            C0=QTableWidgetItem(fila[0])
            C0.setFlags(flags)
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            tw.setItem(row,0, C0)
            # tw.resizeColumnToContents(0)

            FechaSolp=formatearFecha(fila[1])
            C1=QTableWidgetItem(FechaSolp)
            C1.setFlags(flags)
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            tw.setItem(row,1, C1)
            # tw.resizeColumnToContents(1)

            FechaReq=formatearFecha(fila[2])
            C2=QTableWidgetItem(FechaReq)
            C2.setFlags(flags)
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            tw.setItem(row,2, C2)

            for k,v in dicSoli.items():
                if fila[3]==k:
                    C3=QTableWidgetItem(v)
                    C3.setFlags(flags)
                    if tw.rowCount()<=row:
                        tw.insertRow(tw.rowCount())
                    tw.setItem(row,3, C3)

            for k,v in dicArea.items():
                if fila[4]==k:
                    C4=QTableWidgetItem(v)
                    C4.setFlags(flags)
                    if tw.rowCount()<=row:
                        tw.insertRow(tw.rowCount())
                    tw.setItem(row,4, C4)

            now = datetime.now()
            Añito=str(now.year)
            Año=int(Añito)-1
            sqlMonto="SELECT SUM(Cant_Mat_Serv*Precio_ref) FROM `TAB_SOLP_002_Detalle_Solicitud_Pedido` WHERE Cod_Soc='%s' AND Año='%s' AND Nro_Solp='%s'"%(Cod_Soc,Año,fila[0])
            Monto=convlist(sqlMonto)

            f5=round(Decimal(Monto[0]),3)
            C5=QTableWidgetItem(str(f5))
            C5.setFlags(flags)
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            tw.setItem(row,5, C5)

            pb = QPushButton("Consultar",tw)
            tw.setCellWidget(row, 6, pb)
            font = QtGui.QFont()
            font.setPointSize(12)
            pb.setFont(font)
            tw.resizeColumnToContents(6)

            row+=1
    else:
        QMessageBox.critical(self, "Error","No se encontraron solicitudes de pedido en este rango", QMessageBox.Ok)
        Inicio.setCurrentIndex(-1)
        Final.setCurrentIndex(-1)
        Fec_Inicial.clear()
        Fec_Final.clear()

def QDateToStrView(Qdate):
    a1=str(Qdate.date().year())
    m1=str(Qdate.date().month())
    d1=str(Qdate.date().day())

    if len(d1)==1:
        d1='0'+d1
    if len(m1)==1:
        m1='0'+m1
    # strFecha="%s-%s-%s" % (a1,m1,d1)
    strFecha="%s-%s-%s" % (d1,m1,a1)

    return strFecha

    # def formatearFecha1(fecha):
    #     if fecha=="":
    #         return ""
    #     fecha=fecha.split("/")
    #     fecha.reverse()
    #     return "-".join(fecha)

def formatearFecha(fecha):
    if fecha=="":
        return ""
    fecha=fecha.split("-")
    fecha.reverse()
    return "-".join(fecha)
