import poker_game
import gui
import sys


def poker_round(game):
    # Create the table's deck
    game.board = []

    # Handle the player indexes for the small blind and big blind
    game.handle_blinds()

    # Deal cards to every player
    for player in game.players:
        game.deal_cards(2, player)

    # Display the cards and blinds
    current_cards = game.get_player_cards()
    ui.displayCards(current_cards)
    ui.displayBlinds(game.big_blind_player_index,
                     game.small_blind_player_index)

    game.flop()
    game.betting_round()
    ui.displayBoard(game.get_board_cards())


# Set up the Poker Game
game = poker_game.Game(["Justin", "Megan", "TestPlayer1",
                        "TestPlayer2", "TestPlayer3", "TestPlayer4"])

# Set up the GUI
app = gui.QtWidgets.QApplication(sys.argv)
gui.qdarktheme.setup_theme()
MainWindow = gui.QtWidgets.QMainWindow()
ui = gui.Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

# Run the first poker round
poker_round(game)

# Handle exitting the GUI
sys.exit(app.exec_())
