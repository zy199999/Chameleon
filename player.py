class Player:
    def __init__(self, player_id, name, is_human=False):
        self.player_id = player_id
        self.name = name
        self.is_human = is_human
        self.hand = []
        self.closed_pile = []
        self.score = 0
    
    def add_card(self, card):
        if card:
            self.hand.append(card)
    
    def remove_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
            return card
        return None
    
    def close_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
            self.closed_pile.append(card)
            self.score += card.get_score()
            return card
        return None
    
    def get_playable_cards(self, current_color, current_value):
        playable = []
        for card in self.hand:
            if card.is_playable(current_color, current_value):
                playable.append(card)
        return playable
    
    def has_playable_card(self, current_color, current_value):
        return len(self.get_playable_cards(current_color, current_value)) > 0
    
    def is_done(self):
        return len(self.hand) == 0
    
    def get_total_score(self):
        return self.score
    
    def get_closed_pile_score(self):
        return sum(card.get_score() for card in self.closed_pile)
    
    def sort_hand(self):
        """手牌排序：先按黑桃红桃草花方片的顺序，再按分值从大到小排列"""
        self.hand.sort(key=lambda card: card.get_sort_key())
    
    def __str__(self):
        return f"{self.name} ({len(self.hand)}张手牌, {self.score}分)"
    
    def __repr__(self):
        return f"Player({self.player_id}, {self.name}, human={self.is_human})"
