import pyautogui
import time
import logging
logger = logging.getLogger()
time.sleep(2)
pyautogui.moveTo(500, 500, logScreenshot=True)  # 将鼠标移动到窗口内
# # time.sleep(5)
# print(pyautogui.position())

