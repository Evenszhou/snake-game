"""
贪吃蛇游戏 - Snake Game
使用 Python + Pygame 开发
"""
import pygame
import sys
import random

# 初始化 Pygame
pygame.init()

# 游戏常量
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    """蛇类"""
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False
    
    def move(self):
        """移动蛇"""
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
            self.direction = direction
    
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
    
    def random_position(self):
        """生成随机位置"""
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    
    def respawn(self, snake_body):
        """重新生成食物（避免在蛇身上）"""
        while True:
            self.position = self.random_position()
            if self.position not in snake_body:
                break


class Game:
    """游戏主类"""
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('贪吃蛇 - Snake Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.speed = 10
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.__init__()
                    elif event.key == pygame.K_q:
                        return False
                else:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.set_direction(UP)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.set_direction(DOWN)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.set_direction(LEFT)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.set_direction(RIGHT)
        return True
    
    def update(self):
        """更新游戏状态"""
        if not self.game_over:
            self.snake.move()
            
            # 检查是否吃到食物
            if self.snake.body[0] == self.food.position:
                self.snake.grow = True
                self.score += 10
                self.food.respawn(self.snake.body)
                # 提升速度
                self.speed = min(20, 10 + self.score // 50)
            
            # 检查碰撞
            if self.snake.check_collision():
                self.game_over = True
    
    def draw(self):
        """绘制游戏画面"""
        self.screen.fill(BLACK)
        
        # 绘制蛇
        for segment in self.snake.body:
            rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, 
                             GRID_SIZE - 2, GRID_SIZE - 2)
            pygame.draw.rect(self.screen, GREEN, rect)
        
        # 绘制食物
        food_rect = pygame.Rect(self.food.position[0] * GRID_SIZE, 
                               self.food.position[1] * GRID_SIZE,
                               GRID_SIZE - 2, GRID_SIZE - 2)
        pygame.draw.rect(self.screen, RED, food_rect)
        
        # 绘制分数
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 游戏结束提示
        if self.game_over:
            game_over_text = self.font.render('GAME OVER! Press R to restart or Q to quit', 
                                             True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.speed)
        
        pygame.quit()
        sys.exit()


def main():
    """主函数"""
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
