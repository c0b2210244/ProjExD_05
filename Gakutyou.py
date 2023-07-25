import pygame as pg

class Gakutyou(pg.sprite.Sprite):
    """
    学長のクラス（スプライト継承済み）
    コンストラクタでは位置と大きさ（倍率）を指定して作成
    """

    BACK_COLOR = (120, 250, 120)
    COOL_TIME_BASE = 360

    def __init__(self, position: tuple[int, int], size: float, hardMode) -> None:
        super().__init__()
        gImg = pg.image.load("images/gakutyou.png") # 学長画像
        cImg = pg.image.load("images/g_cloud.png") # 学長が乗る雲画像
        self.image = pg.Surface((300, 340)) # 学長の画像を張り付ける用のSurface
        self.image.fill(Gakutyou.BACK_COLOR)
        self.image.blit(pg.transform.rotozoom(gImg, 0, 300 / gImg.get_width() * 1.9), (-210,-70))
        self.image.blit(pg.transform.rotozoom(cImg, 0, 340 / cImg.get_width() * 1.05), (-25,65))
        self.rect = self.image.get_rect()
        self.rect.center = position

        eyeLight = pg.image.load("images/eye_light.png") # 目の光をロード
        eyeLight = pg.transform.rotozoom(eyeLight, 0, 0.035) # サイズ調整
        self.images: list[pg.surface.Surface] = []
        # ここからフレームごとに切り替える学長画像のリストを作成
        for i in range(50): # 光の画像の立ち上がり
            currentImg = self.image.copy()
            currentSurf = pg.Surface((300, 100))
            currentSurf.blit(eyeLight, (117, 40))
            currentSurf.blit(eyeLight, (150, 40))
            currentSurf.set_colorkey((0, 0, 0))
            currentSurf.set_alpha(i * 5)
            currentImg.blit(currentSurf, (0, 0))
            self.images.append(currentImg)
        for i in range(20): # 点灯状態を20フレーム
            self.images.append(self.images[49].copy())
        for i in range(50)[::-1]: # 立ち下がり部分
            self.images.append(self.images[i].copy())
        self.images = [pg.transform.rotozoom(x, 0, size) for x in self.images]
        for i in self.images: # 一気に背景透過
            i.set_colorkey(Gakutyou.BACK_COLOR)
        self.image = self.images[0] # 最初の画像は0番目で固定
        self.timer = 0 # Updateごとに1増やすタイマーを設定
        self.attackTimer = -1 # 攻撃時間を設定（攻撃時以外は-1）
        self.isReady = False # 攻撃中かどうか
        self.coolTime = Gakutyou.COOL_TIME_BASE + hardMode * -120
        self.channel = pg.mixer.Channel(1)

    def update(self):
        """
        update関数のオーバーライド\n
        毎フレーム呼び出してください
        """
        if self.timer >= self.coolTime or self.isReady:
            # 学長の攻撃が始まる時間になったらタイマーをリセット
            self.timer = 0 
            self.isReady = True
            self.image = self.images[50]
        else:
            self.timer += 1
            self.image = self.images[int(self.timer * ((self.timer // 120 + 1) ** 2)) % 120] # タイマーに応じて画像を変更
            if int(self.timer * ((self.timer // 120 + 1) ** 2)) % 120 <= 10:
                self.channel.play(pg.mixer.Sound("sounds/pika.mp3"))
        
    def get_isReady(self):
        """
        クールタイムが終わったかをBool型で返す関数、Trueの時呼び出されると一定時間Trueを返し続ける\n
        引数：無し\n
        戻り値：True(攻撃できるとき) or False(攻撃できないとき)
        """
        if self.attackTimer < 0 and not self.isReady:
            return False
        if self.attackTimer >= 0:
            self.attackTimer -= 1 # attackTimerが設定されている間は1ずつ減算
            if self.attackTimer < 0:
                self.isReady = False # タイマーが0未満になったら攻撃を終了
            return True
        elif self.isReady:
            self.attackTimer = 100 # 攻撃の時間を100に設定
            return True
        
