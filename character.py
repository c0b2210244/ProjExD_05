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

    def calc_mv(self, key_lst: list[bool], bg: pg.sprite.Sprite):
        """
        押下キーに応じてキャラクターの移動量を返す関数
        引数１ key_lst：押下キーの真理値リスト
        """
        mv = 0
        # 左シフトを押すと加速
        if key_lst[pg.K_LSHIFT]:
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

    def update(self, num: int, screen: pg.Surface):
        """
        障害物に当たった時に画像を切り替える
        引数１ num：画像の番号
        引数２ screen：画面Surface
        """
        self.image = pg.transform.flip(pg.transform.rotozoom(pg.image.load(f"images/character{num}.png"), 0, 0.5), True, False)
        screen.blit(self.image, self.rect)

 