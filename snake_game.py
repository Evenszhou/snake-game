"""
贪吃蛇游戏 - Snake Game
使用 Python + Pygame 开发
增强版本：包含美化界面、音效和更多功能
"""
import pygame
import sys
import random
import os

# 初始化 Pygame
pygame.init()
pygame.mixer.init()

# 游戏常量
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
FPS = 60

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (46, 204, 113)
DARK_GREEN = (39, 174, 96)
LIGHT_GREEN = (88, 214, 141)
RED = (231, 76, 60)
DARK_RED = (192, 57, 43)
BLUE = (52, 152, 219)
DARK_BLUE = (41, 128, 185)
YELLOW = (241, 196, 15)
ORANGE = (230, 126, 34)
PURPLE = (155, 89, 182)
GRAY = (149, 165, 166)
DARK_GRAY = (44, 62, 80)
BACKGROUND = (30, 30, 30)
GRID_COLOR = (40, 40, 40)

# 方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class SoundManager:
    """音效管理类"""
    def __init__(self):
        self.enabled = True
        self.sounds = {}
        
        # 创建简单的音效（使用合成音）
        try:
            # 吃食物音效
            eat_sound = pygame.mixer.Sound(buffer=self.create_beep(440, 0.1))
            self.sounds['eat'] = eat_sound
            
            # 游戏结束音效
            gameover_sound = pygame.mixer.Sound(buffer=self.create_beep(220, 0.3))
            self.sounds['gameover'] = gameover_sound
            
            # 移动音效（可选）
            move_sound = pygame.mixer.Sound(buffer=self.create_beep(880, 0.05))
            self.sounds['move'] = move_sound
        except:
            self.enabled = False
    
    def create_beep(self, frequency, duration):
        """生成简单的蜂鸣声"""
        import math
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        
        # 创建波形
        buf = bytes(int(127 + 127 * math.sin(2 * math.pi * frequency * i / sample_rate)) 
                   for i in range(n_samples))
        return buf
    
    def play(self, sound_name):
        """播放音效"""
        if self.enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass


class Snake:
    """蛇类"""
    def __init__(self):
        self.reset()
    
    def reset(self):
        """重置蛇的状态"""
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow = False
    
    def move(self):
        """移动蛇"""
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        
        self.body.insert(0, new_head)
    
    def set_direction(self, direction):
        """设置方向（防止反向移动）"""
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction
    
    def check_collision(self):
        """检查碰撞"""
        head = self.body[0]
        # 撞墙
        if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
            return True
        # 撞自己
        if head in self.body[1:]:
            return True
        return False


class Food:
    """食物类"""
    def __init__(self):
        self.position = self.random_position()
        self.type = 'normal'  # normal, bonus
        self.spawn_time = pygame.time.get_ticks()
    
    def random_position(self):
        """生成随机位置"""
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    
    def respawn(self, snake_body):
        """重新生成食物（避免在蛇身上）"""
        while True:
            self.position = self.random_position()
            if self.position not in snake_body:
                break
        
        # 随机生成奖励食物（10%概率）
        self.type = 'bonus' if random.random() < 0.1 else 'normal'
        self.spawn_time = pygame.time.get_ticks()
    
    def get_score(self):
        """获取食物分数"""
        return 20 if self.type == 'bonus' else 10
    
    def get_color(self):
        """获取食物颜色"""
        return YELLOW if self.type == 'bonus' else RED


class Game:
    """游戏主类"""
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('🐍 贪吃蛇 - Snake Game')
        self.clock = pygame.time.Clock()
        
        # 字体
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # 游戏状态
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_over = False
        self.paused = False
        self.speed = 10
        self.level = 1
        
        # 音效
        self.sound_manager = SoundManager()
        
        # 动画
        self.animation_offset = 0
        
        # 游戏状态
        self.state = 'menu'  # menu, playing, paused, gameover
    
    def load_high_score(self):
        """加载最高分"""
        try:
            if os.path.exists('highscore.txt'):
                with open('highscore.txt', 'r') as f:
                    return int(f.read())
        except:
            pass
        return 0
    
    def save_high_score(self):
        """保存最高分"""
        try:
            with open('highscore.txt', 'w') as f:
                f.write(str(self.high_score))
        except:
            pass
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.state == 'menu':
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.start_game()
                    elif event.key == pygame.K_q:
                        return False
                
                elif self.state == 'playing':
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.set_direction(UP)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.set_direction(DOWN)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.set_direction(LEFT)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.set_direction(RIGHT)
                    elif event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.state = 'paused'
                    elif event.key == pygame.K_q:
                        return False
                
                elif self.state == 'paused':
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        self.state = 'playing'
                    elif event.key == pygame.K_q:
                        return False
                
                elif self.state == 'gameover':
                    if event.key == pygame.K_r or event.key == pygame.K_SPACE:
                        self.start_game()
                    elif event.key == pygame.K_m:
                        self.state = 'menu'
                    elif event.key == pygame.K_q:
                        return False
        
        return True
    
    def start_game(self):
        """开始新游戏"""
        self.snake.reset()
        self.food = Food()
        self.score = 0
        self.speed = 10
        self.level = 1
        self.state = 'playing'
    
    def update(self):
        """更新游戏状态"""
        if self.state != 'playing':
            return
        
        self.snake.move()
        
        # 检查是否吃到食物
        if self.snake.body[0] == self.food.position:
            self.snake.grow = True
            self.score += self.food.get_score()
            self.food.respawn(self.snake.body)
            self.sound_manager.play('eat')
            
            # 更新等级和速度
            self.level = self.score // 100 + 1
            self.speed = min(25, 10 + self.level * 2)
            
            # 更新最高分
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
        
        # 检查碰撞
        if self.snake.check_collision():
            self.state = 'gameover'
            self.sound_manager.play('gameover')
        
        # 动画更新
        self.animation_offset = (self.animation_offset + 1) % 10
    
    def draw_grid(self):
        """绘制网格背景"""
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))
    
    def draw_snake(self):
        """绘制蛇"""
        for i, segment in enumerate(self.snake.body):
            x, y = segment
            rect = pygame.Rect(x * GRID_SIZE + 1, y * GRID_SIZE + 1, 
                             GRID_SIZE - 2, GRID_SIZE - 2)
            
            # 蛇头用不同颜色
            if i == 0:
                color = DARK_GREEN
                # 绘制眼睛
                pygame.draw.rect(self.screen, color, rect, border_radius=5)
                eye_size = 4
                eye_offset = 5
                if self.snake.direction == RIGHT:
                    pygame.draw.circle(self.screen, WHITE, 
                                     (x * GRID_SIZE + GRID_SIZE - eye_offset, y * GRID_SIZE + 7), eye_size)
                    pygame.draw.circle(self.screen, WHITE, 
                                     (x * GRID_SIZE + GRID_SIZE - eye_offset, y * GRID_SIZE + 13), eye_size)
                elif self.snake.direction == LEFT:
                    pygame.draw.circle(self.screen, WHITE, 
                                     (x * GRID_SIZE + eye_offset, y * GRID_SIZE + 7), eye_size)
                    pygame.draw.circle(self.screen, WHITE, 
                                     (x * GRID_SIZE + eye_offset, y * GRID_SIZE + 13), eye_size)
                elif self.snake.direction == UP:
                    pygame.draw.circle(self.screen, WHITE, 
                                     (x * GRID_SIZE + 7, y * GRID_SIZE + eye_offset), eye_size)
                    pygame.draw.circle(self.screen, WHITE, 
                                     (x * GRID_SIZE + 13, y * GRID_SIZE + eye_offset), eye_size)
                else:
                    pygame.draw.circle(self.screen, WHITE, 
                                     (x * GRID_SIZE + 7, y * GRID_SIZE + GRID_SIZE - eye_offset), eye_size)
                    pygame.draw.circle(self.screen, WHITE, 
                                     (x * GRID_SIZE + 13, y * GRID_SIZE + GRID_SIZE - eye_offset), eye_size)
            else:
                # 蛇身渐变色
                ratio = i / len(self.snake.body)
                color = (
                    int(GREEN[0] * (1 - ratio * 0.3)),
                    int(GREEN[1] * (1 - ratio * 0.3)),
                    int(GREEN[2] * (1 - ratio * 0.3))
                )
                pygame.draw.rect(self.screen, color, rect, border_radius=3)
    
    def draw_food(self):
        """绘制食物"""
        x, y = self.food.position
        color = self.food.get_color()
        
        # 添加脉动动画效果
        pulse = abs(5 - self.animation_offset)
        
        rect = pygame.Rect(x * GRID_SIZE + 1 - pulse//2, y * GRID_SIZE + 1 - pulse//2, 
                          GRID_SIZE - 2 + pulse, GRID_SIZE - 2 + pulse)
        
        if self.food.type == 'bonus':
            # 奖励食物用星星形状
            pygame.draw.circle(self.screen, color, rect.center, GRID_SIZE//2 - 2)
            pygame.draw.circle(self.screen, ORANGE, rect.center, GRID_SIZE//2 - 4)
        else:
            # 普通食物
            pygame.draw.ellipse(self.screen, color, rect)
            # 添加高光
            highlight = pygame.Rect(x * GRID_SIZE + 4, y * GRID_SIZE + 4, 4, 4)
            pygame.draw.ellipse(self.screen, WHITE, highlight)
    
    def draw_hud(self):
        """绘制游戏信息"""
        # 分数
        score_text = self.font_small.render(f'分数: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 最高分
        high_score_text = self.font_small.render(f'最高分: {self.high_score}', True, YELLOW)
        self.screen.blit(high_score_text, (10, 45))
        
        # 等级
        level_text = self.font_small.render(f'等级: {self.level}', True, BLUE)
        self.screen.blit(level_text, (10, 80))
        
        # 速度
        speed_text = self.font_small.render(f'速度: {self.speed}', True, PURPLE)
        self.screen.blit(speed_text, (10, 115))
    
    def draw_menu(self):
        """绘制主菜单"""
        self.screen.fill(BACKGROUND)
        
        # 标题
        title = self.font_large.render('🐍 贪吃蛇', True, GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # 副标题
        subtitle = self.font_medium.render('Snake Game', True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 220))
        self.screen.blit(subtitle, subtitle_rect)
        
        # 菜单选项
        options = [
            '按 SPACE 或 ENTER 开始游戏',
            '按 Q 退出'
        ]
        
        for i, option in enumerate(options):
            text = self.font_small.render(option, True, GRAY)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 320 + i * 50))
            self.screen.blit(text, text_rect)
        
        # 最高分
        high_score_text = self.font_medium.render(f'最高分: {self.high_score}', True, YELLOW)
        hs_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, 480))
        self.screen.blit(high_score_text, hs_rect)
        
        # 操作说明
        controls = self.font_small.render('操作: 方向键/WASD 移动 | P/ESC 暂停 | Q 退出', True, GRAY)
        controls_rect = controls.get_rect(center=(WINDOW_WIDTH // 2, 550))
        self.screen.blit(controls, controls_rect)
    
    def draw_pause_screen(self):
        """绘制暂停画面"""
        # 半透明遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # 暂停文字
        pause_text = self.font_large.render('暂停', True, WHITE)
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        self.screen.blit(pause_text, pause_rect)
        
        # 提示
        hint_text = self.font_small.render('按 P/ESC/SPACE 继续 | Q 退出', True, GRAY)
        hint_rect = hint_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
        self.screen.blit(hint_text, hint_rect)
    
    def draw_game_over(self):
        """绘制游戏结束画面"""
        # 半透明遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))
        
        # 游戏结束文字
        gameover_text = self.font_large.render('游戏结束!', True, RED)
        gameover_rect = gameover_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
        self.screen.blit(gameover_text, gameover_rect)
        
        # 分数
        score_text = self.font_medium.render(f'最终得分: {self.score}', True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
        self.screen.blit(score_text, score_rect)
        
        # 是否创造新纪录
        if self.score >= self.high_score and self.score > 0:
            record_text = self.font_medium.render('🎉 新纪录!', True, YELLOW)
            record_rect = record_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
            self.screen.blit(record_text, record_rect)
        
        # 选项
        options = self.font_small.render('R/SPACE - 重新开始 | M - 主菜单 | Q - 退出', True, GRAY)
        options_rect = options.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        self.screen.blit(options, options_rect)
    
    def draw(self):
        """绘制游戏画面"""
        if self.state == 'menu':
            self.draw_menu()
        else:
            self.screen.fill(BACKGROUND)
            self.draw_grid()
            self.draw_food()
            self.draw_snake()
            self.draw_hud()
            
            if self.state == 'paused':
                self.draw_pause_screen()
            elif self.state == 'gameover':
                self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        running = True
        move_timer = 0
        
        while running:
            running = self.handle_events()
            
            # 控制蛇的移动速度
            move_timer += 1
            if move_timer >= FPS // self.speed:
                self.update()
                move_timer = 0
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """主函数"""
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
