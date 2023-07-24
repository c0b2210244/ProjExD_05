import pygame as pg
import main




class Character(pg.sprite.Sprite):
    """
    操作キャラクターに関するクラス
    """
    def __init__(self, xy: tuple[int, int]):
        """
        操作キャラクターSurfaceを描画する
        引数 xy：キャラクターの初期位置
        """
        super().__init__()
        self.image = pg.transform.flip(pg.transform.rotozoom(pg.image.load("images/character1.png"), 0, 0.5), True, False)
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.dx = 10
        self.images: list[pg.Surface] = []
        for i in range(1, 4):
            self.images.append(pg.transform.flip(pg.transform.rotozoom(pg.image.load(f"images/character{i}.png"), 0, 0.5), True, False))
        self.channel = pg.mixer.Channel(3)

    def calc_mv(self, key_lst: list[bool], bg: pg.sprite.Sprite, hardMode):
        """
        押下キーに応じてキャラクターの移動量を返す関数
        引数１ key_lst：押下キーの真理値リスト
        """
        mv = 0
        # 左シフトを押すと加速
        if key_lst[pg.K_LSHIFT] and not hardMode:
            self.dx = 30
        else:
            self.dx = 15
        if key_lst[pg.K_LEFT]:
            mv = self.dx
        elif key_lst[pg.K_RIGHT]:
            mv = -self.dx
        if bg.rect.x >= 0 and mv > 0:
            mv = 0
        return mv

    def update(self, num: int, screen: pg.Surface, isHardmode: bool):
        """
        障害物に当たった時に画像を切り替える
        引数１ num：画像の番号
        引数２ screen：画面Surface
        """
        self.image = self.images[num-1]
        if num in (2, 3):
            # キャラクターの状態が2か3なら効果音を再生
            pg.mixer.Channel(2).stop()
            seName = "sounds/"
            if num == 2:
                seName += "damage.mp3"
                self.rect.move_ip((self.images[0].get_width() - self.images[1].get_width()), 0)
                self.channel.play(pg.mixer.Sound(seName), maxtime=1000)
                return
            elif num == 3 and not isHardmode:
                seName += "normalClear.mp3"
            elif num == 3 and isHardmode:
                seName += "hardClear.mp3"
            self.channel.play(pg.mixer.Sound(seName))
            

 