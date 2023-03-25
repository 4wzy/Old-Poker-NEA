import sys
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel

from poker_game import game


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Texas Hold'Em Poker")

        # Create poker card images
        cards = []
        for player in game.players:
            for card in player.hand.cards:
                cards.append(f"{card.rank}_of_{card.suit}")

        self.labels = []
        for card in cards:
            pixmap = QPixmap(f"images/cards/{card}")
            # Sets the width=100 and height=140
            pixmap = pixmap.scaled(100, 140)
            label = QLabel()
            label.setPixmap(pixmap)
            self.labels.append(label)

        # create buttons and labels
        self.checkButton = QPushButton("Check")
        self.foldButton = QPushButton("Fold")
        self.raiseButton = QPushButton("Raise")
        self.betButton = QPushButton("Bet")

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
        for label in self.labels[:2]:
            vLayout1.addWidget(label)

        vLayout2.addWidget(self.label2)
        vLayout2.addWidget(self.raiseButton)
        vLayout2.addWidget(self.betButton)
        for label in self.labels[2:]:
            vLayout2.addWidget(label)

        # --- Testing
        for p in game.players:
            for c in p.hand.cards:
                print(c)

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
