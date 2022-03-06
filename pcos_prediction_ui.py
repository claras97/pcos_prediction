import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from sklearn.tree import DecisionTreeClassifier
from joblib import dump, load


INFO_XPOS	= 20
INFO_YPOS	= 20
INFO_INTER	= 35
INFO_HEIGHT	= 25


class medUi(QMainWindow):
	def __init__(self, parent=None):
		super(medUi, self).__init__(parent)
		self.resize(350, 390)
		self.setWindowTitle('Previsão de SOP')

		self.cicleLabel = QLabel(self)
		self.cicleLabel.setText('Ciclo (R/I)')
		self.cicleLabel.setGeometry(QRect(INFO_XPOS, INFO_YPOS, 200, INFO_HEIGHT))
		self.cicleEdit = QLineEdit(self)
		self.cicleEdit.setGeometry(QRect(220, INFO_YPOS, 80, INFO_HEIGHT))

		self.nFolLeftLabel = QLabel(self)
		self.nFolLeftLabel.setText('Nº folículos esq.')
		self.nFolLeftLabel.setGeometry(QRect(INFO_XPOS, INFO_YPOS+INFO_INTER*1, 200, INFO_HEIGHT))
		self.nFolLeftEdit = QLineEdit(self)
		self.nFolLeftEdit.setGeometry(QRect(220, INFO_YPOS+INFO_INTER*1, 80, INFO_HEIGHT))

		self.nFolRightLabel = QLabel(self)
		self.nFolRightLabel.setText('Nº folículos dir.')
		self.nFolRightLabel.setGeometry(QRect(INFO_XPOS, INFO_YPOS+INFO_INTER*2, 200, INFO_HEIGHT))
		self.nFolRightEdit = QLineEdit(self)
		self.nFolRightEdit.setGeometry(QRect(220, INFO_YPOS+INFO_INTER*2, 80, INFO_HEIGHT))

		self.weightLabel = QLabel(self)
		self.weightLabel.setText('Aumento de peso (S/N)')
		self.weightLabel.setGeometry(QRect(INFO_XPOS, INFO_YPOS+INFO_INTER*3, 200, INFO_HEIGHT))
		self.weightEdit = QLineEdit(self)
		self.weightEdit.setGeometry(QRect(220, INFO_YPOS+INFO_INTER*3, 50, INFO_HEIGHT))

		self.hairLabel = QLabel(self)
		self.hairLabel.setText('Excesso de pêlos (S/N)')
		self.hairLabel.setGeometry(QRect(INFO_XPOS, INFO_YPOS+INFO_INTER*4, 200, INFO_HEIGHT))
		self.hairEdit = QLineEdit(self)
		self.hairEdit.setGeometry(QRect(220, INFO_YPOS+INFO_INTER*4, 50, INFO_HEIGHT))

		self.darkeningLabel = QLabel(self)
		self.darkeningLabel.setText('Escurecimento da pele (S/N)')
		self.darkeningLabel.setGeometry(QRect(INFO_XPOS, INFO_YPOS+INFO_INTER*5, 200, INFO_HEIGHT))
		self.darkeningEdit = QLineEdit(self)
		self.darkeningEdit.setGeometry(QRect(220, INFO_YPOS+INFO_INTER*5, 50, INFO_HEIGHT))

		self.pimplesLabel = QLabel(self)
		self.pimplesLabel.setText('Acne (S/N)')
		self.pimplesLabel.setGeometry(QRect(INFO_XPOS, INFO_YPOS+INFO_INTER*6, 200, INFO_HEIGHT))
		self.pimplesEdit = QLineEdit(self)
		self.pimplesEdit.setGeometry(QRect(220, INFO_YPOS+INFO_INTER*6, 50, INFO_HEIGHT))

		self.fastfoodLabel = QLabel(self)
		self.fastfoodLabel.setText('Fast food (S/N)')
		self.fastfoodLabel.setGeometry(QRect(INFO_XPOS, INFO_YPOS+INFO_INTER*7, 200, INFO_HEIGHT))
		self.fastfoodEdit = QLineEdit(self)
		self.fastfoodEdit.setGeometry(QRect(220, INFO_YPOS+INFO_INTER*7, 50, INFO_HEIGHT))

		self.resetButton = QPushButton(self)
		self.resetButton.setText('Limpar')
		self.resetButton.setGeometry(QRect(INFO_XPOS, INFO_YPOS+INFO_INTER*9, 60, 25))
		self.resetButton.clicked.connect(self.cicleEdit.clear)
		self.resetButton.clicked.connect(self.weightEdit.clear)
		self.resetButton.clicked.connect(self.hairEdit.clear)
		self.resetButton.clicked.connect(self.darkeningEdit.clear)
		self.resetButton.clicked.connect(self.pimplesEdit.clear)
		self.resetButton.clicked.connect(self.fastfoodEdit.clear)
		self.resetButton.clicked.connect(self.nFolLeftEdit.clear)
		self.resetButton.clicked.connect(self.nFolRightEdit.clear)

		self.printButton = QPushButton(self)
		self.printButton.setText('Prever')
		self.printButton.setGeometry(QRect(INFO_XPOS+70, INFO_YPOS+INFO_INTER*9, 60, 25))
		self.printButton.clicked.connect(self.predictionClicked)

	def predictionClicked(self):
		dialog = QDialog(self)
		dialog.setWindowTitle('Previsão')
		dialogLabel = QLabel(dialog)
		dialogLabel.move(10, 15)
		dialogFile = QFileDialog(self)
		if self.cicleEdit.text() == '' or self.weightEdit.text() == '' or self.hairEdit.text() == '' or self.darkeningEdit.text() == '' or self.pimplesEdit.text() == '' or self.fastfoodEdit.text() == '' or self.nFolLeftEdit.text() == '' or self.nFolRightEdit.text() == '':
			dialog.resize(373, 50)
			dialogLabel.setText('ERRO: Todos os parâmetros devem ser preenchidos.')
			dialog.show()
		else:
			cicleVal = float(self.cicleEdit.text())
			weightVal = 1.0 if self.weightEdit.text() == 'S' or self.weightEdit.text() == 's' else 0.0
			hairVal = 1.0 if self.hairEdit.text() == 'S' or self.hairEdit.text() == 's' else 0.0
			darkeningVal = 1.0 if self.darkeningEdit.text() == 'S' or self.darkeningEdit.text() == 's' else 0.0
			pimplesVal = 1.0 if self.pimplesEdit.text() == 'S' or self.pimplesEdit.text() == 's' else 0.0
			fastfoodVal = 1.0 if self.fastfoodEdit.text() == 'S' or self.fastfoodEdit.text() == 's' else 0.0
			nFolLeftVal = float(self.nFolLeftEdit.text())
			nFolRightVal = float(self.nFolRightEdit.text())

			samples = [[cicleVal, weightVal, hairVal, darkeningVal, pimplesVal, fastfoodVal, nFolLeftVal, nFolRightVal]]

			clf = load('model/pcos_dtree.joblib')
			out = clf.predict(samples)

			if out > 0:
				dialogLabel.setText('O paciente tem SOP.')
			else:
				dialogLabel.setText('O paciente não tem SOP.')

			dialog.resize(190, 50)
			dialog.show()


def main():
	app = QApplication(sys.argv)
	ui = medUi()
	ui.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

