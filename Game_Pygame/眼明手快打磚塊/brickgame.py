import pygame, random, math, time

# 創建顏色(三個參數為RGB)
GREEN = (0,255,0) # 綠色
RED = (255,0,0) # 紅色
BLUE = (0,0,255) # 藍色
WHITE = (255,255,255) # 白色
BLACK = (0,0,0) # 黑色
YELLOW = (255,255,0) #黃色
PURPLE = (255,0,255)

def ini_sprite(Sprite, ini_pos, pic_path=None, color=None, size=None):
    """
    初始化pygame.sprite.Sprite物件
    Sprite: 必順是繼承pygame.sprite.Sprite的class
    ini_pos(tuple): 初始x,y座標(左上角)
    picture_path: 若存在，則讀取指定圖檔
    color(RGB): 顏色
    size(tuple): 物件之矩形框大小
    """
    pygame.sprite.Sprite.__init__(Sprite)
    if size:
        Sprite.image = pygame.Surface(size)
    if color:
        Sprite.image.fill(color)
    if pic_path:
        Sprite.image = pygame.image.load(pic_path)
    Sprite.image.convert()
    Sprite.rect = Sprite.image.get_rect()
    Sprite.rect.topleft = ini_pos
    

class Ball(pygame.sprite.Sprite):  #球體角色
 
    def __init__(self, sp, srx, sry, radium, color):
        """
        sp: 球速度
        srx, sry: 球圓心位置
        """
        ini_sprite(self, (srx-radium,sry-radium), color=WHITE, size=(radium*2, radium*2))
        pygame.draw.circle(self.image, color, (radium,radium), radium, 0)
        self.speed = sp #球移動速度
        self.direction = random.randint(40,70)  #移動角度
 
    def update(self):  #球體移動
        radian = math.radians(self.direction)  #角度轉為弳度
        dx = self.speed * math.cos(radian)  #球水平運動速度
        dy = -self.speed * math.sin(radian)  #球垂直運動速度
        self.rect.topleft = (self.rect.x + dx, self.rect.y + dy)
        if(self.rect.left <= 0 or self.rect.right >= screen.get_width()-10):  #到達左右邊界
            self.bouncelr()
        elif(self.rect.top <= 10):  #到達上邊界
            self.rect.top = 10
            self.bounceup()
        return self.rect.bottom >= screen.get_height()-10 #到達下邊界出界

    def bounceup(self):  #上邊界反彈
        self.direction = 360 - self.direction

    def bouncelr(self):  #左右邊界反彈
        self.direction = (180 - self.direction) % 360
            
class Brick(pygame.sprite.Sprite):  #磚塊角色
    def __init__(self, color, x, y):
        ini_sprite(self, (x,y), color=color, size=(38,13))

class Pad(pygame.sprite.Sprite):  #滑板角色
    def __init__(self):
        ini_sprite(self, (screen.get_width(), screen.get_height()), color=(169,80,27), size=(200,20))
        self.rect.x -= self.rect.width
        self.rect.y -= self.rect.height+20
 
    def update(self):  #滑板位置隨滑鼠移動
        pos = pygame.mouse.get_pos()  #取得滑鼠坐標
        self.rect.x = min(pos[0], screen.get_width() - self.rect.width)  #滑鼠x坐標，但不要移出右邊界

def gameover(msg):  #結束程式
    global running
    show_mes(msg,(screen.get_width()/2-100,screen.get_height()/2-20),32, PURPLE)    
    pygame.display.update()  #更新畫面
    time.sleep(3)  #暫停3秒
    running = False  #結束程式
    
def show_mes(msg, pos, font_size, font_color, font_type='sung'):
    """
    在指定位置顯示msg
    msg(str): 欲顯示的訊息
    pos(tuple): 位置
    font_size(int): 字體大小
    font_color(tuple of RGB):
    font_type(字型): 目前支援kai(楷體)，sung(宋體)
    """
    font = pygame.font.Font(f"{font_type}.ttf", font_size)  #下方訊息字體
    msg = font.render(msg, True, font_color)
    screen.blit(msg, pos)  #繪製訊息

pygame.init()
score = 0  #得分
soundhit = pygame.mixer.Sound("media\\hit.wav")  #接到磚塊音效
soundpad = pygame.mixer.Sound("media\\pad.wav")  #接到滑板音效
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("打磚塊遊戲")
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255,255,255))
allsprite = pygame.sprite.Group()  #建立全部角色群組
bricks = pygame.sprite.Group()  #建立磚塊角色群組
ball = Ball(10, 300, 350, 10, (255,0,0))  #建立紅色球物件
allsprite.add(ball)  #加入全部角色群組
pad = Pad()  #建立滑板球物件
allsprite.add(pad)  #加入全部角色群組
for row in range(4):
    for column in range(15):
        color_dict = {0:GREEN, 1:GREEN, 2: BLUE, 3:BLUE}
        brick = Brick(color_dict[row], column * 40 + 1, row * 15 + 1)
        bricks.add(brick)  #加入磚塊角色群組
        allsprite.add(brick)  #加入全部角色群組

# 遊戲主要無窮迴圈     
clock = pygame.time.Clock() #重要，計時物件
running = True
GAME_STATE = 'INITIAL'
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    if GAME_STATE=='INITIAL':
        show_mes("按滑鼠左鍵開始遊戲！", (screen.get_width()/2-60,screen.get_height()-20), 20, PURPLE)
        buttons = pygame.mouse.get_pressed()  #檢查滑鼠按鈕
        if buttons[0]:  #按滑鼠左鍵後球可移動
            GAME_STATE='PLAY'
            
    if GAME_STATE=='PLAY':  #遊戲進行中
        screen.blit(background, (0,0))  #清除繪圖視窗
        fail = ball.update()  #移動球體
        if fail:  #球出界
            gameover("失敗，再接再勵！")
        pad.update()  #更新滑板位置
        hitbrick = pygame.sprite.spritecollide(ball, bricks, True)  #檢查球和磚塊碰撞
        if len(hitbrick) > 0:  #球和磚塊發生碰撞
            score += len(hitbrick)  #計算分數
            soundhit.play()  #球撞磚塊聲
            ball.rect.y += 20  #球向下移
            ball.bounceup()  #球反彈
            if len(bricks) == 0:  #所有磚塊消失
                gameover("恭喜，挑戰成功！")
        hitpad = pygame.sprite.collide_rect(ball, pad)  #檢查球和滑板碰撞
        if hitpad:  #球和滑板發生碰撞
            soundpad.play()  #球撞滑板聲
            ball.bounceup()  #球反彈
        allsprite.draw(screen)  #繪製所有角色
        show_mes(f"得分：{score}", (screen.get_width()/2-60,screen.get_height()-20), 20, PURPLE)
    pygame.display.update()

pygame.quit()