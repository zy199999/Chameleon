import random
from config import CARD_COLORS, CARD_VALUES, CARD_SCORES, CARD_COLOR_ORDER

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
        self.is_joker = color == 'joker_red' or color == 'joker_black'
        self.is_j = value == 'J'
    
    def is_special(self):
        return self.is_joker or self.is_j
    
    def is_color_matched(self, current_color, current_value):
        """规则a: 判断是否是花色匹配"""
        return current_color != 'special' and self.color == current_color
    
    def is_value_matched(self, current_color, current_value):
        """规则c: 判断是否是大小匹配"""
        return current_value != 'blank' and self.value == current_value
    
    def is_playable(self, current_color, current_value):
        # 规则b: 当前判定花色为特殊，任何牌都可以打
        if current_color == 'special':
            return True
        
        # 规则a: 当前判定花色不为特殊，且牌花色匹配
        if current_color != 'special' and self.color == current_color:
            return True
        
        # 规则c: 当前判定大小不为空白，且牌点数匹配
        if current_value != 'blank' and self.value == current_value:
            return True
        
        # 规则d: 特殊牌（大王/小王/J）可以随时打出
        if self.is_special():
            return True
        
        return False
    
    def get_score(self):
        if self.is_joker:
            return CARD_SCORES['joker']
        return CARD_SCORES.get(self.value, 0)
    
    def get_display_name(self):
        if self.is_joker:
            return '大王' if self.color == 'joker_red' else '小王'
        
        color_names = {'spade': '黑桃', 'heart': '红桃', 'diamond': '方片', 'club': '草花'}
        return f"{color_names.get(self.color, '')}{self.value}"
    
    def get_sort_key(self):
        """获取排序键：先按花色排序，再按分值从大到小排序"""
        if self.is_joker:
            # 大小王排在最前面
            return (-1, 0)  # 或者我们可以定义特殊的排序位置
        
        # 花色索引
        try:
            color_idx = CARD_COLOR_ORDER.index(self.color)
        except ValueError:
            color_idx = len(CARD_COLOR_ORDER)  # 特殊花色放在最后
        
        # 分值：我们希望分值从大到小排列
        # 所以得分越大，排序优先级越高
        score = self.get_score()
        
        # 负数表示分值越大越靠前
        return (color_idx, -score)
    
    def __str__(self):
        return self.get_display_name()
    
    def __repr__(self):
        return f"Card({self.color}, {self.value})"

class Deck:
    def __init__(self, num_decks=1):
        self.cards = []
        self.build_deck(num_decks)
    
    def build_deck(self, num_decks):
        self.cards = []
        
        for _ in range(num_decks):
            for color in CARD_COLORS:
                for value in CARD_VALUES:
                    self.cards.append(Card(color, value))
            
            self.cards.append(Card('joker_red', 'joker'))
            self.cards.append(Card('joker_black', 'joker'))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw(self):
        if self.cards:
            return self.cards.pop()
        return None
    
    def is_empty(self):
        return len(self.cards) == 0
    
    def remaining(self):
        return len(self.cards)
    
    def __len__(self):
        return len(self.cards)
