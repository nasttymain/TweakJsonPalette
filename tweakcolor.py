import json
from sgpg import *
import time
import tkinter.colorchooser
import tkinter.filedialog
import tkinter.simpledialog
import sys
import os.path



sg = None
csel = [0, 0] # [縦、横]
colordata = {"color":[{"colors": [16711680]}]}
if len(sys.argv) >= 2:
    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1], mode="r") as f:
            colordata = json.loads(f.read())


def mbuttondown(mx: int, my: int):
    global colordata, sg, csel
    if 40 < mx < 260 and 40 < my < 320 and len(colordata["color"]) > (my - 40) // 20:
        #色列
        csel[0] = (my - 40) // 20
        if len(colordata["color"][csel[0]]["colors"]) <= csel[1]:
            # 列縮小による補正
            csel[1] = len(colordata["color"][csel[0]]["colors"]) - 1
        if 0 <= ((mx - 80) // 40) < len(colordata["color"][csel[0]]["colors"]):
            # 色が直接選択された
            csel[1] = (mx - 80) // 40
        elif 240 <= mx < 260:
            #「+」が押された
            color = tkinter.colorchooser.askcolor()
            if color != None:
                if color[0] != None:
                    #print(color[0][0] * 65536 + color[0][1] * 256 + color[0][2])
                    colordata["color"][csel[0]]["colors"].append(color[0][0] * 65536 + color[0][1] * 256 + color[0][2])
    if 340 < mx < 560 and my >= 120 and (my - 120) % 50 < 40:
        #機能ボタンの中
        if ((my - 120) // 50) == 0:
            #開く
            fn = tkinter.filedialog.askopenfilename(filetypes=[("json", "json")])
            if fn != None and fn != "":
                with open(fn, mode="r") as f:
                    colordata = json.loads(f.read())
        elif ((my - 120) // 50) == 1:
            #保存
            fn = tkinter.filedialog.asksaveasfilename(filetypes=[("json", "json")])
            if fn != None and fn != "":
                with open(fn, mode="w") as f:
                    f.write(json.dumps(colordata))
        elif ((my - 120) // 50) == 2:
            #編集
            if colordata["color"] != [] and colordata["color"][csel[0]]["colors"] != []:
                color = tkinter.colorchooser.askcolor()
                if color != None:
                    if color[0] != None:
                        #print(color[0][0] * 65536 + color[0][1] * 256 + color[0][2])
                        colordata["color"][csel[0]]["colors"][csel[1]] = color[0][0] * 65536 + color[0][1] * 256 + color[0][2]
        elif ((my - 120) // 50) == 3:
            #名前編集
            nm = tkinter.simpledialog.askstring("Palette Tweaker", "この行につける名前を入力:")
            if nm != None and nm != "":
                colordata["color"][csel[0]]["name"] = nm
        elif ((my - 120) // 50) == 4:
            #削除
            if colordata["color"] != [] and colordata["color"][csel[0]]["colors"] != []:
                del(colordata["color"][csel[0]]["colors"][csel[1]])
                csel[1] = max(0, csel[1] - 1)
                if colordata["color"][csel[0]]["colors"] == []:
                    # 列自体が消滅した
                    del(colordata["color"][csel[0]])
                    csel[0] = max(0, csel[0] - 1)
    if 80 < mx < 220 and 350 < my < 380:
        colordata["color"].append({"name": "", "colors":[0]})
        csel[0] = len(colordata["color"]) - 1
        csel[1] = 0
    draw_all()
    pass

def windowresized(w, h):
    global colordata, sg, csel
    draw_all()

def draw_all():
    global colordata, sg, csel
    sg.clear()
    sg.align("left")
    sg.pos(0, 0)
    sg.color(0, 0, 0)
    sg.line(300, 0, 300, 400)
    for rcnt, row in enumerate(colordata["color"]):
        if csel[0] == rcnt:
            sg.color(255, 192, 192)
            sg.box(40, 40 + rcnt * 20, 260, 40 + rcnt * 20 + 20, 1)
            sg.pos(40, 40 + rcnt * 20)
            sg.align("left")
            sg.text("▶")
        sg.color(0, 0, 0)
        sg.pos(60, 40 + rcnt * 20)
        sg.align("left")
        sg.text(rcnt + 1)
        for ccnt, col in enumerate(colordata["color"][rcnt]["colors"]):
            sg.rgbcolor(col)
            sg.fill(80 + ccnt * 40, 40 + rcnt * 20, 110 + ccnt * 40, 40 + rcnt * 20 + 20)
            sg.color(128, 128, 128)
            sg.box(80 + ccnt * 40, 40 + rcnt * 20, 110 + ccnt * 40, 40 + rcnt * 20 + 20)
            #
            sg.color(32, 32, 32)
            sg.box(240, 40 + rcnt * 20, 260, 40 + rcnt * 20 + 20)
            sg.align("center")
            sg.pos(250, 50 + rcnt * 20)
            sg.text("+")

    sg.color(32, 32, 32)
    sg.box(80, 350, 220, 380)
    sg.align("center")
    sg.pos(150, 365)
    sg.text("行を追加")
    #プロパティ
    sg.color(0, 0, 0)
    sg.align("center")
    sg.pos(450, 40)
    sg.text("行 " + str(csel[0] + 1) + ", 列 " + str(csel[1] + 1))
    if colordata["color"] != [] and colordata["color"][csel[0]]["colors"] != []:
        sg.rgbcolor(colordata["color"][csel[0]]["colors"][csel[1]])
        sg.fill(360, 50, 380, 70)
        sg.color(0, 0, 0)
        sg.box(360, 50, 380, 70)
        sg.align("center")
        sg.pos(450, 60)
        sg.color(0, 0, 0)
        c = (colordata["color"][csel[0]]["colors"][csel[1]])
        c = [c // 65536, c % 65536 // 256, c % 256]
        sg.text(
            '{:#03d}'.format(c[0]) + ", " + 
            '{:#03d}'.format(c[1]) + ", " + 
            '{:#03d}'.format(c[2]) 
        )
        sg.pos(450, 80)
        if "name" in colordata["color"][csel[0]]:
            sg.text(colordata["color"][csel[0]]["name"])
    #機能
    sg.color(0, 0, 0)
    for i in range(5):
        buttontext = ["ファイルを開く", "ファイルに保存", "色を編集", "行の名前を変更", "削除"]
        sg.box(340, 120 + 50 * i, 560, 160 + 50 * i)
        sg.align("center")
        sg.pos(450, 140 + 50 * i)
        sg.text(buttontext[i])


def main():
    global colordata, sg
#    with open("color.json") as f:
#        colordata = json.loads(f.read())
    #print(colordata)
    sg = sgpg()
    sg.screen(0, 600, 400)
    sg.title("Palette Tweaker")
    sg.font("ipaexg.ttf")
    sg.neweventhandler("PG_MBUTTONDOWN", mbuttondown)
    sg.neweventhandler("PG_WINDOWRESIZED", windowresized)
    draw_all()
    sg.stop()
    sg.end()

if __name__ == "__main__":
    print("tweakcolor.py、sgpg.pyは、MITライセンス の下でライセンスされています。詳しくは license.txt をご覧ください。")
    print("IPAexゴシック は IPAフォントライセンスV1.0 の下でライセンスされています。詳しくは IPA_Font_License_Agreement_v1.0.txt をご覧ください。")
    main()