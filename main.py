import poker_game
import gui
import sys


def start_betting_round(game, first_player, last_player):
    # Handle the blinds
    game.handle_blinds()

    ui.displayBlinds(game.big_blind_player_index,
                     game.small_blind_player_index, game.dealer_button_player_index)
    ui.displayChips([player.chips for player in game.players])

    current_player = first_player

    current_highest_bet = game.big_blind_value

    while not game.are_bets_equal():
        while current_player != last_player:
            player = game.players_in_round[current_player]

            # Get input from the user TEMPORARY
            print(f"Cards: {player.hand.cards}")
            print(f"{player.name}: {player.chips} chips")
            while True:
                choice = input("Choose: ")

                if choice == "fold":
                    game.fold(current_player)
                    break

                # IMPORTANT NOTE: The check button will be replaced will the call button if the user can not check.
                elif choice == "check":

                    # Check if the current player's contribution to the pot is equal to the highest bet (check criteria)
                    if game.player_bets[player.name] == current_highest_bet:
                        # Check by moving to the next player (do nothing as the current_player is incremented at the end)
                        break
                    else:
                        continue

                elif choice == "call":
                    call_amount = current_highest_bet - \
                        game.player_bets[player.name]
                    # If the player has enough chips to call, put the appropriate amount of chips in the pot
                    if player.chips >= call_amount:
                        # Call
                        player.chips -= call_amount
                        game.pot.add_chips(call_amount)
                        game.player_bets[player.name] += call_amount
                    else:
                        # If the player DOES NOT have enough chips to call, go all in
                        remaining_chips = player.chips
                        game.pot.add_chips(
                            remaining_chips)
                        player.chips = 0
                        game.player_bets[player.name] += remaining_chips
                    break

                elif choice == "raise":
                    # If the player has enough money to raise, raise
                    if player.chips > current_highest_bet - game.player_bets[player.name]:
                        # The player should only be able to raise up to the total amount of chips that they have.
                        # This could be implemented in the GUI as a slider, but for now
                        # I will implement a while loop that just asks the player for a raise_amount until it is valid.
                        raise_amount = player.chips + 1
                        while raise_amount > player.chips or raise_amount < game.minimum_raise_amount:
                            if raise_amount < game.minimum_raise_amount:
                                print(
                                    f"Raise amount should be at least {game.minimum_raise_amount}")
                            raise_amount = int(input("Raise amount: "))

                        current_highest_bet += raise_amount
                        player.chips -= raise_amount
                        game.pot.add_chips(raise_amount)
                        game.player_bets[player.name] = current_highest_bet

                    # Else if they don't have enough money to raise, tell them that they don't (this will cause the player's turn to be skipped,
                    # so the option to raise must not be on the screen if the player does not have enough money to raise)
                    else:
                        print("You do not have enough money to raise.")
                        continue
                    break

            # After they have made their choice, move to the next player to the left.
            ui.displayChips([player.chips for player in game.players])
            current_player = (
                current_player + 1) % len(game.players_in_round)


def start_poker_round(game):
    game.reset_bets()

    # The first player to act is the player to the left of the big blind, and the play is clockwise
    first_player = game.big_blind_player_index
    current_player = first_player

    # Add the small blinds and big blinds contributions to the player pot contributions
    game.player_bets[game.players[game.small_blind_player_index].name
                     ] = game.small_blind_value
    game.player_bets[game.players[game.big_blind_player_index].name
                     ] = game.big_blind_value

    start_betting_round(game, current_player,
                        game.dealer_button_player_index + 1)
    game.flop()
    ui.displayBoard(game.get_board_cards())
    # The last player is set to game.dealer_button_player_index + 1, as the value of the dealer button index is incremented when handle_blinds() is called at the start.
    # And the last player should be the big blind player.
    start_betting_round(game, current_player,
                        game.dealer_button_player_index + 1)
    game.turn_river()
    ui.displayBoard(game.get_board_cards())
    start_betting_round(game, current_player, game.dealer_button_player_index)
    game.turn_river()
    ui.displayBoard(game.get_board_cards())

    game.distribute_pot()


def start_poker(game):
    game.board = []

    # Deal cards to every player
    for player in game.players:
        game.deal_cards(2, player)

    current_cards = game.get_player_cards()
    ui.displayCards(current_cards)

    start_poker_round(game)


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
# Create the table's deck (community cards)

ui.displayNames([player.name for player in game.players])
start_poker(game)

# Handle exitting the GUI
sys.exit(app.exec_())
