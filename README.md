# Pomodura - Pomodoro Timer Application

A modern and feature-rich Pomodoro Timer application built with Python and tkinter. Pomodura helps you stay productive by following the Pomodoro Technique, which involves working in focused intervals with short breaks in between.

## Features

- 🕒 Classic Pomodoro timing (25 minutes work, 5 minutes break)
- ⏱️ Long break after 4 work sessions (15 minutes)
- 🎨 Modern and clean user interface
- 📱 System tray integration
- ⚙️ Configurable settings:
  - Lock screen on break (Windows only)
  - Minimize to system tray
- 🔄 Pause and reset functionality
- 📊 Cycle counter to track your productivity
- 📱 Mini timer window for quick reference

## Requirements

- Python 3.8 or higher
- Required Python packages:
  - tkinter
  - pystray
  - pillow (PIL)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/Pomodura.git
```

2. Install the required packages:
```bash
pip install pystray pillow
```

3. Run the application:
```bash
python Pomodura.py
```

## Usage

1. Start the timer by clicking the "Start" button
2. Work focused during the 25-minute work session
3. Take a 5-minute break when prompted
4. After 4 work sessions, take a longer 15-minute break
5. Use the "Pause" button to temporarily stop the timer
6. Reset the timer and cycle count with the "Reset" button

## Settings

Access settings through the "Options" menu:
- Enable/disable screen locking during breaks (Windows only)
- Configure minimize to system tray behavior

## System Tray Integration

Pomodura integrates with your system tray, providing quick access to:
- Show/hide the main window
- Start/Pause the timer
- Reset the timer
- Show the mini timer
- Quit the application

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
