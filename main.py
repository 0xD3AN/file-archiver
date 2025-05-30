#   FILE        :   main.py
#   DESCRIPTION :   Entry point source file for an app that allows multiple directory selection and file archiving.
#               :   A couple search filters are included for limiting which files are processed.
#   AUTHOR      :   Chance and Dean
#   DATE        :   May 30th, 2025



# STANDARD IMPORTS
# **********************************************************

import sys

from PyQt5.QtWidgets import QApplication        # we only need this import when in the main source file

from file_archiver_window import FileArchiverWindow

# **********************************************************



# ENTRY POINT
# **********************************************************
if __name__ == "__main__":
    # instantiate the Q application, required for GUI display
    app = QApplication(sys.argv)

    # instantiate and showthe custom window object
    window = FileArchiverWindow()
    window.show()

    # starts the event loop for the window and cleanly exits the program when the window is closed
    sys.exit(app.exec_())
# **********************************************************