import pyxel
import mngcls


SPR_P = [[0,0], [8, 0]]

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

    # vsync 親のupdateで叩かれれます
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

        #print("DIR=" + str(dir) + ":tile=" + str(dir_tile))
        
        #self.p_x += dir_x
        #self.p_y += dir_y

        #now_tile = pyxel.tilemap(mngcls.TILEMAP_0).get(self.p_x, self.p_y)
        #print("NOW=" + str(dir_x) + ":" + str(dir_y) + ":tile=" + str(now_tile))

        if dir_tile == mngcls.TILE_NONE:    #移動OK

            self.p_slide_cnt = mngcls.TILE_SIZE
            self.p_slide_x = self.p_x * mngcls.SPR_WIDTH
            self.p_slide_y = self.p_y * mngcls.SPR_HEIGHT
            self.p_ofs_x = dir_x
            self.p_ofs_y = dir_y

            self.p_x += dir_x
            self.p_y += dir_y
            self.p_moving = True
            
            #self.p_KnockBk == False

            

            #self.ofs_x = dir_x * mngcls.TILE_SIZE
            #self.ofs_y = dir_y * mngcls.TILE_SIZE

        elif dir_tile == mngcls.TILE_WALL0 or dir_tile == mngcls.TILE_WALL1:
            print(" 壁に当たった！")
            self.p_slide_cnt = mngcls.TILE_SIZE / 4
            self.p_slide_x = self.p_x * mngcls.SPR_WIDTH
            self.p_slide_y = self.p_y * mngcls.SPR_HEIGHT
            self.p_ofs_x = dir_x
            self.p_ofs_y = dir_y

            #self.p_x += dir_x
            #self.p_y += dir_y
            
            self.p_moving = False
            self.p_KnockBk = True
        else:
            pass
    
    # スプライトの描画周りをここにまとめる予定
    def draw_spr(self, x, y, dir):
        
        cid = 0
        if 30 < self.vsync : cid = 1

        ox = SPR_P[cid][0]
        oy = SPR_P[cid][1]
        lr = 1

        if dir == mngcls.DIR_L:
            lr = -1
        elif dir == mngcls.DIR_R:
            lr = 1


        pyxel.blt(x, y, mngcls.SPR_IMGBNK, ox, oy, mngcls.SPR_WIDTH * lr, mngcls.SPR_HEIGHT, mngcls.TRANS_COL) 

    def draw(self):
        if self.p_moving == True:   #移動モーション中
            if 0 <= self.p_slide_cnt:
                #pyxel.blt(self.p_slide_x, self.p_slide_y, 0, 0, 0, 8, 8, 15)
                self.draw_spr(self.p_slide_x, self.p_slide_y, self.p_dir)
                                
                self.p_slide_x += self.p_ofs_x
                self.p_slide_y += self.p_ofs_y
                self.p_slide_cnt -= 1
            else:
                self.p_moving = False #移動スライド完了
                #self.draw_spr(self.p_x, self.p_y, self.p_dir)
                self.draw_spr(self.p_x * mngcls.SPR_WIDTH, self.p_y * mngcls.SPR_HEIGHT, self.p_dir)

        elif self.p_moving == False:    #移動中モーション中ではない

            if self.p_KnockBk == True:  #壁などに当たってノックバック発生
                if 0 <= self.p_slide_cnt:
                    print("ノックバック2")

                    #pyxel.blt(self.p_slide_x, self.p_slide_y, 0, 0, 0, 8,8, 15)
                    self.draw_spr(self.p_slide_x, self.p_slide_y, self.p_dir)
                    
                    self.p_slide_x += self.p_ofs_x
                    self.p_slide_y += self.p_ofs_y
                    self.p_slide_cnt -= 1
                else:
                    #pyxel.blt(self.p_slide_x, self.p_slide_y, 0, 0, 0, 8,8, 15)
                    self.draw_spr(self.p_slide_x, self.p_slide_y, self.p_dir)
                    #self.draw_spr(self.p_slide_x, self.p_slide_y, self.p_dir)
                    self.p_KnockBk = False
                    self.p_moving = False   
            else:   #移動が発生してない 
                self.draw_spr(self.p_x * mngcls.SPR_WIDTH, self.p_y * mngcls.SPR_HEIGHT, self.p_dir)

    #移動処理中かどうかを返す
    def get_moving_state(self):
        return self.p_moving
