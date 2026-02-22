🧮 Advanced Multi-Mode Python Calculator

➡ A fully featured Windows-style desktop calculator built using Python and Tkinter — combining Standard, Scientific, Programmer, Date, Currency, and 12+ Unit Conversion tools into one modern dark-themed application.

✨ Overview

➼ This project is a complete multi-utility desktop calculator inspired by modern operating system calculators.

It supports:-
⁕ multiple calculation modes
⁕ real-time conversions
⁕ base transformations
⁕ date operations
⁕ live currency exchange —> all inside a custom-designed dark UI.

🛠 Built entirely with:
• Python
• Tkinter (no external GUI frameworks)

🚀 Features

🧮 Standard Mode

<img width="268" height="412" alt="Screenshot 2026-02-23 003633" src="https://github.com/user-attachments/assets/f11474e1-224a-457d-a0bc-a092297de915" />

<img width="461" height="414" alt="Screenshot 2026-02-23 003654" src="https://github.com/user-attachments/assets/4b589d4a-73dd-4440-8f77-6729e3633897" />

➥ Basic arithmetic operations
➥ Live expression evaluation
➥ Memory system (MC, MR, M+, M-, MS)
➥ Calculation history panel
➥ Windows-style numeric keypad
➥ Smart formatting

🔬 Scientific Mode

<img width="270" height="410" alt="Screenshot 2026-02-23 004040" src="https://github.com/user-attachments/assets/f9255593-f13d-4a7e-ad0b-72bcd0b869bf" />
<img width="106" height="163" alt="Screenshot 2026-02-23 004056" src="https://github.com/user-attachments/assets/c4c7feb2-72f2-4851-867a-1d1ab10c6dfb" />
<img width="107" height="153" alt="Screenshot 2026-02-23 004106" src="https://github.com/user-attachments/assets/dd35ddd0-3b5a-4490-8612-812d7be07608" />

✯Trigonometric functions
✯Logarithmic & exponential functions
✯Power & root operations
✯Parentheses support
✯Dynamic dropdown function selection
✯Clean scientific layout

💻 Programmer Mode

<img width="270" height="409" alt="Screenshot 2026-02-23 004625" src="https://github.com/user-attachments/assets/69a9601b-7dde-4eeb-8a34-90ee9c1521d5" />

<img width="927" height="605" alt="calc50x" src="https://github.com/user-attachments/assets/3aab5328-2c75-49ce-9519-f292d81526b2" />

➢ Base conversions:
    ● Binary (BIN)
    ● Octal (OCT)
    ● Decimal (DEC)
    ● Hexadecimal (HEX)
➢ Bitwise operations:
    ● AND, OR, XOR, NOT
    ● Left Shift / Right Shift
    ● Rotate operations
➢ Word size selection:
    ● 8-bit
    ● 16-bit
    ● 32-bit
    ● 64-bit
➢ Masking & overflow control

📅 Date Calculation

<img width="425" height="515" alt="206184234-53e27de0-0395-488e-8d58-1a20d08b0747" src="https://github.com/user-attachments/assets/5e372780-39e1-49ff-876d-81ad0ce7674f" />

![Date-Calculator-Kedar_1](https://github.com/user-attachments/assets/92f77f61-4ed4-446f-8552-46c457bd2782)

☞ Difference between two dates (Years, Months, Days)
☞ Add or subtract years/months/days
☞ Scrollable year selector (1600–2500)
☞ Custom calendar UI
☞ Smart date validation

💱 Currency Converter

https://store-images.s-microsoft.com/image/apps.10406.9007199266262249.a621181e-d758-4873-b765-a109eec189e0.2ebca3ff-026e-4ac3-b834-a07428c41f5b

<img width="270" height="415" alt="Screenshot 2026-02-23 010030" src="https://github.com/user-attachments/assets/e4be69a3-416b-4718-9945-69552a963d82" />

<img width="270" height="419" alt="Screenshot 2026-02-23 010047" src="https://github.com/user-attachments/assets/d526a084-df76-4f19-9f7f-27ca47b73618" />

➥ Live exchange rates
➥ Real-time conversion
➥ Country-based currency listing
➥ Update rates button
➥ Exchange rate display
➥ Last updated timestamp

➢ Exchange rate API used:
    ● https://open.er-api.com/v6/latest/USD

📏 Unit Converters

➼ The calculator includes multiple real-time unit conversion modules:
    ⁕ Energy
    ⁕ Area
    ⁕ Speed
    ⁕ Time
    ⁕ Power
    ⁕ Data
    ⁕ Pressure
    ⁕ Angle
    ⁕ Volume
    ⁕ Length
    ⁕ Weight & Mass
    ⁕ Temperature
✅ Each converter includes:
  ➥ Swap button (⇅)
  ➥ “About equal to” base unit display
  ➥ Smart decimal formatting
  ➥ Scientific notation for extreme values
  ➥ Windows-style numeric keypad
  ➥ Custom DarkDropdown component

🎨 UI / UX Highlights:-
  ✧ Modern dark theme
  ✧ Custom dropdown system
  ✧ Animated navigation panel
  ✧ Responsive grid layout
  ✧ Dynamic UI rebuild per mode
  ✧ Windows-inspired keypad layout
  ✧ Clean typography (Segoe UI)

🛠 Tech Stack:-
  ● Python 3.x
  ● Tkinter
  ● requests
  ● pycountry
  ● datetime
  ● python-dateutil

📦 Installation
  ☛ git clone https://github.com/yourusername/advanced-calculator.git
  ☛ cd advanced-calculator
  ☛ pip install -r requirements.txt
  ☛ python calculator.py

📋 Requirements

✓ Create a requirements.txt file in your root directory:-
    ➥ requests
    ➥ pycountry
    ➥ python-dateutil

🧠 Project Architecture

➥calculator.py
│
├── Standard Mode
├── Scientific Mode
├── Programmer Mode
├── Date Calculation
├── Currency Converter
├── Unit Converters
│     ├── Energy
│     ├── Area
│     ├── Speed
│     ├── Time
│     ├── Power
│     ├── Data
│     ├── Pressure
│     ├── Angle
│     ├── Volume
│     ├── Length
│     ├── Weight
│     ├── Temperature
│
└── Custom UI Components
      ├── DarkDropdown
      ├── Animated Navigation
      ├── Windows Keypad Layout

🔐 Security Note

➫ This project uses Python expression evaluation for calculations.

➔ For production-level applications:
    ● Avoid raw eval()
    ● Use a safe math parser
    ● Consider sandboxed expression evaluation
    ● Validate user input before execution

➫ This version is safe for local desktop usage but should be hardened for enterprise deployment.


💡 Future Roadmap:-
  📊 Graph plotting mode
  🧮 Matrix calculator
  📐 Equation solver
  📁 History export (CSV / TXT)
  🎨 Theme customization (Light / Dark toggle)
  ⚙️ Settings panel
  📦 Windows installer (.exe using PyInstaller)
  🧩 Modular code structure (separate files per mode)


🏆 Why This Project Stands Out:-
  🚀 Not a basic calculator
  🧠 15+ functional modules
  🌍 Live API integration
  🖥 Advanced programmer tools
  🎨 Custom UI system
  ⚡ Real-time data handling
  🏗 Portfolio-level desktop software




  
