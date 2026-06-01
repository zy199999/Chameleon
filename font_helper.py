import pygame
import os
import sys


def get_font(size: int = 24):
    """
    获取支持中文的字体，多级回退链
    
    优先级:
    1. 项目目录下的中文字体文件
    2. Windows系统字体目录
    3. pygame默认字体(最后手段)
    """
    # 1. 项目目录下查找字体
    project_dir = os.path.dirname(os.path.abspath(__file__)) if __file__ else '.'
    
    local_fonts = [
        os.path.join(project_dir, 'simhei.ttf'),
        os.path.join(project_dir, 'SimHei.ttf'),
        os.path.join(project_dir, 'msyh.ttf'),
        os.path.join(project_dir, 'MicrosoftYaHei.ttf'),
    ]
    
    for font_path in local_fonts:
        if os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, size)
            except:
                continue
    
    # 2. Windows系统字体目录
    if sys.platform == 'win32':
        system_font_dirs = [
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts'),
            'C:\\Windows\\Fonts'
        ]
        
        windows_fonts = [
            'simhei.ttf', 'msyh.ttf', 'msyhbd.ttf', 'msyhl.ttf',
            'simsun.ttc', 'simkai.ttf', 'SIMHEI.TTF', 'MSYH.TTF'
        ]
        
        for font_dir in system_font_dirs:
            if os.path.exists(font_dir):
                for font_name in windows_fonts:
                    font_path = os.path.join(font_dir, font_name)
                    if os.path.exists(font_path):
                        try:
                            return pygame.font.Font(font_path, size)
                        except:
                            continue
    
    # 3. 尝试用match_font查找字体名
    try:
        font_names = [
            'SimHei', 'Microsoft YaHei UI', 'Microsoft YaHei',
            'SimSun', 'KaiTi'
        ]
        
        for font_name in font_names:
            font_path = pygame.font.match_font(font_name)
            if font_path:
                try:
                    return pygame.font.Font(font_path, size)
                except:
                    continue
    except:
        pass
    
    # 4. 最后手段: 使用默认字体
    return pygame.font.Font(None, size)


def get_title_font():
    return get_font(48)


def get_small_font():
    return get_font(18)
