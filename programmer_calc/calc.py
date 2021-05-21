from tkinter import *
from tkinter import ttk, messagebox

debug_mode_is_on = False

# Main window
root = Tk()
root.title("Programmer's Calculator")
window_width = 340
if debug_mode_is_on:
    window_height = 400
else:
    window_height = 355
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.iconbitmap('calc.ico')
root.resizable(False, False)

# Initial value
currval = 0

# Version
version = StringVar()
version.set(f'Version: 2021.05')

# Debug
curval_debug = StringVar()
curval_debug.set(f'Debug: {currval}')

varbit = IntVar()  # 1 - 16 bit, 2 - 32 bit
varstart = IntVar()  # 1 - Start 0, 2 - Start 1
varsign = IntVar()  # 1 - Signed, 2 - Unsigned
OnTopVar = BooleanVar()  # True - On top, False - Not on top

varbit.set(1)  # Default value
varstart.set(1)  # Default value
varsign.set(2)  # Default value
OnTopVar.set(0)  # Default value


def check_limits(val):
    if varsign.get() == 2:  # Unsigned
        if val < 0:
            val = 0
        if varbit.get() == 1:  # 16-bit
            if val > 65535:
                val = 65535
        else:  # 32-bit
            if val > 4294967295:
                val = 4294967295
    else:  # Signed
        if varbit.get() == 1:  # 16-bit
            if val > 32767:
                val = 32767
            if val < -32768:
                val = -32768
        else:  # 32-bit
            if val > 2147483647:
                val = 2147483647
            if val < -2147483648:
                val = -2147483648
    return val


def convert_negative_value(val):
    val = abs(val)
    str_bin_val = str(bin(val)[2:])

    if varbit.get() == 1:  # 16-bit
        str_bin_val = '0' * (16 - len(str_bin_val)) + str_bin_val
    else:  # 32-bit
        str_bin_val = '0' * (32 - len(str_bin_val)) + str_bin_val

    bin_list = []
    for ch in str_bin_val:
        if ch == '0':
            bin_list.append(1)
        if ch == '1':
            bin_list.append(0)
    bin_list[0] = 1

    total_value = 0
    bin_list.reverse()
    for i in range(len(bin_list)):
        total_value = total_value + 2 ** i * bin_list[i]
    total_value += 1

    return total_value


def update_entries(cur):
    cur = check_limits(cur)

    if cur >= 0:
        str_dec = str(cur)
        str_oct = str(oct(cur)[2:])
        str_hex = str(hex(cur)[2:]).upper()
        str_bin = str(bin(cur)[2:])
    else:
        str_dec = str(cur)

        value = convert_negative_value(cur)
        str_oct = str(oct(value)[2:])
        str_hex = str(hex(value)[2:]).upper()
        str_bin = str(bin(value)[2:])

    if varbit.get() == 1:  # 16-bit
        str_oct = '0' * (6 - len(str_oct)) + str_oct
        str_hex = '0' * (4 - len(str_hex)) + str_hex
        str_bin = '0' * (16 - len(str_bin)) + str_bin
    else:  # 32-bit
        str_oct = '0' * (11 - len(str_oct)) + str_oct
        str_hex = '0' * (8 - len(str_hex)) + str_hex
        str_bin = '0' * (32 - len(str_bin)) + str_bin

    entry_dec.delete(0, END)
    entry_oct.delete(0, END)
    entry_hex.delete(0, END)
    entry_bin.delete(0, END)

    entry_dec.insert(0, str_dec)
    entry_oct.insert(0, str_oct)
    entry_hex.insert(0, str_hex)
    entry_bin.insert(0, str_bin)

    set_bits('0' * (32 - len(str_bin)) + str_bin)

    # Debug
    curval_debug.set(f'Debug: {cur}')


def set_zeros():
    global currval
    currval = 0
    update_entries(currval)


def set_ones():
    global currval
    if varsign.get() == 2:  # Unsigned
        if varbit.get() == 1:  # 16-bit
            currval = 65535
        else:  # 32-bit
            currval = 4294967295
    else:  # Signed
        currval = -1
    update_entries(currval)


def increment():
    global currval
    if varbit.get() == 1:  # 16-bit
        if currval >= 65535:
            currval = 65535
        else:
            currval += 1
    else:  # 32-bit
        if currval >= 4294967295:
            currval = 4294967295
        else:
            currval += 1
    update_entries(currval)


def decrement():
    global currval
    if varsign.get() == 2:  # Unsigned
        if currval <= 0:
            currval = 0
        else:
            currval -= 1
    else:  # Signed
        currval -= 1
    update_entries(currval)


def rightshift():
    global currval
    if varsign.get() == 1:  # Signed
        # varsign.set(2)  # Set Unsigned
        pass
    if currval <= 0:
        # currval = 0
        pass
    elif currval == 1:
        currval = 1
    else:
        currval = currval >> 1
    update_entries(currval)


def leftshift():
    global currval
    if varsign.get() == 1:  # Signed
        # varsign.set(2)  # Set Unsigned
        pass
    if currval <= 0:
        # currval = 0
        pass
    else:
        if varbit.get() == 1:  # 16-bit
            if currval > 32768:
                currval = currval - 32768
                currval = currval << 1
            elif currval == 32768:
                pass
            else:
                currval = currval << 1
        else:  # 32-bit
            if currval > 2147483648:
                currval = currval - 2147483648
                currval = currval << 1
            elif currval == 2147483648:
                pass
            else:
                currval = currval << 1
    update_entries(currval)


def set_value_dec(event):
    global currval
    try:
        currval = int(entry_dec.get())
    except:
        messagebox.showwarning('Warning!', 'Введите десятичное число')
    update_entries(currval)


def set_value_oct(event):
    global currval
    try:
        currval = int(entry_oct.get(), 8)
    except:
        messagebox.showwarning('Warning!', 'Введите восьмеричное число')
    update_entries(currval)


def set_value_hex(event):
    global currval
    try:
        currval = int(entry_hex.get(), 16)
    except:
        messagebox.showwarning('Warning!', 'Введите шестнадцатеричное число')
    update_entries(currval)


def set_value_bin(event):
    global currval
    try:
        currval = int(entry_bin.get(), 2)
    except:
        messagebox.showwarning('Warning!', 'Введите двоичное число')
    update_entries(currval)


def set_bits(str_bin_val):
    i = 31
    for bit_button in bit_buttons:
        if int(str_bin_val[i]) == 1:
            bit_button.select()
        else:
            bit_button.deselect()
        i -= 1


def count_total_positive():
    total = 0
    for i in range(32):
        total = total + 2 ** i * cb_var[i].get()
    return total


def count_total_negative():
    total = 0
    bin_list = []

    for i in range(32):
        bin_list.append(cb_var[i].get())

    if varbit.get() == 1:  # 16-bit
        for i in range(15):
            total = total + 2 ** i * bin_list[i]
    else:  # 32-bit
        for i in range(31):
            total = total + 2 ** i * bin_list[i]
    total -= 1

    if total < 0:
        str_bin = str(bin(total)[3:])
    else:
        str_bin = str(bin(total)[2:])

    if varbit.get() == 1:  # 16-bit
        str_bin = '0' + '0' * (15 - len(str_bin)) + str_bin
    else:  # 32-bit
        str_bin = '0' + '0' * (31 - len(str_bin)) + str_bin
    reversed_str_bin = str_bin[::-1]

    bin_list2 = []
    for ch in reversed_str_bin:
        if ch == '0':
            bin_list2.append(1)
        if ch == '1':
            bin_list2.append(0)
    bin_list2[-1] = 0

    total2 = 0
    for i in range(len(bin_list2)):
        total2 = total2 + 2 ** i * bin_list2[i]
    total2 *= -1

    return total2


def get_bits():
    global currval
    if varsign.get() == 2:  # Unsigned
        currval = count_total_positive()
    else:  # Signed
        if varbit.get() == 1:  # 16-bit
            if cb_var[15].get() == 1:  # It's negative value
                currval = count_total_negative()
            else:  # It's positive value
                currval = count_total_positive()
        else:  # 32-bit
            if cb_var[31].get() == 1:  # It's negative value
                currval = count_total_negative()
            else:  # It's positive value
                currval = count_total_positive()
    update_entries(currval)


def selbit():
    i = 0
    if varbit.get() == 1:  # 16-bit
        for bit_button in bit_buttons:
            i += 1
            if i > 16:
                bit_button['state'] = DISABLED
                bit_button.deselect()
    else:  # 32-bit
        for bit_button in bit_buttons:
            i += 1
            if i > 16:
                bit_button['state'] = NORMAL
    get_bits()


def selstart():
    if varstart.get() == 1:
        i = 0
        for bit_label in bit_labels:
            bit_label['text'] = i
            i += 1
    else:
        i = 1
        for bit_label in bit_labels:
            bit_label['text'] = i
            i += 1


def selsign():
    pass


def setontop():
    if OnTopVar.get():
        root.attributes('-topmost', 1)
    else:
        root.attributes('-topmost', 0)


# Calc Frame
calc_frame = Frame(root)
calc_frame.pack(fill=X, pady=10)
calc_frame.grid_columnconfigure(1, weight=1)

# Titles
titles = ['DEC', 'OCT', 'HEX', 'BIN']
for i in range(4):
    Label(calc_frame, text=titles[i], width=3, anchor=W, font='Arial 10 bold').grid(row=i, column=0, padx=(10, 0))

# DEC
entry_dec = ttk.Entry(calc_frame, justify=RIGHT, font="Arial 10")
entry_dec.grid(row=0, column=1, pady=2, padx=10, sticky=EW)
entry_dec.bind("<Return>", set_value_dec)
# entry_dec.insert(0, START_VALUE)

# OCT
entry_oct = ttk.Entry(calc_frame, justify=RIGHT, font="Arial 10")
entry_oct.grid(row=1, column=1, pady=2, padx=10, sticky=EW)
entry_oct.bind("<Return>", set_value_oct)
# entry_oct.insert(0, START_VALUE)

# HEX
entry_hex = ttk.Entry(calc_frame, justify=RIGHT, font="Arial 10")
entry_hex.grid(row=2, column=1, pady=2, padx=10, sticky=EW)
entry_hex.bind("<Return>", set_value_hex)
# entry_hex.insert(0, START_VALUE)

# BIN
entry_bin = ttk.Entry(calc_frame, justify=RIGHT, font="Arial 10")
entry_bin.grid(row=3, column=1, pady=2, padx=10, sticky=EW)
entry_bin.bind("<Return>", set_value_bin)
# entry_bin.insert(0, START_VALUE)


# CheckButtons Frame
checkbuttons_frame = Frame(root)
checkbuttons_frame.pack(fill=X, padx=10)
checkbuttons_frame.grid_columnconfigure(0, weight=1)
checkbuttons_frame.grid_columnconfigure(1, weight=1)
checkbuttons_frame.grid_columnconfigure(2, weight=1)
checkbuttons_frame.grid_columnconfigure(3, weight=1)
checkbuttons_frame.grid_columnconfigure(4, weight=1)
checkbuttons_frame.grid_columnconfigure(5, weight=1)
checkbuttons_frame.grid_columnconfigure(6, weight=1)
checkbuttons_frame.grid_columnconfigure(7, weight=1)
checkbuttons_frame.grid_columnconfigure(8, weight=1)
checkbuttons_frame.grid_columnconfigure(9, weight=1)
checkbuttons_frame.grid_columnconfigure(10, weight=1)
checkbuttons_frame.grid_columnconfigure(11, weight=1)
checkbuttons_frame.grid_columnconfigure(12, weight=1)
checkbuttons_frame.grid_columnconfigure(13, weight=1)
checkbuttons_frame.grid_columnconfigure(14, weight=1)
checkbuttons_frame.grid_columnconfigure(15, weight=1)

s = ttk.Style()
s.configure("TLabel", width=3, anchor="w", font="Arial 8 bold")

bit_labels = []
for i in range(32):
    if varstart.get() == 1:
        bit_labels.append(ttk.Label(checkbuttons_frame, text=i))
    else:
        bit_labels.append(ttk.Label(checkbuttons_frame, text=i + 1))

i = 0
for bit_label in bit_labels:
    if i < 16:
        bit_label.grid(row=2, column=15-i)
    else:
        bit_label.grid(row=0, column=31-i)
    i += 1

bit_buttons = []
cb_var = []
for i in range(32):
    cb_var.append(IntVar())
    bit_buttons.append(Checkbutton(checkbuttons_frame, variable=cb_var[i], onvalue=1, offvalue=0, command=get_bits))

i = 0
if varbit.get() == 1:
    for bit_button in bit_buttons:
        i += 1
        if i > 16:
            bit_button['state'] = DISABLED

i = 0
for bit_button in bit_buttons:
    if i < 16:
        bit_button.grid(row=3, column=15-i)
    else:
        bit_button.grid(row=1, column=31-i)
    i += 1

update_entries(currval)

# Buttons Frame
buttons_frame = Frame(root)
buttons_frame.pack(fill=X, padx=10, pady=10)
buttons_frame.grid_columnconfigure(0, weight=1)
buttons_frame.grid_columnconfigure(1, weight=1)
buttons_frame.grid_columnconfigure(2, weight=1)
buttons_frame.grid_columnconfigure(3, weight=1)
buttons_frame.grid_columnconfigure(4, weight=1)
buttons_frame.grid_columnconfigure(5, weight=1)

# Button "-1"
btn1 = ttk.Button(buttons_frame, text="-1", command=decrement)
btn1.grid(row=0, column=0)

# Button "<<"
btn2 = ttk.Button(buttons_frame, text="<<", command=leftshift)
btn2.grid(row=0, column=1)

# Button ">>"
btn3 = ttk.Button(buttons_frame, text=">>", command=rightshift)
btn3.grid(row=0, column=2)

# Button "+1"
btn4 = ttk.Button(buttons_frame, text="+1", command=increment)
btn4.grid(row=0, column=3)

# Button "=1"
btn5 = ttk.Button(buttons_frame, text="=1", command=set_ones)
btn5.grid(row=0, column=4)

# Button "=0"
btn6 = ttk.Button(buttons_frame, text="=0", command=set_zeros)
btn6.grid(row=0, column=5)

# Options Frame
options_frame = Frame(root)
options_frame.pack(fill=X, padx=10)
options_frame.grid_columnconfigure(2, weight=1)

R1 = Radiobutton(options_frame, text="16-bit", variable=varbit, value=1, command=selbit)
R2 = Radiobutton(options_frame, text="32-bit", variable=varbit, value=2, command=selbit)
R3 = Radiobutton(options_frame, text="Start 0", variable=varstart, value=1, command=selstart)
R4 = Radiobutton(options_frame, text="Start 1", variable=varstart, value=2, command=selstart)
R5 = Radiobutton(options_frame, text="Signed", variable=varsign, value=1, command=selsign)
R6 = Radiobutton(options_frame, text="Unsigned", variable=varsign, value=2, command=selsign)

R1.grid(row=0, column=0, sticky=W)
R2.grid(row=0, column=1, sticky=W)
R3.grid(row=1, column=0, sticky=W)
R4.grid(row=1, column=1, sticky=W)
R5.grid(row=2, column=0, sticky=W)
R6.grid(row=2, column=1, sticky=W)

# Footer Frame
footer_frame = Frame(root)
footer_frame.pack(fill=X, padx=10)
footer_frame.grid_columnconfigure(1, weight=1)

OnTop = Checkbutton(footer_frame, text='Always on top', onvalue=1, offvalue=0, variable=OnTopVar, command=setontop)
OnTop.grid(row=0, column=0, sticky=W)
Label(footer_frame, textvariable=version).grid(row=0, column=1, sticky=E)


# Debug Frame
debug_frame = Frame(root)
debug_frame.pack(fill=X, padx=10)

# Debug
debug_label = Label(debug_frame, textvariable=curval_debug)
debug_label.pack(side=LEFT)

root.mainloop()
