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
STAGE_WIDTH = 7000  # ステージの横幅
TREE_BOTTOM = 47
WALL_NUM = 10  # 木の数
screen: pg.Surface = None

class Wall(pg.sprite.Sprite):
    """
    遮蔽物(以下、木)の描画、判定処理
    """
    def __init__(self, screen: pg.Surface, number):
        """
        遮蔽物(木)を描画
        引数: screen: 画面Surface
        """
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load("images/tree.png"), 0, 0.5)  # 木の画像を読み込む
        self.rect = self.image.get_rect()  # 木のrectを作成
        self.rect.bottom = HEIGHT - TREE_BOTTOM  # 木のY座標を固定
        treeExistWidth = STAGE_WIDTH // WALL_NUM
        self.rect.centerx = random.randint(treeExistWidth * number, treeExistWidth * (number + 2)) # 木のX座標を決定。一定間隔の間にランダムで生成
    
    def update(self, screen: pg.Surface, mv):
        """
        ユーザの操作に応じで木の描画位置を変更
        引数1 key_lst: 押下キーの真理値リスト
        引数2 screen: 画面Surface
        """
        # 旧版
        # self.speedx = 0  # もし、キーボードを押していなければ移動しない
        # if key_lst[pg.K_LEFT]:  # もし、左矢印を押していたら...
        #     self.speedx = 10  # 右に20動く
        # if key_lst[pg.K_RIGHT]:  # もし、右矢印を押していたら...
        #     self.speedx = 10 * (-1)  # 左に20動く

        self.rect.centerx += mv  # 木の位置を更新




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
        creditsFont = pg.font.Font("fonts/POP.ttf", 20)
        self.menu_credit = creditsFont.render("効果音：OtoLogic - https://otologic.jp/", False, (255, 255, 255))
        
    def button(self, screen: pg.Surface, num:int):
        """
        どのボタンを選択しようとしているのかを表示する
        引数1 screen 画面の表示
        引数2 num どのボタンが選択中か
        """
        if num == 0:
            self.left_button = self.font.render("スタート", True, (255, 0, 0))
            self.right_button = self.font.render("ヤメル",True, (255, 255, 255))
        elif num == 1:
            self.left_button = self.font.render("スタート", True, (255, 255, 255))
            self.right_button = self.font.render("ヤメル",True, (255, 0, 0))
        elif num == 2:
            self.left_button = self.font.render("ふつう", True, (255, 0, 0))
            self.right_button = self.font.render("むずかしい",True, (255, 255, 255))
        elif num == 3:
            self.left_button = self.font.render("ふつう", True, (255, 255, 255))
            self.right_button = self.font.render("むずかしい",True, (255, 0, 0))
        
        screen.fill((0, 0, 0))
        screen.blit(self.menu_title, (WITDH/2 - self.menu_title.get_width()/2, HEIGHT/2 - self.menu_title.get_height()))
        screen.blit(self.menu_credit, (WITDH - self.menu_credit.get_width() - 30, HEIGHT - self.menu_credit.get_height()))
        screen.blit(self.left_button, (WITDH/3 - self.left_button.get_width()/2, HEIGHT/2 + self.left_button.get_height()))
        screen.blit(self.right_button, (WITDH/3 * 2 - self.right_button.get_width()/2, HEIGHT/2 + self.right_button.get_height()))


class Enemy(pg.sprite.Sprite):
    """
    道中の障害物(おさかなさん等)に関するクラス
    """

    def __init__(self, hardMode: bool, bg: pg.sprite.Sprite):
        super().__init__()
        pict= pg.image.load(random.choice(("images/ojama.png",) + ("images/frogFSM.png",) * (hardMode * (bg.rect.left < -3000)))) # 敵キャラの抽選
        self.image = pg.transform.rotozoom(pict, 0, 80000 / (pict.get_width() * pict.get_height()))   # 障害物の画像読み込み
        self.rect = self.image.get_rect()
        self.rect.center = WITDH + 100, HEIGHT / 4
        self.vy = +40
        self.ay = +1.0
        self.vx = -4 + hardMode * -8
        self.radian = 0
        self.randomJump = random.randint(100, 200)

    def update(self, mv_value):
        """
        お魚が地面ではねるところ
        引数screen：画面Surface
        """
        self.radian += self.vx * self.randomJump / 100
        self.rect.centerx += self.vx + mv_value
        self.rect.bottom = -abs(math.sin(self.radian / self.randomJump)) * (870 - self.image.get_height()) + 870
        
        
def displayInit():
    global screen
    pg.display.set_caption("学長が転んだ")
    screen = pg.display.set_mode((WITDH, HEIGHT))

def main():
    global screen
    # ここからメニュー画面
    start_menu = Start_menu()
    game_state = "menu_start"
    start_menu.button(screen, 0)
    while game_state != "choiceDifficulty":
        pg.display.update()
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if (event.type == pg.KEYDOWN and event.key == pg.K_RIGHT):#右キーを押下で設定画面に移れる状態にする
                start_menu.button(screen, 1)
                game_state = "menu_end"
            if(event.type == pg.KEYDOWN and event.key == pg.K_LEFT):#左キーを押下でゲーム画面に移れる状態にする
                start_menu.button(screen, 0)
                game_state = "menu_start"
            if event.type == pg.KEYDOWN and event.key in (pg.K_SPACE, pg.K_ESCAPE, pg.K_DOWN) and game_state == "menu_start":
                game_state = "choiceDifficulty"
            if event.type == pg.KEYDOWN and event.key in (pg.K_SPACE, pg.K_ESCAPE, pg.K_DOWN) and game_state == "menu_end":    
                return "end"
    # 難易度選択
    isHardmode = False
    game_state = "menu_normal"
    start_menu.button(screen, 2)
    while game_state != "running":
        pg.display.update()
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:#右キーを押下でふつう画面に移れる状態にする
                start_menu.button(screen, 3)
                game_state = "menu_hard"
            if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:#左キーを押下でむずかしい画面に移れる状態にする
                start_menu.button(screen, 2)
                game_state = "menu_normal"
            if event.type == pg.KEYDOWN and event.key in (pg.K_SPACE, pg.K_ESCAPE, pg.K_DOWN) and game_state == "menu_normal":
                game_state = "running"
                isHardmode = False
            if event.type == pg.KEYDOWN and event.key in (pg.K_SPACE, pg.K_ESCAPE, pg.K_DOWN) and game_state == "menu_hard":    
                game_state = "running"
                isHardmode = True
        
    # ここからゲームスタート
    gakutyou = Gakutyou((1000, 200), 1, isHardmode) # 学長インスタンスを作成
    character = ch.Character([200, 704])
    bg = background()
    emy: Enemy = None
    trees = pg.sprite.Group() # 木のグループ

    tmr = 0
    clock = pg.time.Clock()
    clock.get_time()
    for i in range(WALL_NUM):  # WALL_NUMの分だけ繰り返す
        trees.add(Wall(screen, i))  # 木の情報を追加

    while True:
        if emy is None:
            emy = Enemy(isHardmode, bg)
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return "end"
        mv = character.calc_mv(key_lst, bg, isHardmode)
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
        trees.update(screen, mv)  # 木の位置を更新する
        trees.draw(screen)

        # クリア
        if bg.rect.x <= -6800:
            character.update(3, screen, isHardmode)   
            screen.blit(character.image, character.rect) # キャラクター描画        
            pg.display.update()
            time.sleep(2)
            return "clear"

        
        # キャラクターと障害物の衝突判定
        if math.sqrt((character.rect.centerx - emy.rect.centerx)**2
                     + (character.rect.centery - emy.rect.bottom)**2) <= 170 \
                     and (character.rect.centerx - emy.rect.centerx) < 100: # 当たり判定の調節
            game_state = "game_over"
        
        if emy is not None:
            emy.update(mv)
            screen.blit(emy.image, emy.rect)
            if emy.rect.right <= 0:
                emy = None #画面外に出たら自身をkill

        # ゲームオーバー判定
        if game_state == "game_over":
            fonto = pg.font.Font("fonts/onryou.TTF", 200)
            txt = fonto.render("退学", True, (255, 0, 0))
            txt_rect = txt.get_rect()
            txt_rect.center = (WITDH / 2, HEIGHT / 2)
            screen.blit(txt, txt_rect)
            character.update(2, screen, isHardmode)
            screen.blit(character.image, character.rect)
            pg.display.update()
            time.sleep(2)
            return "damage"
        screen.blit(character.image, character.rect) # キャラクター描画
        clock.tick(50)
        pg.display.update()
        tmr += 1
        

if __name__ == "__main__":
    pg.init()
    displayInit()
    status = "first"
    while status != "end":
        status = main()
        if status != "clear":
            pg.mixer.music.stop()
    pg.quit()
    sys.exit()
