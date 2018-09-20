suits = ('Heart', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
value = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
game = None

import random

class Game:
    def __init__(self):
        self.playing = True
        self.players = []
        self.dealer = Dealer(self)
        self.turn = None
        self.deck = Deck()

    def add_player(self, player):
        self.players.append(player)

    def start_game(self):
        self.players.append(self.dealer)
        self.turn = self.players[0]
        self.deck.shuffle()

    def deal(self):
        self.deck.deal(self.players)

    def bet(self, amount):
        self.bet_money = amount
    
    def bust(self, player):
        ##player.adjust_chips(self.bet_money * -1)
        self.end_turn()

    def end_turn(self):
            
        self.turn = self.players[self.players.index(self.turn) + 1]

    def find_winner(self):
        max = 0
        winner = None
        for player in self.players:
            if player.get_sum() > 21:
                continue
            if player.get_sum() > max:
                max = player.get_sum()
                winner = player
                
            elif player.get_sum() == max:
                if len(player.hand.cards) < len(winner.hand.cards):
                    winner = player
                elif len(player.hand.cards) == len(winner.hand.cards):
                    '''
                    if sum & number of cards are all equal
                    needs to be added
                    '''
        
        return winner

    def win(self,player):
        player.adjust_chips(self.bet_money)

    def lose(self, player):
        player.adjust_chips(-1* self.bet_money)

class Participant:
    '''
    interface for player & dealer
    '''
    def __init__(self, game):
        self.game = game
        self.hand = Hand()

    def vacate(self):
        self.hand = Hand()

    def hit(self, deck):
        for card in deck.draw():
            self.hand.add_card(card)
            ##print(f'player {self.name} got {card}')
            print(f'now sum is {self.hand.sum}')
        if self.hand.sum > 21:
            self.bust()
        

    def get_sum(self):
        return self.hand.sum

    def bust(self):
        self.game.bust(self)

    def show(self):
        raise NotImplementedError('subclass must implement this method')


class Player(Participant):
    def __init__(self, name, game):
        Participant.__init__(self, game)
        self.name = name
        self.chips = 100

    def stand(self):
        self.game.end_turn()

    def show(self):
        print(f"player {self.name}'s cards: '")
        for card in self.hand.cards:
            print(f"{card}")

    def adjust_chips(self,amount):
        self.chips+=amount

    def bet(self,amount):
        self.game.bet(amount)

class Dealer(Participant):
    def __init__(self, game):
        Participant.__init__(self, game)
        self.name = 'Dealer'

    def show(self):
        print(f'dealer\'s card: {self.hand.cards[0]}')

    def bust(self):
        self.game.bust(self)

    def hit(self, deck):
        while self.hand.sum <17:
            for card in deck.draw():
                self.hand.add_card(card)
                ##print(f'player {self.name} got {card}')
                print(f'now sum is {self.hand.sum}')
            if self.hand.sum > 21:
                self.bust()

class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self, amount=1):
        for i in range(0, amount):
            yield self.deck.pop()

    def deal(self, players):
        for player in players:
            for card in self.draw(2):
                player.hand.add_card(card)

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.suit} {self.rank}'
  

class Hand:
    '''
    Store info about cards in the hand
    '''
    def __init__(self):
        self.cards = []
        self.sum = 0
        self.aces_of_11 = 0

    def add_card(self, card):
        self.cards.append(card)
        if card.rank is 'Ace':
            if self.sum > 10:
                self.sum += 1
            else:
                self.sum+=11
                self.aces_of_11 += 1
        else:
            self.sum+=value[card.rank]

        if self.sum > 21:
            if self.aces_of_11 > 0:
                self.sum-=10
                self.aces_of_11=0

def hit_or_stand(player):
    while True:
        res = input(f'what do you wanna do {player.name}?\nhit:type 1\nstand: type 2\n')
        if res is '1':
            player.hit(game.deck)
            if player.get_sum() > 21:
                print('you busted!!, you lose')
                break
            
        elif res is '2':
            player.stand()
            print('You chose stand, turn ended')
            break

player1 = None
while True:
    print('Welcome to the BlackJack Table')
    game = Game()
    
    if player1 is None:
        name = input('new Customer!! type your name\n')
        player1  = Player(name, game)
    
    res = input('if you wanna play a game, type \'yes\' if not, type \'no\'\n')

    if res == 'yes':
        '''
        Let's start a game
        set deck
        '''
        print(f'you have {player1.chips} chips')
        game.add_player(player1)
        bet_money = int(input('how much do you wanna bet?'))
        game.bet(bet_money)
        game.start_game()
        game.deal()
        
        for player in game.players:
            player.show()

        while game.turn != game.dealer:
            print(f'player {game.turn.name}\'s turn!!')
            hit_or_stand(game.turn)

        print('dealer\'s turn!!')
        game.dealer.hit(game.deck)
        winner = game.find_winner()

        if winner is game.dealer:
            print(f"dealer won")
        else:
            game.win(winner)
            print(f"the winner is {winner.name}")

        for player in game.players:
            if player != winner and not isinstance(player, Dealer):
                game.lose(player)

    elif res is 'no':
        print('Game will be quited')
        break
    
    else: 
        print('Type valid answer!!')
            
        


    
