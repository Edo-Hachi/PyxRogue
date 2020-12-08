import pyxel

# ====================================================================
# 定数
# ====================================================================

# pyxel画面サイズ、FPS
PYX_WIDTH = 256
PYX_HEIGHT = 256
PYX_FPS = 60

# タイルマップ
TILEMAP_WIDTH = 64
TILEMAP_HEIGHT = 64
TILEMAP_0 = 0   # 迷路描画用


# タイルマップ種別
TILE_NONE = 0
TILE_WALL0 = 1
TILE_WALL1 = 2
TILE_STONE = 5
TILE_DOOR = 6
TILE_UPSTR = 7
TILE_DNSTR = 8

TILE_SIZE = 8


#スプライト情報
TRANS_COL = 15  # スプライト透過色番号
SPR_WIDTH = 8
SPR_HEIGHT = 8
SPR_IMGBNK = 0


#ゲームステート
STAT_TITLE = 0
STAT_GAMEPLAY = 1
STAT_GAMEOVER = 2


#プレイヤー情報
DIR_U = 0 # プレイヤーの向き
DIR_L = 1
DIR_D = 2
DIR_R = 3

#            UP        LEFT    DOWN   RIGHT
DIRECTION = [[0, -1], [-1,0], [0, 1], [1, 0]]

