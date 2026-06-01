#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from game_engine import GameEngine


# 测试 GameEngine
game = GameEngine(num_decks=2, num_players=2)
game.setup_game(num_decks=2, num_players=2)

print("=== 游戏开始时的状态 ===")

# 统计所有的大小王
all_jokers = []

# 1. 牌堆中的大小王
for card in game.deck.cards:
    if card.is_joker:
        all_jokers.append(("牌堆", card))

# 2. 玩家手牌中的大小王
for player in game.players:
    for card in player.hand:
        if card.is_joker:
            all_jokers.append((player.name, card))

# 3. discard_pile 中的大小王
for card in game.discard_pile:
    if card.is_joker:
        all_jokers.append(("出牌区", card))


print(f"所有大小王数量: {len(all_jokers)}")
joker_black_count = 0
joker_red_count = 0
for source, card in all_jokers:
    print(f"  {source}: {card.get_display_name()} (color: {card.color})")
    if card.color == 'joker_black':
        joker_black_count +=1
    if card.color == 'joker_red':
        joker_red_count +=1

print(f"\n小王 (joker_black) 数量: {joker_black_count}")
print(f"大王 (joker_red) 数量: {joker_red_count}")
print(f"总计: {joker_black_count + joker_red_count}")
