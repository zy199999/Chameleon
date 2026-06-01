#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from card import Deck

# 测试 2 副牌
deck = Deck(num_decks=2)
print(f"总牌数: {len(deck.cards)}")

# 统计小王和大王的数量
joker_black_count = 0
joker_red_count = 0
for card in deck.cards:
    if card.color == 'joker_black':
        joker_black_count += 1
    if card.color == 'joker_red':
        joker_red_count += 1

print(f"小王 (joker_black) 数量: {joker_black_count}")
print(f"大王 (joker_red) 数量: {joker_red_count}")

# 打印所有大小王
print("\n大小王列表:")
for i, card in enumerate(deck.cards):
    if card.is_joker:
        print(f"  位置 {i}: {card.get_display_name()}")
