# Cards: https://opengameart.org/content/playing-cards-vector-png

from random import randint
import sys
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} {self.suit}"


class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank)
                      for suit in ["Clubs", "Diamonds", "Spades", "Hearts"] for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]]

    def shuffle(self):
        for i in range(len(self.cards)):
            swap_number = randint(0, len(self.cards) - 1)
            self.cards[swap_number], self.cards[i] = self.cards[i], self.cards[swap_number]

    # The following function is for testing purposes only, remove at the end of project
    def print_cards(self):
        for card in self.cards:
            print(card)

    def deal_card(self):
        # This method deals a single card from the top of the deck
        return self.cards.pop()


class Player:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = Hand([])

    def add_card(self, card):
        self.hand.cards.append(card)


class Game:
    def __init__(self, player_names, starting_chips=500):
        self.players = [Player(name, starting_chips) for name in player_names]
        self.pot = Pot()
        self.board = []
        self.deck = Deck()
        self.deck.shuffle()

    def deal_cards(self, num_cards, player):
        for i in range(num_cards):
            card = self.deck.deal_card()
            player.add_card(card)

    def start_round(self):
        self.board = []
        for player in self.players:
            self.deal_cards(2, player)

    def flop(self):
        for i in range(3):
            card = self.deck.deal_card()
            self.board.append(card)

    def turn_river(self):
        card = self.deck.deal_card()
        self.board.append(card)


class Pot:
    def __init__(self):
        self.chips = 0

    def add_chips(self, amount):
        self.chips += amount

    def subtract_chips(self, amount):
        self.chips -= amount

    def reset_pot(self):
        self.chips = 0


class Hand:
    def __init__(self, cards):
        self.cards = cards

    def evaluate_strength(self):
        pass


game = Game(["Justin", "Megan"])
game.start_round()


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
