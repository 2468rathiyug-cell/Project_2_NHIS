import tkinter as tk
import math
import re
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
import requests
import pycountry

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Calculator")
root.geometry("360x520")
root.configure(bg="#121212")
root.resizable(False, False)

expression = ""
history = []
panel_open = False
current_panel = None
nav_open = False
second_mode = False
memory_value = 0
deg_mode = True
prog_digit_buttons = {}
active_dropdown = None

# -------- DATE CALENDAR GLOBALS --------
from_date = None
to_date = None
current_year = datetime.now().year
current_month = datetime.now().month
selecting_from = True
open_dropdown = None
open_button = None
prevent_dropdown_open = False

currency_rates = {}
currency_display_list = []
currency_map = {}


volume_units = {
    # Metric
    "Cubic metres": 1,
    "Litres": 1000,
    "Millilitres": 1_000_000,
    "Cubic centimetres": 1_000_000,

    # US Customary
    "Teaspoons (US)": 202884.136,
    "Tablespoons (US)": 67628.045,
    "Fluid ounces (US)": 33814.023,
    "Cups (US)": 4226.753,
    "Pints (US)": 2113.376,
    "Quarts (US)": 1056.688,
    "Gallons (US)": 264.172,

    # Imperial / UK
    "Teaspoons (UK)": 168936.383,
    "Tablespoons (UK)": 56312.127,
    "Fluid ounces (UK)": 35195.079,
    "Pints (UK)": 1759.754,
    "Quarts (UK)": 879.877,
    "Gallons (UK)": 219.969,

    # Cubic
    "Cubic inches": 61023.744,
    "Cubic feet": 35.3147,
    "Cubic yards": 1.30795
}


length_units = {
    "Angstroms": 1e-10,
    "Nanometres": 1e-9,
    "Microns": 1e-6,
    "Millimetres": 1e-3,
    "Centimetres": 1e-2,
    "Metres": 1,
    "Kilometres": 1000,
    "Inches": 0.0254,
    "Feet": 0.3048,
    "Yards": 0.9144,
    "Miles": 1609.344,
    "Nautical miles": 1852
}


weight_units = {
    "Carats": 0.0002,
    "Milligrams": 0.000001,
    "Centigrams": 0.00001,
    "Decigrams": 0.0001,
    "Grams": 0.001,
    "Decagrams": 0.01,
    "Hectograms": 0.1,
    "Kilograms": 1,
    "Metric tonnes": 1000,
    "Ounces": 0.0283495,
    "Pounds": 0.453592,
    "Stone": 6.35029,
    "Short tons (US)": 907.184,
    "Long tons (UK)": 1016.0469088
}


temperature_units = ["Celsius", "Fahrenheit", "Kelvin"]


energy_units = {
    "Electron volts": 1.60218e-19,
    "Joules": 1,
    "Kilojoules": 1000,
    "Thermal calories": 4.184,
    "Food calories": 4184,
    "Foot-pounds": 1.35582,
    "British thermal units": 1055.06,
    "Kilowatt-hours": 3.6e6
}


area_units = {
    "Square millimetres": 0.000001,
    "Square centimetres": 0.0001,
    "Square metres": 1,
    "Hectares": 10000,
    "Square kilometres": 1_000_000,
    "Square inches": 0.00064516,
    "Square feet": 0.092903,
    "Square yards": 0.836127,
    "Acres": 4046.86,
    "Square miles": 2_589_988.11
}


speed_units = {
    "Centimetres per second": 0.01,
    "Metres per second": 1,
    "Kilometres per hour": 0.277778,
    "Feet per second": 0.3048,
    "Miles per hour": 0.44704,
    "Knots": 0.514444,
    "Mach": 343  # approx at sea level
}


time_units = {
    "Microseconds": 0.000001,
    "Milliseconds": 0.001,
    "Seconds": 1,
    "Minutes": 60,
    "Hours": 3600,
    "Days": 86400,
    "Weeks": 604800,
    "Years": 31557600  # 365.25 days
}


power_units = {
    "Watts": 1,
    "Kilowatts": 1000,
    "Horsepower (US)": 745.699872,
    "Foot-pounds/minute": 0.0225969658,
    "BTUs/minute": 17.5842667
}


data_units = {
    "Bits": 1/8,
    "Nibble": 0.5,
    "Bytes": 1,
    "Kilobits": 1000/8,
    "Kibibits": 1024/8,
    "Kilobytes": 1000,
    "Kibibytes": 1024,
    "Megabits": 1000**2/8,
    "Mebibits": 1024**2/8,
    "Megabytes": 1000**2,
    "Mebibytes": 1024**2,
    "Gigabits": 1000**3/8,
    "Gibibits": 1024**3/8,
    "Gigabytes": 1000**3,
    "Gibibytes": 1024**3,
    "Terabits": 1000**4/8,
    "Tebibits": 1024**4/8,
    "Terabytes": 1000**4,
    "Tebibytes": 1024**4,
    "Petabits": 1000**5/8,
    "Pebibits": 1024**5/8,
    "Petabytes": 1000**5,
    "Pebibytes": 1024**5,
    "Exabits": 1000**6/8,
    "Exbibits": 1024**6/8,
    "Exabytes": 1000**6,
    "Exbibytes": 1024**6,
    "Zetabits": 1000**7/8,
    "Zebibits": 1024**7/8,
    "Zetabytes": 1000**7,
    "Zebibytes": 1024**7,
    "Yottabits": 1000**8/8,
    "Yobibits": 1024**8/8,
    "Yottabytes": 1000**8,
    "Yobibytes": 1024**8,
}


pressure_units = {
    "Atmospheres": 101325,
    "Bars": 100000,
    "Kilopascals": 1000,
    "Millimetres of mercury": 133.322,
    "Pascals": 1,
    "Pounds per square inch": 6894.757
}


angle_units = {
    "Degrees": 1,
    "Radians": 57.29577951308232,
    "Gradians": 0.9
}

# ---------------- MAIN CONTAINER ----------------
main = tk.Frame(root, bg="#121212")
main.pack(fill="both", expand=True)

main.rowconfigure(0, weight=0)   # Top section (fixed)
main.rowconfigure(1, weight=1)   # Keypad section (expand)
main.columnconfigure(0, weight=1)

# >>> ADDED: LEFT NAV PANEL <<<
nav_panel = tk.Frame(root, bg="#1a1a1a", width=260)
nav_panel.place_forget()

NAV_WIDTH = 260
ANIM_SPEED = 15

def slide_nav_in(x):
    if x < 0:
        nav_panel.place(x=x, y=0, relheight=1)
        root.after(10, lambda: slide_nav_in(x + ANIM_SPEED))
    else:
        nav_panel.place(x=0, y=0, relheight=1)

def slide_nav_out(x):
    if x > -NAV_WIDTH:
        nav_panel.place(x=x, y=0, relheight=1)
        root.after(10, lambda: slide_nav_out(x - ANIM_SPEED))
    else:
        nav_panel.place_forget()

def toggle_nav():
    global nav_open

    if not nav_open:
        nav_panel.place(x=-NAV_WIDTH, y=0, relheight=1)
        root.geometry("620x520")
        slide_nav_in(-NAV_WIDTH)

        # Bind scroll globally while nav is open
        root.bind_all("<MouseWheel>", _on_mousewheel)

        nav_open = True
    else:
        slide_nav_out(0)
        root.geometry("360x520")

        # Remove scroll binding
        root.unbind_all("<MouseWheel>")

        nav_open = False

def close_nav_on_click(event):
    global nav_open
    if nav_open and event.x > NAV_WIDTH:
        toggle_nav()


tk.Label(
    nav_panel, text="Calculator",
    bg="#1a1a1a", fg="white",
    font=("Segoe UI", 16, "bold")
).pack(anchor="w", padx=20, pady=20)

# ================= SCROLLABLE NAV =================
nav_canvas = tk.Canvas(
    nav_panel,
    bg="#1a1a1a",
    highlightthickness=0,
    width=NAV_WIDTH
)
nav_scrollbar = tk.Scrollbar(nav_panel, orient="vertical", command=nav_canvas.yview)

nav_scroll_frame = tk.Frame(nav_canvas, bg="#1a1a1a")

nav_scroll_frame.bind(
    "<Configure>",
    lambda e: nav_canvas.configure(scrollregion=nav_canvas.bbox("all"))
)

nav_canvas.create_window((0, 0), window=nav_scroll_frame, anchor="nw")
nav_canvas.configure(yscrollcommand=nav_scrollbar.set)

nav_canvas.pack(side="left", fill="both", expand=True)
nav_scrollbar.pack(side="right", fill="y")

def _on_mousewheel(event):
    nav_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

nav_open = False

def nav_click(name):
    title_label.config(text=name.title())

    # ---- ALWAYS RESTORE IN ORIGINAL POSITION ----
    display.pack(fill="x", padx=10, pady=(10, 5), ipady=10, before=btns)
    result_label.pack(fill="x", padx=12, before=btns)
    top.pack(fill="x", pady=5, before=btns)


    if name == "Scientific":
        build_scientific_buttons()

    elif name == "Standard":
        rebuild_standard_buttons()

    elif name == "Programmer":
        build_programmer_buttons()

    elif name == "Date calculation":
        build_date_calculation()
        display.pack_forget()
        result_label.pack_forget()
        top.pack_forget()

    elif name == "Currency":
        build_currency_ui()
        # ---- HIDE NORMAL CALCULATOR UI ----
        display.pack_forget()
        result_label.pack_forget()
        top.pack_forget()

    elif name == "Volume":
        build_volume_ui()
        display.pack_forget()
        result_label.pack_forget()
        top.pack_forget()

    elif name == "Length":
        build_length_ui()
        display.pack_forget()
        result_label.pack_forget()
        top.pack_forget()

    elif name == "Weight and mass":
        build_weight_ui()
        display.pack_forget()
        result_label.pack_forget()
        top.pack_forget()

    elif name == "Temperature":
        build_temperature_ui()
        display.pack_forget()
        result_label.pack_forget()
        top.pack_forget()

    elif name == "Energy":
        build_energy_ui()
        display.pack_forget()
        result_label.pack_forget()
        top.pack_forget()

    elif name == "Area":
        build_area_ui()
        display.pack_forget()
        result_label.pack_forget()
        top.pack_forget()

    elif name == "Speed":
        build_speed_ui()
        display.pack_forget()
        result_label.pack_forget()
        top.pack_forget()

    elif name == "Time":
        build_time_ui()
        display.pack_forget()
        result_label.pack_forget()
        top.pack_forget()

    elif name == "Power":
        build_power_ui()
        display.pack_forget()
        result_label.pack_forget()
        top.pack_forget()

    elif name == "Data":
        build_data_ui()
        display.pack_forget()
        result_label.pack_forget()
        top.pack_forget()

    elif name == "Pressure":
        build_pressure_ui()
        display.pack_forget()
        result_label.pack_forget()
        top.pack_forget()

    elif name == "Angle":
        build_angle_ui()
        display.pack_forget()
        result_label.pack_forget()
        top.pack_forget()

for item in [
    "Standard", "Scientific",
    "Programmer", "Date calculation",
    "Currency", "Volume", "Length", "Weight and mass",
    "Temperature", "Energy", "Area" ,"Speed", "Time", "Power",
    "Data", "Pressure", "Angle"
]:
    tk.Button(
        nav_scroll_frame, text=item,
        bg="#1a1a1a", fg="white",
        bd=0, font=("Segoe UI", 12),
        anchor="w",
        command=lambda x=item: nav_click(x)
    ).pack(fill="x", padx=25, pady=6)

calc_area = tk.Frame(main, bg="#121212")
calc_area.pack(side="left", fill="both", expand=True)

side_panel = tk.Frame(main, bg="#1a1a1a", width=260)

# >>> ADDED: STANDARD TOP BAR (ABOVE RESULT) <<<
standard_bar = tk.Frame(calc_area, bg="#121212", height=45)
standard_bar.pack(fill="x")

tk.Button(
    standard_bar, text="☰",
    font=("Segoe UI", 16),
    bg="#121212", fg="white",
    bd=0,
    command=toggle_nav
).pack(side="left", padx=10)

title_label = tk.Label(
    standard_bar,
    text="Standard",
    font=("Segoe UI", 14, "bold"),
    bg="#121212",
    fg="white"
)
title_label.pack(side="left")

# ---------------- DISPLAY ----------------
display = tk.Entry(
    calc_area, font=("Segoe UI", 22),
    bg="#1e1e1e", fg="white",
    bd=0, justify="right"
)
display.pack(fill="x", padx=10, pady=(10, 5), ipady=10)

result_label = tk.Label(
    calc_area, text="",
    font=("Segoe UI", 14),
    bg="#121212", fg="#aaaaaa",
    anchor="e"
)
result_label.pack(fill="x", padx=12)

# ---------------- TOP BAR ----------------
top = tk.Frame(calc_area, bg="#121212")
top.pack(fill="x", pady=5)

def open_panel():
    global panel_open
    if not panel_open:
        side_panel.pack(side="right", fill="y")
        root.geometry("620x520")
        panel_open = True

def close_panel():
    global panel_open, current_panel
    side_panel.pack_forget()
    root.geometry("360x520")
    panel_open = False
    current_panel = None

tk.Button(top, text="HISTORY", bg="#CCFFBE", fg="black",
          command=lambda: toggle_history()).pack(side="left", padx=5)

tk.Button(top, text="AC", bg="#b00020", fg="white",
          command=lambda: clear()).pack(side="right", padx=5)

tk.Button(top, text="⌫", bg="#1e1e1e", fg="white",
          command=lambda: backspace()).pack(side="right")

# ---------------- SIDE PANEL ----------------
side_panel = tk.Frame(main, bg="#1a1a1a", width=260)

panel_content = tk.Frame(side_panel, bg="#1a1a1a")
panel_content.pack(fill="both", expand=True, padx=10, pady=10)

def clear_panel():
    for w in panel_content.winfo_children():
        w.destroy()

# ---------------- SAFE EVAL ----------------
def safe_eval(expr):
    expr = re.sub(r'(\d+(\.\d+)?)%', r'(\1/100)', expr)
    return eval(expr)

# ---------------- LOGIC ----------------
def update_live():
    try:
        res = safe_eval(expression)
        result_label.config(text=f"= {res}")
    except:
        result_label.config(text="")

def press(val):
    global expression
    expression += str(val)
    display.delete(0, tk.END)
    display.insert(tk.END, expression)
    update_live()

def clear():
    global expression
    expression = ""
    display.delete(0, tk.END)
    result_label.config(text="")

def backspace():
    global expression
    expression = expression[:-1]
    display.delete(0, tk.END)
    display.insert(tk.END, expression)
    update_live()

def calculate():
    global expression
    try:
        result = safe_eval(expression)
        history.append(f"{expression} = {result}")
        display.delete(0, tk.END)
        display.insert(tk.END, result)
        expression = str(result)
        update_live()
    except:
        display.delete(0, tk.END)
        display.insert(tk.END, "Error")
        expression = ""

def toggle_sign():
    global expression

    # Case 1: ends with (-number)
    match = re.search(r'\(-(\d+(\.\d+)?)\)$', expression)
    if match:
        expression = expression[:-len(match.group(0))] + match.group(1)

    # Case 2: ends with number
    else:
        match = re.search(r'(\d+(\.\d+)?)$', expression)
        if not match:
            return
        num = match.group(1)
        expression = expression[:match.start()] + f"(-{num})"

    display.delete(0, tk.END)
    display.insert(tk.END, expression)
    update_live()

# ---------------- FUNCTION APPLY (KEY FIX) ----------------
def apply_func(func):
    global expression

    match = re.search(r'(\d+(\.\d+)?)$', expression)
    if match:
        num = match.group(1)
        expression = expression[:match.start()] + f"{func}({num})"
    else:
        expression += f"{func}("

    display.delete(0, tk.END)
    display.insert(tk.END, expression)
    update_live()

def apply_rand():
    global expression
    expression += str(random.random())
    display.delete(0, tk.END)
    display.insert(tk.END, expression)
    update_live()

# ---------------- HISTORY ----------------
def toggle_history():
    global current_panel
    if panel_open and current_panel == "history":
        close_panel()
        return

    clear_panel()
    open_panel()
    current_panel = "history"

    tk.Label(panel_content, text="History",
             fg="white", bg="#1a1a1a",
             font=("Segoe UI", 14)).pack(anchor="w")

    for item in history[::-1]:
        tk.Label(panel_content, text=item,
                 fg="white", bg="#1a1a1a",
                 anchor="e").pack(fill="x", pady=4)


memory_value = 0
def mc():
    global memory_value
    memory_value = 0

def mr():
    press(memory_value)

def m_plus():
    global memory_value
    try:
        memory_value += float(display.get())
    except:
        pass

def m_minus():
    global memory_value
    try:
        memory_value -= float(display.get())
    except:
        pass

def ms():
    global memory_value
    try:
        memory_value = float(display.get())
    except:
        pass

def build_memory_row(row_number=0):
    global deg_btn

    memory_row = tk.Frame(btns, bg="#121212")
    memory_row.grid(row=row_number, column=0, columnspan=6, sticky="w", pady=(5,5))

    for t, cmd in [
        ("MC", mc), ("MR", mr),
        ("M+", m_plus), ("M-", m_minus), ("MS", ms)
    ]:
        tk.Button(
            memory_row,
            text=t,
            width=4,
            bg="#B1CBFF",
            fg="black",
            command=cmd
        ).pack(side="left", padx=3)

# ---------------- BUTTON GRID ----------------
btns = tk.Frame(calc_area, bg="#121212")
btns.pack(fill="both", expand=True)
for i in range(6):
    btns.columnconfigure(i, weight=1)

build_memory_row(row_number=0)
layout = [
    ("(","("), (")",")"), ("+/-", "SIGN"), ("÷", "/"),
    ("7","7"),("8","8"),("9","9"),("×","*"),
    ("4","4"),("5","5"),("6","6"),("−","-"),
    ("1","1"),("2","2"),("3","3"),("+","+"),
    ("%","%"),("0","0"),(".","."),("=","=")
]

r = 1
c = 0
for t, v in layout:
    # Determine button command and color
    if v == "SIGN":
        cmd = toggle_sign
        bg_color = "#1e1e1e"
    elif v == "=":
        cmd = calculate
        bg_color = "#2962ff"  # blue color
    else:
        cmd = lambda x=v: press(x)
        bg_color = "#1e1e1e"

    tk.Button(
        btns, text=t,
        width=6, height=1,
        font=("Segoe UI", 14),
        bg=bg_color, fg="white",
        command=cmd
    ).grid(row=r, column=c, padx=6, pady=6)

    c += 1
    if c == 4:
        c = 0
        r += 1
root.bind("<Button-1>", close_nav_on_click)

# ================= SCIENTIFIC MODE ADDON =================

memory_value = 0
deg_mode = True

def clear_buttons():
    for widget in btns.winfo_children():
        widget.destroy()

# ---------- DEG / RAD ----------
def toggle_deg():
    global deg_mode
    deg_mode = not deg_mode
    deg_btn.config(text="DEG" if deg_mode else "RAD")

def convert_angle(x):
    return math.radians(x) if deg_mode else x

# ---------- MEMORY ----------
def mc():
    global memory_value
    memory_value = 0

def mr():
    press(memory_value)

def m_plus():
    global memory_value
    try:
        memory_value += float(display.get())
    except:
        pass

def m_minus():
    global memory_value
    try:
        memory_value -= float(display.get())
    except:
        pass

def ms():
    global memory_value
    try:
        memory_value = float(display.get())
    except:
        pass

# ---------- SCI FUNCTIONS ----------
def sci_trig(func):
    global expression

    if expression == "":
        return  # prevents empty error

    try:
        value = float(expression)

        if deg_mode:
            value = math.radians(value)

        result = func(value)

        expression = str(result)

        display.delete(0, tk.END)
        display.insert(tk.END, expression)

        update_live()

    except:
        display.delete(0, tk.END)
        display.insert(tk.END, "Error")
        expression = ""

def sci_factorial():
    try:
        val = int(float(display.get()))
        display.delete(0, tk.END)
        display.insert(tk.END, math.factorial(val))
    except:
        display.delete(0, tk.END)
        display.insert(tk.END, "Error")

def sci_square(): press("**2")
def sci_power(): press("**")
def sci_sqrt(): press("math.sqrt(")
def sci_log(): press("math.log10(")
def sci_ln(): press("math.log(")
def sci_exp(): press("math.exp(")
def sci_mod(): press("%")
def sci_pi(): press(str(math.pi))
def sci_e(): press(str(math.e))
def sci_rand(): press(str(random.random()))

# ---------- BUILD SCIENTIFIC ----------
def toggle_second():
    global second_mode
    second_mode = not second_mode


def animate_dropdown(window, target_height):
    width = window.winfo_width()
    x = window.winfo_x()
    y = window.winfo_y()

    current_height = 1
    step = 20

    def expand():
        nonlocal current_height
        if current_height < target_height:
            current_height += step
            window.geometry(f"{width}x{current_height}+{x}+{y}")
            window.after(8, expand)
        else:
            window.geometry(f"{width}x{target_height}+{x}+{y}")

    expand()

def open_trig_dropdown(btn):
    global active_dropdown

    if active_dropdown:
        close_dropdown()
        return

    x = btn.winfo_rootx()
    y = btn.winfo_rooty() + btn.winfo_height()

    dropdown = tk.Toplevel(root)
    dropdown.overrideredirect(True)
    dropdown.configure(bg="#1e1e1e")

    width = btn.winfo_width()
    dropdown.geometry(f"{width}x1+{x}+{y}")   # height = 1 (NOT 0)
    dropdown.update()  # force draw

    active_dropdown = dropdown

    options = [
        ("sin", lambda: sci_trig(math.sin)),
        ("cos", lambda: sci_trig(math.cos)),
        ("tan", lambda: sci_trig(math.tan)),
        ("sec", lambda: sci_trig(lambda x: 1/math.cos(x))),
        ("csc", lambda: sci_trig(lambda x: 1/math.sin(x))),
        ("cot", lambda: sci_trig(lambda x: 1/math.tan(x))),
    ]

    frame = tk.Frame(dropdown, bg="#1e1e1e")
    frame.pack(fill="both", expand=True)

    for text, cmd in options:
        tk.Button(
            frame,
            text=text,
            bg="#2a2a2a",
            fg="white",
            relief="flat",
            command=lambda f=cmd: (f(), close_dropdown())
        ).pack(fill="x", pady=1)

    animate_dropdown(dropdown, len(options)*32)


def open_function_dropdown(btn):
    global active_dropdown

    if active_dropdown:
        close_dropdown()
        return

    x = btn.winfo_rootx()
    y = btn.winfo_rooty() + btn.winfo_height()

    dropdown = tk.Toplevel(root)
    dropdown.overrideredirect(True)
    dropdown.configure(bg="#1e1e1e")

    width = btn.winfo_width()
    dropdown.geometry(f"{width}x1+{x}+{y}")  # height = 1
    dropdown.update()

    active_dropdown = dropdown

    options = [
        ("abs", lambda: apply_func("abs")),
        ("floor", lambda: apply_func("math.floor")),
        ("ceil", lambda: apply_func("math.ceil")),
        ("round", lambda: apply_func("round")),
        ("sinh", lambda: apply_func("math.sinh")),
        ("cosh", lambda: apply_func("math.cosh")),
    ]

    frame = tk.Frame(dropdown, bg="#1e1e1e")
    frame.pack(fill="both", expand=True)

    for text, cmd in options:
        tk.Button(
            frame,
            text=text,
            bg="#2a2a2a",
            fg="white",
            relief="flat",
            command=lambda f=cmd: (f(), close_dropdown())
        ).pack(fill="x", pady=1)

    animate_dropdown(dropdown, len(options)*32)


def build_scientific_buttons():
    clear_buttons()

    global deg_btn

    # ---------- ROW 0 : TRIG + FUNCTION ----------
    top_select = tk.Frame(btns, bg="#121212")
    top_select.grid(row=0, column=0, columnspan=6, sticky="ew", pady=(5, 5))

    trig_btn = tk.Button(
    top_select, text="Trigonometry ▾",
    bg="#B1CBFF", fg="black",
    width=18
)
    trig_btn.config(command=lambda: open_trig_dropdown(trig_btn))
    trig_btn.pack(side="left", padx=5)

    func_btn = tk.Button(
    top_select, text="Function ▾",
    bg="#B1CBFF", fg="black",
    width=18
)
    func_btn.config(command=lambda: open_function_dropdown(func_btn))
    func_btn.pack(side="left", padx=5)


    # ---------- MAIN SCIENTIFIC GRID ----------
    layout = [
        ("√",sci_sqrt),("e",sci_e),("rand",sci_rand),("exp",sci_exp),("mod",sci_mod),
        ("π",sci_pi),("(","("),(")",")"),("n!",sci_factorial),("÷","/"),
        ("x²",sci_square),("7","7"),("8","8"),("9","9"),("×","*"),
        ("xʸ",sci_power),("4","4"),("5","5"),("6","6"),("−","-"),
        ("log",sci_log),("1","1"),("2","2"),("3","3"),("+","+"),
        ("ln",sci_ln),("+/-","SIGN"),("0","0"),(".","."),("=","=")
    ]

    r = 1
    c = 0

    for t, v in layout:
        bg_color = "#1e1e1e"

        if t == "=":
            cmd = calculate
            bg_color = "#2962ff"
        elif v == "SIGN":
            cmd = toggle_sign
        elif v == "SECOND":
            cmd = toggle_second
        elif callable(v):
            cmd = v
        else:
            cmd = lambda x=v: press(x)

        tk.Button(
            btns, text=t,
            width=6, height=1,
            font=("Segoe UI", 13),
            bg=bg_color, fg="white",
            command=cmd
        ).grid(row=r, column=c, padx=4, pady=4)

        c += 1
        if c == 5:
            c = 0
            r += 1

def rebuild_standard_buttons():
    clear_buttons()
    build_memory_row(row_number=0)

    layout = [
        ("(","("), (")",")"), ("+/-", "SIGN"), ("÷", "/"),
        ("7","7"),("8","8"),("9","9"),("×","*"),
        ("4","4"),("5","5"),("6","6"),("−","-"),
        ("1","1"),("2","2"),("3","3"),("+","+"),
        ("%","%"),("0","0"),(".","."),("=","=")
    ]

    r = 1
    c = 0
    for t, v in layout:
        tk.Button(
            btns, text=t,
            width=6, height=1,
            font=("Segoe UI", 14),
            bg="#1e1e1e", fg="white",
            command=toggle_sign if v == "SIGN" else lambda x=v: press(x)
        ).grid(row=r, column=c, padx=6, pady=6)

        c += 1
        if c == 4:
            c = 0
            r += 1

    r = 1
    c = 0
    for t, v in layout:
    # Determine button command and color
        if v == "SIGN":
            cmd = toggle_sign
            bg_color = "#1e1e1e"
        elif v == "=":
            cmd = calculate
            bg_color = "#2962ff"  # blue color
        else:
            cmd = lambda x=v: press(x)
            bg_color = "#1e1e1e"

        tk.Button(
            btns, text=t,
            width=6, height=1,
            font=("Segoe UI", 14),
            bg=bg_color, fg="white",
            command=cmd
        ).grid(row=r, column=c, padx=6, pady=6)

        c += 1
        if c == 4:
            c = 0
            r += 1

# ================= PROGRAMMER MODE (ADVANCED) =================

programmer_base = "DEC"
word_modes = [64, 32, 16, 8]
word_labels = {64: "QWORD", 32: "DWORD", 16: "WORD", 8: "BYTE"}
word_index = 0
carry_flag = 0

def current_bits():
    return word_modes[word_index]

def mask_value(val):
    bits = current_bits()
    return val & ((1 << bits) - 1)

def cycle_word():
    global word_index
    word_index = (word_index + 1) % 4
    word_btn.config(text=word_labels[current_bits()])
    try:
        num = int(display.get(), get_base())
        update_programmer_display(num)
    except:
        pass

def get_base():
    return {"HEX":16,"DEC":10,"OCT":8,"BIN":2}[programmer_base]

def set_base(base):
    global programmer_base
    programmer_base = base
    update_button_states()

    try:
        num = int(display.get(), get_base())
        update_programmer_display(num)
    except:
        pass

def update_button_states():
    for key, btn in prog_digit_buttons.items():

        btn.config(state="normal")

        if programmer_base == "BIN":
            if key not in ["0", "1"]:
                btn.config(state="disabled")

        elif programmer_base == "OCT":
            if key not in [str(i) for i in range(8)]:
                btn.config(state="disabled")

        elif programmer_base == "DEC":
            if key not in [str(i) for i in range(10)]:
                btn.config(state="disabled")

        elif programmer_base == "HEX":
            if key not in [str(i) for i in range(10)] + list("ABCDEF"):
                btn.config(state="disabled")


def update_programmer_display(num):
    global expression
    num = mask_value(num)

    if programmer_base == "HEX":
        expression = format(num, "X")
    elif programmer_base == "DEC":
        expression = str(num)
    elif programmer_base == "OCT":
        expression = format(num, "o")
    elif programmer_base == "BIN":
        expression = format(num, "b")

    display.delete(0, tk.END)   
    display.insert(tk.END, expression)

    hex_label.config(text=format(num, "X"))
    dec_label.config(text=str(num))
    oct_label.config(text=format(num, "o"))
    bin_label.config(text=format(num, "b"))

def prog_press(val):
    global expression
    expression += str(val)
    display.delete(0, tk.END)
    display.insert(tk.END, expression)

def prog_clear():
    global expression
    expression = ""
    display.delete(0, tk.END)

# -------- BITWISE DROPDOWN --------
def open_bitwise_dropdown(btn):
    global active_dropdown

    if active_dropdown:
        active_dropdown.destroy()
        active_dropdown = None
        return

    x = btn.winfo_rootx()
    y = btn.winfo_rooty() + btn.winfo_height()

    dropdown = tk.Toplevel(root)
    dropdown.overrideredirect(True)
    dropdown.configure(bg="#1e1e1e")
    dropdown.geometry(f"180x150+{x}+{y}")

    active_dropdown = dropdown

    options = [
        ("AND", lambda: prog_press("&")),
        ("OR", lambda: prog_press("|")),
        ("XOR", lambda: prog_press("^")),
        ("NOT", prog_not),
    ]

    for text, cmd in options:
        tk.Button(
            dropdown,
            text=text,
            bg="#2a2a2a",
            fg="white",
            relief="flat",
            command=lambda c=cmd: (c(), close_dropdown())
        ).pack(fill="x", pady=2)


def prog_not():
    try:
        num = int(display.get(), get_base())
        update_programmer_display(~num)
    except:
        pass

# -------- BIT SHIFT DROPDOWN --------
def open_shift_dropdown(btn):
    global active_dropdown

    if active_dropdown:
        active_dropdown.destroy()
        active_dropdown = None
        return

    x = btn.winfo_rootx()
    y = btn.winfo_rooty() + btn.winfo_height()

    dropdown = tk.Toplevel(root)
    dropdown.overrideredirect(True)
    dropdown.configure(bg="#1e1e1e")
    dropdown.geometry(f"230x180+{x}+{y}")

    active_dropdown = dropdown

    options = [
        ("Arithmetic shift", arithmetic_shift),
        ("Logical shift", logical_shift),
        ("Rotate circular shift", rotate_shift),
        ("Rotate through carry", rotate_through_carry),
    ]

    for text, cmd in options:
        tk.Button(
            dropdown,
            text=text,
            bg="#2a2a2a",
            fg="white",
            relief="flat",
            command=lambda c=cmd: (c(), close_dropdown())
        ).pack(fill="x", pady=2)

active_dropdown = None

def arithmetic_shift():
    try:
        num = int(display.get(), get_base())
        update_programmer_display(num >> 1)
    except:
        pass

def logical_shift():
    try:
        num = int(display.get(), get_base())
        bits = current_bits()
        update_programmer_display((num % (1<<bits)) >> 1)
    except:
        pass

def rotate_shift():
    try:
        num = int(display.get(), get_base())
        bits = current_bits()
        result = ((num << 1) | (num >> (bits-1))) & ((1<<bits)-1)
        update_programmer_display(result)
    except:
        pass

def rotate_through_carry():
    global carry_flag
    try:
        num = int(display.get(), get_base())
        bits = current_bits()
        new_carry = (num >> (bits-1)) & 1
        result = ((num << 1) | carry_flag) & ((1<<bits)-1)
        carry_flag = new_carry
        update_programmer_display(result)
    except:
        pass

# -------- BUILD UI --------
def build_programmer_buttons():
    clear_buttons()

    global hex_label, dec_label, oct_label, bin_label, word_btn

    # Reset columns
    for i in range(10):
        btns.columnconfigure(i, weight=0)
    # Make columns expandable
    for i in range(5):
        btns.columnconfigure(i, weight=1)

    # BASE DISPLAY
    base_frame = tk.Frame(btns, bg="#121212")
    base_frame.grid(row=0, column=0, columnspan=5, sticky="nsew")


    tk.Button(base_frame,text="HEX",command=lambda:set_base("HEX")).grid(row=0,column=0,sticky="w")
    hex_label = tk.Label(base_frame,text="0",fg="white",bg="#121212")
    hex_label.grid(row=0,column=1)

    tk.Button(base_frame,text="DEC",command=lambda:set_base("DEC")).grid(row=1,column=0,sticky="w")
    dec_label = tk.Label(base_frame,text="0",fg="white",bg="#121212")
    dec_label.grid(row=1,column=1)

    tk.Button(base_frame,text="OCT",command=lambda:set_base("OCT")).grid(row=2,column=0,sticky="w")
    oct_label = tk.Label(base_frame,text="0",fg="white",bg="#121212")
    oct_label.grid(row=2,column=1)

    tk.Button(base_frame,text="BIN",command=lambda:set_base("BIN")).grid(row=3,column=0,sticky="w")
    bin_label = tk.Label(base_frame,text="0",fg="white",bg="#121212")
    bin_label.grid(row=3,column=1)

    # WORD + DROPDOWNS
    top_row = tk.Frame(btns, bg="#121212")
    top_row.grid(row=1, column=1, columnspan=5, pady=5, sticky="nsew")

    bitwise_btn = tk.Button(
    top_row,
    text="Bitwise ▾",
    bg="#B1CBFF",
    fg="black",
    command=lambda: open_bitwise_dropdown(bitwise_btn)
)
    bitwise_btn.pack(side="left", padx=5)

    bitshift_btn = tk.Button(
    top_row,
    text="Bit shift ▾",
    bg="#B1CBFF",
    fg="black",
    command=lambda: open_shift_dropdown(bitshift_btn)
)
    bitshift_btn.pack(side="left", padx=5)



    word_btn = tk.Button(top_row,text="QWORD",
                         bg="#B1CBFF",fg="black",
                         command=cycle_word)
    word_btn.pack(side="left", padx=5)

    # MAIN GRID
    layout = [
        ("A","A"),("<<","<<"),(">>",">>"),("x³","CUBE"),("2ˣ","POW2"),
        ("B","B"),("(","("), (")",")"),("%","%"),("÷", "/"),
        ("C","C"),("7","7"),("8","8"),("9","9"),("×","*"),
        ("D","D"),("4","4"),("5","5"),("6","6"),("−","-"),
        ("E","E"),("1","1"),("2","2"),("3","3"),("+","+"),
        ("F","F"),("+/-","SIGN"),("0","0"),(".","."),("=","=")
    ]

    r = 2
    c = 0

    for t, v in layout:
        bg_color = "#1e1e1e"

        if v == "CLR":
            cmd = prog_clear

        elif v == "BACK":
            cmd = backspace

        elif v == "=":
            cmd = prog_calculate
            bg_color = "#2962ff"

        elif v == "SIGN":
            cmd = toggle_sign

        elif v == "CUBE":
            cmd = prog_cube

        elif v == "POW2":
            cmd = prog_power_two

        elif v in ["&","|","^","<<",">>"]:
            cmd = lambda x=v: prog_press(x)

        else:
            cmd = lambda x=v: prog_press(x)

        btn = tk.Button(
            btns,
            text=t,
            bg=bg_color,
            fg="white",
            command=cmd
        )

        btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

        # store only digit/hex buttons
        if t in list("0123456789ABCDEF"):
            prog_digit_buttons[t] = btn

        c += 1
        if c == 5:
            c = 0
            r += 1

    update_button_states()

def prog_cube():
    try:
        num = int(display.get(), get_base())
        result = num ** 3
        update_programmer_display(result)
    except:
        pass


def prog_power_two():
    try:
        num = int(display.get(), get_base())
        result = 2 ** num
        update_programmer_display(result)
    except:
        pass

def prog_calculate():
    global expression
    try:
        expr = display.get()

        # Replace visual symbols with Python operators
        expr = expr.replace("÷", "/")
        expr = expr.replace("×", "*")
        expr = expr.replace("−", "-")

        result = eval(expr, {"__builtins__": None}, {})

        update_programmer_display(result)
        expression = display.get()

    except Exception as e:
        display.delete(0, tk.END)
        display.insert(tk.END, "Error")


def open_calendar(parent, is_from=True):
    global selecting_from, current_year, current_month
    selecting_from = is_from

    cal = tk.Toplevel(root)
    cal.configure(bg="#1e1e1e")
    cal.geometry("320x380")
    cal.title("Select Date")

    # ----- Top bar -----
    top_bar = tk.Frame(cal, bg="#2a2a2a")
    top_bar.pack(fill="x")

    year_btn = tk.Button(top_bar,
                     text=str(current_year),
                     bg="#2a2a2a",
                     fg="white",
                     bd=0)
    year_btn.pack(side="left", padx=10)

# THIS IS THE LINE YOU ADD/CHANGE:
    year_btn.config(command=lambda: open_year_view(year_btn, parent))


    month_btn = tk.Button(top_bar,
                          text=calendar.month_name[current_month],
                          bg="#2a2a2a",
                          fg="white",
                          bd=0,
                          command=lambda: show_months(cal, parent))
    month_btn.pack(side="left")

    tk.Button(top_bar, text="▲", bg="#2a2a2a", fg="white", bd=0,
              command=lambda: change_month(-1, cal, parent)).pack(side="right", padx=5)
    tk.Button(top_bar, text="▼", bg="#2a2a2a", fg="white", bd=0,
              command=lambda: change_month(1, cal, parent)).pack(side="right")

    # ----- Day grid -----
    show_days(cal, parent)

def show_days(cal, parent):
    # Remove previous content
    for w in cal.winfo_children():
        if isinstance(w, tk.Frame) and w != cal.winfo_children()[0]:
            w.destroy()

    grid = tk.Frame(cal, bg="#1e1e1e")
    grid.pack()

    days = ["Mo","Tu","We","Th","Fr","Sa","Su"]
    for i, d in enumerate(days):
        tk.Label(grid, text=d, bg="#1e1e1e", fg="white").grid(row=0,column=i,padx=5,pady=5)

    month_days = calendar.monthcalendar(current_year, current_month)
    for r, week in enumerate(month_days):
        for c, day in enumerate(week):
            if day != 0:
                tk.Button(grid, text=str(day), width=3, bg="#2a2a2a", fg="white",
                          relief="flat",
                          command=lambda d=day: select_date(d, cal, parent)).grid(row=r+1,column=c,padx=4,pady=4)

def show_years(cal, parent):
    # Remove previous day grid
    for w in cal.winfo_children():
        if isinstance(w, tk.Frame) and w != cal.winfo_children()[0]:
            w.destroy()

    frame = tk.Frame(cal, bg="#1e1e1e")
    frame.pack(expand=True, fill="both", padx=10, pady=10)

    start_year = current_year - 6
    rows, cols = 4, 3
    for i in range(rows*cols):
        y = start_year + i
        tk.Button(frame, text=str(y), width=8, bg="#2a2a2a", fg="white", relief="flat",
                  command=lambda year=y: select_year(year, cal, parent)).grid(row=i//cols, column=i%cols, padx=5, pady=5)

def show_months(cal, parent):
    for w in cal.winfo_children():
        if isinstance(w, tk.Frame) and w != cal.winfo_children()[0]:
            w.destroy()

    frame = tk.Frame(cal, bg="#1e1e1e")
    frame.pack(expand=True, fill="both", padx=10, pady=10)

    months = list(calendar.month_name)[1:]
    r = c = 0
    for i, m in enumerate(months):
        tk.Button(frame, text=m, width=8, bg="#2a2a2a", fg="white",
                  relief="flat",
                  command=lambda month=i+1: select_month(month, cal, parent)
                  ).grid(row=r, column=c, padx=5, pady=5)
        c += 1
        if c == 3:
            c = 0
            r += 1



def change_month(direction, window, parent):
    global current_month, current_year, prevent_dropdown_open

    prevent_dropdown_open = True
    close_dropdown()

    current_month += direction

    if current_month < 1:
        current_month = 12
        current_year -= 1
    elif current_month > 12:
        current_month = 1
        current_year += 1

    window.destroy()
    open_calendar(parent, selecting_from)
    root.after(200, reset_dropdown_flag)

def open_month_view(window, parent):
    window.destroy()

    cal = tk.Toplevel(root)
    cal.configure(bg="#1e1e1e")
    cal.geometry("320x350")

    frame = tk.Frame(cal, bg="#1e1e1e")
    frame.pack(pady=20)

    months = list(calendar.month_abbr)[1:]

    r = c = 0
    for i, m in enumerate(months):
        tk.Button(frame,
                  text=m,
                  width=6,
                  bg="#2a2a2a",
                  fg="white",
                  command=lambda x=i+1: select_month(x, cal, parent)
                  ).grid(row=r, column=c, padx=10, pady=10)

        c += 1
        if c == 4:
            c = 0
            r += 1

def select_month(month, window, parent):
    global current_month, prevent_dropdown_open
    prevent_dropdown_open = True
    close_dropdown()
    current_month = month
    window.destroy()
    open_calendar(parent, selecting_from)
    root.after(200, reset_dropdown_flag)

def open_year_view(window, parent):
    window.destroy()

    cal = tk.Toplevel(root)
    cal.configure(bg="#1e1e1e")
    cal.geometry("320x300")  # FIXED HEIGHT smaller than content

    # ===== SCROLLABLE CANVAS =====
    canvas = tk.Canvas(cal, bg="#1e1e1e", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(cal, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas, bg="#1e1e1e")
    canvas.create_window((0,0), window=frame, anchor="nw")

    # ===== ADD YEAR BUTTONS =====
    start = 1900
    r = c = 0
    for i in range(start, 2101):
        tk.Button(frame,
                  text=str(i),
                  width=6,
                  bg="#2a2a2a",
                  fg="white",
                  command=lambda x=i: select_year(x, cal, parent)
                  ).grid(row=r, column=c, padx=10, pady=5)
        c += 1
        if c == 4:
            c = 0
            r += 1

    # ===== UPDATE SCROLL REGION =====
    frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    # ===== MOUSE WHEEL SCROLL =====
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)


def select_year(year, window, parent):
    global current_year
    current_year = year
    # Simply reopen the main calendar view
    window.destroy()
    open_calendar(parent, selecting_from)


def select_date(day, window, parent):
    global from_date, to_date, selecting_from

    selected = datetime(current_year, current_month, day)

    if selecting_from:
        from_date = selected
        parent.from_display.config(text=selected.strftime("%d %B %Y"))
    else:
        to_date = selected
        parent.to_display.config(text=selected.strftime("%d %B %Y"))

    window.destroy()

def open_year_dropdown(btn, parent):
    global active_dropdown, prevent_dropdown_open

    if prevent_dropdown_open:
        return

    # Close any existing dropdown
    if active_dropdown:
        active_dropdown.destroy()
        active_dropdown = None
        return

    x = btn.winfo_rootx()
    y = btn.winfo_rooty() + btn.winfo_height()  # OPEN BELOW BUTTON
    width = btn.winfo_width()
    height = 300  # visible height

    dropdown = tk.Toplevel(root)
    dropdown.overrideredirect(True)
    dropdown.configure(bg="#1e1e1e")
    dropdown.geometry(f"{width}x{height}+{x}+{y}")

    active_dropdown = dropdown

    # Canvas + Scrollbar
    canvas = tk.Canvas(dropdown, bg="#1e1e1e", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(dropdown, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas, bg="#1e1e1e")
    canvas.create_window((0,0), window=frame, anchor="nw")

    # Add year buttons
    for i, y in enumerate(range(1600, 2501)):
        tk.Button(
            frame,
            text=str(y),
            width=8,
            bg="#2a2a2a",
            fg="white",
            relief="flat",
            command=lambda year=y: select_year(year, dropdown, parent)
        ).grid(row=i, column=0, sticky="ew", padx=2, pady=1)

    frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    # Mouse wheel scroll
    def _on_mousewheel(event):
        nav_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# ================= CURRENCY DATA LOADER =================

def load_currency_data():
    global currency_rates, currency_display_list, currency_map

    currency_display_list.clear()
    currency_map.clear()

    try:
        response = requests.get("https://open.er-api.com/v6/latest/USD")
        data = response.json()
        currency_rates = data["rates"]
    except:
        print("No internet")
        return

    for code in currency_rates.keys():

        currency = pycountry.currencies.get(alpha_3=code)

        if currency:
            currency_name = currency.name

            # Try to get country by currency numeric code
            country_name = ""

            for country in pycountry.countries:
                if hasattr(country, "numeric"):
                    if currency.numeric == country.numeric:
                        country_name = country.name
                        break

            # If not found, fallback
            if not country_name:
                country_name = currency_name.split()[0]

            display_text = f"{country_name}  -  {currency_name}"

            currency_display_list.append(display_text)
            currency_map[display_text] = code

    currency_display_list.sort()


def build_date_calculation():
    clear_buttons()
    title_label.config(text="Date calculation")

    container = tk.Frame(btns, bg="#121212")
    container.grid(row=0, column=0, columnspan=6, sticky="nsew", pady=10)

    option_var = tk.StringVar(value="Difference between dates")

    option_menu = tk.OptionMenu(
        container,
        option_var,
        "Difference between dates",
        "Add or subtract days"
    )
    option_menu.config(bg="#1e1e1e", fg="white", width=25)
    option_menu.pack(anchor="w", pady=10)

    content = tk.Frame(container, bg="#121212")
    content.pack(fill="both", expand=True)

    def refresh(*args):
        for w in content.winfo_children():
            w.destroy()

        if option_var.get() == "Difference between dates":
            build_difference_ui(content)
        else:
            build_add_subtract_ui(content)

    option_var.trace_add("write", lambda *args: refresh())
    refresh()

def build_difference_ui(parent):
    global from_date, to_date

    tk.Label(parent, text="From",
         bg="#121212", fg="white").pack(anchor="w", pady=(10,0))

    from_frame = tk.Frame(parent, bg="#1e1e1e")
    from_frame.pack(fill="x", pady=5)

    from_display = tk.Label(from_frame,
                            text="Select start date",
                            bg="#1e1e1e",
                            fg="white",
                            anchor="w",
                            padx=10)
    from_display.pack(side="left", fill="x", expand=True)

    from_icon = tk.Button(from_frame,
                          text="📅",
                          bg="#1e1e1e",
                          fg="white",
                          bd=0,
                          command=lambda: open_calendar(parent, True))
    from_icon.pack(side="right", padx=5)


    tk.Label(parent, text="To",
         bg="#121212", fg="white").pack(anchor="w", pady=(10,0))

    to_frame = tk.Frame(parent, bg="#1e1e1e")
    to_frame.pack(fill="x", pady=5)

    to_display = tk.Label(to_frame,
                          text="Select end date",
                          bg="#1e1e1e",
                          fg="white",
                          anchor="w",
                          padx=10)
    to_display.pack(side="left", fill="x", expand=True)

    to_icon = tk.Button(to_frame,
                        text="📅",
                        bg="#1e1e1e",
                        fg="white",
                        bd=0,
                        command=lambda: open_calendar(parent, False))
    to_icon.pack(side="right", padx=5)

    parent.from_display = from_display
    parent.to_display = to_display


    # store references
    parent.from_display = from_display
    parent.to_display = to_display

    result_label = tk.Label(parent,
                            bg="#121212",
                            fg="white",
                            font=("Segoe UI",12))
    result_label.pack(pady=15)

    def calculate_difference():
        if not from_date or not to_date:
            result_label.config(text="Select both dates")
            return

        delta = relativedelta(to_date, from_date)

        result_label.config(
            text=f"{abs(delta.years)} Years  "
                 f"{abs(delta.months)} Months  "
                 f"{abs(delta.days)} Days"
        )

    tk.Button(parent,
              text="Calculate",
              bg="#2962ff",
              fg="white",
              command=calculate_difference
              ).pack(pady=5)

def build_add_subtract_ui(parent):

    tk.Label(parent, text="From",
         bg="#121212", fg="white").pack(anchor="w", pady=(10,0))

    from_frame = tk.Frame(parent, bg="#121212")
    from_frame.pack(fill="x", pady=5)

    from_display = tk.Label(from_frame,
                            text="Select start date",
                            bg="#1e1e1e",
                            fg="white",
                            anchor="w",
                            padx=10)
    from_display.pack(side="left", fill="x", expand=True)

    from_icon = tk.Button(from_frame,
                          text="📅",
                          bg="#1e1e1e",
                          fg="white",
                          bd=0,
                          command=lambda: open_calendar(parent, True))
    from_icon.pack(side="right", padx=5)

    parent.from_display = from_display

    mode_var = tk.StringVar(value="Add")

    radio_frame = tk.Frame(parent, bg="#121212")
    radio_frame.pack(pady=10)
    dropdown_row = tk.Frame(parent, bg="#121212")
    dropdown_row.pack(fill="x", pady=10)

    year_var = tk.IntVar(value=0)
    month_var = tk.IntVar(value=0)
    day_var = tk.IntVar(value=0)

    year_btn = tk.Button(
        dropdown_row,
        text="0 ▼",
        bg="#2a2a2a",
        fg="white",
        bd=0,
        command=lambda: toggle_dropdown(parent, year_var, year_btn)
)
    year_btn.grid(row=0, column=0, padx=5, sticky="ew")

    month_btn = tk.Button(
        dropdown_row,
        text="0 ▼",
        bg="#2a2a2a",
        fg="white",
        bd=0,
        command=lambda: toggle_dropdown(parent, month_var, month_btn)
)
    month_btn.grid(row=0, column=1, padx=5, sticky="ew")

    day_btn = tk.Button(
        dropdown_row,
        text="0 ▼",
        bg="#2a2a2a",
        fg="white",
        bd=0,
        command=lambda: toggle_dropdown(parent, day_var, day_btn)
)
    day_btn.grid(row=0, column=2, padx=5, sticky="ew")

    tk.Radiobutton(radio_frame,
                   text="Add",
                   variable=mode_var,
                   value="Add",
                   bg="#121212",
                   fg="white",
                   selectcolor="#1e1e1e").pack(side="left", padx=10)

    tk.Radiobutton(radio_frame,
                   text="Subtract",
                   variable=mode_var,
                   value="Subtract",
                   bg="#121212",
                   fg="white",
                   selectcolor="#1e1e1e").pack(side="left", padx=10)

    # VARIABLES
    years_var = tk.IntVar(value=0)
    months_var = tk.IntVar(value=0)
    days_var = tk.IntVar(value=0)

# YEARS BUTTON
    years_btn = tk.Button(dropdown_row,
                      text="Years: 0",
                      bg="#1e1e1e",
                      fg="white",
                      relief="flat",
                      command=lambda: toggle_dropdown(parent, years_var, years_btn))
    years_btn.grid(row=0, column=0, padx=5, sticky="ew")

# MONTHS BUTTON
    months_btn = tk.Button(dropdown_row,
                       text="Months: 0",
                       bg="#1e1e1e",
                       fg="white",
                       relief="flat",
                       command=lambda: toggle_dropdown(parent, months_var, months_btn))
    months_btn.grid(row=0, column=1, padx=5, sticky="ew")

# DAYS BUTTON
    days_btn = tk.Button(dropdown_row,
                     text="Days: 0",
                     bg="#1e1e1e",
                     fg="white",
                     relief="flat",
                     command=lambda: toggle_dropdown(parent, days_var, days_btn))
    days_btn.grid(row=0, column=2, padx=5, sticky="ew")

    dropdown_row.columnconfigure(0, weight=1)
    dropdown_row.columnconfigure(1, weight=1)
    dropdown_row.columnconfigure(2, weight=1)

    result_label = tk.Label(parent,
                            bg="#121212",
                            fg="white",
                            font=("Segoe UI",12))
    result_label.pack(pady=15)

    def update_labels(*args):
        years_btn.config(text=f"Years: {years_var.get()}")
        months_btn.config(text=f"Months: {months_var.get()}")
        days_btn.config(text=f"Days: {days_var.get()}")

    years_var.trace_add("write", update_labels)
    months_var.trace_add("write", update_labels)
    days_var.trace_add("write", update_labels)

    def calculate_new_date():
        try:
            base = datetime.strptime(parent.from_display["text"], "%d %B %Y")

            y = years_var.get()
            m = months_var.get()
            d = days_var.get()

            delta = relativedelta(years=y, months=m, days=d)

            if mode_var.get() == "Add":
                new_date = base + delta
            else:
                new_date = base - delta

            result_label.config(text=new_date.strftime("%d %B %Y"))

        except:
            result_label.config(text="Invalid input")

    tk.Button(parent,
              text="Calculate",
              bg="#2962ff",
              fg="white",
              command=calculate_new_date
              ).pack(pady=5)

open_dropdown = None

def reset_dropdown_flag():
    global prevent_dropdown_open
    prevent_dropdown_open = False

def close_dropdown():
    global open_dropdown, open_button, active_dropdown

    # ----- Close Date dropdown -----
    if open_dropdown:
        dropdown = open_dropdown
        width = dropdown.winfo_width()
        x = dropdown.winfo_x()
        y = dropdown.winfo_y()

        current_height = dropdown.winfo_height()
        step = 20

        def animate_close():
            nonlocal current_height
            if current_height > 0:
                current_height -= step
                dropdown.geometry(f"{width}x{current_height}+{x}+{y}")
                dropdown.after(8, animate_close)
            else:
                dropdown.destroy()

        animate_close()

        if open_button:
            text = open_button["text"].replace(" ▲", "")
            open_button.config(text=text + " ▼")

        open_dropdown = None
        open_button = None

    # ----- Close Scientific / Programmer dropdown -----
    if active_dropdown:
        active_dropdown.destroy()
        active_dropdown = None
        return

def toggle_dropdown(parent, var, btn):
    global active_dropdown, prevent_dropdown_open, active_dropdown_button

    if prevent_dropdown_open:
        return

    # If dropdown already open for this button, close it
    if active_dropdown and active_dropdown_button == btn:
        active_dropdown.destroy()
        active_dropdown = None
        active_dropdown_button = None
        return

    # Close any other dropdown first
    if active_dropdown:
        active_dropdown.destroy()
        active_dropdown = None

    x = btn.winfo_rootx()
    y = btn.winfo_rooty() + btn.winfo_height()

    dropdown = tk.Toplevel(root)
    dropdown.overrideredirect(True)
    dropdown.configure(bg="#1e1e1e")

    width = btn.winfo_width()
    height = 150  # visible dropdown height
    dropdown.geometry(f"{width}x{height}+{x}+{y}")

    active_dropdown = dropdown
    active_dropdown_button = btn  # track which button opened this dropdown

    # ====== Scrollable frame setup ======
    container = tk.Frame(dropdown, bg="#1e1e1e")
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg="#1e1e1e", highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    frame = tk.Frame(canvas, bg="#1e1e1e")
    canvas.create_window((0, 0), window=frame, anchor="nw")

    def on_frame_config(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
    frame.bind("<Configure>", on_frame_config)

    def _on_mousewheel(event):
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")
    frame.bind_all("<MouseWheel>", _on_mousewheel)

    # ====== Determine dropdown values ======
    text = btn.cget("text").lower()
    if "year" in text:
        values = list(range(0, 1000))
    elif "month" in text:
        values = list(range(0, 1000))
    elif "day" in text:
        values = list(range(0, 1000))
    else:
        values = list(range(0, 1000))

    # Add buttons
    def select_val(v):
        var.set(v)
        btn.config(text=f"{v} ▼")
        dropdown.destroy()
        global active_dropdown, active_dropdown_button
        active_dropdown = None
        active_dropdown_button = None

    for val in values:
        tk.Button(
            frame,
            text=str(val),
            bg="#2a2a2a",
            fg="white",
            relief="flat",
            command=lambda v=val: select_val(v)
        ).pack(fill="x", pady=1)


def select_dropdown_value(value, var, btn):
    global active_dropdown, open_button
    var.set(value)
    # Keep the arrow ▼
    btn.config(text=f"{btn['text'].split(':')[0]}: {value} ▼")
    if active_dropdown:
        active_dropdown.destroy()
        active_dropdown = None
        open_button = None


def reset_dropdown_flag():
    global prevent_dropdown_open
    prevent_dropdown_open = False

# ================= CURRENCY MODE =================

def load_currencies():
    global currency_rates, currency_display_list, currency_map

    # Get live exchange rates
    url = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(url)
    data = response.json()

    currency_rates = data["rates"]

    currency_display_list.clear()
    currency_map.clear()

    for code in currency_rates.keys():
        currency = pycountry.currencies.get(alpha_3=code)
        if currency:
            currency_name = currency.name

            # Try to find country using this currency
            country_name = ""
            for country in pycountry.countries:
                if hasattr(country, "alpha_2"):
                    country_name = country.name
                    break

            display_text = f"{country_name}  -  {currency_name}"

            currency_display_list.append(display_text)
            currency_map[display_text] = code

    currency_display_list.sort()


class DarkDropdown:
    def __init__(self, parent, variable, options, width=30):
        self.parent = parent
        self.variable = variable
        self.options = options
        self.popup = None

        self.button = tk.Button(
            parent,
            textvariable=self.variable,
            bg="#B1CBFF",
            fg="black",
            activebackground="#2962ff",
            activeforeground="white",
            relief="flat",
            height=1,          # 👈 force small height
            padx=5,            # 👈 reduce horizontal padding
            pady=2,            # 👈 reduce vertical padding
            anchor="w",
            font=("Segoe UI", 9),   # 👈 slightly smaller font
            command=self.toggle_dropdown
)
        self.button.pack(pady=2)   # 👈 smaller spacing


    def toggle_dropdown(self):
        global active_dropdown

        # If same dropdown is already open → close it
        if active_dropdown == self:
            self.close_dropdown()
            return

        # Close any other dropdown
        if active_dropdown:
            active_dropdown.close_dropdown()

        active_dropdown = self

        self.popup = tk.Toplevel(self.parent)
        self.popup.overrideredirect(True)
        self.popup.configure(bg="#1e1e1e")

        x = self.button.winfo_rootx()
        y = self.button.winfo_rooty() + self.button.winfo_height()
        # Calculate required width based on longest option
        longest = max(self.options, key=len)
        font = ("Segoe UI", 10)

        temp = tk.Label(self.popup, text=longest, font=font)
        temp.update_idletasks()
        required_width = temp.winfo_reqwidth() + 40  # padding
        temp.destroy()

        popup_width = max(self.button.winfo_width(), required_width)

        self.popup.geometry(f"{popup_width}x200+{x}+{y}")


        frame = tk.Frame(self.popup, bg="#1e1e1e")
        frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            frame,
            bg="#1e1e1e",
            fg="white",
            selectbackground="#2962ff",
            selectforeground="white",
            highlightthickness=0,
            relief="flat",
            yscrollcommand=scrollbar.set,
            font=("Segoe UI", 10),
            activestyle="none"
)

        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.listbox.yview)

        for item in self.options:
            self.listbox.insert("end", item)

        self.listbox.bind("<<ListboxSelect>>", self.select_item)
        self.listbox.bind("<MouseWheel>", self.on_mousewheel)
        self.listbox.bind("<Button-4>", self.on_mousewheel)
        self.listbox.bind("<Button-5>", self.on_mousewheel)

        # 🔥 CLICK ANYWHERE TO CLOSE
        self.parent.bind_all("<Button-1>", self.handle_click_outside)

    def handle_click_outside(self, event):
        if not self.popup:
            return

        widget = event.widget

        # If clicked button or inside popup → ignore
        if widget == self.button or str(widget).startswith(str(self.popup)):
            return

        self.close_dropdown()

    def on_mousewheel(self, event):
        if event.num == 4:
            self.listbox.yview_scroll(-1, "units")
        elif event.num == 5:
            self.listbox.yview_scroll(1, "units")
        else:
            self.listbox.yview_scroll(int(-1*(event.delta/120)), "units")

    def select_item(self, event):
        selection = self.listbox.get(self.listbox.curselection())
        self.variable.set(selection)
        self.close_dropdown()

    def close_dropdown(self):
        global active_dropdown

        if self.popup:
            self.popup.destroy()
            self.popup = None

        self.parent.unbind_all("<Button-1>")
        active_dropdown = None

def reset_main_layout(top_weight=3, keypad_weight=2):
    # Clear all previous row weights
    for i in range(10):
        btns.rowconfigure(i, weight=0)

    for i in range(6):
        btns.columnconfigure(i, weight=1)

    btns.rowconfigure(0, weight=top_weight)
    btns.rowconfigure(1, weight=keypad_weight)


def build_currency_ui():
    clear_buttons()
    title_label.config(text="Currency")

    container = tk.Frame(btns, bg="#121212")
    container.grid(row=0, column=0, columnspan=6, sticky="nsew", pady=5)

    load_currency_data()

    if not currency_display_list:
        tk.Label(container, text="No internet connection",
                 bg="#121212", fg="white").pack()
        return

    # Default selections
    default_from = None
    default_to = None

    for display_text, code in currency_map.items():
        if code == "USD":
            default_from = display_text
        if code == "INR":
            default_to = display_text

# Fallback if not found
    if not default_from:
        default_from = currency_display_list[0]

    if not default_to:
        default_to = currency_display_list[1]

    from_var = tk.StringVar(value=default_from)
    to_var = tk.StringVar(value=default_to)

    amount_var = tk.StringVar(value="0")

    # ================= TOP AMOUNT =================
    amount_label = tk.Label(container,
                            textvariable=amount_var,
                            font=("Segoe UI", 32),
                            bg="#121212",
                            fg="white",
                            anchor="e")
    amount_label.pack(fill="x", padx=15, pady=(5,0))

    # FROM DROPDOWN
    DarkDropdown(container, from_var, currency_display_list)

    # ================= RESULT =================
    result_var = tk.StringVar(value="0")
    result_label = tk.Label(container,
                            textvariable=result_var,
                            font=("Segoe UI", 32),
                            bg="#121212",
                            fg="#cccccc",
                            anchor="e")
    result_label.pack(fill="x", padx=15, pady=(5,0))

    # TO DROPDOWN
    DarkDropdown(container, to_var, currency_display_list)

    # ================= RATE INFO =================
    rate_label = tk.Label(container,
                          text="",
                          font=("Segoe UI", 10),
                          bg="#121212",
                          fg="#888888",
                          anchor="w")
    rate_label.pack(fill="x", padx=15, pady=(5,0))

    updated_label = tk.Label(container,
                             text="",
                             font=("Segoe UI", 9),
                             bg="#121212",
                             fg="#666666",
                             anchor="w")
    updated_label.pack(fill="x", padx=15)

    # ================= CONVERT FUNCTION =================
    def convert(*args):
        try:
            amount = float(amount_var.get())

            from_code = currency_map[from_var.get()]
            to_code = currency_map[to_var.get()]

            usd_amount = amount / currency_rates[from_code]
            result = usd_amount * currency_rates[to_code]

            result_var.set(f"{result:.4f}")

            rate_value = currency_rates[to_code] / currency_rates[from_code]
            rate_label.config(text=f"1 {from_code} = {rate_value:.5f} {to_code}")

            from datetime import datetime
            updated_label.config(
                text="Updated " + datetime.now().strftime("%d-%m-%Y %H:%M")
            )

        except:
            result_var.set("")
            rate_label.config(text="")

    amount_var.trace_add("write", convert)
    from_var.trace_add("write", convert)
    to_var.trace_add("write", convert)

    # ================= UPDATE BUTTON =================
    tk.Button(container,
              text="Update rates",
              bg="#121212",
              fg="#4fc3f7",
              bd=0,
              command=lambda: [load_currency_data(), convert()]
              ).pack(anchor="w", padx=15, pady=5)


# ================= WINDOWS STYLE KEYPAD =================

    keypad_frame = tk.Frame(btns, bg="#121212")
    btns.rowconfigure(6, weight=1)
    btns.columnconfigure(0, weight=1)
    keypad_frame.grid(row=6, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)

# Make columns expand equally
    for i in range(3):
        keypad_frame.columnconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, minsize=30)  # Increase this value


    def press(val):
        if val == "CE":
            amount_var.set("0")

        elif val == "⌫":
            current = amount_var.get()
            amount_var.set(current[:-1] if len(current) > 1 else "0")

        else:
            if amount_var.get() == "0":
                amount_var.set(val)
            else:
                amount_var.set(amount_var.get() + val)


# ---- Row 0 (CE and Backspace) ----
    tk.Button(keypad_frame,
              text="CE",
              bg="#b00020",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("CE")
              ).grid(row=0, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

    tk.Button(keypad_frame,
              text="⌫",
              bg="#1ab4f6",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("⌫")
              ).grid(row=0, column=2, sticky="nsew", padx=3, pady=3)


# ---- Number Rows ----
    numbers = [
        ["7","8","9"],
        ["4","5","6"],
        ["1","2","3"]
]

    for r, row in enumerate(numbers):
        for c, num in enumerate(row):
            tk.Button(keypad_frame,
                      text=num,
                      bg="#1e1e1e",
                      fg="white",
                      font=("Segoe UI", 14),
                      relief="flat",
                      command=lambda n=num: press(n)
                      ).grid(row=r+1, column=c, sticky="nsew", padx=3, pady=3)


# ---- Last Row (0 wide + dot) ----
    tk.Button(keypad_frame,
              text="0",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press("0")
              ).grid(row=4, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)

    tk.Button(keypad_frame,
              text=".",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press(".")
              ).grid(row=4, column=2, sticky="nsew", padx=3, pady=3)


def build_volume_ui():
    clear_buttons()
    title_label.config(text="Volume")

    # Ensure full grid layout is active

    for i in range(6):
        btns.columnconfigure(i, weight=1)

    container = tk.Frame(btns, bg="#121212")
    container.grid(row=0, column=0, columnspan=6, sticky="nsew", pady=5)

    from_var = tk.StringVar(value="Litres")
    to_var = tk.StringVar(value="Millilitres")
    amount_var = tk.StringVar(value="0")
    result_var = tk.StringVar(value="0")

    # ================= TOP AMOUNT =================
    amount_label = tk.Label(
        container,
        textvariable=amount_var,
        font=("Segoe UI", 28),
        bg="#121212",
        fg="white",
        anchor="e"
    )
    amount_label.pack(fill="x", padx=15, pady=(5,0))

    DarkDropdown(container, from_var, list(volume_units.keys()))

    # ================= SWAP BUTTON =================
    swap_btn = tk.Button(
        container,
        text="⇅",
        bg="#CCFFBE",
        fg="black",
        relief="flat",
        font=("Segoe UI", 12),
        command=lambda: swap_units()
    )
    swap_btn.pack(pady=2)

    # ================= RESULT =================
    result_label = tk.Label(
        container,
        textvariable=result_var,
        font=("Segoe UI", 28),
        bg="#121212",
        fg="#cccccc",
        anchor="e"
    )
    result_label.pack(fill="x", padx=15, pady=(5,0))

    DarkDropdown(container, to_var, list(volume_units.keys()))

    # ================= ABOUT EQUAL =================
    equal_label = tk.Label(
        container,
        text="",
        font=("Segoe UI", 10),
        bg="#121212",
        fg="#888888",
        anchor="w"
    )
    equal_label.pack(fill="x", padx=15, pady=(5,5))

    # ================= CONVERT FUNCTION =================
    def convert(*args):
        try:
            value = float(amount_var.get())

            base = value / volume_units[from_var.get()]
            result = base * volume_units[to_var.get()]

            # Smart formatting
            if result > 100000:
                formatted = f"{result:,.2f}"
            else:
                formatted = f"{result:.4f}".rstrip("0").rstrip(".")

            result_var.set(formatted)

            equal_label.config(
                text=f"About equal to {formatted} {to_var.get()}"
            )

        except:
            result_var.set("")
            equal_label.config(text="")

    # ================= SWAP FUNCTION =================
    def swap_units():
        from_unit = from_var.get()
        to_unit = to_var.get()
        from_var.set(to_unit)
        to_var.set(from_unit)
        convert()

    amount_var.trace_add("write", convert)
    from_var.trace_add("write", convert)
    to_var.trace_add("write", convert)

# ================= WINDOWS STYLE KEYPAD =================

    keypad_frame = tk.Frame(btns, bg="#121212")
    btns.rowconfigure(6, weight=1)
    btns.columnconfigure(0, weight=1)
    keypad_frame.grid(row=6, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)

# Make columns expand equally
    for i in range(3):
        keypad_frame.columnconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, minsize=30)  # Increase this value


    def press(val):
        if val == "CE":
            amount_var.set("0")

        elif val == "⌫":
            current = amount_var.get()
            amount_var.set(current[:-1] if len(current) > 1 else "0")

        else:
            if amount_var.get() == "0":
                amount_var.set(val)
            else:
                amount_var.set(amount_var.get() + val)


# ---- Row 0 (CE and Backspace) ----
    tk.Button(keypad_frame,
              text="CE",
              bg="#b00020",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("CE")
              ).grid(row=0, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

    tk.Button(keypad_frame,
              text="⌫",
              bg="#1ab4f6",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("⌫")
              ).grid(row=0, column=2, sticky="nsew", padx=3, pady=3)


# ---- Number Rows ----
    numbers = [
        ["7","8","9"],
        ["4","5","6"],
        ["1","2","3"]
]

    for r, row in enumerate(numbers):
        for c, num in enumerate(row):
            tk.Button(keypad_frame,
                      text=num,
                      bg="#1e1e1e",
                      fg="white",
                      font=("Segoe UI", 14),
                      relief="flat",
                      command=lambda n=num: press(n)
                      ).grid(row=r+1, column=c, sticky="nsew", padx=3, pady=3)


# ---- Last Row (0 wide + dot) ----
    tk.Button(keypad_frame,
              text="0",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press("0")
              ).grid(row=4, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)

    tk.Button(keypad_frame,
              text=".",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press(".")
              ).grid(row=4, column=2, sticky="nsew", padx=3, pady=3)


def build_length_ui():
    clear_buttons()
    title_label.config(text="Length")

    # Activate full grid layout
    for i in range(6):
        btns.columnconfigure(i, weight=1)

    container = tk.Frame(btns, bg="#121212")
    container.grid(row=0, column=0, columnspan=6, sticky="nsew", pady=5)

    from_var = tk.StringVar(value="Inches")
    to_var = tk.StringVar(value="Centimetres")
    amount_var = tk.StringVar(value="0")
    result_var = tk.StringVar(value="0")

    # ================= TOP AMOUNT =================
    amount_label = tk.Label(
        container,
        textvariable=amount_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="white",
        anchor="e"
    )
    amount_label.pack(fill="x", padx=15, pady=(5,0))

    DarkDropdown(container, from_var, list(length_units.keys()))

    # ================= SWAP BUTTON =================
    def swap_units():
        f = from_var.get()
        t = to_var.get()
        from_var.set(t)
        to_var.set(f)
        convert()

    tk.Button(
        container,
        text="⇅",
        bg="#CCFFBE",
        fg="black",
        relief="flat",
        font=("Segoe UI", 12),
        command=swap_units
    ).pack(pady=2)

    # ================= RESULT =================
    result_label = tk.Label(
        container,
        textvariable=result_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="#cccccc",
        anchor="e"
    )
    result_label.pack(fill="x", padx=15, pady=(5,0))

    DarkDropdown(container, to_var, list(length_units.keys()))

    # ================= ABOUT TEXT =================
    equal_label = tk.Label(
        container,
        text="",
        font=("Segoe UI", 10),
        bg="#121212",
        fg="#888888",
        anchor="w"
    )
    equal_label.pack(fill="x", padx=15, pady=(5,5))

    # ================= CONVERT FUNCTION =================
    def convert(*args):
        try:
            value = float(amount_var.get())

            base = value * length_units[from_var.get()]
            result = base / length_units[to_var.get()]

            # Smart formatting
            if result > 100000:
                formatted = f"{result:,.2f}"
            else:
                formatted = f"{result:.4f}".rstrip("0").rstrip(".")

            result_var.set(formatted)

            equal_label.config(
                text=f"About equal to {formatted} {to_var.get()}"
            )

        except:
            result_var.set("")
            equal_label.config(text="")

    amount_var.trace_add("write", convert)
    from_var.trace_add("write", convert)
    to_var.trace_add("write", convert)

# ================= WINDOWS STYLE KEYPAD =================

    keypad_frame = tk.Frame(btns, bg="#121212")
    btns.rowconfigure(6, weight=1)
    btns.columnconfigure(0, weight=1)
    keypad_frame.grid(row=6, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)

# Make columns expand equally
    for i in range(3):
        keypad_frame.columnconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, minsize=30)  # Increase this value


    def press(val):
        if val == "CE":
            amount_var.set("0")

        elif val == "⌫":
            current = amount_var.get()
            amount_var.set(current[:-1] if len(current) > 1 else "0")

        else:
            if amount_var.get() == "0":
                amount_var.set(val)
            else:
                amount_var.set(amount_var.get() + val)


# ---- Row 0 (CE and Backspace) ----
    tk.Button(keypad_frame,
              text="CE",
              bg="#b00020",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("CE")
              ).grid(row=0, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

    tk.Button(keypad_frame,
              text="⌫",
              bg="#1ab4f6",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("⌫")
              ).grid(row=0, column=2, sticky="nsew", padx=3, pady=3)


# ---- Number Rows ----
    numbers = [
        ["7","8","9"],
        ["4","5","6"],
        ["1","2","3"]
]

    for r, row in enumerate(numbers):
        for c, num in enumerate(row):
            tk.Button(keypad_frame,
                      text=num,
                      bg="#1e1e1e",
                      fg="white",
                      font=("Segoe UI", 14),
                      relief="flat",
                      command=lambda n=num: press(n)
                      ).grid(row=r+1, column=c, sticky="nsew", padx=3, pady=3)


# ---- Last Row (0 wide + dot) ----
    tk.Button(keypad_frame,
              text="0",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press("0")
              ).grid(row=4, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)

    tk.Button(keypad_frame,
              text=".",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press(".")
              ).grid(row=4, column=2, sticky="nsew", padx=3, pady=3)


def build_weight_ui():
    clear_buttons()
    title_label.config(text="Weight and mass")

    # Activate full grid layout
    for i in range(6):
        btns.columnconfigure(i, weight=1)

    container = tk.Frame(btns, bg="#121212")
    container.grid(row=0, column=0, columnspan=6, sticky="nsew", pady=5)

    from_var = tk.StringVar(value="Pounds")
    to_var = tk.StringVar(value="Kilograms")
    amount_var = tk.StringVar(value="0")
    result_var = tk.StringVar(value="0")

    # ================= TOP AMOUNT =================
    tk.Label(
        container,
        textvariable=amount_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="white",
        anchor="e"
    ).pack(fill="x", padx=15, pady=(5,0))

    DarkDropdown(container, from_var, list(weight_units.keys()))

    # ================= SWAP BUTTON =================
    def swap_units():
        f = from_var.get()
        t = to_var.get()
        from_var.set(t)
        to_var.set(f)
        convert()

    tk.Button(
        container,
        text="⇅",
        bg="#CCFFBE",
        fg="black",
        relief="flat",
        font=("Segoe UI", 12),
        command=swap_units
    ).pack(pady=2)

    # ================= RESULT =================
    tk.Label(
        container,
        textvariable=result_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="#cccccc",
        anchor="e"
    ).pack(fill="x", padx=15, pady=(5,0))

    DarkDropdown(container, to_var, list(weight_units.keys()))

    # ================= ABOUT TEXT =================
    equal_label = tk.Label(
        container,
        text="",
        font=("Segoe UI", 10),
        bg="#121212",
        fg="#888888",
        anchor="w"
    )
    equal_label.pack(fill="x", padx=15, pady=(5,5))

    # ================= CONVERT FUNCTION =================
    def convert(*args):
        try:
            value = float(amount_var.get())

            # Convert to kilograms base
            base = value * weight_units[from_var.get()]
            result = base / weight_units[to_var.get()]

            # Smart formatting
            if result > 100000:
                formatted = f"{result:,.2f}"
            else:
                formatted = f"{result:.4f}".rstrip("0").rstrip(".")

            result_var.set(formatted)

            equal_label.config(
                text=f"About equal to {formatted} {to_var.get()}"
            )

        except:
            result_var.set("")
            equal_label.config(text="")

    amount_var.trace_add("write", convert)
    from_var.trace_add("write", convert)
    to_var.trace_add("write", convert)

    # ================= WINDOWS STYLE KEYPAD =================
    keypad_frame = tk.Frame(btns, bg="#121212")
    btns.rowconfigure(6, weight=1)
    keypad_frame.grid(row=6, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)

    for i in range(3):
        keypad_frame.columnconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, weight=1)
        keypad_frame.rowconfigure(i, minsize=28)  # slightly smaller to fit

    def press(val):
        if val == "CE":
            amount_var.set("0")

        elif val == "⌫":
            current = amount_var.get()
            amount_var.set(current[:-1] if len(current) > 1 else "0")

        else:
            if amount_var.get() == "0":
                amount_var.set(val)
            else:
                amount_var.set(amount_var.get() + val)

    # Row 0
    tk.Button(keypad_frame, text="CE", bg="#b00020", fg="white",
              font=("Segoe UI", 12), relief="flat",
              command=lambda: press("CE")
              ).grid(row=0, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

    tk.Button(keypad_frame, text="⌫", bg="#1ab4f6", fg="white",
              font=("Segoe UI", 12), relief="flat",
              command=lambda: press("⌫")
              ).grid(row=0, column=2, sticky="nsew", padx=3, pady=3)

    # Number rows
    numbers = [["7","8","9"],
               ["4","5","6"],
               ["1","2","3"]]

    for r, row in enumerate(numbers):
        for c, num in enumerate(row):
            tk.Button(keypad_frame,
                      text=num,
                      bg="#1e1e1e",
                      fg="white",
                      font=("Segoe UI", 14),
                      relief="flat",
                      command=lambda n=num: press(n)
                      ).grid(row=r+1, column=c, sticky="nsew", padx=3, pady=3)

    # Last row
    tk.Button(keypad_frame,
              text="0",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press("0")
              ).grid(row=4, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)

    tk.Button(keypad_frame,
              text=".",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press(".")
              ).grid(row=4, column=2, sticky="nsew", padx=3, pady=3)


def build_temperature_ui():
    clear_buttons()
    title_label.config(text="Temperature")

    for i in range(6):
        btns.columnconfigure(i, weight=1)

    container = tk.Frame(btns, bg="#121212")
    container.grid(row=0, column=0, columnspan=6, sticky="nsew", pady=5)

    from_var = tk.StringVar(value="Fahrenheit")
    to_var = tk.StringVar(value="Celsius")
    amount_var = tk.StringVar(value="0")
    result_var = tk.StringVar(value="0")

    # ================= TOP VALUE =================
    amount_label = tk.Label(
        container,
        textvariable=amount_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="white",
        anchor="e"
    )
    amount_label.pack(fill="x", padx=15, pady=(5,0))

    DarkDropdown(container, from_var, temperature_units)

    # ================= SWAP BUTTON =================
    def swap_units():
        f = from_var.get()
        t = to_var.get()
        from_var.set(t)
        to_var.set(f)
        convert()

    tk.Button(
        container,
        text="⇅",
        bg="#CCFFBE",
        fg="black",
        relief="flat",
        font=("Segoe UI", 12),
        command=swap_units
    ).pack(pady=2)

    # ================= RESULT =================
    result_label = tk.Label(
        container,
        textvariable=result_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="#cccccc",
        anchor="e"
    )
    result_label.pack(fill="x", padx=15, pady=(5,0))

    DarkDropdown(container, to_var, temperature_units)

    # ================= ABOUT EQUAL =================
    equal_label = tk.Label(
        container,
        text="",
        font=("Segoe UI", 10),
        bg="#121212",
        fg="#888888",
        anchor="w"
    )
    equal_label.pack(fill="x", padx=15, pady=(5,5))

    # ================= CONVERT FUNCTION =================
    def convert(*args):
        try:
            value = float(amount_var.get())

            # Convert input to Celsius (base)
            if from_var.get() == "Celsius":
                c = value
            elif from_var.get() == "Fahrenheit":
                c = (value - 32) * 5/9
            else:  # Kelvin
                c = value - 273.15

            # Convert Celsius to target
            if to_var.get() == "Celsius":
                result = c
            elif to_var.get() == "Fahrenheit":
                result = (c * 9/5) + 32
            else:  # Kelvin
                result = c + 273.15

            formatted = f"{result:.4f}".rstrip("0").rstrip(".")
            result_var.set(formatted)

            # About equal to Kelvin
            kelvin = c + 273.15
            equal_label.config(
                text=f"About equal to {kelvin:.1f} K"
            )

        except:
            result_var.set("")
            equal_label.config(text="")

    amount_var.trace_add("write", convert)
    from_var.trace_add("write", convert)
    to_var.trace_add("write", convert)

# ================= WINDOWS STYLE KEYPAD =================

    keypad_frame = tk.Frame(btns, bg="#121212")
    btns.rowconfigure(6, weight=1)
    btns.columnconfigure(0, weight=1)
    keypad_frame.grid(row=6, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)

# Make columns expand equally
    for i in range(3):
        keypad_frame.columnconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, minsize=30)  # Increase this value


    def press(val):
        if val == "CE":
            amount_var.set("0")

        elif val == "⌫":
            current = amount_var.get()
            amount_var.set(current[:-1] if len(current) > 1 else "0")

        else:
            if amount_var.get() == "0":
                amount_var.set(val)
            else:
                amount_var.set(amount_var.get() + val)


# ---- Row 0 (CE and Backspace) ----
    tk.Button(keypad_frame,
              text="CE",
              bg="#b00020",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("CE")
              ).grid(row=0, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

    tk.Button(keypad_frame,
              text="⌫",
              bg="#1ab4f6",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("⌫")
              ).grid(row=0, column=2, sticky="nsew", padx=3, pady=3)


# ---- Number Rows ----
    numbers = [
        ["7","8","9"],
        ["4","5","6"],
        ["1","2","3"]
]

    for r, row in enumerate(numbers):
        for c, num in enumerate(row):
            tk.Button(keypad_frame,
                      text=num,
                      bg="#1e1e1e",
                      fg="white",
                      font=("Segoe UI", 14),
                      relief="flat",
                      command=lambda n=num: press(n)
                      ).grid(row=r+1, column=c, sticky="nsew", padx=3, pady=3)


# ---- Last Row (0 wide + dot) ----
    tk.Button(keypad_frame,
              text="0",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press("0")
              ).grid(row=4, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)

    tk.Button(keypad_frame,
              text=".",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press(".")
              ).grid(row=4, column=2, sticky="nsew", padx=3, pady=3)


def build_energy_ui():
    clear_buttons()
    title_label.config(text="Energy")

    for i in range(6):
        btns.columnconfigure(i, weight=1)

    container = tk.Frame(btns, bg="#121212")
    container.grid(row=0, column=0, columnspan=6, sticky="nsew", pady=5)

    from_var = tk.StringVar(value="Joules")
    to_var = tk.StringVar(value="Food calories")
    amount_var = tk.StringVar(value="0")
    result_var = tk.StringVar(value="0")

    # ================= INPUT =================
    amount_label = tk.Label(
        container,
        textvariable=amount_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="white",
        anchor="e"
    )
    amount_label.pack(fill="x", padx=15, pady=(5,0))

    DarkDropdown(container, from_var, list(energy_units.keys()))

    # ================= SWAP =================
    def swap_units():
        f = from_var.get()
        t = to_var.get()
        from_var.set(t)
        to_var.set(f)
        convert()

    tk.Button(
        container,
        text="⇅",
        bg="#CCFFBE",
        fg="black",
        relief="flat",
        font=("Segoe UI", 12),
        command=swap_units
    ).pack(pady=2)

    # ================= RESULT =================
    result_label = tk.Label(
        container,
        textvariable=result_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="#cccccc",
        anchor="e"
    )
    result_label.pack(fill="x", padx=15, pady=(5,0))

    DarkDropdown(container, to_var, list(energy_units.keys()))

# ================= ABOUT EQUAL =================
    equal_label = tk.Label(
        container,
        text="",
        font=("Segoe UI", 10),
        bg="#121212",
        fg="#888888",
        anchor="w"
)
    equal_label.pack(fill="x", padx=15, pady=(5,5))

    # ================= CONVERT =================
    def convert(*args):
        try:
            value = float(amount_var.get())

        # Convert to base (Joules)
            base = value * energy_units[from_var.get()]

        # Convert to target
            result = base / energy_units[to_var.get()]

            formatted = f"{result:.4f}".rstrip("0").rstrip(".")
            result_var.set(formatted)

        # About equal to Joules
            equal_formatted = f"{base:.2f}".rstrip("0").rstrip(".")
            equal_label.config(text=f"About equal to {equal_formatted} J")

        except:
            result_var.set("")
            equal_label.config(text="")

    amount_var.trace_add("write", convert)
    from_var.trace_add("write", convert)
    to_var.trace_add("write", convert)

# ================= WINDOWS STYLE KEYPAD =================

    keypad_frame = tk.Frame(btns, bg="#121212")
    btns.rowconfigure(6, weight=1)
    btns.columnconfigure(0, weight=1)
    keypad_frame.grid(row=6, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)

# Make columns expand equally
    for i in range(3):
        keypad_frame.columnconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, minsize=30)  # Increase this value


    def press(val):
        if val == "CE":
            amount_var.set("0")

        elif val == "⌫":
            current = amount_var.get()
            amount_var.set(current[:-1] if len(current) > 1 else "0")

        else:
            if amount_var.get() == "0":
                amount_var.set(val)
            else:
                amount_var.set(amount_var.get() + val)


# ---- Row 0 (CE and Backspace) ----
    tk.Button(keypad_frame,
              text="CE",
              bg="#b00020",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("CE")
              ).grid(row=0, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

    tk.Button(keypad_frame,
              text="⌫",
              bg="#1ab4f6",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("⌫")
              ).grid(row=0, column=2, sticky="nsew", padx=3, pady=3)


# ---- Number Rows ----
    numbers = [
        ["7","8","9"],
        ["4","5","6"],
        ["1","2","3"]
]

    for r, row in enumerate(numbers):
        for c, num in enumerate(row):
            tk.Button(keypad_frame,
                      text=num,
                      bg="#1e1e1e",
                      fg="white",
                      font=("Segoe UI", 14),
                      relief="flat",
                      command=lambda n=num: press(n)
                      ).grid(row=r+1, column=c, sticky="nsew", padx=3, pady=3)


# ---- Last Row (0 wide + dot) ----
    tk.Button(keypad_frame,
              text="0",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press("0")
              ).grid(row=4, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)

    tk.Button(keypad_frame,
              text=".",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press(".")
              ).grid(row=4, column=2, sticky="nsew", padx=3, pady=3)


def build_area_ui():
    clear_buttons()
    title_label.config(text="Area")

    for i in range(6):
        btns.columnconfigure(i, weight=1)

    container = tk.Frame(btns, bg="#121212")
    container.grid(row=0, column=0, columnspan=6, sticky="nsew", pady=5)

    from_var = tk.StringVar(value="Square feet")
    to_var = tk.StringVar(value="Square metres")
    amount_var = tk.StringVar(value="0")
    result_var = tk.StringVar(value="0")

    # ================= INPUT =================
    amount_label = tk.Label(
        container,
        textvariable=amount_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="white",
        anchor="e"
    )
    amount_label.pack(fill="x", padx=15, pady=(5,0))

    DarkDropdown(container, from_var, list(area_units.keys()))

    # ================= SWAP =================
    def swap_units():
        f = from_var.get()
        t = to_var.get()
        from_var.set(t)
        to_var.set(f)
        convert()

    tk.Button(
        container,
        text="⇅",
        bg="#CCFFBE",
        fg="black",
        relief="flat",
        font=("Segoe UI", 12),
        command=swap_units
    ).pack(pady=2)

    # ================= RESULT =================
    result_label = tk.Label(
        container,
        textvariable=result_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="#cccccc",
        anchor="e"
    )
    result_label.pack(fill="x", padx=15, pady=(5,0))

    DarkDropdown(container, to_var, list(area_units.keys()))

    # ================= ABOUT EQUAL =================
    equal_label = tk.Label(
        container,
        text="",
        font=("Segoe UI", 10),
        bg="#121212",
        fg="#888888",
        anchor="w"
    )
    equal_label.pack(fill="x", padx=15, pady=(5,5))

    # ================= CONVERT =================
    def convert(*args):
        try:
            value = float(amount_var.get())

            # Convert to base (square metres)
            base = value * area_units[from_var.get()]

            # Convert to target
            result = base / area_units[to_var.get()]

            formatted = f"{result:.4f}".rstrip("0").rstrip(".")
            result_var.set(formatted)

            # About equal to square metres
            equal_formatted = f"{base:,.2f}".rstrip("0").rstrip(".")
            equal_label.config(
                text=f"About equal to {equal_formatted} m²"
            )

        except:
            result_var.set("")
            equal_label.config(text="")

    amount_var.trace_add("write", convert)
    from_var.trace_add("write", convert)
    to_var.trace_add("write", convert)

# ================= WINDOWS STYLE KEYPAD =================

    keypad_frame = tk.Frame(btns, bg="#121212")
    btns.rowconfigure(6, weight=1)
    btns.columnconfigure(0, weight=1)
    keypad_frame.grid(row=6, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)

# Make columns expand equally
    for i in range(3):
        keypad_frame.columnconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, minsize=30)  # Increase this value


    def press(val):
        if val == "CE":
            amount_var.set("0")

        elif val == "⌫":
            current = amount_var.get()
            amount_var.set(current[:-1] if len(current) > 1 else "0")

        else:
            if amount_var.get() == "0":
                amount_var.set(val)
            else:
                amount_var.set(amount_var.get() + val)


# ---- Row 0 (CE and Backspace) ----
    tk.Button(keypad_frame,
              text="CE",
              bg="#b00020",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("CE")
              ).grid(row=0, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

    tk.Button(keypad_frame,
              text="⌫",
              bg="#1ab4f6",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("⌫")
              ).grid(row=0, column=2, sticky="nsew", padx=3, pady=3)


# ---- Number Rows ----
    numbers = [
        ["7","8","9"],
        ["4","5","6"],
        ["1","2","3"]
]

    for r, row in enumerate(numbers):
        for c, num in enumerate(row):
            tk.Button(keypad_frame,
                      text=num,
                      bg="#1e1e1e",
                      fg="white",
                      font=("Segoe UI", 14),
                      relief="flat",
                      command=lambda n=num: press(n)
                      ).grid(row=r+1, column=c, sticky="nsew", padx=3, pady=3)


# ---- Last Row (0 wide + dot) ----
    tk.Button(keypad_frame,
              text="0",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press("0")
              ).grid(row=4, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)

    tk.Button(keypad_frame,
              text=".",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press(".")
              ).grid(row=4, column=2, sticky="nsew", padx=3, pady=3)


def build_speed_ui():
    clear_buttons()
    title_label.config(text="Speed")

    for i in range(6):
        btns.columnconfigure(i, weight=1)

    container = tk.Frame(btns, bg="#121212")
    container.grid(row=0, column=0, columnspan=6, sticky="nsew", pady=5)

    from_var = tk.StringVar(value="Miles per hour")
    to_var = tk.StringVar(value="Kilometres per hour")
    amount_var = tk.StringVar(value="0")
    result_var = tk.StringVar(value="0")

    # ================= INPUT =================
    amount_label = tk.Label(
        container,
        textvariable=amount_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="white",
        anchor="e"
    )
    amount_label.pack(fill="x", padx=15, pady=(5,0))

    DarkDropdown(container, from_var, list(speed_units.keys()))

    # ================= SWAP =================
    def swap_units():
        f = from_var.get()
        t = to_var.get()
        from_var.set(t)
        to_var.set(f)
        convert()

    tk.Button(
        container,
        text="⇅",
        bg="#CCFFBE",
        fg="black",
        relief="flat",
        font=("Segoe UI", 12),
        command=swap_units
    ).pack(pady=2)

    # ================= RESULT =================
    result_label = tk.Label(
        container,
        textvariable=result_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="#cccccc",
        anchor="e"
    )
    result_label.pack(fill="x", padx=15, pady=(5,0))

    DarkDropdown(container, to_var, list(speed_units.keys()))

    # ================= ABOUT EQUAL =================
    equal_label = tk.Label(
        container,
        text="",
        font=("Segoe UI", 10),
        bg="#121212",
        fg="#888888",
        anchor="w"
    )
    equal_label.pack(fill="x", padx=15, pady=(5,5))

    # ================= CONVERT =================
    def convert(*args):
        try:
            value = float(amount_var.get())

            # Convert to base (m/s)
            base = value * speed_units[from_var.get()]

            # Convert to target
            result = base / speed_units[to_var.get()]

            formatted = f"{result:.6f}".rstrip("0").rstrip(".")
            result_var.set(formatted)

            # About equal to metres per second
            equal_formatted = f"{base:,.2f}".rstrip("0").rstrip(".")
            equal_label.config(
                text=f"About equal to {equal_formatted} m/s"
            )

        except:
            result_var.set("")
            equal_label.config(text="")

    amount_var.trace_add("write", convert)
    from_var.trace_add("write", convert)
    to_var.trace_add("write", convert)

# ================= WINDOWS STYLE KEYPAD =================

    keypad_frame = tk.Frame(btns, bg="#121212")
    btns.rowconfigure(6, weight=1)
    btns.columnconfigure(0, weight=1)
    keypad_frame.grid(row=6, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)

# Make columns expand equally
    for i in range(3):
        keypad_frame.columnconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, minsize=30)  # Increase this value


    def press(val):
        if val == "CE":
            amount_var.set("0")

        elif val == "⌫":
            current = amount_var.get()
            amount_var.set(current[:-1] if len(current) > 1 else "0")

        else:
            if amount_var.get() == "0":
                amount_var.set(val)
            else:
                amount_var.set(amount_var.get() + val)


# ---- Row 0 (CE and Backspace) ----
    tk.Button(keypad_frame,
              text="CE",
              bg="#b00020",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("CE")
              ).grid(row=0, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

    tk.Button(keypad_frame,
              text="⌫",
              bg="#1ab4f6",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("⌫")
              ).grid(row=0, column=2, sticky="nsew", padx=3, pady=3)


# ---- Number Rows ----
    numbers = [
        ["7","8","9"],
        ["4","5","6"],
        ["1","2","3"]
]

    for r, row in enumerate(numbers):
        for c, num in enumerate(row):
            tk.Button(keypad_frame,
                      text=num,
                      bg="#1e1e1e",
                      fg="white",
                      font=("Segoe UI", 14),
                      relief="flat",
                      command=lambda n=num: press(n)
                      ).grid(row=r+1, column=c, sticky="nsew", padx=3, pady=3)


# ---- Last Row (0 wide + dot) ----
    tk.Button(keypad_frame,
              text="0",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press("0")
              ).grid(row=4, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)

    tk.Button(keypad_frame,
              text=".",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press(".")
              ).grid(row=4, column=2, sticky="nsew", padx=3, pady=3)


def build_time_ui():
    clear_buttons()
    title_label.config(text="Time")

    for i in range(6):
        btns.columnconfigure(i, weight=1)

    container = tk.Frame(btns, bg="#121212")
    container.grid(row=0, column=0, columnspan=6, sticky="nsew", pady=5)

    from_var = tk.StringVar(value="Hours")
    to_var = tk.StringVar(value="Minutes")
    amount_var = tk.StringVar(value="0")
    result_var = tk.StringVar(value="0")

    # ================= INPUT =================
    amount_label = tk.Label(
        container,
        textvariable=amount_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="white",
        anchor="e"
    )
    amount_label.pack(fill="x", padx=15, pady=(5,0))

    DarkDropdown(container, from_var, list(time_units.keys()))

    # ================= SWAP =================
    def swap_units():
        f = from_var.get()
        t = to_var.get()
        from_var.set(t)
        to_var.set(f)
        convert()

    tk.Button(
        container,
        text="⇅",
        bg="#CCFFBE",
        fg="black",
        relief="flat",
        font=("Segoe UI", 12),
        command=swap_units
    ).pack(pady=2)

    # ================= RESULT =================
    result_label = tk.Label(
        container,
        textvariable=result_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="#cccccc",
        anchor="e"
    )
    result_label.pack(fill="x", padx=15, pady=(5,0))

    DarkDropdown(container, to_var, list(time_units.keys()))

    # ================= ABOUT EQUAL =================
    equal_label = tk.Label(
        container,
        text="",
        font=("Segoe UI", 10),
        bg="#121212",
        fg="#888888",
        anchor="w"
    )
    equal_label.pack(fill="x", padx=15, pady=(5,5))

    # ================= CONVERT =================
    def convert(*args):
        try:
            value = float(amount_var.get())

            # Convert to base (seconds)
            base = value * time_units[from_var.get()]

            # Convert to target
            result = base / time_units[to_var.get()]

            formatted = f"{result:.6f}".rstrip("0").rstrip(".")
            result_var.set(formatted)

            # About equal to seconds
            equal_formatted = f"{base:,.2f}".rstrip("0").rstrip(".")
            equal_label.config(
                text=f"About equal to {equal_formatted} s"
            )

        except:
            result_var.set("")
            equal_label.config(text="")

    amount_var.trace_add("write", convert)
    from_var.trace_add("write", convert)
    to_var.trace_add("write", convert)

# ================= WINDOWS STYLE KEYPAD =================

    keypad_frame = tk.Frame(btns, bg="#121212")
    btns.rowconfigure(6, weight=1)
    btns.columnconfigure(0, weight=1)
    keypad_frame.grid(row=6, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)

# Make columns expand equally
    for i in range(3):
        keypad_frame.columnconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, minsize=30)  # Increase this value


    def press(val):
        if val == "CE":
            amount_var.set("0")

        elif val == "⌫":
            current = amount_var.get()
            amount_var.set(current[:-1] if len(current) > 1 else "0")

        else:
            if amount_var.get() == "0":
                amount_var.set(val)
            else:
                amount_var.set(amount_var.get() + val)


# ---- Row 0 (CE and Backspace) ----
    tk.Button(keypad_frame,
              text="CE",
              bg="#b00020",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("CE")
              ).grid(row=0, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

    tk.Button(keypad_frame,
              text="⌫",
              bg="#1ab4f6",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("⌫")
              ).grid(row=0, column=2, sticky="nsew", padx=3, pady=3)


# ---- Number Rows ----
    numbers = [
        ["7","8","9"],
        ["4","5","6"],
        ["1","2","3"]
]

    for r, row in enumerate(numbers):
        for c, num in enumerate(row):
            tk.Button(keypad_frame,
                      text=num,
                      bg="#1e1e1e",
                      fg="white",
                      font=("Segoe UI", 14),
                      relief="flat",
                      command=lambda n=num: press(n)
                      ).grid(row=r+1, column=c, sticky="nsew", padx=3, pady=3)


# ---- Last Row (0 wide + dot) ----
    tk.Button(keypad_frame,
              text="0",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press("0")
              ).grid(row=4, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)

    tk.Button(keypad_frame,
              text=".",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press(".")
              ).grid(row=4, column=2, sticky="nsew", padx=3, pady=3)


def build_power_ui():
    clear_buttons()
    title_label.config(text="Power")

    for i in range(6):
        btns.columnconfigure(i, weight=1)

    container = tk.Frame(btns, bg="#121212")
    container.grid(row=0, column=0, columnspan=6, sticky="nsew", pady=5)

    from_var = tk.StringVar(value="Kilowatts")
    to_var = tk.StringVar(value="Horsepower (US)")
    amount_var = tk.StringVar(value="0")
    result_var = tk.StringVar(value="0")

    # ================= INPUT =================
    amount_label = tk.Label(
        container,
        textvariable=amount_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="white",
        anchor="e"
    )
    amount_label.pack(fill="x", padx=15, pady=(5, 0))

    DarkDropdown(container, from_var, list(power_units.keys()))

    # ================= RESULT =================
    result_label = tk.Label(
        container,
        textvariable=result_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="white",
        anchor="e"
    )
    result_label.pack(fill="x", padx=15, pady=(5, 0))

    DarkDropdown(container, to_var, list(power_units.keys()))

    # ================= ABOUT EQUAL =================
    equal_frame = tk.Frame(container, bg="#121212")
    equal_frame.pack(fill="x", padx=20, pady=(8, 5))

    about_label = tk.Label(
        equal_frame,
        text="About equal to",
        font=("Segoe UI", 11),
        bg="#121212",
        fg="#aaaaaa",
        anchor="w"
    )
    about_label.pack(anchor="w")

    equal_values = tk.Label(
        equal_frame,
        text="",
        font=("Segoe UI", 12),
        bg="#121212",
        fg="#cccccc",
        anchor="w"
    )
    equal_values.pack(anchor="w")

    # ================= CONVERT =================
    def convert(*args):
        try:
            value = float(amount_var.get())

            base = value * power_units[from_var.get()]
            result = base / power_units[to_var.get()]

            result_var.set(f"{result:.4f}".rstrip("0").rstrip("."))

            # About equal to values
            btu = base * 0.056869   # watts → BTU/min
            ftlb = base * 44.2537   # watts → ft·lb/min

            equal_values.config(
                text=f"{btu:.0f} BTU/min     {ftlb:.0f} ft·lb/min"
            )

        except:
            result_var.set("")
            equal_values.config(text="")

    amount_var.trace_add("write", convert)
    from_var.trace_add("write", convert)
    to_var.trace_add("write", convert)

# ================= WINDOWS STYLE KEYPAD =================

    keypad_frame = tk.Frame(btns, bg="#121212")
    btns.rowconfigure(6, weight=1)
    btns.columnconfigure(0, weight=1)
    keypad_frame.grid(row=6, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)

# Make columns expand equally
    for i in range(3):
        keypad_frame.columnconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, minsize=30)  # Increase this value


    def press(val):
        if val == "CE":
            amount_var.set("0")

        elif val == "⌫":
            current = amount_var.get()
            amount_var.set(current[:-1] if len(current) > 1 else "0")

        else:
            if amount_var.get() == "0":
                amount_var.set(val)
            else:
                amount_var.set(amount_var.get() + val)


# ---- Row 0 (CE and Backspace) ----
    tk.Button(keypad_frame,
              text="CE",
              bg="#b00020",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("CE")
              ).grid(row=0, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

    tk.Button(keypad_frame,
              text="⌫",
              bg="#1ab4f6",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("⌫")
              ).grid(row=0, column=2, sticky="nsew", padx=3, pady=3)


# ---- Number Rows ----
    numbers = [
        ["7","8","9"],
        ["4","5","6"],
        ["1","2","3"]
]

    for r, row in enumerate(numbers):
        for c, num in enumerate(row):
            tk.Button(keypad_frame,
                      text=num,
                      bg="#1e1e1e",
                      fg="white",
                      font=("Segoe UI", 14),
                      relief="flat",
                      command=lambda n=num: press(n)
                      ).grid(row=r+1, column=c, sticky="nsew", padx=3, pady=3)


# ---- Last Row (0 wide + dot) ----
    tk.Button(keypad_frame,
              text="0",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press("0")
              ).grid(row=4, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)

    tk.Button(keypad_frame,
              text=".",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press(".")
              ).grid(row=4, column=2, sticky="nsew", padx=3, pady=3)


def build_data_ui():
    clear_buttons()
    title_label.config(text="Data")

    for i in range(6):
        btns.columnconfigure(i, weight=1)

    container = tk.Frame(btns, bg="#121212")
    container.grid(row=0, column=0, columnspan=6, sticky="nsew", pady=5)

    from_var = tk.StringVar(value="Gigabytes")
    to_var = tk.StringVar(value="Megabytes")
    amount_var = tk.StringVar(value="0")
    result_var = tk.StringVar(value="0")

    # ================= INPUT =================
    tk.Label(
        container,
        textvariable=amount_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="white",
        anchor="e"
    ).pack(fill="x", padx=15, pady=(5, 0))

    DarkDropdown(container, from_var, list(data_units.keys()))

    # ================= SWAP =================
    def swap_units():
        f = from_var.get()
        t = to_var.get()
        from_var.set(t)
        to_var.set(f)
        convert()

    tk.Button(
        container,
        text="⇅",
        bg="#CCFFBE",
        fg="black",
        relief="flat",
        font=("Segoe UI", 12),
        command=swap_units
    ).pack(pady=2)

    # ================= RESULT =================
    tk.Label(
        container,
        textvariable=result_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="#cccccc",
        anchor="e"
    ).pack(fill="x", padx=15, pady=(5, 0))

    DarkDropdown(container, to_var, list(data_units.keys()))

    # ================= ABOUT EQUAL =================
    equal_label = tk.Label(
        container,
        text="",
        font=("Segoe UI", 10),
        bg="#121212",
        fg="#888888",
        anchor="w"
    )
    equal_label.pack(fill="x", padx=15, pady=(5, 5))

    # ================= CONVERT =================
    def convert(*args):
        try:
            value = float(amount_var.get())

            # Convert to base (Bytes)
            base = value * data_units[from_var.get()]

            # Convert to target
            result = base / data_units[to_var.get()]
            if abs(result) >= 1e12 or (abs(result) > 0 and abs(result) < 1e-6):
                result_var.set(f"{result:.6e}")
            else:
                result_var.set(f"{result:.6f}".rstrip("0").rstrip("."))

            # About equal to Bytes
            equal_label.config(
                text=f"About equal to {base:,.2f} Bytes"
            )

        except:
            result_var.set("")
            equal_label.config(text="")

    amount_var.trace_add("write", convert)
    from_var.trace_add("write", convert)
    to_var.trace_add("write", convert)

# ================= WINDOWS STYLE KEYPAD =================

    keypad_frame = tk.Frame(btns, bg="#121212")
    btns.rowconfigure(6, weight=1)
    btns.columnconfigure(0, weight=1)
    keypad_frame.grid(row=6, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)

# Make columns expand equally
    for i in range(3):
        keypad_frame.columnconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, minsize=30)  # Increase this value


    def press(val):
        if val == "CE":
            amount_var.set("0")

        elif val == "⌫":
            current = amount_var.get()
            amount_var.set(current[:-1] if len(current) > 1 else "0")

        else:
            if amount_var.get() == "0":
                amount_var.set(val)
            else:
                amount_var.set(amount_var.get() + val)


# ---- Row 0 (CE and Backspace) ----
    tk.Button(keypad_frame,
              text="CE",
              bg="#b00020",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("CE")
              ).grid(row=0, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

    tk.Button(keypad_frame,
              text="⌫",
              bg="#1ab4f6",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("⌫")
              ).grid(row=0, column=2, sticky="nsew", padx=3, pady=3)


# ---- Number Rows ----
    numbers = [
        ["7","8","9"],
        ["4","5","6"],
        ["1","2","3"]
]

    for r, row in enumerate(numbers):
        for c, num in enumerate(row):
            tk.Button(keypad_frame,
                      text=num,
                      bg="#1e1e1e",
                      fg="white",
                      font=("Segoe UI", 14),
                      relief="flat",
                      command=lambda n=num: press(n)
                      ).grid(row=r+1, column=c, sticky="nsew", padx=3, pady=3)


# ---- Last Row (0 wide + dot) ----
    tk.Button(keypad_frame,
              text="0",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press("0")
              ).grid(row=4, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)

    tk.Button(keypad_frame,
              text=".",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press(".")
              ).grid(row=4, column=2, sticky="nsew", padx=3, pady=3)


def build_pressure_ui():
    clear_buttons()
    title_label.config(text="Pressure")

    for i in range(6):
        btns.columnconfigure(i, weight=1)

    container = tk.Frame(btns, bg="#121212")
    container.grid(row=0, column=0, columnspan=6, sticky="nsew", pady=5)

    from_var = tk.StringVar(value="Atmospheres")
    to_var = tk.StringVar(value="Bars")
    amount_var = tk.StringVar(value="0")
    result_var = tk.StringVar(value="0")

    # ================= INPUT =================
    tk.Label(
        container,
        textvariable=amount_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="white",
        anchor="e"
    ).pack(fill="x", padx=15, pady=(5, 0))

    DarkDropdown(container, from_var, list(pressure_units.keys()))

    # ================= SWAP =================
    def swap_units():
        f = from_var.get()
        t = to_var.get()
        from_var.set(t)
        to_var.set(f)
        convert()

    tk.Button(
        container,
        text="⇅",
        bg="#CCFFBE",
        fg="black",
        relief="flat",
        font=("Segoe UI", 12),
        command=swap_units
    ).pack(pady=2)

    # ================= RESULT =================
    tk.Label(
        container,
        textvariable=result_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="#cccccc",
        anchor="e"
    ).pack(fill="x", padx=15, pady=(5, 0))

    DarkDropdown(container, to_var, list(pressure_units.keys()))

    # ================= ABOUT EQUAL =================
    equal_label = tk.Label(
        container,
        text="",
        font=("Segoe UI", 10),
        bg="#121212",
        fg="#888888",
        anchor="w"
    )
    equal_label.pack(fill="x", padx=15, pady=(5, 5))

    # ================= CONVERT =================
    def convert(*args):
        try:
            value = float(amount_var.get())

            # Convert to base (Pascals)
            base = value * pressure_units[from_var.get()]

            # Convert to target
            result = base / pressure_units[to_var.get()]

            # Scientific formatting like Data converter
            if abs(result) >= 1e12 or (abs(result) > 0 and abs(result) < 1e-6):
                result_var.set(f"{result:.6e}")
            else:
                result_var.set(f"{result:.6f}".rstrip("0").rstrip("."))

            equal_label.config(
                text=f"About equal to {base:,.2f} Pa"
            )

        except:
            result_var.set("")
            equal_label.config(text="")

    amount_var.trace_add("write", convert)
    from_var.trace_add("write", convert)
    to_var.trace_add("write", convert)

# ================= WINDOWS STYLE KEYPAD =================

    keypad_frame = tk.Frame(btns, bg="#121212")
    btns.rowconfigure(6, weight=1)
    btns.columnconfigure(0, weight=1)
    keypad_frame.grid(row=6, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)

# Make columns expand equally
    for i in range(3):
        keypad_frame.columnconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, minsize=30)  # Increase this value


    def press(val):
        if val == "CE":
            amount_var.set("0")

        elif val == "⌫":
            current = amount_var.get()
            amount_var.set(current[:-1] if len(current) > 1 else "0")

        else:
            if amount_var.get() == "0":
                amount_var.set(val)
            else:
                amount_var.set(amount_var.get() + val)


# ---- Row 0 (CE and Backspace) ----
    tk.Button(keypad_frame,
              text="CE",
              bg="#b00020",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("CE")
              ).grid(row=0, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

    tk.Button(keypad_frame,
              text="⌫",
              bg="#1ab4f6",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("⌫")
              ).grid(row=0, column=2, sticky="nsew", padx=3, pady=3)


# ---- Number Rows ----
    numbers = [
        ["7","8","9"],
        ["4","5","6"],
        ["1","2","3"]
]

    for r, row in enumerate(numbers):
        for c, num in enumerate(row):
            tk.Button(keypad_frame,
                      text=num,
                      bg="#1e1e1e",
                      fg="white",
                      font=("Segoe UI", 14),
                      relief="flat",
                      command=lambda n=num: press(n)
                      ).grid(row=r+1, column=c, sticky="nsew", padx=3, pady=3)


# ---- Last Row (0 wide + dot) ----
    tk.Button(keypad_frame,
              text="0",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press("0")
              ).grid(row=4, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)

    tk.Button(keypad_frame,
              text=".",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press(".")
              ).grid(row=4, column=2, sticky="nsew", padx=3, pady=3)


def build_angle_ui():
    clear_buttons()
    title_label.config(text="Angle")

    global amount_var, from_unit, to_unit

    amount_var = tk.StringVar(value="0")
    from_unit = tk.StringVar(value="Degrees")
    to_unit = tk.StringVar(value="Radians")

    container = tk.Frame(btns, bg="#121212")
    container.grid(row=0, column=0, columnspan=6, sticky="nsew", pady=5)

    # ---------------- INPUT VALUE ----------------
    input_label = tk.Label(
        container,
        textvariable=amount_var,
        font=("Segoe UI", 40),
        bg="#121212",
        fg="white",
        anchor="w"
    )
    input_label.pack(fill="x", padx=20, pady=(10, 0))

    # ---------------- FROM UNIT DROPDOWN ----------------
    from_menu = tk.OptionMenu(container, from_unit, *angle_units.keys())
    from_menu.config(bg="#121212", fg="white", bd=0, highlightthickness=0)
    from_menu["menu"].config(bg="#2a2a2a", fg="white")
    from_menu.pack(anchor="w", padx=20)

    # ---------------- OUTPUT VALUE ----------------
    output_var = tk.StringVar(value="0")

    output_label = tk.Label(
        container,
        textvariable=output_var,
        font=("Segoe UI", 32),
        bg="#121212",
        fg="white",
        anchor="w"
    )
    output_label.pack(fill="x", padx=20, pady=(20, 0))

    # ---------------- TO UNIT DROPDOWN ----------------
    to_menu = tk.OptionMenu(container, to_unit, *angle_units.keys())
    to_menu.config(bg="#121212", fg="white", bd=0, highlightthickness=0)
    to_menu["menu"].config(bg="#2a2a2a", fg="white")
    to_menu.pack(anchor="w", padx=20)

    # ---------------- ABOUT EQUAL TO ----------------
    about_label = tk.Label(
        container,
        text="About equal to\n0 grad",
        font=("Segoe UI", 12),
        bg="#121212",
        fg="#aaaaaa",
        justify="left"
    )
    about_label.pack(anchor="w", padx=20, pady=(5, 10))

    # ---------------- CONVERSION FUNCTION ----------------
    def convert(*args):
        try:
            value = float(amount_var.get())

            # Convert to degrees first
            value_in_deg = value * angle_units[from_unit.get()]

            # Convert to target
            result = value_in_deg / angle_units[to_unit.get()]

            # Scientific format if large
            if abs(result) > 1e9:
                output_var.set(f"{result:.6e}")
            else:
                output_var.set(str(round(result, 6)).rstrip("0").rstrip("."))

            # About equal to grad
            grad_value = value_in_deg / angle_units["Gradians"]
            about_label.config(text=f"About equal to\n{round(grad_value, 6)} grad")

        except:
            output_var.set("0")

    amount_var.trace_add("write", convert)
    from_unit.trace_add("write", convert)
    to_unit.trace_add("write", convert)

    convert()

# ================= WINDOWS STYLE KEYPAD =================

    keypad_frame = tk.Frame(btns, bg="#121212")
    btns.rowconfigure(6, weight=1)
    btns.columnconfigure(0, weight=1)
    keypad_frame.grid(row=6, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)

# Make columns expand equally
    for i in range(3):
        keypad_frame.columnconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, weight=1)

    for i in range(5):
        keypad_frame.rowconfigure(i, minsize=30)  # Increase this value


    def press(val):
        if val == "CE":
            amount_var.set("0")

        elif val == "⌫":
            current = amount_var.get()
            amount_var.set(current[:-1] if len(current) > 1 else "0")

        else:
            if amount_var.get() == "0":
                amount_var.set(val)
            else:
                amount_var.set(amount_var.get() + val)


# ---- Row 0 (CE and Backspace) ----
    tk.Button(keypad_frame,
              text="CE",
              bg="#b00020",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("CE")
              ).grid(row=0, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

    tk.Button(keypad_frame,
              text="⌫",
              bg="#1ab4f6",
              fg="white",
              font=("Segoe UI", 12),
              relief="flat",
              command=lambda: press("⌫")
              ).grid(row=0, column=2, sticky="nsew", padx=3, pady=3)


# ---- Number Rows ----
    numbers = [
        ["7","8","9"],
        ["4","5","6"],
        ["1","2","3"]
]

    for r, row in enumerate(numbers):
        for c, num in enumerate(row):
            tk.Button(keypad_frame,
                      text=num,
                      bg="#1e1e1e",
                      fg="white",
                      font=("Segoe UI", 14),
                      relief="flat",
                      command=lambda n=num: press(n)
                      ).grid(row=r+1, column=c, sticky="nsew", padx=3, pady=3)


# ---- Last Row (0 wide + dot) ----
    tk.Button(keypad_frame,
              text="0",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press("0")
              ).grid(row=4, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)

    tk.Button(keypad_frame,
              text=".",
              bg="#1e1e1e",
              fg="white",
              font=("Segoe UI", 14),
              relief="flat",
              command=lambda: press(".")
              ).grid(row=4, column=2, sticky="nsew", padx=3, pady=3)


load_currency_data()
root.mainloop()