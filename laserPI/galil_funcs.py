
# import gclib
#
# g = gclib.py()
#
# def connect():
#     g.GOpen('192.168.1.40 -d')

def jog(direction):
    if direction == D_UP:
        # g.GCommand('d_up=1')
        if DEBUG == 1:
            print('up_on')
        return
    if direction == D_DOWN:
        # g.GCommand('d_down=1')
        if DEBUG == 1:
            print('down_on')
        return
    if direction == D_LEFT:
        # g.GCommand('d_left=1')
        if DEBUG == 1:
            print('left_on')
        return
    if direction == D_RIGHT:
        # g.GCommand('d_right=1')
        if DEBUG == 1:
            print('right_on')
        return

def jog_stop():
    # g.GCommand('d_up=0')
    # g.GCommand('d_left=0')
    # g.GCommand('d_right=0')
    # g.GCommand('d_down=0')
    return
#
# def change_speed(up_down):
#
# def x_enable():
#
# def y_enable():
#
# def switch_origin():
#
# def home():
#
# def set_home():
#
# def set_nudge_disp():
#