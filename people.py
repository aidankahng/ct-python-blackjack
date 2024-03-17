# class Person:
# has a name, id, and hand of cards
class Person:
    id = 0
    def __init__(self, name='Anon'):
        self.hand = []
        self.id = Person.id
        Person.id += 1
        self.name = name
        if self.name == 'anon_':
            self.name += str(self.id)
    
    def __repr__(self) -> str:
        return f"<Person {self.id} | {self.name}>"

    def bj_score(self):
        num_cards = len(self.hand) # Used to check if blackjack
        total_score = 0
        ace_count = 0
        for card in self.hand:
            total_score += card.bjval
            if card.rank == 'A':
                ace_count += 1
        while total_score > 21 and ace_count > 0: # If busting, check aces to lower score
            total_score -= 10
            ace_count -= 1
        if total_score > 21: # If bust, score becomes set to -1
            total_score = -1
        if total_score == 21 and num_cards == 2:
            total_score = 100 # Blackjack's arbitrarily large value
        return total_score


# class Dealer:
# inherits from Person with name set to dealer and attribute hidden
# __str__ only displays one of their cards if hidden is True
class Dealer(Person):
    def __init__(self):
        super().__init__('Dealer')
        self.__hidden = True
        self.winnings = 0

    def __str__(self) -> str:
        if self.hand == []:
            return f"[{self.name}] has no cards"
        elif not self.__hidden: # This should happen if hidden attribute is False
            return (f"[{self.name}] has: " 
                    + f"{"".join([str(card)+', ' for card in self.hand])}"[:-2] 
                    + f"\nScore: {min(self.bj_score(), 21)}")
        else: # This happens if hidden attribute is True
            return (f"[{self.name}] has: HIDDEN, " 
                    + f"{"".join([str(card)+', ' for card in self.hand[1:]])}"[:-2])

    def hide(self):
        self.__hidden = True    
    
    def unhide(self):
        self.__hidden = False
        

# class Player:
# inherits from Person with a cash balance
# also has ability to buy-in
# __str__ shows all of their cards
class Player(Person):
    def __init__(self, name='Anon', cash=100, debt=100):
        super().__init__(name)
        self.cash = cash
        self.debt = debt
        self.bet = 0
        self.stand = False

    
    def __str__(self) -> str:
        if self.hand != []:
            return (f"[{self.name}] has: " 
                    + f"{"".join([str(card)+', ' for card in self.hand])}"[:-2]
                    + f"\nScore: {min(self.bj_score(), 21)}")
        else:
            return (f"[{self.name}] has ${self.cash} cash and" 
                    + f" a ${self.debt} debt")
    
    def __repr__(self) -> str:
        return f"<Player {self.name}| Cash:${self.cash} Debt:${self.debt}>"