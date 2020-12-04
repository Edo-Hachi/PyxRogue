import pyxel

class PyxRogue:
    def __init__(self):
        # 初期化
        pyxel.init(128, 128, fps = 60)
        self.x = 0

        # 実行
        pyxel.run(self.update, self.draw)

    def update(self):
        # 更新
        self.x = (self.x + 1) % pyxel.width


    def draw(self):
        # 描画
        # 画面を消去
        pyxel.cls(2)
        # 矩形を描画
        pyxel.rect(self.x, 0, self.x + 7, 7, 9)
    

PyxRogue()
