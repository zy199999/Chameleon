import pygame
import sys
import time
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GAME_COLORS, 
    CARD_WIDTH, CARD_HEIGHT, CARD_SPACING, 
    CARD_COLOR_NAMES, BASE_SCREEN_WIDTH, BASE_SCREEN_HEIGHT,
    scale_factor, update_scale
)
from game_engine import GameEngine
from font_helper import get_font

class ChameleonGameGUI:
    def __init__(self):
        pygame.init()
        self.original_width = SCREEN_WIDTH
        self.original_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("变色龙扑克游戏")
        self.clock = pygame.time.Clock()
        
        # 保存不同缩放级别的字体
        self.update_fonts()
        
        self.phase = 'menu'
        self.game = None
        self.selected_card_index = None
        self.choosing_color = False
        self.card_rects = []
        self.button_rects = []
        self.selected_decks = 1
        self.selected_players = 2
        self.needs_ai_turn = False
        self.ai_turn_timer = 0
    
    def update_fonts(self):
        """根据当前缩放比例更新所有字体大小"""
        global scale_factor
        base_font_size = int(24 * scale_factor)
        base_small_font = int(18 * scale_factor)
        base_title_font = int(48 * scale_factor)
        
        self.font = get_font(base_font_size)
        self.small_font = get_font(base_small_font)
        self.title_font = get_font(base_title_font)
    
    def resize_window(self, new_width, new_height):
        """调整窗口大小并等比例缩放"""
        # 计算新的缩放比例（保持16:10的宽高比）
        aspect_ratio = BASE_SCREEN_WIDTH / BASE_SCREEN_HEIGHT
        new_height_auto = int(new_width / aspect_ratio)
        new_width_auto = int(new_height * aspect_ratio)
        
        # 选择最接近目标尺寸的等比例缩放
        if abs(new_height_auto - new_height) < abs(new_width_auto - new_width):
            target_width = new_width
            target_height = new_height_auto
        else:
            target_width = new_width_auto
            target_height = new_height
        
        # 计算缩放比例，限制在合理范围内（0.5到2.0）
        new_scale = min(2.0, max(0.5, target_width / BASE_SCREEN_WIDTH))
        
        # 更新全局变量
        update_scale(new_scale)
        
        # 重新设置显示模式
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        self.update_fonts()
    
    def draw_version(self):
        version_text = self.small_font.render("V001.18", True, (0, 0, 0))
        version_rect = version_text.get_rect(topleft=(10, 10))
        pygame.draw.rect(self.screen, (255, 255, 255), (5, 5, version_rect.width + 10, version_rect.height + 10), border_radius=5)
        self.screen.blit(version_text, version_rect)
    
    def draw_menu(self):
        self.screen.fill(GAME_COLORS['background'])
        self.draw_version()
        self.button_rects = []
        
        title = self.title_font.render("变色龙扑克", True, GAME_COLORS['text'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title, title_rect)
        
        pygame.draw.rect(self.screen, (0, 150, 0), (400, 250, 400, 80), border_radius=10)
        pygame.draw.rect(self.screen, (255, 215, 0), (400, 250, 400, 80), 3, border_radius=10)
        start_text = self.font.render("开始游戏", True, GAME_COLORS['text'])
        start_rect = start_text.get_rect(center=(600, 290))
        self.screen.blit(start_text, start_rect)
        self.button_rects.append((400, 250, 400, 80, 'start'))
        
        pygame.display.flip()
    
    def draw_setup(self):
        self.screen.fill(GAME_COLORS['background'])
        self.draw_version()
        self.button_rects = []
        
        title = self.title_font.render("游戏设置", True, GAME_COLORS['text'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # 牌数选择 (1或2副)
        deck_label = self.font.render("牌堆数量:", True, (255, 255, 255))
        self.screen.blit(deck_label, (300, 200))
        
        for i in range(1, 3):
            x = 450 + i * 80
            color = (0, 150, 0) if self.selected_decks == i else (80, 80, 80)
            pygame.draw.rect(self.screen, color, (x, 190, 70, 40), border_radius=8)
            pygame.draw.rect(self.screen, (255, 215, 0), (x, 190, 70, 40), 3, border_radius=8)
            deck_text = self.font.render(str(i), True, (255, 255, 255))
            text_rect = deck_text.get_rect(center=(x + 35, 210))
            self.screen.blit(deck_text, text_rect)
            self.button_rects.append((x, 190, 70, 40, f'deck_{i}'))
        
        # 玩家数量选择 (2到8名)
        player_label = self.font.render("玩家数量:", True, (255, 255, 255))
        self.screen.blit(player_label, (300, 280))
        
        for i in range(2, 9):
            x = 370 + i * 70
            color = (0, 150, 0) if self.selected_players == i else (80, 80, 80)
            pygame.draw.rect(self.screen, color, (x, 270, 55, 40), border_radius=8)
            pygame.draw.rect(self.screen, (255, 215, 0), (x, 270, 55, 40), 3, border_radius=8)
            player_text = self.font.render(str(i), True, (255, 255, 255))
            text_rect = player_text.get_rect(center=(x + 27, 290))
            self.screen.blit(player_text, text_rect)
            self.button_rects.append((x, 270, 55, 40, f'player_{i}'))
        
        pygame.draw.rect(self.screen, (0, 150, 0), (400, 400, 400, 60), border_radius=10)
        pygame.draw.rect(self.screen, (255, 215, 0), (400, 400, 400, 60), 3, border_radius=10)
        confirm_text = self.font.render("确认", True, GAME_COLORS['text'])
        confirm_rect = confirm_text.get_rect(center=(600, 430))
        self.screen.blit(confirm_text, confirm_rect)
        self.button_rects.append((400, 400, 400, 60, 'confirm'))
        
        pygame.draw.rect(self.screen, (150, 150, 150), (400, 480, 400, 60), border_radius=10)
        pygame.draw.rect(self.screen, (255, 215, 0), (400, 480, 400, 60), 3, border_radius=10)
        back_text = self.font.render("返回主菜单", True, GAME_COLORS['text'])
        back_rect = back_text.get_rect(center=(600, 510))
        self.screen.blit(back_text, back_rect)
        self.button_rects.append((400, 480, 400, 60, 'back'))
    
    def draw_card(self, card, x, y, highlight=False, face_up=True):
        bg_color = (220, 220, 220)
        if card and not card.is_joker:
            if card.color in ['spade', 'club']:
                bg_color = (200, 200, 200)
            elif card.color in ['heart', 'diamond']:
                bg_color = (255, 220, 220)
        
        pygame.draw.rect(self.screen, bg_color, (x, y, CARD_WIDTH, CARD_HEIGHT), border_radius=8)
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, CARD_WIDTH, CARD_HEIGHT), 2, border_radius=8)
        
        if highlight:
            pygame.draw.rect(self.screen, (0, 255, 0), (x - 3, y - 3, CARD_WIDTH + 6, CARD_HEIGHT + 6), 3, border_radius=10)
        
        if face_up and card:
            if card.is_joker:
                pygame.draw.rect(self.screen, (200, 0, 0) if card.color == 'joker_red' else (0, 0, 200), (x + 10, y + 10, CARD_WIDTH - 20, CARD_HEIGHT - 20), border_radius=5)
                joker_text = self.font.render("王", True, (255, 255, 255))
                text_rect = joker_text.get_rect(center=(x + CARD_WIDTH//2, y + CARD_HEIGHT//2))
                self.screen.blit(joker_text, text_rect)
            else:
                value_color = (0, 0, 0) if card.color in ['spade', 'club'] else (200, 0, 0)
                value_text = self.font.render(card.value, True, value_color)
                text_rect = value_text.get_rect(topleft=(x + 8, y + 5))
                self.screen.blit(value_text, text_rect)
                self.draw_suit_symbol(card.color, x + CARD_WIDTH//2, y + CARD_HEIGHT//2, 30)
    
    def draw_suit_symbol(self, color, x, y, size):
        if color == 'spade':
            # 黑桃：完美还原标准扑克牌 - 根据用户建议调整
            # 1. 画两个主要的圆 - 横向分开一点点
            pygame.draw.circle(self.screen, (0, 0, 0), (x - size*3//8, y), size*5//12)
            pygame.draw.circle(self.screen, (0, 0, 0), (x + size*3//8, y), size*5//12)
            # 2. 画顶部的三角形，尖向上 - 继续往上
            pygame.draw.polygon(self.screen, (0, 0, 0), [
                (x, y - size),
                (x - size*7//12, y + size//10),
                (x + size*7//12, y + size//10)
            ])
            # 3. 画底部的三角形，调整方向 - 保持向下但调整更完美
            pygame.draw.polygon(self.screen, (0, 0, 0), [
                (x - size*2//5, y + size//10),
                (x + size*2//5, y + size//10),
                (x, y + size//2)
            ])
            # 4. 画底部的小柄
            pygame.draw.polygon(self.screen, (0, 0, 0), [
                (x - size//10, y + size//4),
                (x + size//10, y + size//4),
                (x + size//16, y + size*3//4),
                (x, y + size),
                (x - size//16, y + size*3//4),
            ])
        elif color == 'heart':
            # 红桃：心形，标准扑克牌形状
            pygame.draw.polygon(self.screen, (200, 0, 0), [
                (x, y + size//3),           # 底部尖端
                (x - size//2, y - size//6), # 左上部
                (x - size//4, y - size//2), # 左圆顶
                (x, y - size//4),           # 中心
                (x + size//4, y - size//2), # 右圆顶
                (x + size//2, y - size//6), # 右上部
            ])
            # 补充两个圆来做圆润的心形
            pygame.draw.circle(self.screen, (200, 0, 0), (x - size//4, y - size//4), size//4)
            pygame.draw.circle(self.screen, (200, 0, 0), (x + size//4, y - size//4), size//4)
        elif color == 'diamond':
            pygame.draw.polygon(self.screen, (200, 0, 0), [
                (x, y - size//2), (x + size//3, y), (x, y + size//2), (x - size//3, y)
            ])
        elif color == 'club':
            pygame.draw.circle(self.screen, (0, 0, 0), (x, y - size//3), size//3)
            pygame.draw.circle(self.screen, (0, 0, 0), (x - size//3, y + size//6), size//4)
            pygame.draw.circle(self.screen, (0, 0, 0), (x + size//3, y + size//6), size//4)
            pygame.draw.polygon(self.screen, (0, 0, 0), [
                (x, y + size//3), (x + size//5, y + size//3), (x, y + size), (x - size//5, y + size//3)
            ])
    
    def draw_game(self):
        self.screen.fill(GAME_COLORS['background'])
        self.draw_version()
        self.button_rects = []
        
        if not self.game:
            return
        
        state = self.game.get_game_state()
        
        if state['game_over']:
            self.phase = 'end'
            return
        
        current_player = self.game.get_current_player()
        
        turn_text = self.title_font.render(f"第 {state['turn_count']} 回合", True, (255, 215, 0))
        turn_rect = turn_text.get_rect(center=(SCREEN_WIDTH//2, 60))
        self.screen.blit(turn_text, turn_rect)
        
        current_text = self.font.render(f"当前: {current_player.name}", True, (255, 255, 0))
        self.screen.blit(current_text, (450, 110))
        
        # 判定花色和大小将在出牌区上方显示
        
        deck_text = self.font.render(f"抽牌堆: {state['deck_remaining']}张", True, (255, 255, 255))
        self.screen.blit(deck_text, (1000, 60))
        
        for i, player in enumerate(self.game.players):
            y_pos = 140 + i * 40
            color = (255, 255, 255) if i != self.game.current_player_index else (255, 255, 0)
            if player.is_human:
                player_text = self.small_font.render(
                    f"{player.name}: {len(player.hand)}张手牌 {player.score}分",
                    True, color
                )
            else:
                player_text = self.small_font.render(
                    f"{player.name}: {len(player.hand)}张手牌",
                    True, color
                )
            self.screen.blit(player_text, (20, y_pos))
        
        discard_x = SCREEN_WIDTH // 2 - CARD_WIDTH // 2
        discard_y = SCREEN_HEIGHT // 2 - CARD_HEIGHT // 2 - 50
        
        # 在出牌区上方居中显示判定花色和判定大小（向上移动，不影响卡牌位置）
        text_top_y = discard_y - 100
        if state['current_color']:
            color_name = CARD_COLOR_NAMES.get(state['current_color'], '特殊')
            color_text = self.font.render(f"判定花色: {color_name}", True, (255, 255, 255))
            color_rect = color_text.get_rect(center=(SCREEN_WIDTH//2, text_top_y))
            self.screen.blit(color_text, color_rect)
        
        if state['current_value'] and state['current_value'] != 'blank':
            value_text = self.font.render(f"判定大小: {state['current_value']}", True, (255, 255, 255))
            value_rect = value_text.get_rect(center=(SCREEN_WIDTH//2, text_top_y + 30))
            self.screen.blit(value_text, value_rect)
        
        discard_label = self.font.render("出牌区", True, (255, 255, 255))
        discard_rect = discard_label.get_rect(center=(SCREEN_WIDTH//2, text_top_y + 60))
        self.screen.blit(discard_label, discard_rect)
        
        if state['discard_top']:
            self.draw_card(state['discard_top'], discard_x, discard_y)
        else:
            pygame.draw.rect(self.screen, (200, 200, 200), 
                           (discard_x, discard_y, CARD_WIDTH, CARD_HEIGHT), 
                           border_radius=8)
        
        # 显示最近的出牌历史（从最新到最旧，一行8个，居中）
        if self.game.play_history:
            history_y = discard_y + CARD_HEIGHT + 20
            history_label = self.small_font.render("最近出牌:", True, (200, 200, 200))
            label_rect = history_label.get_rect(center=(SCREEN_WIDTH//2, history_y))
            self.screen.blit(history_label, label_rect)
            
            num_cards = min(len(self.game.play_history), 8)
            card_spacing = 10
            small_width = 60
            small_height = 85
            total_width = num_cards * small_width + (num_cards - 1) * card_spacing
            start_history_x = SCREEN_WIDTH//2 - total_width//2
            
            # 显示最近8张牌
            for i, (player_name, card) in enumerate(self.game.play_history[:8]):
                x = start_history_x + i * (small_width + card_spacing)
                y = history_y + 10
                
                # 绘制小牌
                bg_color = (200, 200, 200)
                if not card.is_joker:
                    if card.color in ['spade', 'club']:
                        bg_color = (180, 180, 180)
                    elif card.color in ['heart', 'diamond']:
                        bg_color = (255, 200, 200)
                pygame.draw.rect(self.screen, bg_color, (x, y, small_width, small_height), border_radius=5)
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, small_width, small_height), 1, border_radius=5)
                
                if not card.is_joker:
                    # 绘制小牌内容
                    value_color = (0, 0, 0) if card.color in ['spade', 'club'] else (200, 0, 0)
                    # 使用已有的小字体
                    value_text = self.small_font.render(card.value, True, value_color)
                    # 调整文本位置以适合小牌
                    scaled_text = pygame.transform.scale(value_text, (int(value_text.get_width()*0.7), int(value_text.get_height()*0.7)))
                    self.screen.blit(scaled_text, (x + 5, y + 5))
                    
                    # 绘制小花色
                    if card.color in ['spade', 'heart', 'diamond', 'club']:
                        self.draw_suit_symbol(card.color, x + small_width//2, y + small_height//2, 20)
                else:
                    # 大小王
                    joker_color = (200, 0, 0) if card.color == 'joker_red' else (0, 0, 200)
                    pygame.draw.rect(self.screen, joker_color, (x + 8, y + 8, small_width - 16, small_height - 16), border_radius=3)
                    joker_text = self.small_font.render("王", True, (255, 255, 255))
                    scaled_joker = pygame.transform.scale(joker_text, (int(joker_text.get_width()*0.7), int(joker_text.get_height()*0.7)))
                    text_rect = scaled_joker.get_rect(center=(x + small_width//2, y + small_height//2))
                    self.screen.blit(scaled_joker, text_rect)
                
                # 绘制玩家名（小字体）
                name_text = self.small_font.render(player_name, True, (255, 255, 255))
                scaled_name = pygame.transform.scale(name_text, (int(name_text.get_width()*0.6), int(name_text.get_height()*0.6)))
                name_rect = scaled_name.get_rect(center=(x + small_width//2, y + small_height + 12))
                self.screen.blit(scaled_name, name_rect)
        
        draw_deck_x = SCREEN_WIDTH - 200
        draw_deck_y = SCREEN_HEIGHT // 2 - CARD_HEIGHT // 2
        
        deck_label = self.font.render("抽牌堆", True, (255, 255, 255))
        self.screen.blit(deck_label, (draw_deck_x + 5, draw_deck_y - 30))
        
        for offset in range(3):
            self.draw_card(None, draw_deck_x - offset*2, draw_deck_y - offset*2, face_up=False)
        
        player = self.game.players[0]
        hand_cards = player.hand
        total_width = len(hand_cards) * (CARD_WIDTH + CARD_SPACING) - CARD_SPACING
        start_x = (SCREEN_WIDTH - total_width) // 2
        hand_y = SCREEN_HEIGHT - CARD_HEIGHT - 60
        
        self.card_rects = []
        playable = []
        
        if player.is_human:
            playable = self.game.get_playable_cards(player)
        
        for i, card in enumerate(hand_cards):
            x = start_x + i * (CARD_WIDTH + CARD_SPACING)
            is_playable = card in playable
            highlight = (self.selected_card_index == i)
            
            self.draw_card(card, x, hand_y, highlight=highlight)
            
            if is_playable:
                pygame.draw.circle(self.screen, (0, 255, 0), (x + CARD_WIDTH//2, hand_y - 10), 5)
            
            self.card_rects.append((x, hand_y, CARD_WIDTH, CARD_HEIGHT, i))
        
        pygame.draw.rect(self.screen, (0, 0, 0), (0, hand_y - 40, SCREEN_WIDTH, 35))
        score_text = self.font.render(f"你的累计积分: {player.score}", True, (255, 255, 0))
        self.screen.blit(score_text, (SCREEN_WIDTH//2 - 100, hand_y - 30))
        
        if player.is_human and self.selected_card_index is not None:
            action_x = SCREEN_WIDTH - 150
            action_y = hand_y
            
            selected_card = hand_cards[self.selected_card_index]
            is_playable = selected_card in playable
            
            selected_info = self.small_font.render(f"已选择: {selected_card.get_display_name()}", True, (255, 255, 255))
            self.screen.blit(selected_info, (action_x - 50, action_y - 40))
            
            # 上面是扣牌按钮
            pygame.draw.rect(self.screen, (200, 100, 100), 
                           (action_x, action_y, 100, 50), border_radius=10)
            pygame.draw.rect(self.screen, (255, 215, 0), (action_x, action_y, 100, 50), 3, border_radius=10)
            close_text = self.font.render("扣牌", True, (255, 255, 255))
            self.screen.blit(close_text, (action_x + 15, action_y + 12))
            self.button_rects.append((action_x, action_y, 100, 50, 'close'))
            
            # 下面是出牌按钮（仅当牌可出时显示）
            if is_playable:
                pygame.draw.rect(self.screen, (100, 200, 100), 
                               (action_x, action_y + 60, 100, 50), border_radius=10)
                pygame.draw.rect(self.screen, (255, 215, 0), (action_x, action_y + 60, 100, 50), 3, border_radius=10)
                play_text = self.font.render("出牌", True, (255, 255, 255))
                self.screen.blit(play_text, (action_x + 15, action_y + 72))
                self.button_rects.append((action_x, action_y + 60, 100, 50, 'play'))
        
        message_text = self.font.render(state['message'], True, (255, 255, 255))
        message_rect = message_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 20))
        self.screen.blit(message_text, message_rect)
        
        if self.choosing_color:
            self.draw_color_selection()
    
    def draw_color_selection(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        title = self.font.render("选择新判定花色:", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 150))
        self.screen.blit(title, title_rect)
        
        start_x = SCREEN_WIDTH//2 - 200
        y = SCREEN_HEIGHT//2 - 50
        
        self.button_rects = []
        for i, color in enumerate(['spade', 'heart', 'diamond', 'club']):
            x = start_x + i * 110
            pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 100, 100), border_radius=10)
            pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 100, 100), 2, border_radius=10)
            pygame.draw.rect(self.screen, (255, 215, 0), (x, y, 100, 100), 3, border_radius=10)
            self.draw_suit_symbol(color, x + 50, y + 35, 25)
            color_name = CARD_COLOR_NAMES[color]
            text = self.font.render(color_name, True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + 50, y + 75))
            self.screen.blit(text, text_rect)
            self.button_rects.append((x, y, 100, 100, f'color_{color}'))
    
    def draw_end_screen(self):
        self.screen.fill(GAME_COLORS['background'])
        self.draw_version()
        self.button_rects = []
        
        if not self.game:
            return
        
        title = self.title_font.render("游戏结束!", True, (255, 215, 0))
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 80))
        self.screen.blit(title, title_rect)
        
        winner = self.game.winner
        if winner:
            winner_text = self.font.render(f"获胜者: {winner.name} (积分最低)", True, (0, 255, 0))
            winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH//2, 150))
            self.screen.blit(winner_text, winner_rect)
        
        y = 200
        for i, player in enumerate(self.game.players):
            is_winner = player == winner
            color = (0, 255, 0) if is_winner else (255, 255, 255)
            
            # 一行显示两个玩家
            col = i % 2
            x = 250 if col == 0 else 700
            
            total_score = player.get_total_score()
            text = self.font.render(f"{player.name}: 积分 {total_score}", True, color)
            self.screen.blit(text, (x, y))
            
            if player.closed_pile:
                # 扣牌信息在玩家信息下方
                closed_cards = ", ".join([card.get_display_name() for card in player.closed_pile])
                cards_text = self.small_font.render(f"扣牌: {closed_cards}", True, (200, 200, 200))
                self.screen.blit(cards_text, (x, y + 30))
            
            # 每两个玩家换下一行
            if i % 2 == 1:
                y += 80
        
        # 按钮放在同一行
        pygame.draw.rect(self.screen, (0, 180, 0), (300, 600, 280, 60), border_radius=10)
        pygame.draw.rect(self.screen, (255, 215, 0), (300, 600, 280, 60), 3, border_radius=10)
        restart_text = self.font.render("再来一局", True, GAME_COLORS['text'])
        restart_rect = restart_text.get_rect(center=(440, 630))
        self.screen.blit(restart_text, restart_rect)
        self.button_rects.append((300, 600, 280, 60, 'restart'))
        
        pygame.draw.rect(self.screen, (150, 150, 150), (620, 600, 280, 60), border_radius=10)
        pygame.draw.rect(self.screen, (255, 215, 0), (620, 600, 280, 60), 3, border_radius=10)
        menu_text = self.font.render("返回主菜单", True, GAME_COLORS['text'])
        menu_rect = menu_text.get_rect(center=(760, 630))
        self.screen.blit(menu_text, menu_rect)
        self.button_rects.append((620, 600, 280, 60, 'menu'))
    
    def handle_click(self, pos):
        x, y = pos
        
        if self.phase == 'menu':
            for button in self.button_rects:
                bx, by, bw, bh, action = button
                if bx <= x <= bx + bw and by <= y <= by + bh:
                    if action == 'start':
                        self.phase = 'setup'
        
        elif self.phase == 'setup':
            for button in self.button_rects:
                bx, by, bw, bh, action = button
                if bx <= x <= bx + bw and by <= y <= by + bh:
                    if action.startswith('deck_'):
                        self.selected_decks = int(action.split('_')[1])
                    elif action.startswith('player_'):
                        self.selected_players = int(action.split('_')[1])
                    elif action == 'confirm':
                        self.game = GameEngine(self.selected_decks, self.selected_players)
                        self.game.setup_game(self.selected_decks, self.selected_players)
                        self.phase = 'game'
                        self.selected_card_index = None
                        self.choosing_color = False
                        if not self.game.get_current_player().is_human:
                            self.needs_ai_turn = True
                            self.ai_turn_timer = time.time()
                    elif action == 'back':
                        self.phase = 'menu'
        
        elif self.phase == 'game':
            if self.choosing_color:
                for button in self.button_rects:
                    bx, by, bw, bh, action = button
                    if bx <= x <= bx + bw and by <= y <= by + bh:
                        if action.startswith('color_'):
                            color = action.split('_')[1]
                            player = self.game.get_current_player()
                            self.game.select_color(player, color)
                            self.choosing_color = False
                            self.game.player_draw_card(player)
                            self.game.check_game_over()
                            self.game.next_player()
                            if self.game.get_game_state()['game_over']:
                                return
                            if not self.game.get_current_player().is_human:
                                self.needs_ai_turn = True
                                self.ai_turn_timer = time.time()
            else:
                card_clicked = False
                for rect in self.card_rects:
                    cx, cy, cw, ch, index = rect
                    if cx <= x <= cx + cw and cy <= y <= cy + ch:
                        self.selected_card_index = index
                        card_clicked = True
                        break
                
                if not card_clicked:
                    for button in self.button_rects:
                        bx, by, bw, bh, action = button
                        if bx <= x <= bx + bw and by <= y <= by + bh:
                            player = self.game.players[0]
                            if action == 'play' and self.selected_card_index is not None:
                                card = player.hand[self.selected_card_index]
                                state_before = self.game.get_game_state()
                                
                                if self.game.play_card(player, card):
                                    needs_color_choice = card.is_special() or card.is_value_matched(
                                        state_before['current_color'], state_before['current_value'])
                                    
                                    if needs_color_choice:
                                        self.choosing_color = True
                                    else:
                                        self.game.player_draw_card(player)
                                        self.game.check_game_over()
                                        if self.game.get_game_state()['game_over']:
                                            return
                                        self.game.next_player()
                                        if not self.game.get_current_player().is_human:
                                            self.needs_ai_turn = True
                                            self.ai_turn_timer = time.time()
                            
                            elif action == 'close' and self.selected_card_index is not None:
                                card = player.hand[self.selected_card_index]
                                player.close_card(card)
                                self.game.player_draw_card(player)
                                self.game.check_game_over()
                                if not self.game.get_game_state()['game_over']:
                                    self.game.next_player()
                                    if not self.game.get_current_player().is_human:
                                        self.needs_ai_turn = True
                                        self.ai_turn_timer = time.time()
                            self.selected_card_index = None
        
        elif self.phase == 'end':
            for button in self.button_rects:
                bx, by, bw, bh, action = button
                if bx <= x <= bx + bw and by <= y <= by + bh:
                    if action == 'restart':
                        if self.game:
                            self.game.setup_game(self.selected_decks, self.selected_players)
                            self.phase = 'game'
                            self.selected_card_index = None
                            self.choosing_color = False
                            if not self.game.get_current_player().is_human:
                                self.needs_ai_turn = True
                                self.ai_turn_timer = time.time()
                    elif action == 'menu':
                        self.phase = 'menu'
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_r and self.phase == 'end':
                        if self.game:
                            self.game.setup_game(self.selected_decks, self.selected_players)
                            self.phase = 'game'
                            if not self.game.get_current_player().is_human:
                                self.needs_ai_turn = True
                                self.ai_turn_timer = time.time()
                    if event.key == pygame.K_F11:
                        # F11 键切换全屏模式
                        if self.screen.get_flags() & pygame.FULLSCREEN:
                            # 退出全屏，恢复等比例窗口
                            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF)
                        else:
                            # 进入全屏
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
                            # 等比例缩放填充整个屏幕
                            w, h = self.screen.get_size()
                            self.resize_window(w, h)
                
                if event.type == pygame.VIDEORESIZE:
                    # 窗口调整事件，等比例缩放
                    if not (self.screen.get_flags() & pygame.FULLSCREEN):
                        self.resize_window(event.w, event.h)
            
            if self.needs_ai_turn and self.phase == 'game':
                if self.game and self.game.get_current_player().is_human:
                    self.needs_ai_turn = False
                else:
                    current_time = time.time()
                    if current_time - self.ai_turn_timer >= 0.5:
                        if self.game and not self.game.get_current_player().is_human:
                            self.game.ai_make_move()
                            if not self.game.check_game_over():
                                self.game.next_player()
                                if not self.game.get_current_player().is_human:
                                    self.ai_turn_timer = time.time()
                                else:
                                    self.needs_ai_turn = False
                            else:
                                self.needs_ai_turn = False
            
            if self.phase == 'menu':
                self.draw_menu()
            elif self.phase == 'setup':
                self.draw_setup()
            elif self.phase == 'game':
                self.draw_game()
            elif self.phase == 'end':
                self.draw_end_screen()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = ChameleonGameGUI()
    game.run()
