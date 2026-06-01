VERSION_MAJOR = "001"
VERSION_MINOR = 18

# 原始尺寸作为基准
BASE_SCREEN_WIDTH = 1200
BASE_SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

BASE_CARD_WIDTH = 80
BASE_CARD_HEIGHT = 115
BASE_CARD_SPACING = 8
CARD_WIDTH = 80
CARD_HEIGHT = 115
CARD_SPACING = 8

# 缩放比例
scale_factor = 1.0

# 更新尺寸函数
def update_scale(new_scale):
    global scale_factor, SCREEN_WIDTH, SCREEN_HEIGHT, CARD_WIDTH, CARD_HEIGHT, CARD_SPACING
    scale_factor = new_scale
    SCREEN_WIDTH = int(BASE_SCREEN_WIDTH * scale_factor)
    SCREEN_HEIGHT = int(BASE_SCREEN_HEIGHT * scale_factor)
    CARD_WIDTH = int(BASE_CARD_WIDTH * scale_factor)
    CARD_HEIGHT = int(BASE_CARD_HEIGHT * scale_factor)
    CARD_SPACING = int(BASE_CARD_SPACING * scale_factor)

CARD_COLORS = ['spade', 'heart', 'diamond', 'club']
CARD_COLOR_ORDER = ['spade', 'heart', 'club', 'diamond']  # 黑桃、红桃、草花、方片的排序
CARD_COLOR_NAMES = {
    'spade': '黑桃',
    'heart': '红桃',
    'diamond': '方片',
    'club': '草花'
}

CARD_VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
CARD_VALUE_NAMES = {
    'A': 'A', '2': '2', '3': '3', '4': '4', '5': '5',
    '6': '6', '7': '7', '8': '8', '9': '9', '10': '10',
    'J': 'J', 'Q': 'Q', 'K': 'K', 'joker': '王'
}

CARD_COLOR_RGB = {
    'spade': (0, 0, 0),
    'heart': (220, 20, 60),
    'diamond': (220, 20, 60),
    'club': (0, 0, 0),
    'joker_red': (220, 20, 60),
    'joker_black': (0, 0, 0),
    'special': (128, 128, 128)
}

CARD_SCORES = {
    'J': 11, 'Q': 12, 'K': 13, 'A': 1,
    '2': 2, '3': 3, '4': 4, '5': 5,
    '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'joker': 0
}

GAME_COLORS = {
    'background': (34, 139, 34),
    'card_back': (70, 130, 180),
    'button': (100, 149, 237),
    'button_hover': (65, 105, 225),
    'text': (255, 255, 255),
    'text_dark': (0, 0, 0)
}

HAND_SIZE_RULES = {
    'small': 5,
    'medium': 7,
    'large': 9
}

def get_hand_size(player_count):
    if player_count <= 4:
        return HAND_SIZE_RULES['small']
    elif player_count <= 6:
        return HAND_SIZE_RULES['medium']
    else:
        return HAND_SIZE_RULES['large']
