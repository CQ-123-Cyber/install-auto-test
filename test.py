# import pyautogui
# import time
# time.sleep(2)
# pyautogui.moveTo(500, 500)  # 将鼠标移动到窗口内
# # time.sleep(5)
# print(pyautogui.position())


from pynput.mouse import Button, Controller
import time

mouse = Controller()
time.sleep(2)
# 将鼠标移动到屏幕的某个位置
mouse.position = (500, 500)

# 模拟鼠标点击
mouse.click(Button.left, 1)

# 模拟鼠标滚动
mouse.scroll(0, 2)