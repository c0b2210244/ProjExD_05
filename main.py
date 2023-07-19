import sys
import random
import pygame as pg
import random
import time
import math

import character as ch
from background import background
from Gakutyou import Gakutyou # 学長クラスのインポート

WITDH = 1600
HEIGHT = 900
STAGE_WIDTH = 10000  # ステージの横幅
TREE_BOTTOM = 100
WALL_NUM = 15  # 木の数
screen = None

class Wall(pg.sprite.Sprite):
    """
    遮蔽物(以下、木)の描画、判定処理
    """
    def __init__(self, screen: pg.Surface):
        """
        遮蔽物(木)を描画
        引数: screen: 画面Surface
        """
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load("images/tree.png"), 0, 0.5)  # 木の画像を読み込む
        screen.blit(self.image, [WITDH, HEIGHT - 350])  # 木を表示
        self.rect = self.image.get_rect()  # 木のrectを作成
        self.rect.bottom = HEIGHT - TREE_BOTTOM + 53  # 木のY座標を固定
        self.rect.centerx = random.randint(500, STAGE_WIDTH)  # 木のX座標を決定。500～ステージのサイズの間にランダムで生成
    
    def update(self, key_lst: list[bool], screen: pg.Surface, mv):
        """
        ユーザの操作に応じで木の描画位置を変更
        引数1 key_lst: 押下キーの真理値リスト
        引数2 screen: 画面Surface
        """
        self.speedx = 0  # もし、キーボードを押していなければ移動しない
        if key_lst[pg.K_LEFT]:  # もし、左矢印を押していたら...
            self.speedx = 10  # 右に20動く
        if key_lst[pg.K_RIGHT]:  # もし、右矢印を押していたら...
            self.speedx = 10 * (-1)  # 左に20動く

        self.rect.centerx += mv  # 木の位置を更新
        screen.blit(self.image, self.rect)  # 更新後の木を描画



class Start_menu:
    """
    スタート画面を表示させるクラス
    """
    def __init__(self):
        """
        フォント、メニュータイトルの表示
        """
        self.font = pg.font.Font("fonts/onryou.TTF", 100)
        self.menu_title = self.font.render("学長が転んだ", True, (255, 255, 255))
        
    def button(self, screen: pg.Surface, num:int):
        """
        どのボタンを選択しようとしているのかを表示する
        引数1 screen 画面の表示
        引数2 num どのボタンが選択中か
        """
        if num == 0:
            self.start_button = self.font.render("スタート", True, (255, 0, 0))
            self.hoge_button = self.font.render("ヤメル",True, (255, 255, 255))
            screen.fill((0, 0, 0))
            screen.blit(self.menu_title, (WITDH/2 - self.menu_title.get_width()/2, HEIGHT/2 - self.menu_title.get_height()))
            screen.blit(self.start_button, (WITDH/3 - self.start_button.get_width()/2, HEIGHT/2 + self.start_button.get_height()))
            screen.blit(self.hoge_button, (WITDH/2 + self.hoge_button.get_width()/2, HEIGHT/2 + self.start_button.get_height()))
        
        if num == 1:
            self.start_button = self.font.render("スタート", True, (255, 255, 255))
            self.hoge_button = self.font.render("ヤメル",True, (255, 0, 0))
            screen.fill((0, 0, 0))
            screen.blit(self.menu_title, (WITDH/2 - self.menu_title.get_width()/2, HEIGHT/2 - self.menu_title.get_height()))
            screen.blit(self.start_button, (WITDH/3 - self.start_button.get_width()/2, HEIGHT/2 + self.start_button.get_height()))
            screen.blit(self.hoge_button, (WITDH/2 + self.hoge_button.get_width()/2, HEIGHT/2 + self.start_button.get_height()))


class Enemy(pg.sprite.Sprite):
    """
    道中の障害物(おさかなさん)に関するクラス
    """

    def __init__(self):
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load("images/ojama.png"), 0, 0.3)   # 障害物の画像読み込み
        self.rect = self.image.get_rect()
        self.rect.center = WITDH + 100, HEIGHT / 4
        self.vy = +40
        self.ay = +1.0
        self.vx = -8
        self.timer = 0

    def update(self, mv_value, timeDeray):
        """
        お魚が地面ではねるところ
        地面の座標(マージ前は750と仮定)に到達するまで等加速し、地面で速度を反転
        引数screen：画面Surface
        """
        # if self.rect.centery >= 750:
        #     self.vy = -40 * timeDeray
        # self.vy += self.ay * timeDeray
        self.timer += self.vx * timeDeray
        self.rect.centerx += self.vx * timeDeray + mv_value
        self.rect.centery = -abs(math.sin(self.timer / 200 * (timeDeray*2))) * 700 + 800
        if self.rect.right <= 0:
            self.kill() #画面外に出たら自身をkill
        
def displayInit():
    global screen
    pg.display.set_caption("学長が転んだ")
    screen = pg.display.set_mode((WITDH, HEIGHT))

def main():
    global screen, recentTime
    # ここからメニュー画面
    start_menu = Start_menu()
    game_state = "menu_start"
    start_menu.button(screen, 0)
    while game_state != "runnnig":
        pg.display.update()
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if (event.type == pg.KEYDOWN and event.key == pg.K_RIGHT):#右キーを押下で設定画面に移れる状態にする
                start_menu.button(screen, 1)
                game_state = "menu_end"
            if(event.type == pg.KEYDOWN and event.key == pg.K_LEFT):#左キーを押下でゲーム画面に移れる状態にする
                start_menu.button(screen, 0)
                game_state = "menu_start"
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and game_state == "menu_start":
                game_state = "runnnig"
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and game_state == "menu_end":    
                return "end"
        
    # ここからゲームスタート
    bg_image = pg.transform.rotozoom(pg.image.load("images/sky_img.png"), 0, 1.0)

    gakutyou = Gakutyou((1000, 200), 1) # 学長インスタンスを作成
    character = ch.Character([200, 720])
    bg = background()
    emys = pg.sprite.Group()
    trees = pg.sprite.Group() # 木のグループ

    tmr = 0
    clock = pg.time.Clock()
    clock.get_time()
    for i in range(WALL_NUM):  # WALL_NUMの分だけ繰り返す
        trees.add(Wall(screen))  # 木の情報を追加

    while True:
        if len(emys) == 0:
            emys.add(Enemy())
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return "end"
            
        timeDeray = max(clock.tick(50), 100) / 100
        mv = character.calc_mv(key_lst, bg) * timeDeray
        bg.update(-mv)
        screen.blit(bg.image,bg.rect)

        gakutyou.update() # 学長インスタンスの更新
        if gakutyou.get_isReady(): # 学長の攻撃中
            shadeSurface = pg.Surface((WITDH, HEIGHT))
            shadeSurface.fill((0, 0, 0))
            shadeSurface.set_alpha(100)
            screen.blit(shadeSurface, (0, 0))
            # 隠れられているか判定
            if len(pg.sprite.spritecollide(character, trees, False)) == 0:
                game_state = "game_over"
        screen.blit(gakutyou.image, gakutyou.rect) # 学長インスタンスを描画
        trees.update(key_lst, screen, mv)  # 木の位置を更新する
        key_lst = pg.key.get_pressed()


        # クリア
        if bg.rect.x <= -6800:
            character.update(3, screen)            
            pg.display.update()
            time.sleep(2)
            return "clear"

        screen.blit(character.image, character.rect) # キャラクター描画
        # キャラクターと障害物の衝突判定
        if len(pg.sprite.spritecollide(character, emys, True)) != 0:
            game_state = "game_over"
        else:
            character.update(1, screen)
        
        if len(emys) != 0:
            emys.update(mv, timeDeray)
            emys.draw(screen)

        # ゲームオーバー判定
        if game_state == "game_over":
            fonto = pg.font.Font("fonts/onryou.TTF", 200)
            txt = fonto.render("退学", True, (255, 0, 0))
            txt_rect = txt.get_rect()
            txt_rect.center = (WITDH / 2, HEIGHT / 2)
            screen.blit(txt, txt_rect)
            character.update(2, screen)
            pg.display.update()
            time.sleep(2)
            return "damage"
        
        pg.display.update()
        tmr += 1
        

if __name__ == "__main__":
    pg.init()
    displayInit()
    status = "first"
    while status != "end":
        status = main()
    pg.quit()
    sys.exit()
