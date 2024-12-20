# DesktopPet

這是一支簡單的桌面寵物程式，可雙擊或拖曳與寵物互動，並且有閒置動作和結束動作。  
****
功能概述  
1. 雙擊寵物會有隨機5種不同的反應，可連續雙擊切換。
2. 拖曳寵物放開後，寵物緩慢落下至螢幕底部，於播放完落地動畫後，切換回一般狀態。(快速移動寵物不視為拖曳)
3. 寵物閒置10秒後，會有隨機6種不同的反應，雙擊或拖曳互動後解除。
4. 右鍵選單關閉程式(Good Bye!)後，切換為關閉動畫後結束程式。
****
程式開發流程  
1. 設定圖片路徑
2. 建立寵物視窗
3. 設定滑鼠事件
4. 設定圖片函式
5. 製作閒置狀態(計時並檢測是否超過閒置時間、閒置狀態更換圖片)
6. 製作選單以關閉程式，設定關閉動畫
7. 撰寫滑鼠事件(按下、移動、放開、雙擊)
8. 於滑鼠放開部分增加判定拖曳放開動作，製作落下效果
9. 調整各項滑鼠事件不互相錯誤觸發
10. 建立重置計時器，避免互動演示過程計入閒置時間內
11. pyinstaller打包為.exe可執行檔(參數: --i -F -D --noconsole)
****
程式撰寫主要技巧  
1. 初始定義圖片路徑，方便路徑及檔名更動。
2. 各項功能盡量以函式個別撰寫，較易閱讀及維護。
3. 以變數作為標籤，或利用計時器重置、時間差比較等方式，避免滑鼠事件相互觸發干擾。
****
改進空間  
1. 事件觸發後，應鎖定無法觸發其他事件，避免過程干擾。(例如: 寵物落下事件中，故意觸發雙擊事件，造成寵物行為混亂)
2. 寵物落下過程應鎖定寵物，不允許拖曳。
****
開發環境  
Windows 10  
Anaconda Jupyter(本機環境開發，虛擬環境打包)  
Python 3.13.0  
PyQt5 5.15.11  
