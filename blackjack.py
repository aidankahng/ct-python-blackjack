# Python implemented blackjack game through commandline
# Supports having multiple players, tracks winnings
# Can also modify number of decks and have players sit out of games
# 
import time
from playing_cards import Deck
from people import Player, Dealer
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
            time.sleep(0.5)
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
                    if buy_in.startswith('y'):
                        player.debt += curr_bet - player.cash
                        player.cash = curr_bet
                    else:
                        print("Let's try this again")
                        curr_bet = -1
            player.cash -= curr_bet
            player.bet = curr_bet
    
    # Dealer's automated turn
    def dealer_turn(self):
        self.d.unhide()
        print("Dealer's Turn:")
        print(self.d)
        while self.d.bj_score() > 0 and self.d.bj_score() < 17:
            time.sleep(1.5)
            print(f"Dealer Hit!")
            self.deal_to(self.d)
            time.sleep(1.5)
            print(f"[Dealer] drew a {self.d.hand[-1]}")
            time.sleep(1.5)
            print(self.d)
        if self.d.bj_score() < 0:
            time.sleep(1)
            print(f"Dealer BUSTED!")
        else:
            time.sleep(1.5)
            print(f"Dealer Stood!")
            
    
    # Asks a player to make an action. Hit or Stand
    def hit_or_stand(self, player : Player):
        time.sleep(0.5)
        print(player)
        time.sleep(0.5)
        player_input = input(f"[{player.name}] would you like to (H)it or (S)tand? ").lower()
        while not (player_input.startswith('h') or player_input.startswith('s')):
            player_input = input(f"[{player.name}] Please enter h to hit, s to stand. ").lower()
        if player_input.startswith('h'):
            time.sleep(0.5)
            print(f"[{player.name}] Hit!")
            time.sleep(0.5)
            self.deal_to(player)
            print(f"[{player.name}] drew a {player.hand[-1]}")
            time.sleep(0.5)
            if player.bj_score() < 0:
                print(f"[{player.name}] BUSTED!")
                time.sleep(0.5)
            else:
                self.hit_or_stand(player)
        # If s, continue without doing anything.

    # Asks all players for their bet this round
    # sets .playing attribute to True
    # deals 2 cards to all players and the dealer
    def start_round(self):
        self.d.hide()
        for player in self.p:
            self.collect_bet(player)
        self.playing = True
        time.sleep(0.5)
        print("Dealing Cards...")
        time.sleep(2)
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
    options = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '?'}
    b = BlackjackTable()
    b.reset_deck()
    all_players = []
    symbols = f"{chr(9827)} {chr(9830)} {chr(9829)} {chr(9824)} "
    winning = False


    # Helper function to create a player, asking for user input
    def add_new_player(b:BlackjackTable):
        name = ''
        wealth = 0
        debt = 0
        while name == '':
            name = input("What is the name of our new player? ").strip().title()
            # Check if name is already at the table to avoid bugs with duplicate names
            if len(all_players) != 0:
                if name in [pl.name for pl in all_players]:
                    print(f"{name} is already here. Please use a unique name.")
                    name = ''
        wealth_input = input(f"How much money did {name} bring today?"
                             + "\n Default is $0"
                             + "\n::")
        if wealth_input.isdigit():
            wealth = int(wealth_input)
        print(f"Player {name} has been added to the table "
              + f"starting with ${wealth}")
        new_player = Player(name, wealth, debt)
        all_players.append(new_player)
        b.add_player(new_player)

    # Shows unseated players
    # Asks to select a player
    # That player will be added to the table
    # KNOWN BUG: if two players have same name, can only select the first player of that name
    def add_to_table(b:BlackjackTable):
        if all_players == []:
            print("[Eerie whooshing noises can be heard in the distance]")
            time.sleep(1)
            print("It would seem that no one has ever been here")
            time.sleep(1)
            print("Only a lonely Dealer sitting in a large empty room")
            time.sleep(1)
            print("Perhaps you need to recruit someone first...")
            time.sleep(1)
            return
        playernames = [player.name for player in all_players]
        seatedplayers = [pl.name for pl in b.p]
        unseated = [name for name in playernames if not name in seatedplayers]
        if unseated:
            print("Unseated Players: "+ ' | '.join(unseated))
            player_choice = ''
            while not player_choice in unseated:
                player_choice = input("Which player would you like to add? ").strip().title()
            b.p.append(all_players[playernames.index(player_choice)])
            print(f"{player_choice} has been seated at the table")
        else:
            print("All players are already seated")
    
    # Show players at table
    # ask to select player
    # Player will be removed
    def leave_table(b:BlackjackTable):
        if b.p == []:
            print("[Sound of crickets chirping]")
            time.sleep(1)
            print("There's no one but the Dealer at the table right now")
            time.sleep(1)
            return
        playernames = [pl.name for pl in b.p]
        print("Players: "+ ' | '.join(playernames))
        player_choice = ''
        while not player_choice in playernames:
            player_choice = input("Which player would like to leave the table? ").strip().title()
        b.p.pop(playernames.index(player_choice))
        print(f"{player_choice} has left the table")
    
    # Displays the Dealer and all players currently seated
    def view_table(b:BlackjackTable):
        playernames = [pl.name for pl in b.p]
        print("Dealer | "+ ' | '.join(playernames))
        if b.p == []:
            time.sleep(0.5)
            print("The table stands empty.")
            time.sleep(0.5)
            print("The dealer looks lonely")
            time.sleep(0.5)

    # Attempts to pay off as much debt as possible for all players
    def pay_debt():
        for player in all_players:
            if player.debt > 0:
                sub = min(player.debt, player.cash)
                player.debt -= sub
                player.cash -= sub
            time.sleep(0.5)
            print(player)    
    
    # MAIN LOOP TO KEEP GAME RUNNING
    while True:
        choice = "NA"
        while not choice in options:
            choice = input(symbols*2 + f"LETS PLAY BLACKJACK " + symbols*2
                              + "\n\t\t0: Play A Game"
                              + "\n1: Add New Player  2: Add To Table  "
                              + "3: Leave Table\n4: View Table  5: Pay Debts  "
                              + "6: View House Earnings  "
                              + "\n7: View Player Wallets  8: Change Decks  9: QUIT"
                              + "\nEnter '?' to learn how to play"
                              + '\n::')
        print(symbols * 6)
        if choice == '0':
            if b.p != []:
                print("Shuffling Cards...")
                time.sleep(1)
                b.reset_deck()
                b.start_round()
                print("Time to Play your Hands!")
                time.sleep(1)
                b.play_game()
                print("Calculating results...")
                time.sleep(1)
                b.end_round()
                time.sleep(1.5)
            else:
                print("There are no players at the table"
                      + "\nAdd a player before you start the game")
        elif choice == '1':
            add_new_player(b)
            print('Welcome In\n')
        elif choice == '2':
            add_to_table(b)
            time.sleep(1.5)
            print('')
        elif choice == '3':
            leave_table(b)
            time.sleep(1.5)
            print('')
        elif choice == '4':
            view_table(b)
            time.sleep(1.5)
            print('')
        elif choice == '5':
            print("Attempting to Pay Debts...")
            pay_debt()
            time.sleep(1.5)
            print('')
        elif choice == '6':
            print("Viewing House Earnings...")
            time.sleep(0.4)
            house = b.d.winnings
            if house > 0:
                print(f"So far the house is up ${house}")
            elif house < 0:
                print(f"So far the house is down -${abs(house)}")
            else:
                print(f"The house is even for now")
            time.sleep(1.5)
            print('')
        elif choice == '7':
            print("Viewing Player Wallets...")
            for player in all_players:
                time.sleep(0.75)
                print(player)
            time.sleep(1.5)
            print('')
        elif choice == '8':
            decks_input = 'NA'
            while not decks_input.isdigit():
                decks_input = input("How many decks would you like to play with?" 
                                + "(default = 2)\n::").strip()
            b.deck = Deck(int(decks_input))
            print(f"The game is now using {decks_input} decks of cards")
        if choice == '9':
            if b.d.winnings < 0:
                winning = True
            break
        if choice == '?':
            print("""
        Welcome to Blackjack!
    Blackjack is an incredibly popular, exciting and easy card game to play. 
    The object is to have a hand with a total value higher than the dealer's without going over 21. 
    Kings, Queens, Jacks and Tens are worth a value of 10. 
    An Ace has the value of 1 or 11. 
    The remaining cards are counted at face value.
""")
            input("Press Enter to continue...")
            print("""
    To start each round, all players must make a bet
    Then, 2 cards will be dealt to each player including the dealer
    However, one of the dealer's cards will be face down (hidden from view)   
""")
            input("Press Enter to continue...")
            print("""
    On your turn, you have a choice to Hit or Stand
    Hit: You will get a new card face up
    Stand: Your current hand is final and you end your turn
    If your total value ever goes over 21, you 'Bust' and LOSE
""")
            input("Press Enter to continue...")
            print("""
    On the dealer's turn they will Hit if their total value is < 17
    and Stand whenever their value is 17 or greater
    The dealer can also bust if their score goes over 21
""")
            input("Press Enter to continue...")
            print("""
    Special rule: Blackjack
    If your first 2 cards add up to 21 exactly you have a blackjack!
    Unless the dealer also has a blackjack you earn 1.5 times your bet
    
    Normal wins will earn the same as your bet
    All losses will lose your bet
                  
I hope this explanation helps you get started! Have fun!
""")
            input("Press Enter to return to the menu\n")
        choice = "NA"
    if winning:
        print("Enjoy your winnings!")
        # time.sleep(1)
        # print("Dealer: So you want to leave?")
        # time.sleep(1)
        # print("Do you want to run?")
        # time.sleep(1)
        # print("When we have only just met?")
        # time.sleep(1)
        # print("Oh no...")
        # time.sleep(1)
        # print("I can't let you go so easily")
        # time.sleep(1)
        # print("Especially not when I'm losing...")
        # time.sleep(1)
        # print("\nYou: Why am I so dizzy?")
        # time.sleep(1)
        # print("\nDealer: Sleep child... this was all just a dream...")
        # time.sleep(1)
        # print("The house always wins...")
    else:
        print("Goodbye! Maybe next time you'll earn a profit!")
        # time.sleep(1)
        # print("Dealer: Leaving already?")
        # time.sleep(1)
        # print("Thank you for playing")
        # time.sleep(1)
        # print("An invoice will be sent to you soon")
        # time.sleep(1)
        # print("And if you're ever feeling lucky")
        # time.sleep(1)
        # print("You know where to find me")
        

###### TESTING #####
if __name__ == "__main__":
    BlackJackInterface()