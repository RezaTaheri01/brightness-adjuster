* * *

# Brightness Adjuster

Description
-----------

Brightness Adjuster is a PyQt5 application designed to manage screen brightness levels across multiple virtual desktops. The application allows users to set and adjust brightness levels for each virtual desktop and provides an option to start or stop the brightness adjustment process.

Features
--------

*   **Brightness Control**: Adjust brightness for multiple virtual desktops.
*   **System Tray Integration**: Minimize to system tray and restore window from the tray.
*   **Dark Theme**: Modern dark theme for better visual comfort.
*   **Persistent Settings**: Save and load brightness settings across sessions using a cache file.

Requirements
------------

*   Python 3.x
*   PyQt5
*   pyvda
*   screen-brightness-control
*   keyboard
*   tendo

You can install the required packages using `pip`:

```
pip install PyQt5 pyvda screen-brightness-control keyboard tendo
```

Installation
------------

1.  **Clone the repository:**
2.  
    ```
    git clone https://github.com/yourusername/brightness-adjuster.git
    ```
    
4.  **Navigate to the project directory:**
    
    ```
    cd brightness-adjuster
    ```
    
6.  **Install the required dependencies (virtual environment recommended):**
    
    ```
    pip install -r req.txt
    ```
    
8.  **Run the application:**
    
    ```
    python Brightness.py
    ```
    

Usage
-----

*   **Start/Stop**: Click the "Start" button to begin adjusting brightness. Click the "Stop" button to halt brightness adjustment.
*   **Adjust Brightness**: Use the spin boxes to set the brightness levels for each virtual desktop.
*   **Exit**: When app started use ctrl+e to exit or from system tray right click on app icon.

Configuration
-------------

*   **Cache File**: Brightness settings are saved to and loaded from `./cache.txt`. Ensure this file is writable.

License
-------

This project is licensed under the MIT License - see the [LICENSE](https://github.com/RezaTaheri01/brightness-adjuster/blob/main/LICENSE) file for details.

Acknowledgements
----------------

*   Thanks to the PyQt5 and pyvda libraries for their robust GUI and virtual desktop management features.
*   Special thanks to the `screen-brightness-control` library for its ease of use in controlling screen brightness.
*   Also thanks ChatGPT for this readme :)

* * *
