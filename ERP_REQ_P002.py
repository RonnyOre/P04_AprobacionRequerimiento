import sys
from datetime import datetime
from Funciones04 import *
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import urllib.request
from ERP_REQ_P002_Consultar import Consultar

sqlTipo_Solp="SELECT `Descrip_Tip_Solp`,`Tipo_Solp` FROM `TAB_SOLP_003_Solicitud Pedido`"

Estado_Solp={'1':'Activo','2':'-','3':'Para Aprobación','4':'Anulado','5':'Aprobado','6':'Proceso de invitacion','7':'--','8':'Prov. Cotizo','9':'Concluido'}

class ERP_REQ_P002(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("ERP_PSOLP_003.ui",self)

        self.pbSalir.clicked.connect(self.Salir)
        self.cbTipo_SOLP.activated.connect(self.TipoSOLP)
        self.pbCargar.clicked.connect(self.Cargar)
        self.deInicial.dateChanged.connect(self.Fecha_Inicial)
        self.deFinal.setDateTime(QtCore.QDateTime.currentDateTime())
        self.deFinal.dateChanged.connect(self.Fecha_Final)

    def datosGenerales(self, codSoc, empresa, usuario):
        global Cod_Soc, Nom_Soc, Cod_Usuario,TipoSolp
        Cod_Soc = codSoc
        Nom_Soc = empresa
        Cod_Usuario = usuario

        cargarLogo(self.lbLogo_Mp,'multiplay')
        cargarLogo(self.lbLogo_Soc, Cod_Soc)
        cargarIcono(self, 'erp')
        cargarIcono(self.pbSalir, 'salir')
        cargarIcono(self.pbCargar, 'cargar')

        #Diccionario tipos de documento
        Tipo_Solp=consultarSql(sqlTipo_Solp)
        TipoSolp={}
        for dato in Tipo_Solp:
            TipoSolp[dato[1]]=dato[0]

        insertarDatos(self.cbTipo_SOLP,Tipo_Solp)
        self.cbTipo_SOLP.setCurrentIndex(-1)

    def TipoSOLP(self):
        self.leInicial.clear()
        self.leFinal.clear()
        self.tbwSolicitud_Pedido_Autorizar.clearContents()
        rows=self.tbwSolicitud_Pedido_Autorizar.rowCount()
        for r in range(rows):
            self.tbwSolicitud_Pedido_Autorizar.removeRow(1)
        TS=self.cbTipo_SOLP.currentText()
        for k,v in TipoSolp.items():
            if TS==v:
                Tipo_Solp=k

        now = datetime.now()
        Año=str(now.year)

        sqlNro_Solp="SELECT Nro_Solp FROM TAB_SOLP_001_Cabecera_Solicitud_Pedido WHERE Cod_Soc='%s' AND Año='%s' AND Tipo_solp='%s' AND Estado_Solp='3'" %(Cod_Soc,Año,Tipo_Solp)
        Nro_Solp=consultarSql(sqlNro_Solp)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cbNro_Inicial.setEditable(True)

        self.cbNro_Inicial.setFont(font)
        In = self.cbNro_Inicial.lineEdit()
        In.setFont(font)

        self.cbNro_Final.setEditable(True)
        self.cbNro_Final.setFont(font)
        Fi = self.cbNro_Final.lineEdit()
        Fi.setFont(font)

        insertarDatos(self.cbNro_Inicial,Nro_Solp)
        self.cbNro_Inicial.setCurrentIndex(-1)
        insertarDatos(self.cbNro_Final,Nro_Solp)
        self.cbNro_Final.setCurrentIndex(-1)

    def Fecha_Inicial(self):
        Fec_Inicial=QDateToStrView(self.deInicial)
        self.leInicial.setReadOnly(True)
        self.leInicial.setText(Fec_Inicial)

    def Fecha_Final(self):
        Fec_Final=QDateToStrView(self.deFinal)
        self.leFinal.setReadOnly(True)
        self.leFinal.setText(Fec_Final)

    def Cargar(self):
        try:
            self.tbwSolicitud_Pedido_Autorizar.clearContents()
            rows=self.tbwSolicitud_Pedido_Autorizar.rowCount()
            for r in range(rows):
                self.tbwSolicitud_Pedido_Autorizar.removeRow(1)

            Nro_Inicial=self.cbNro_Inicial.currentText()
            Nro_Final=self.cbNro_Final.currentText()
            Fec_Inicial=formatearFecha(self.leInicial.text())
            Fec_Final=formatearFecha(self.leFinal.text())

            TS=self.cbTipo_SOLP.currentText()
            for k,v in TipoSolp.items():
                if TS==v:
                    Tipo_Solp=k

            now = datetime.now()
            Año=str(now.year)

            if Nro_Inicial!='' and Nro_Final!='' and Fec_Inicial!='' and Fec_Final!='':
                sqlTabla="SELECT  a.Nro_Solp,a.Fecha_Solp, a.Fecha_Req_Global, c.Nom_usuario, d.Descripción_Área FROM TAB_SOLP_001_Cabecera_Solicitud_Pedido a LEFT JOIN TAB_SOC_005_Usuarios c ON a.Cod_Soc=c.Cod_Soc AND a.Solicita_Solp=c.Cod_usuario LEFT JOIN TAB_SOC_010_Áreas_de_la_empresa d ON a.Area_Solp=d.Cod_Área WHERE a.Cod_Soc='%s' AND a.Año='%s' AND a.Tipo_solp='%s' AND a.Estado_Solp='3' AND a.Nro_Solp >='%s' AND a.Nro_Solp<='%s'AND a.Fecha_Solp>='%s' AND a.Fecha_Solp<='%s';"%(Cod_Soc,Año,Tipo_Solp,Nro_Inicial,Nro_Final,Fec_Inicial,Fec_Final)

            elif Nro_Inicial!='' and Nro_Final!='' and Fec_Inicial!='' and Fec_Final=='':
                sqlTabla="SELECT  a.Nro_Solp,a.Fecha_Solp, a.Fecha_Req_Global, c.Nom_usuario, d.Descripción_Área FROM TAB_SOLP_001_Cabecera_Solicitud_Pedido a LEFT JOIN TAB_SOC_005_Usuarios c ON a.Cod_Soc=c.Cod_Soc AND a.Solicita_Solp=c.Cod_usuario LEFT JOIN TAB_SOC_010_Áreas_de_la_empresa d ON a.Area_Solp=d.Cod_Área WHERE a.Cod_Soc='%s' AND a.Año='%s' AND a.Tipo_solp='%s' AND a.Estado_Solp='3' AND a.Nro_Solp >='%s' AND a.Nro_Solp<='%s'AND a.Fecha_Solp>='%s';"%(Cod_Soc,Año,Tipo_Solp,Nro_Inicial,Nro_Final,Fec_Inicial)

            elif Nro_Inicial!='' and Nro_Final!='' and Fec_Inicial=='' and Fec_Final=='':
                sqlTabla="SELECT  a.Nro_Solp,a.Fecha_Solp, a.Fecha_Req_Global, c.Nom_usuario, d.Descripción_Área FROM TAB_SOLP_001_Cabecera_Solicitud_Pedido a LEFT JOIN TAB_SOC_005_Usuarios c ON a.Cod_Soc=c.Cod_Soc AND a.Solicita_Solp=c.Cod_usuario LEFT JOIN TAB_SOC_010_Áreas_de_la_empresa d ON a.Area_Solp=d.Cod_Área WHERE a.Cod_Soc='%s' AND a.Año='%s' AND a.Tipo_solp='%s' AND a.Estado_Solp='3' AND a.Nro_Solp >='%s' AND a.Nro_Solp<='%s';"%(Cod_Soc,Año,Tipo_Solp,Nro_Inicial,Nro_Final)

            elif Nro_Inicial!='' and Nro_Final=='' and Fec_Inicial=='' and Fec_Final=='':
                sqlTabla="SELECT  a.Nro_Solp,a.Fecha_Solp, a.Fecha_Req_Global, c.Nom_usuario, d.Descripción_Área FROM TAB_SOLP_001_Cabecera_Solicitud_Pedido a LEFT JOIN TAB_SOC_005_Usuarios c ON a.Cod_Soc=c.Cod_Soc AND a.Solicita_Solp=c.Cod_usuario LEFT JOIN TAB_SOC_010_Áreas_de_la_empresa d ON a.Area_Solp=d.Cod_Área WHERE a.Cod_Soc='%s' AND a.Año='%s' AND a.Tipo_solp='%s' AND a.Estado_Solp='3' AND a.Nro_Solp >='%s';"%(Cod_Soc,Año,Tipo_Solp,Nro_Inicial)

            elif Nro_Inicial!='' and Nro_Final=='' and Fec_Inicial!='' and Fec_Final=='':
                sqlTabla="SELECT  a.Nro_Solp,a.Fecha_Solp, a.Fecha_Req_Global, c.Nom_usuario, d.Descripción_Área FROM TAB_SOLP_001_Cabecera_Solicitud_Pedido a LEFT JOIN TAB_SOC_005_Usuarios c ON a.Cod_Soc=c.Cod_Soc AND a.Solicita_Solp=c.Cod_usuario LEFT JOIN TAB_SOC_010_Áreas_de_la_empresa d ON a.Area_Solp=d.Cod_Área WHERE a.Cod_Soc='%s' AND a.Año='%s' AND a.Tipo_solp='%s' AND a.Estado_Solp='3' AND a.Nro_Solp >='%s' AND a.Fecha_Solp>='%s';"%(Cod_Soc,Año,Tipo_Solp,Nro_Inicial,Fec_Inicial)

            elif Fec_Inicial!='' and Fec_Final!='' and Nro_Inicial!='' and Nro_Final=='':
                sqlTabla="SELECT  a.Nro_Solp,a.Fecha_Solp, a.Fecha_Req_Global, c.Nom_usuario, d.Descripción_Área FROM TAB_SOLP_001_Cabecera_Solicitud_Pedido a LEFT JOIN TAB_SOC_005_Usuarios c ON a.Cod_Soc=c.Cod_Soc AND a.Solicita_Solp=c.Cod_usuario LEFT JOIN TAB_SOC_010_Áreas_de_la_empresa d ON a.Area_Solp=d.Cod_Área WHERE a.Cod_Soc='%s' AND a.Año='%s' AND a.Tipo_solp='%s' AND a.Estado_Solp='3' AND a.Nro_Solp >='%s' AND a.Fecha_Solp>='%s' AND a.Fecha_Solp<='%s';"%(Cod_Soc,Año,Tipo_Solp,Nro_Inicial,Fec_Inicial,Fec_Final)

            elif Fec_Inicial!='' and Fec_Final!='' and Nro_Inicial=='' and Nro_Final=='':
                sqlTabla="SELECT  a.Nro_Solp,a.Fecha_Solp, a.Fecha_Req_Global, c.Nom_usuario, d.Descripción_Área FROM TAB_SOLP_001_Cabecera_Solicitud_Pedido a LEFT JOIN TAB_SOC_005_Usuarios c ON a.Cod_Soc=c.Cod_Soc AND a.Solicita_Solp=c.Cod_usuario LEFT JOIN TAB_SOC_010_Áreas_de_la_empresa d ON a.Area_Solp=d.Cod_Área WHERE a.Cod_Soc='%s' AND a.Año='%s' AND a.Tipo_solp='%s' AND a.Estado_Solp='3' AND a.Fecha_Solp>='%s' AND a.Fecha_Solp<='%s';"%(Cod_Soc,Año,Tipo_Solp,Fec_Inicial,Fec_Final)

            elif Fec_Inicial!='' and Fec_Final=='' and Nro_Inicial=='' and Nro_Final=='':
                sqlTabla="SELECT  a.Nro_Solp,a.Fecha_Solp, a.Fecha_Req_Global, c.Nom_usuario, d.Descripción_Área FROM TAB_SOLP_001_Cabecera_Solicitud_Pedido a LEFT JOIN TAB_SOC_005_Usuarios c ON a.Cod_Soc=c.Cod_Soc AND a.Solicita_Solp=c.Cod_usuario LEFT JOIN TAB_SOC_010_Áreas_de_la_empresa d ON a.Area_Solp=d.Cod_Área WHERE a.Cod_Soc='%s' AND a.Año='%s' AND a.Tipo_solp='%s' AND a.Estado_Solp='3' AND a.Fecha_Solp>='%s';"%(Cod_Soc,Año,Tipo_Solp,Fec_Inicial)

            elif Nro_Inicial=='' and Nro_Final=='' and Fec_Inicial=='' and Fec_Final=='':
                sqlTabla="SELECT  a.Nro_Solp,a.Fecha_Solp, a.Fecha_Req_Global, c.Nom_usuario, d.Descripción_Área FROM TAB_SOLP_001_Cabecera_Solicitud_Pedido a LEFT JOIN TAB_SOC_005_Usuarios c ON a.Cod_Soc=c.Cod_Soc AND a.Solicita_Solp=c.Cod_usuario LEFT JOIN TAB_SOC_010_Áreas_de_la_empresa d ON a.Area_Solp=d.Cod_Área WHERE a.Cod_Soc='%s' AND a.Año='%s' AND a.Tipo_solp='%s' AND a.Estado_Solp='3';"%(Cod_Soc,Año,Tipo_Solp)

            Cargar(self,self.tbwSolicitud_Pedido_Autorizar,sqlTabla,self.cbNro_Inicial,self.cbNro_Final,self.leInicial,self.leFinal,Cod_Soc,Año)

        except:
            mensajeDialogo("error", "Error", "No se selecciono ningun rango, verifique")
            self.leInicial.clear()
            self.leFinal.clear()
            self.cbNro_Inicial.setCurrentIndex(-1)
            self.cbNro_Final.setCurrentIndex(-1)


    def Consultar(self):
        Num_Solp=self.tbwSolicitud_Pedido_Autorizar.item(self.tbwSolicitud_Pedido_Autorizar.currentRow(),0).text()
        self.co=Consultar()
        self.co.datosGenerales(Cod_Soc, Nom_Soc, Cod_Usuario, Num_Solp)
        self.co.pbGrabar.clicked.connect(self.Cargar)
        self.co.showMaximized()

    def Salir(self):
        self.close()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    _main=ERP_REQ_P002()
    _main.showMaximized()
    app.exec_()
