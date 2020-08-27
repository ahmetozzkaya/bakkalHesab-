from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import mysql.connector
import pandas as pd



class bakkalHesabı(QDialog):
    def __init__(self, ebeveyn=None):
        super(bakkalHesabı, self).__init__(ebeveyn)
        grid = QGridLayout()
        grid.addWidget(QLabel("Ekmek Fiyatı:"), 0, 0)
        grid.addWidget(QLabel("Çikolata Fiyatı:"), 1, 0)
        grid.addWidget(QLabel("Sigara Fiyatı:"), 2, 0)
        grid.addWidget(QLabel("Toplam Fiyat:"), 3, 0)
        grid.addWidget(QLabel("Ekmek Adeti:"), 0, 2)
        grid.addWidget(QLabel("Çikolata Adeti:"), 1, 2)
        grid.addWidget(QLabel("Sigara Adeti:"), 2, 2)
        grid.addWidget(QLabel("Ekmek Tahmini:"),0,4)
        grid.addWidget(QLabel("Çikolata Tahmini:"),1,4)
        grid.addWidget(QLabel("Sigara Tahmini:"),2,4)

        self.sonuc = QLabel("")
        grid.addWidget(self.sonuc, 3, 1)

        self.ekmekSonuc = QLabel("")
        grid.addWidget(self.ekmekSonuc,0,5)

        self.cikolataSonuc = QLabel("")
        grid.addWidget(self.cikolataSonuc,1,5)

        self.sigaraSonuc = QLabel("")
        grid.addWidget(self.sigaraSonuc,2,5)

        self.ekmekFiyati = QLineEdit()
        self.ekmekFiyati.setInputMask("0.00")

        self.cikolataFiyati = QLineEdit()
        self.cikolataFiyati.setInputMask("0.00")

        self.sigaraFiyati = QLineEdit()
        self.sigaraFiyati.setInputMask("00.00")

        self.ekmekAdeti = QSpinBox()
        self.ekmekAdeti.setRange(0, 100)
        # self.ekmekAdeti.setValue(1)
        grid.addWidget(self.ekmekAdeti, 0, 3)

        self.cikolataAdeti = QSpinBox()
        self.cikolataAdeti.setRange(0, 100)
        # self.cikolataAdeti.setValue(1)
        grid.addWidget(self.cikolataAdeti, 1, 3)

        self.sigaraAdeti = QSpinBox()
        self.sigaraAdeti.setRange(0, 100)
        # self.sigaraAdeti.setValue(1)
        grid.addWidget(self.sigaraAdeti, 2, 3)

        grid.addWidget(self.ekmekFiyati, 0, 1)
        grid.addWidget(self.cikolataFiyati, 1, 1)
        grid.addWidget(self.sigaraFiyati, 2, 1)

        hesaplaDugme = QPushButton("Hesapla")
        hesaplaDugme.clicked.connect(self.fiyatHesapla)
        grid.addWidget(hesaplaDugme, 4, 1)

        kaydetDugme = QPushButton("Kaydet")
        kaydetDugme.clicked.connect(self.veriKaydet)
        grid.addWidget(kaydetDugme, 4, 2)

        ekmekDugme = QPushButton("Ekmek Tahminle")
        ekmekDugme.clicked.connect(self.ekmekTahmin)
        grid.addWidget(ekmekDugme,0,6)

        cikolataDugme = QPushButton("Çikolata Tahminle")
        cikolataDugme.clicked.connect(self.cikolataTahmin)
        grid.addWidget(cikolataDugme,1,6)

        sigaraDugme = QPushButton("Sigara Tahminle")
        sigaraDugme.clicked.connect(self.sigaraTahmin)
        grid.addWidget(sigaraDugme,2,6)

        self.setLayout(grid)
        self.setWindowTitle("Bakkal Hesabı")

    def fiyatHesapla(self):
        ekmek = float(self.ekmekFiyati.text())
        cikolata = float(self.cikolataFiyati.text())
        sigara = float(self.sigaraFiyati.text())

        ekmekAdet = int(self.ekmekAdeti.text())
        cikolataAdet = int(self.cikolataAdeti.text())
        sigaraAdet = int(self.sigaraAdeti.text())

        tutar = float((ekmek * ekmekAdet) + (cikolata * cikolataAdet) + (sigara * sigaraAdet))
        self.sonuc.setText('<font color="red">%0.2f</font>' % tutar)

    def veriKaydet(self):
        ekmek = int(self.ekmekAdeti.text())
        cikolata = int(self.cikolataAdeti.text())
        sigara = int(self.sigaraAdeti.text())
        baglanti = mysql.connector.connect(user="root", host="127.0.0.7", database="final")
        isaretci = baglanti.cursor()
        isaretci.execute(
            '''INSERT INTO bakkal (ekmek,cikolata,sigara) VALUES("%i","%i","%i")''' % (ekmek, cikolata, sigara))
        baglanti.commit()
        baglanti.close()



    def ekmekTahmin(self):
        from sklearn.linear_model import LinearRegression
        data = pd.read_table("C:\\Users\\hp-not\\Desktop\\bakkal.csv", sep=';')
        lr = LinearRegression()
        lr.fit(data[['ID']], data.ekmek)
        tahmin = lr.predict([[7]])
        self.ekmekSonuc.setText('<font color="red">%0.2f</font>' % tahmin)



    def cikolataTahmin(self):
        from sklearn.linear_model import LinearRegression
        data = pd.read_table("C:\\Users\\hp-not\\Desktop\\bakkal.csv", sep=';')
        lr = LinearRegression()
        lr.fit(data[['ID']], data.cikolata)
        tahmin = lr.predict([[7]])
        self.cikolataSonuc.setText('<font color="red">%0.2f</font>' % tahmin)


    def sigaraTahmin(self):
        from sklearn.linear_model import LinearRegression
        data = pd.read_table("C:\\Users\\hp-not\\Desktop\\bakkal.csv", sep=';')
        #data = pd.read_table("C:\\Users\\hp-not\\Desktop\\bakkal.csv", sep=';')
        #from sklearn.linear_model import LinearRegression
        lr = LinearRegression()
        lr.fit(data[['ID']], data.sigara)
        tahmin = lr.predict([[7]])
        self.sigaraSonuc.setText('<font color="red">%0.2f</font>' % tahmin)



uyg = QApplication([])
pencere = bakkalHesabı()
pencere.show()
uyg.exec_()
