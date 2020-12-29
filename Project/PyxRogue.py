import pyxel
import mng_class as mngcls
import player_class

#----------------------------------------------------------
#Func:Call By Update() when GameState == STAT_GAMEPLAY
#----------------------------------------------------------
def _Update_GamePlay(self):
    
    KEY_SENCE = 10

    #なくても良いかも
    if self.player.get_moving_state(): return
    
    if pyxel.btnp(pyxel.KEY_LEFT, KEY_SENCE, KEY_SENCE):
        self.player.move(mngcls.DIR_L)
    elif pyxel.btnp(pyxel.KEY_RIGHT, KEY_SENCE, KEY_SENCE):
        self.player.move(mngcls.DIR_R)  
    elif pyxel.btnp(pyxel.KEY_UP, KEY_SENCE, KEY_SENCE):
        self.player.move(mngcls.DIR_U)
    elif pyxel.btnp(pyxel.KEY_DOWN, KEY_SENCE, KEY_SENCE):
        self.player.move(mngcls.DIR_D)
    else:
        pass

#----------------------------------------------------------
#Func:Call By Draw() when GameState == self.cmn.STAT_TITLE
#----------------------------------------------------------
def _Draw_GamePlay(self):
    pyxel.cls(0)

    #マップ表示
    pyxel.bltm(mngcls.TILEMAP_0, 0, 0, 0, 0, mngcls.TILEMAP_WIDTH, mngcls.TILEMAP_HEIGHT, mngcls.TRANS_COL)

    #プレイヤー描画
    self.player.draw()

#----------------------------------------------------------
#Class Main roop PxyRogue
#----------------------------------------------------------
class PyxRogue:
    def __init__(self):
        # 初期化

        #共通管理クラス
        #self.cmn = cls_common.Common()
                
        pyxel.init(mngcls.PYX_WIDTH, mngcls.PYX_HEIGHT, caption="PyxRogue", fps = mngcls.PYX_FPS)
        pyxel.load("./assets/pyxrogue.pyxres")

        self.GameState = mngcls.STAT_GAMEPLAY

        self.player = player_class.Player(3, 6, mngcls.DIR_R)
       
        # 実行
        pyxel.run(self.update, self.draw)

    def update(self):

        self.player.vsync_inc() #プレイヤークラスのvsyncを更新

        # 更新
        if self.GameState == mngcls.STAT_TITLE:
            pass
            #_Update_Title(self)
        elif self.GameState == mngcls.STAT_GAMEPLAY:
            _Update_GamePlay(self)
        elif self.GameState == mngcls.STAT_GAMEOVER:
            pass

    def draw(self):

        # 更新
        if self.GameState == mngcls.STAT_TITLE:
            #_Draw_Start(self)
            pass
        elif self.GameState == mngcls.STAT_GAMEPLAY:
            _Draw_GamePlay(self)
        elif self.GameState == mngcls.STAT_GAMEOVER:
            pass

PyxRogue()
