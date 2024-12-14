#!/usr/bin/env python
# coding: utf-8

# In[2]:


import sys
import random
from PyQt5.QtWidgets import QApplication, QLabel, QMenu
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QTimer, QPoint, QElapsedTimer

# 全域變數
idle_time = 0  # 閒置時間
on_idle = False  # 閒置狀態
is_dragging = False  # 拖曳狀態
drag_position = None  # 滑鼠點擊位置與寵物視窗左上角的座標差異
elapsed_timer = QElapsedTimer()  # 算間隔時間
restore_timer = QTimer()  # 計時器

# 圖片路徑定義
normal_gif = "./pet/normal.gif"
idle_gifs = [f"./pet/idle/idle_{i}.gif" for i in range(1, 7)]
double_click_gifs = [f"./pet/double_click/double_click_{i}.gif" for i in range(1, 6)]
falling_gif = "./pet/drag_falling/fall0.png"
fallen_gif = "./pet/drag_falling/fall.gif"
quit_gif = "./pet/quit.gif"

# 創建寵物
def create_desktop_pet():
    global pet_label, pet_movie

    # 建立標籤
    pet_label = QLabel()
    pet_label.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)  # 無框、置頂、子視窗
    pet_label.setAttribute(Qt.WA_TranslucentBackground, True)  # 透明

    # 載入寵物預設圖片
    pet_movie = QMovie(normal_gif)
    pet_label.setMovie(pet_movie)
    pet_label.setScaledContents(True)  # 大小自動調整
    pet_movie.start()

    # 設定滑鼠事件
    pet_label.mousePressEvent = lambda event: mouse_press_event(event, pet_label)
    pet_label.mouseMoveEvent = lambda event: mouse_move_event(event, pet_label)
    pet_label.mouseReleaseEvent = lambda event: mouse_release_event(event, pet_label)
    pet_label.mouseDoubleClickEvent = lambda event: mouse_double_click_event(event, pet_label)
    pet_label.contextMenuEvent = lambda event: context_menu_event(event, pet_label)

    # 檢測閒置
    start_idle_timer(pet_label)

    return pet_label

# 設定圖片
def set_gif(gif_file):
    global pet_label, pet_movie, idle_time
    pet_movie.stop()
    new_movie = QMovie(gif_file)
    pet_label.setMovie(new_movie)
    new_movie.start()
    idle_time = 0  # 重置閒置時間，避免等待自動更換圖片時間被計入閒置時間

# 閒置計時
def start_idle_timer(pet_label):
    global idle_timer
    idle_timer = QTimer()
    idle_timer.timeout.connect(lambda: check_idle_time(pet_label))
    idle_timer.start(1000)  # 每1秒檢查是否已達閒置時間
        
# 閒置10秒更換閒置圖片
def check_idle_time(pet_label):
    global idle_time, on_idle
    idle_time += 1
    if idle_time >= 10 and not on_idle:  # 檢查是否已達10秒 且 目前非閒置狀態
        on_idle = True
        # 更換為隨機閒置圖片
        selected_gif = random.choice(idle_gifs)
        set_gif(selected_gif)

# 選單事件
def context_menu_event(event, pet_label):
    closing = False
    menu = QMenu(pet_label)
    quit_action = menu.addAction("Good Bye!")
    action = menu.exec_(pet_label.mapToGlobal(event.pos()))
    if action == quit_action and not closing:  # 檢測是否為關閉動作 且 不是正在關閉中
        closing = True
        show_closing_gif(pet_label)
            
# 更換關閉動畫
def show_closing_gif(pet_label):
    global pet_movie
    pet_movie.stop()
    closing_movie = QMovie(quit_gif)
    pet_label.setMovie(closing_movie)
    closing_movie.start()
    close_timer = QTimer()
    close_timer.singleShot(2300, lambda: quit_application(pet_label))  # 2.3秒後關閉
        
# 關閉
def quit_application(pet_label):
    pet_label.close()
    QApplication.instance().quit()

# 滑鼠按下事件
def mouse_press_event(event, pet_label):
    global drag_position, is_dragging, idle_time, on_idle, elapsed_timer
    idle_time = 0  # 重置閒置時間
    on_idle = False
    if event.button() == Qt.LeftButton:  # 左鍵按下
        drag_position = event.globalPos() - pet_label.frameGeometry().topLeft()  # 紀錄滑鼠點擊位置與寵物視窗左上角的座標差異
        is_dragging = False  # 非拖曳狀態
        elapsed_timer.restart()  # 開始計時
        event.accept()  # 避免誤觸其他事件

# 滑鼠移動事件
def mouse_move_event(event, pet_label):
    global drag_position, is_dragging, idle_time, on_idle
    idle_time = 0  # 重置閒置時間
    on_idle = False
    if event.buttons() == Qt.LeftButton:  # 左鍵觸發
        is_dragging = True
        pet_label.move(event.globalPos() - drag_position)  # 移動寵物
        event.accept()  # 避免誤觸其他事件

# 滑鼠放開事件
def mouse_release_event(event, pet_label):
    global is_dragging, idle_time, on_idle, elapsed_timer
    idle_time = 0  # 重置閒置時間
    on_idle = False
    # 拖曳放開事件
    if event.button() == Qt.LeftButton and is_dragging:  # 由左鍵觸發且為拖曳狀態中
        if elapsed_timer.elapsed() > QApplication.doubleClickInterval():  # 動作時間大於滑鼠雙擊時間間隔，避免雙擊誤觸
            is_dragging = False
            # 停止之前的計時，避免中途自動更換圖片
            if restore_timer.isActive():
                restore_timer.stop()
            set_gif(falling_gif)  # 更換為落下圖片
            move_to_bottom(pet_label)  # 移動至底部
    event.accept()  # 避免誤觸其他事件
        
# 滑鼠雙擊事件
def mouse_double_click_event(event, pet_label):
    global idle_time, on_idle, restore_timer
    idle_time = 0  # 重置閒置時間
    on_idle = False
    # 是否左鍵觸發 和 動作時間是否小於等於滑鼠雙擊時間間隔 判斷是否為左鍵雙擊
    if event.button() == Qt.LeftButton and elapsed_timer.elapsed() <= QApplication.doubleClickInterval():
        # 為了可以連續觸發雙擊變更圖片，每變換一次便重置計時器
        # 停止之前的計時
        if restore_timer.isActive():
            restore_timer.stop()
        # 更換為隨機雙擊圖片
        selected_gif = random.choice(double_click_gifs)
        set_gif(selected_gif)
        # 開始計時
        restore_timer = QTimer()
        restore_timer.setSingleShot(True)
        restore_timer.timeout.connect(lambda: set_gif(normal_gif))  # 更換回初始圖片
        restore_timer.start(3000)  # 計時器重置至3秒

# 移動至底部
def move_to_bottom(pet_label):
    global pet_movie
    current_pos = pet_label.pos()  # 紀錄目前寵物位置
    end_pos = QPoint(current_pos.x(), QApplication.desktop().height() - pet_label.height())  # 目的位置(底部位置)
    step = 10  # 每次移動10px
    timer = QTimer()

    def animate():
        nonlocal current_pos
        if current_pos.y() < end_pos.y():  # 判斷是否尚未掉落至底部
            current_pos.setY(current_pos.y() + step)  # 每次y座標+10px(寵物往下掉10px)
            pet_label.move(current_pos)  # 移動寵物
        else:
            timer.stop()
            set_gif(fallen_gif)  # 更換為掉落完畢動畫
            QTimer.singleShot(3500, lambda: set_gif(normal_gif))  # 3.5秒後更換回初始圖片

    timer.timeout.connect(animate)
    timer.start(30)  # 每30毫秒讓寵物往下移動一次

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = create_desktop_pet()
    pet.show()
    sys.exit(app.exec_())


# In[ ]:




