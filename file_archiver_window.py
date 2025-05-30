#   FILE        :   file_archiver_window.py
#   DESCRIPTION :   Module for handling GUI display and user events.
#   AUTHOR      :   Chance and Dean
#   DATE        :   May 30th, 2025



# STANDARD IMPORTS
# **********************************************************

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,                # app and layouts
    QTreeView, QListWidget, QSplitter, QMenu, QFileSystemModel,     # containers and special controls
    QComboBox, QCheckBox, QPushButton,                              # standard controls
)

from PyQt5.QtCore import Qt, QModelIndex, QDir

# **********************************************************



# A QWidget that represents a custom window implementation
# **********************************************************

class FileArchiverWindow(QWidget):
    # class constructor
    def __init__(self):
        # calls QWidget constructor
        super().__init__()

        # basic metadata init for window
        self.setWindowTitle("File Archiver")
        self.setGeometry(100, 100, 1000, 600)

        # constructs the GUI
        self.init_ui()

    def init_ui(self):
        # create the main vertical stack layout (QVBoxLayout). arranges items in vertical fashion
        layout = QVBoxLayout(self)

        # this is the filter ribbon. it's a horizontal layout (QHBoxLayout) similar to above.
        top_bar = QHBoxLayout()

        # the first filter is the dropdown that specifies what kind of filters you want.
        # TODO: Update this as needed
        self.filter_dropdown = QComboBox()
        self.filter_dropdown.addItems([
            "All Files",
            "Files older than 1 month",
            "Files older than 6 months",
            "Files larger than 10MB"
        ])

        # the second filter is the checkbox that indicates whether the files will be MOVED or COPIED during
        # the archiving process
        self.retain_checkbox = QCheckBox("Retain Original Files?")

        # this is where we add the filters to the "ribbon"
        top_bar.addWidget(self.filter_dropdown)
        top_bar.addWidget(self.retain_checkbox)

        # and finally we add the ribbon to the main vertical stack layout
        layout.addLayout(top_bar)

        # this is a splitter and helps arrange the controls horizontally.
        # it also allows the user to resize the file explorer and directory list
        splitter = QSplitter(Qt.Horizontal)

        # this is a file system model. it is passed to the tree view to
        # initialize it. it also specifies the "folders-only" mode that hides files.
        self.file_model = QFileSystemModel()
        self.file_model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
        self.file_model.setRootPath("")  # root of file system

        # this is the tree view control. it is used to browse the folders for targetted archiving
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(""))
        self.tree_view.doubleClicked.connect(self.add_to_list)          # convenient way to add click event for dir selection. calls class method to add.
        self.tree_view.setSelectionMode(QTreeView.SingleSelection)
        splitter.addWidget(self.tree_view)

        # this is the list that displays the targetted directories.
        # to remove a directory, use the Delete key.
        # a custom context menu can be created for this if additional functionality is necessary per directory.
        self.selected_list = QListWidget()
        self.selected_list.keyPressEvent = self.key_press_event_override
        splitter.addWidget(self.selected_list)

        # finally, we add the splitter back to the vertical stack
        layout.addWidget(splitter)

        # action button that starts the archive process
        self.go_button = QPushButton("Start Archiving")
        self.go_button.clicked.connect(self.process_files)
        layout.addWidget(self.go_button)

    # member helper function to add a directory to the target list.
    # the QModelIndex parameter is passed from the tree view control
    # and used to get the index of the selected folder.
    def add_to_list(self, index: QModelIndex):
        # get the actual path from the selected item
        path = self.file_model.filePath(index)

        # ensure that the selected item is a folder (redundant) and that it
        # doesn't already exist in the target list
        if self.file_model.isDir(index) and not self.is_in_list(path):
            self.selected_list.addItem(path)

    # helper function for determining existance in the target list.
    # honestly there is probably a list-type function that can do this better.
    def is_in_list(self, path):
        for i in range(self.selected_list.count()):
            if self.selected_list.item(i).text() == path:
                return True
        return False

    # keypress event handler for the target list. we just
    # care about intercepting the Delete key so the items get removed
    def key_press_event_override(self, event):
        # verify which key was pressed
        if event.key() == Qt.Key_Delete:
            
            # locate/purge the doomed item
            for item in self.selected_list.selectedItems():
                self.selected_list.takeItem(self.selected_list.row(item))
        else:
            # important to call super. this allows for arrow key navigation.
            # this is typical of event-driven programming for GUIs. we intercept
            # the events we care about (like delete key presses), then fallback
            # to a default behavior (like calling super)
            super(QListWidget, self.selected_list).keyPressEvent(event)

    # this is where you hook up to the file archiving logic. reference the filter parameters
    # and get after the files!
    def process_files(self):
        targetDirectories = [self.selected_list.item(i).text() for i in range(self.selected_list.count())]
        retain_original = self.retain_checkbox.isChecked()
        filter_option = self.filter_dropdown.currentText()

        print("Target Directories:", targetDirectories)
        print("Retain Original Files:", "YES" if retain_original else "NO")
        print("File Age Filter:", filter_option)

        # TODO: Loop over the target directories and call file archive logic here. Add your module to this one. Try to keep "main.py" clean.

# **********************************************************