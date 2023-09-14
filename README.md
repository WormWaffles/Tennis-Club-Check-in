# Tennis Club Check-in Program

The Tennis Club Check-in Program is a Python application designed to manage member check-ins at a tennis club. It offers a graphical user interface (GUI) built using the Tkinter library and provides features for tracking member attendance and generating daily logs.

## Table of Contents
- [Introduction](#tennis-club-check-in-program)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Features
- Member check-in and check-out functionality.
- Customizable passcode for access control.
- Randomly generated bypass code for emergencies.
- Dynamic image display for each member.
- Logging of member attendance with date and time.
- User-friendly graphical interface.

## Prerequisites
Before running the Tennis Club Check-in Program, make sure you have the following installed:
- Python (version 3.6 or higher)
- Tkinter (usually included with Python)
- PIL (Python Imaging Library)
- NumPy
- Matplotlib (matplotlib.backends.backend_tkagg)
- Pillow (Python Imaging Library Fork)

## Installation
1. Clone or download the repository to your local machine.

   ```shell
   git clone https://github.com/yourusername/tennis-club-checkin.git
   ```
2. Navigate to the project directory.
   ```shell
   cd tennis-club-checkin
   ```
3. Install the required Python packages using pip.
   ```shell
   pip install -r requirements.txt
   ```

## Usage
1. Run the program using Python.
   ```shell
   python app.py
   ```
2. Enter the passcode or use the randomly generated bypass code to access the program.
3. Check-in members by clicking on their displayed image.
4. The program will log member check-ins with date and time.
5. To check out a member, click on their image again.