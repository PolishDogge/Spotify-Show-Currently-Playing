# Spotify Currently Playing Tracker

This Python application tracks the currently playing song on Spotify and displays it in a graphical user interface (GUI) using Tkinter. It also periodically updates the album artwork associated with the currently playing song.

## Features

- Displays the name of the currently playing song and the associated artist.
- Automatically refreshes the access token when it expires.
- Updates the album artwork of the currently playing song automatically.

## Setup Instructions

### 1. Dependencies Installation

Ensure you have Python installed on your system. Additionally, install the required Python dependencies using pip:

`pip install -r requirements.txt`

### 2. Authorization Setup

1. Run the application.
2. Follow the provided Spotify authorization link in your browser.
3. After granting access, you will be redirected to a page with a code in the URL. Copy this code.
   ![Image showing the part users needs to copy](/img/code.png)
4. Paste the code into the application when prompted.
5. Wait a few seconds for the application to process the code.

## License

This project is licensed under the [MIT License](LICENSE).
