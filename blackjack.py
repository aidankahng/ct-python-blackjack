# ## Python Blackjack
# For this project you will make a Blackjack game using Python. Click <a href="http://www.hitorstand.net/strategy.php">here</a> to familiarize yourself with the the rules of the game. You won't be implementing every rule "down to the letter" with the game, but we will doing a simpler version of the game. This assignment will be given to further test your knowledge on object-oriented programming concepts.
# ### Rules:
# `1. ` The game will have two players: the Dealer and the Player. The game will start off with a deck of 52 cards. The 52 cards will consist of 4 different suits: Clubs, Diamonds, Hearts and Spades. For each suit, there will be cards numbered 1 through 13. <br>
# **Note: No wildcards will be used in the program**
# `2. ` When the game begins, the dealer will shuffle the deck of cards, making them randomized. After the dealer shuffles, it will deal the player 2 cards and will deal itself 2 cards from. The Player should be able to see both of their own cards, but should only be able to see one of the Dealer's cards.
# `3. ` The objective of the game is for the Player to count their cards after they're dealt. If they're not satisfied with the number, they have the ability to 'Hit'. A hit allows the dealer to deal the Player one additional card. The Player can hit as many times as they'd like as long as they don't 'Bust'. A bust is when the Player is dealt cards that total more than 21.
# `4. ` If the dealer deals the Player cards equal to 21 on the **first** deal, the Player wins. This is referred to as Blackjack. Blackjack is **NOT** the same as getting cards that equal up to 21 after the first deal. Blackjack can only be attained on the first deal.
# `5. ` The Player will never see the Dealer's hand until the Player chooses to 'stand'. A Stand is when the player tells the dealer to not deal it anymore cards. Once the player chooses to Stand, the Player and the Dealer will compare their hands. Whoever has the higher number wins. Keep in mind that the Dealer can also bust. 
import time
from playing_cards import Deck
from people import Person, Player, Dealer
import re


# class BlackJack:
# has a list of players, a dealer, and a deck
# handles dealing cards to each Person
# handles managing the deck
# handles win / lose conditions
class BlackjackTable():
    def __init__(self, num_decks=2) -> None:
        self.deck = Deck(num_decks)
        self.p = []
        self.d = Dealer()
        self.bets = []
        self.playing = False
    
    def __str__(self) -> str:
        if self.playing:
            return f"""
{"".join([str(i) + '\n' for i in self.p])[:-1]}
{str(self.d)}
"""
        else:
            return f"""
{''.join([player.name + ' has $' + str(player.cash) 
          + ' in cash and $' + str(player.debt) 
          + ' debt\n' for player in self.p])}
"""
    
    def add_player(self, player : Player):
        self.p.append(player)
    
    def remove_player(self, player : Player):
        if player in self.p:
            self.p.remove(player)


    def reset_deck(self):
        for player in self.p:
            player.hand = []
        self.d.hand = []
        self.deck.reset()
    
    def deal_to(self, person):
        if person in self.p or person == self.d:
            card = self.deck.deal_card()
            person.hand.append(card)

    #checks if bet_str can be safely casted to int. Returns -1 if false
    def check_bet_int(self, bet_str) -> int:
        bet_lst = re.findall(r"[0-9]+", bet_str)
        if bet_lst:
            bet_str = bet_lst[0]
        if bet_str.isdigit():
            return int(bet_str)
        else:
            return -1
    
    # Asks player to input their bet
    def collect_bet(self, player): # gets a valid bet from a single player
        if player in self.p:
            # ask for an input and validate if it is a valid input (int and less than player.cash)
            curr_bet = -1 # Initialized as an inappropriate value
            input_bet = input(f"[{player.name}] Please place a bet for this round: $")
            curr_bet = self.check_bet_int(input_bet)
            while curr_bet < 0 or curr_bet > player.cash:
                if curr_bet < 0:
                    print('Invalid Input')
                    input_bet = input(f"[{player.name}] Please place a valid integer bet: $")
                    curr_bet = self.check_bet_int(input_bet)
                if curr_bet > player.cash:
                    print(f"You only have ${player.cash} in cash")
                    buy_in = input(f"Would you like to buy in the difference?(y/n) ").lower()
                    if buy_in == 'y':
                        player.debt += curr_bet - player.cash
                        player.cash = curr_bet
                    else:
                        curr_bet = -1
            player.cash -= curr_bet
            player.bet = curr_bet
    
    # Dealer's automated turn
    def dealer_turn(self):
        while self.d.bj_score() > 0 and self.d.bj_score() < 17:
            print(f"Dealer Hit!")
            self.deal_to(self.d)
            print(f"[Dealer] drew a {self.d.hand[-1]}")
        if self.d.bj_score() < 0:
            print(f"Dealer BUSTED!")
            
    
    # Asks a player to make an action. Hit or Stand
    def hit_or_stand(self, player : Player):
        print(player)
        player_input = input(f"[{player.name}] would you like to (H)it or (S)tand? ").lower()
        while not (player_input.startswith('h') or player_input.startswith('s')):
            player_input = input(f"[{player.name}] Please enter h to hit, s to stand. ").lower()
        if player_input.startswith('h'):
            print(f"[{player.name}] Hit!")
            self.deal_to(player)
            print(f"[{player.name}] drew a {player.hand[-1]}")
            if player.bj_score() < 0:
                print(f"[{player.name}] BUSTED!")
            else:
                self.hit_or_stand(player)
        # If s, continue without doing anything.
        pass

    # Asks all players for their bet this round
    # sets .playing attribute to True
    # deals 2 cards to all players and the dealer
    def start_round(self):
        self.d.hide()
        for player in self.p:
            self.collect_bet(player)
        self.playing = True
        print("Dealing Cards...")
        for i in range(2):
            for player in self.p:
                self.deal_to(player)
            self.deal_to(self.d)
        print(self)
    
    def play_game(self):
        for player in self.p:
            self.hit_or_stand(player)
        self.dealer_turn()

    def end_round(self):
        self.d.unhide()
        dealer_score = max(0, self.d.bj_score())
        print(self)
        # Now to compare each player's score with the dealer's score
        for player in self.p:
            if player.bj_score() == 100 and dealer_score != 100:
                player.cash += int(round(2.5 * player.bet))
                self.d.winnings -= int(round(1.5 * player.bet))
                print(f"[{player.name}] won ${1.5 * player.bet} with blackjack!!")
            elif player.bj_score() == dealer_score or (player.bj_score() == 21 
                                                       and dealer_score == 100):
                player.cash += player.bet
                print(f"[{player.name}] tied the dealer")
            elif player.bj_score() > dealer_score:
                player.cash += 2 * player.bet
                self.d.winnings -= player.bet
                print(f"[{player.name}] won ${player.bet}!")
            else:
                self.d.winnings += player.bet
                print(f"[{player.name}] lost ${player.bet}...")
            player.bet = 0
        self.reset_deck()
        self.playing = False

# Function to display friendly interfaces            
def BlackJackInterface():
    # Defining some variables
    options = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}
    b = BlackjackTable()
    b.reset_deck()
    all_players = []
    symbols = f"{chr(9827)} {chr(9830)} {chr(9829)} {chr(9824)} "


    # Helper function to create a player
    def add_new_player(b:BlackjackTable):
        name = ""
        wealth = 100
        debt = 100
        while name == "":
            name = input("What is the name of our new player? ").title()
        wealth_input = input(f"How much money did {name} bring today?"
                             + "\n Default is $0"
                             + "\n::")
        if wealth_input.isdigit():
            wealth = int(wealth_input)
            if wealth > 0:
                debt = 0
        print(f"Player {name} has been added to the table "
              + f"starting with ${wealth}")
        new_player = Player(name, wealth, debt)
        all_players.append(new_player)
        b.add_player(new_player)

    def add_to_table(b:BlackjackTable):
        playernames = [player.name for player in all_players]
        print("Players: "+ ' | '.join(playernames))
        player_choice = ''
        while not player_choice in playernames:
            player_choice = input("Which player would you like to add? ").title()
        for pl in b.p:
            if pl.name == player_choice:
                print(f"{player_choice} already has a seat at the table")
                return
        b.p.append(all_players[playernames.index(player_choice)])
        print(f"{player.choice} has been seated at the table")

        # Show all players
        # ask to select player
        # Player will be added or says already at table
    
    def leave_table(b:BlackjackTable):
        playernames = [pl.name for pl in b.p]
        print("Players: "+ ' | '.join(playernames))
        player_choice = ''
        while not player_choice in playernames:
            player_choice = input("Which player would like to leave the table? ").title()
        b.p.pop(playernames.index(player_choice))
        print(f"{player_choice} has left the table")
        # Show players at table
        # ask to select player
        # Player will be removed
    
    def view_table(b:BlackjackTable):
        playernames = [pl.name for pl in b.p]
        print("Dealer | "+ ' | '.join(playernames))

    def pay_debt():
        for player in all_players:
            if player.debt > 0:
                sub = min(player.debt, player.cash)
                player.debt -= sub
                player.cash -= sub
            time.sleep(0.25)
            print(player)    
    
    # MAIN LOOP TO KEEP GAME RUNNING
    while True:
        choice = "NA"
        while not choice in options:
            choice = input(symbols*2 + f"BLACKJACK INTERFACE " + symbols*2
                              + "\n\t\t0: Play A Game"
                              + "\n1: Add New Player  2: Add To Table  "
                              + "3: Leave Table\n4: View Table  5: Pay Debts  "
                              + "6: View House Earnings  "
                              + "\n7: View Player Wallets  8/9: Quit"
                              + '\n::')
        print(symbols * 6)
        if choice == '0':
            if all_players != []:
                print("Shuffling Cards...")
                time.sleep(0.4)
                b.reset_deck()
                b.start_round()
                print("Time to Play your Hands!")
                time.sleep(0.4)
                b.play_game()
                print("Calculating results...")
                time.sleep(0.4)
                b.end_round()
                time.sleep(2)
            else:
                print("There are no players at the table"
                      + "\nAdd a player before you start the game")
        if choice == '1':
            add_new_player(b)
        if choice == '2':
            add_to_table(b)
        if choice == '3':
            leave_table(b)
        if choice == '4':
            view_table(b)
        if choice == '5':
            print("Attempting to pay debts...")
            pay_debt()
            time.sleep(1.5)
        if choice == '6':
            print("Viewing House Earnings...")
            time.sleep(0.4)
            house = b.d.winnings
            if house > 0:
                print(f"So far the house is up ${house}")
            elif house < 0:
                print(f"So far the house is down ${house}")
            else:
                print(f"The house is even for now")
            time.sleep(1.5)
        if choice == '7':
            print("Viewing Player Wallets")
            for player in all_players:
                time.sleep(0.75)
                print(player)
            time.sleep(1.5)
            print('')
        if choice == '8':
            break
        if choice == '9':
            break
        choice = "NA"
    print("Goodbye")



###### TESTING #####
if __name__ == "__main__":
    BlackJackInterface()