from random import shuffle

# class Card
# each card has a displayed name and a black_jack value
class Card:
    card_dict = {
        '1' : ['Ace', 11],
        '2' : ['2', 2],
        '3' : ['3', 3],
        '4' : ['4', 4],
        '5' : ['5', 5],
        '6' : ['6', 6],
        '7' : ['7', 7],
        '8' : ['8', 8],
        '9' : ['9', 9],
        '10' : ['10', 10],
        '11' : ['Jack', 10],
        '12' : ['Queen', 10],
        '13' : ['King', 10]
    }
    suit_dict = {
        '1' : chr(9827),
        '2' : chr(9830),
        '3' : chr(9829),
        '4' : chr(9824)
    }
    def __init__(self, rank, suit_val) -> None:
        c = Card.card_dict[str(rank)]
        self.suit = Card.suit_dict[str(suit_val)]
        self.rank = c[0]
        self.name = self.rank + self.suit
        self.bjval = c[1]
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"<Card {self.name} | bjval={self.bjval}>"
    

# class Deck:
# creates a list of 52 Cards
# is able to reset
# can keep track of current cards left / dealt
# is able to shuffle each time
class Deck:
    def __init__(self, num_decks=1) -> None:
        self.cards_in_deck = []
        self.cards_dealt = []
        for i in range(num_decks):
            for suit in range(1,5):
                for rank in range(1,14):
                    self.cards_in_deck.append(Card(rank, suit))
    
    def __str__(self) -> str:
        return f"Deck: {self.cards_in_deck}"
    
    def __repr__(self) -> str:
        return f"<Deck | In Deck: {len(self.cards_in_deck)} Dealt: {len(self.cards_dealt)}>"
    
    def reset(self):
        self.cards_in_deck = self.cards_in_deck + self.cards_dealt
        self.cards_dealt = []
        self.shuffle_deck()
    
    def shuffle_deck(self):
        shuffle(self.cards_in_deck)
    
    # Returns the card that is dealt from the deck
    def deal_card(self) -> Card:
        if self.cards_in_deck != []:
            card_to_deal = self.cards_in_deck.pop()
            self.cards_dealt.append(card_to_deal)
            return card_to_deal
        else:
            print(f"There are no cards in the deck to deal")