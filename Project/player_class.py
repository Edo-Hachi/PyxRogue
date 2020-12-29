import pyxel
import mng_class as mngcls


SPR_U = [[0,0], [8, 0]]
SPR_L = [[16,0], [24, 0]]
SPR_D = [[32,0], [40, 0]]
SPR_R = [[48,0], [56, 0]]

SPR_ING = [[64,0], [72, 0], [80, 0]]    #インジケーター（青、黄、赤）

class Player:
    def __init__(self, x, y, dir):
        self.p_x = x    #プレイヤーのタイル系座標
        self.p_y = y
        self.p_dir = dir        #移動方向
        self.p_moving = False    #移動中
        self.p_KnockBk = False  #障害物に当たった時のノックバックアニメの実行フラグ

        self.p_slide_cnt = 0    #移動が発生した場合のスライド量カウンタ
        self.p_slide_x = self.p_x * mngcls.SPR_WIDTH   #スライドアニメの実座標
        self.p_slide_y = self.p_y * mngcls.SPR_HEIGHT
        self.p_ofs_x = 0    #スライド方向
        self.p_ofs_y = 0

        self.vsync = 0  #vsync

    # vsync 親のupdateで呼ばれてます
    def vsync_inc(self):
        self.vsync += 1
        if 60 <= self.vsync:
            self.vsync = 0

    
    #キャラクタを指定方向に移動
    def move(self, dir):
        #進行方向チェック
        dir_x = mngcls.DIRECTION[dir][0]    #Xの移動予定方向
        dir_y = mngcls.DIRECTION[dir][1]    #yの移動予定方向
        self.p_dir = dir

        #イメージマップの進行方向のオブジェクトチェック
        dir_tile = pyxel.tilemap(mngcls.TILEMAP_0).get(self.p_x + dir_x, self.p_y + dir_y)

        print("DIR=" + str(dir) + ":tile=" + str(dir_tile))
        
        #self.p_x += dir_x
        #self.p_y += dir_y

        #now_tile = pyxel.tilemap(mngcls.TILEMAP_0).get(self.p_x, self.p_y)
        #print("NOW=" + str(dir_x) + ":" + str(dir_y) + ":tile=" + str(now_tile))

        if dir_tile == mngcls.TILE_NONE:    #空白なので移動OK

            self.p_slide_cnt = mngcls.TILE_SIZE
            self.p_slide_x = self.p_x * mngcls.SPR_WIDTH
            self.p_slide_y = self.p_y * mngcls.SPR_HEIGHT
            self.p_ofs_x = dir_x
            self.p_ofs_y = dir_y

            self.p_x += dir_x
            self.p_y += dir_y
            self.p_moving = True

        #elif dir_tile == mngcls.TILE_WALL0 or dir_tile == mngcls.TILE_WALL1:
        else:
            print(" なにかに当たった！")
            self.p_slide_cnt = mngcls.TILE_SIZE / 4
            self.p_slide_x = self.p_x * mngcls.SPR_WIDTH
            self.p_slide_y = self.p_y * mngcls.SPR_HEIGHT
            self.p_ofs_x = dir_x
            self.p_ofs_y = dir_y

            # 音ならしてみる
            pyxel.play(0, 0)

            self.p_moving = False
            self.p_KnockBk = True
        #else:
        #    pass
    
    # スプライトの描画周りをここにまとめる予定
    def draw_spr(self, x, y, dir):
        
        cid = 0
        if 30 < self.vsync : cid = 1

        if self.p_dir == mngcls.DIR_U:
            spr_x = SPR_U[cid][0]
            spr_y = SPR_U[cid][1]
        elif self.p_dir == mngcls.DIR_L:
            spr_x = SPR_L[cid][0]
            spr_y = SPR_L[cid][1]
        elif self.p_dir == mngcls.DIR_D:
            spr_x = SPR_D[cid][0]
            spr_y = SPR_D[cid][1]

        elif self.p_dir == mngcls.DIR_R:
            spr_x = SPR_R[cid][0]
            spr_y = SPR_R[cid][1]

        #HPインジケーターのスプライト
        #ing_cr = 0 #青
        #ing_cr = 1 #黄
        ing_cr = 2 #赤

        spr_ing_x = SPR_ING[ing_cr][0]
        spr_ing_y = SPR_ING[ing_cr][1]

        # プレイヤーのボディ
        pyxel.blt(x, y, mngcls.SPR_IMGBNK, spr_x, spr_y, mngcls.SPR_WIDTH, mngcls.SPR_HEIGHT, mngcls.TRANS_COL)
        # HPインジケーター
        pyxel.blt(x, y, mngcls.SPR_IMGBNK, spr_ing_x, spr_ing_y, mngcls.SPR_WIDTH, mngcls.SPR_HEIGHT, mngcls.TRANS_COL)

    # 描画処理
    def draw(self):
        if self.p_moving == True:   #移動モーション中
            if 0 <= self.p_slide_cnt:   # 移動スライド処理実行
                self.draw_spr(self.p_slide_x, self.p_slide_y, self.p_dir)
                                
                self.p_slide_x += self.p_ofs_x
                self.p_slide_y += self.p_ofs_y
                self.p_slide_cnt -= 1
            else:
                self.p_moving = False #移動スライドアニメーション完了
                self.draw_spr(self.p_x * mngcls.SPR_WIDTH, self.p_y * mngcls.SPR_HEIGHT, self.p_dir)

        elif self.p_moving == False:    #移動中モーション中ではない

            if self.p_KnockBk == True:  #壁などに当たってノックバック発生
                if 0 <= self.p_slide_cnt:
                    print("ノックバック2")

                    self.draw_spr(self.p_slide_x, self.p_slide_y, self.p_dir)
                    
                    self.p_slide_x += self.p_ofs_x
                    self.p_slide_y += self.p_ofs_y
                    self.p_slide_cnt -= 1
                else: #ノックバック処理終了
                    self.draw_spr(self.p_slide_x, self.p_slide_y, self.p_dir)
                    self.p_KnockBk = False
                    self.p_moving = False

                    # __debug__ 壁以外の場合はアイテム、ドアなどを消す処理

            else:   #移動が発生してない 停止中アニメ
                self.draw_spr(self.p_x * mngcls.SPR_WIDTH, self.p_y * mngcls.SPR_HEIGHT, self.p_dir)

    #移動処理(スライド)中かどうかを返す
    def get_moving_state(self):
        return self.p_moving
