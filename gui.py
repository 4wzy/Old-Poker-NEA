import sys
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Texas Hold'Em Poker")

        # create buttons and labels
        self.checkButton = QPushButton("Check")
        self.foldButton = QPushButton("Fold")
        self.raiseButton = QPushButton("Raise")
        self.betButton = QPushButton("Bet")

        # Generate cards

        self.label1 = QLabel("Player 1:")

        self.label2 = QLabel("Player 2:")

        # create vertical and horizontal layouts
        vLayout1 = QVBoxLayout()
        vLayout2 = QVBoxLayout()
        hLayout = QHBoxLayout()

        # add buttons and labels to the layouts
        vLayout1.addWidget(self.label1)
        vLayout1.addWidget(self.checkButton)
        vLayout1.addWidget(self.foldButton)

        vLayout2.addWidget(self.label2)
        vLayout2.addWidget(self.raiseButton)
        vLayout2.addWidget(self.betButton)

        hLayout.addLayout(vLayout1)
        hLayout.addLayout(vLayout2)

        # set the main widget
        centralWidget = QWidget()
        centralWidget.setLayout(hLayout)
        self.setCentralWidget(centralWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
