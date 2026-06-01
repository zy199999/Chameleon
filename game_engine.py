import random
from card import Deck
from player import Player
from config import get_hand_size, CARD_COLORS

class GameEngine:
    def __init__(self, num_decks=1, num_players=2):
        self.num_decks = num_decks
        self.num_players = num_players
        self.deck = None
        self.players = []
        self.current_player_index = 0
        self.discard_pile = []
        self.current_color = None
        self.current_value = None
        self.game_over = False
        self.winner = None
        self.first_player_index = 0
        self.game_phase = 'setup'
        self.message = ""
        self.turn_count = 0
        self.play_history = []  # 记录最近的出牌，从最新到最旧
        
    def setup_game(self, num_decks, num_players):
        self.num_decks = num_decks
        self.num_players = num_players
        self.deck = Deck(num_decks)
        self.deck.shuffle()
        self.players = []
        self.play_history = []  # 重置出牌历史
        
        for i in range(num_players):
            is_human = (i == 0)
            name = "玩家" if is_human else f"电脑{i}"
            self.players.append(Player(i, name, is_human))
        
        hand_size = get_hand_size(num_players)
        self.first_player_index = random.randint(0, num_players - 1)
        
        for _ in range(hand_size):
            for player in self.players:
                card = self.deck.draw()
                if card:
                    player.add_card(card)
        
        first_card = self.deck.draw()
        if first_card:
            self.discard_pile = [first_card]
            self.update_game_state(first_card)
        
        self.current_player_index = self.first_player_index
        self.game_phase = 'playing'
        self.game_over = False
        self.winner = None
        self.turn_count = 0
        # 在游戏开始时，对第一个玩家的手牌进行排序
        first_player = self.get_current_player()
        first_player.sort_hand()
        self.message = f"{first_player.name}的回合"
    
    def update_game_state(self, card):
        if card.is_special():
            self.current_color = 'special'
            self.current_value = 'blank'
        else:
            self.current_color = card.color
            self.current_value = card.value
    
    def get_current_player(self):
        return self.players[self.current_player_index]
    
    def get_playable_cards(self, player):
        return player.get_playable_cards(self.current_color, self.current_value)
    
    def play_card(self, player, card):
        if card in player.hand:
            if card.is_playable(self.current_color, self.current_value):
                player.remove_card(card)
                self.discard_pile.append(card)
                self.update_game_state(card)
                self.turn_count += 1
                # 记录出牌历史
                self.play_history.insert(0, (player.name, card))
                # 保留最近16次出牌记录
                if len(self.play_history) > 16:
                    self.play_history.pop()
                return True
        return False
    
    def player_draw_card(self, player):
        if not self.deck.is_empty():
            card = self.deck.draw()
            if card:
                player.add_card(card)
                return card
        return None
    
    def next_player(self):
        original_index = self.current_player_index
        while True:
            self.current_player_index = (self.current_player_index + 1) % self.num_players
            current_player = self.get_current_player()
            
            if not current_player.is_done():
                # 在玩家回合开始时，对其手牌进行排序
                current_player.sort_hand()
                self.message = f"{current_player.name}的回合"
                return
            
            if self.current_player_index == original_index:
                self.check_game_over()
                return
    
    def check_game_over(self):
        all_done = True
        for player in self.players:
            if not player.is_done():
                all_done = False
                break
        
        if all_done:
            self.game_over = True
            self.winner = self.get_winner()
            self.game_phase = 'end'
            self.message = f"游戏结束！{self.winner.name}获胜！"
            return True
        return False
    
    def get_winner(self):
        min_score = float('inf')
        winner = None
        for player in self.players:
            total = player.get_total_score()
            if total < min_score:
                min_score = total
                winner = player
        return winner
    
    def select_color(self, player, color):
        if color in CARD_COLORS:
            self.current_color = color
            return True
        return False
    
    def is_game_over(self):
        return self.game_over
    
    def get_game_state(self):
        return {
            'phase': self.game_phase,
            'current_player': self.current_player_index,
            'current_color': self.current_color,
            'current_value': self.current_value,
            'deck_remaining': self.deck.remaining() if self.deck else 0,
            'discard_top': self.discard_pile[-1] if self.discard_pile else None,
            'message': self.message,
            'game_over': self.game_over,
            'winner': self.winner,
            'turn_count': self.turn_count
        }
    
    def ai_select_color(self):
        current_player = self.get_current_player()
        color_counts = {}
        for card in current_player.hand:
            if not card.is_special():
                color_counts[card.color] = color_counts.get(card.color, 0) + 1
        
        if color_counts:
            return max(color_counts, key=color_counts.get)
        return random.choice(CARD_COLORS)
    
    def ai_make_move(self):
        current_player = self.get_current_player()
        playable = self.get_playable_cards(current_player)
        
        if playable:
            card = playable[0]
            state_before = {
                'current_color': self.current_color,
                'current_value': self.current_value
            }
            self.play_card(current_player, card)
            
            needs_color_choice = card.is_special() or card.is_value_matched(
                state_before['current_color'], state_before['current_value'])
            
            if needs_color_choice:
                chosen_color = self.ai_select_color()
                self.select_color(current_player, chosen_color)
        else:
            if current_player.hand:
                card = current_player.hand[0]
                current_player.close_card(card)
                self.turn_count += 1
                self.message = f"{current_player.name}扣了{card.get_display_name()}"
        
        self.player_draw_card(current_player)
        self.check_game_over()
