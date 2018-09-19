from time import sleep
import random

class Card:
    suits={'heart':'♥', 'diamond':'♦', 'club':'♣', 'spade':'♠'}
    values={'A':11,'J':10,'Q':10,'K':10}
    def __init__(self, value_suit):
        self.name=value_suit[0]
        if type(self.name) is int:
            self.value=self.name
        else:
            self.value=Card.values[self.name]
        self.suit=value_suit[1]

    def __eq__(self, other):
        return (self.value == other.value) and (self.suit == other.suit)

    def __hash__(self):
        return hash((self.value, self.suit))

    def __str__(self):
        if self.name == 10:
            card_string='_______\n| '+str(self.name)+'  |\n| '+Card.suits[self.suit]+'   |\n|   '+Card.suits[self.suit]+' |\n|  '+str(self.name)+' |\n_______\n'
        else:
            card_string='_______\n| '+str(self.name)+'   |\n| '+Card.suits[self.suit]+'   |\n|   '+Card.suits[self.suit]+' |\n|   '+str(self.name)+' |\n_______\n'
        return card_string


class CollectionOfCards:
    full_deck={(2,'heart'),(2,'diamond'),(2,'club'),(2,'spade'),
            (3,'heart'),(3,'diamond'),(3,'club'),(3,'spade'),
            (4,'heart'),(4,'diamond'),(4,'club'),(4,'spade'),
            (5,'heart'),(5,'diamond'),(5,'club'),(5,'spade'),
            (6,'heart'),(6,'diamond'),(6,'club'),(6,'spade'),
            (7,'heart'),(7,'diamond'),(7,'club'),(7,'spade'),
            (8,'heart'),(8,'diamond'),(8,'club'),(8,'spade'),
            (9,'heart'),(9,'diamond'),(9,'club'),(9,'spade'),
            (10,'heart'),(10,'diamond'),(10,'club'),(10,'spade'),
            ('A','heart'),('A','diamond'),('A','club'),('A','spade'),
            ('J','heart'),('J','diamond'),('J','club'),('J','spade'),
            ('Q','heart'),('Q','diamond'),('Q','club'),('Q','spade'),
            ('K','heart'),('K','diamond'),('K','club'),('K','spade')
    }
    def __init__(self, deck='default', *args):
        if deck.lower() == 'full deck':
            self.cards = list(CollectionOfCards.full_deck)
        else:
            self.cards=list(args)

    def __del__(self):
        #print('Buh bye deck')
        self.cards = []

    def __str__(self):
        all_cards = '\n\n\n\n\n\n'
        for card in self.cards:
            next_card = str(card).split('\n')
            prev_cards = all_cards.split('\n')
            all_cards = ''.join(prev + cur + '\n' for prev, cur in zip(prev_cards,next_card))
        grand_total = '\nHand total: ' + str(self.total()) + '\n\n\n\n\n'
        all_cards = ''.join(x + y + '\n' for x, y in zip(all_cards.split('\n'),grand_total.split('\n')))
        return all_cards

    def total(self):
        total = 0
        for card in self.cards:
            total += card.value
        return total

    def addCard(self, card):
        self.cards += [card]

    def drawCard(self):
        card = self.cards.pop()
        return card

    def __len__(self):
        return len(self.cards)

class Bankroll:
    max_bet = 100
    min_bet = 10
    def __init__(self):
        ammount = 0
        while True:
            try:
                ammount = int(input("Enter available funds: "))
            except:
                print("Buddy, I will assume that was by mistake, try again (IN-TE-GER)")
            else:
                break
        self.betsize = Bankroll.min_bet
        self.bet = self.betsize
        self.ammount = ammount - self.bet

    def __del__(self):
        #print('Buh bye moneyz')
        pass

    def winMoney(self):
        self.ammount += self.bet
        print('Player won ' + str(self.bet) + ' bucks.')

    def placeBet(self):
        self.ammount += self.bet
        if self.ammount <= self.betsize:
            self.bet = self.ammount
            self.ammount = 0
        else:
            self.bet = self.betsize
            self.ammount -= self.bet
        print('Bet placed: ' + str(self.bet))

    def loseBet(self):
        if self.ammount <= self.bet:
            self.bet = self.ammount
            self.ammount = 0
        else:
            self.ammount -= self.bet
        print('Player lost!')

    def tiedRound(self):
        print("It's a tie!")

    def setBetSize(self):
        ammount = 0
        while ammount > Bankroll.max_bet or ammount < Bankroll.min_bet:
            ammount = int(input("Please type bet size (" + str(Bankroll.min_bet) + ' - ' + str(Bankroll.max_bet) + "): "))
        self.betsize = ammount
        print('Bet size increased to ' + str(self.betsize))

    def __str__(self):
        return 'Cash: ' + str(self.ammount) + '\nCurrent bet: ' + str(self.bet)

class Player:

    def __init__(self, name='Player 1', hand=CollectionOfCards(), aces=CollectionOfCards()):
        self.name = name
        self.hand = hand
        self.aces = aces
        if self.name != 'dealer':
            self.bankroll = Bankroll()
        else:
            self.bankroll = "I'm the dealer\n"

    def __del__(self):
        del self.hand
        del self.aces
        del self.bankroll
        #print('Buh bye' + self.name)

    def deal(self):
        card = Card(deck.cards.pop())
        if card.name == 'A':
            self.aces.addCard(card)
        while self.hand.total() + card.value > 21 and len(self.aces) > 0:
            ace = self.aces.drawCard()
            ace.value = 1
        self.hand.addCard(card)
        return card

    def aiDeal(self, *args):
        humans_to_beat = [score for score in list(args) if score <= 21]
        if self.name.lower() == 'dealer':
            while self.hand.total() < 21 and  self.hand.total() < max(humans_to_beat):
                self.deal()

    def newHand(self):
        del self.hand
        del self.aces
        self.hand = CollectionOfCards()
        self.aces = CollectionOfCards()

    def playerEndHand(self, outcome):
        if outcome.lower() == 'loss':
            self.bankroll.loseBet()
        elif outcome.lower() == 'tie':
            self.bankroll.tiedRound()
        else:
            self.bankroll.winMoney()
        self.newHand()
        print(self)

    def action(self):
        key = ''
        while not key in ['b','d','s','q']:
            key = str(input("\nPlease choose action\nchange (b)et ammount, (d)eal new card, (s)tay, (q)uit\n"))
        return key

    def __str__(self):
        #name + hand + Bankroll
        #hand already includes total
        bankroll_split = ('\n\n' + str(self.bankroll) + '\n\n').split('\n')
        player_string = '\n' + self.name.upper() + '\n' + ''.join(x + y + '\n' for x, y in zip(str(self.hand).split('\n'),bankroll_split))
        return player_string

    def playAgain(self):
        key = ''
        while not key in ['y','n']:
            key = str(input("\nPlay again? (y/n): "))
        if key == 'y':
            return True
        else:
            return False



while True:
    print("\n" * 100)
    player = Player()
    dealer = Player('dealer')
    print('BlackJack - prepare to lose all your money!\n Game Starting...')

    while player.bankroll.bet > 0:
        player.newHand()
        dealer.newHand()
        deck = CollectionOfCards('full deck')
        random.shuffle(deck.cards)

        #player's turn
        player_turn = True
        while player_turn:

            action = player.action()
            if action == 'b':
                player.bankroll.setBetSize()
                player.bankroll.placeBet()
                print('_________________________')
                print(player.bankroll)
                print('_________________________')
            elif action == 'd':
                print("\n" * 100)
                player.bankroll.placeBet()
                print(player)
                print('Dealer seems shady, he deals you a new card:\n')
                card = player.deal()
                print(card)
                print('PLAYER hand now: ' + str(player.hand.total()))
                if player.hand.total() >= 21:
                    player_turn = False
            elif action == 'q':
                quit()
            else:
                player_turn = False
            #sleep(1)
        print("\n" * 100)
        print(player)
        #dealer's turn
        if player.hand.total()<=21:
            dealer.aiDeal(player.hand.total())
            print(dealer)
            print('DEALER hand total: ' + str(dealer.hand.total()))
            if dealer.hand.total() <= 21:
                if dealer.hand.total() > player.hand.total():
                    player.playerEndHand('loss')
                elif dealer.hand.total() == player.hand.total():
                    player.playerEndHand('tie')
                else:
                    player.playerEndHand('win')
            else:
                player.playerEndHand('win')
        else:
            player.playerEndHand('loss')

    if not player.playAgain():
        break
    else:
        del deck
        del player
        del dealer
