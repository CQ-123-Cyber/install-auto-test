import win32api, win32con, win32gui
import ctypes


def switch_input_method():
    IMC_GETOPENSTATUS = 0x0005
    IMC_SETOPENSTATUS = 0x0006

    imm32 = ctypes.WinDLL('imm32', use_last_error=True)
    handle = win32gui.GetForegroundWindow()  # 某进程窗口句柄
    hIME = imm32.ImmGetDefaultIMEWnd(handle)
    status = win32api.SendMessage(hIME, win32con.WM_IME_CONTROL, IMC_GETOPENSTATUS, 0)  # 返回值 0:英文 1:中文
    print(status)

    if status:
        print('当前中文，切换为英文')
        win32api.SendMessage(hIME, win32con.WM_IME_CONTROL, IMC_SETOPENSTATUS, 0)  # 关闭中文
    else:
        print('当前英文')


#   win32api.SendMessage(hIME, win32con.WM_IME_CONTROL, IMC_SETOPENSTATUS, 0)	# 关闭中文
#   win32api.SendMessage(hIME, win32con.WM_IME_CONTROL, IMC_SETOPENSTATUS, 1)	# 开启中文
if __name__ == "__main__":
    switch_input_method()
