# Copyright (c) 2022 Adriano Angelone
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the
# Software.
#
# This file is part of sem.
# 
# This file may be used under the terms of the GNU General
# Public License version 3.0 as published by the Free Software
# Foundation and appearing in the file LICENSE included in the
# packaging of this file.  Please review the following
# information to ensure the GNU General Public License version
# 3.0 requirements will be met:
# http://www.gnu.org/copyleft/gpl.html.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from PyQt6 import QtCore
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QWidget, QApplication,\
        QToolBar, QFileDialog, QLineEdit
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout

from modules.Common import ErrorMsg
from modules.ModelWrapper import ModelWrapper

from modules.ListForm import ListForm



MAIN_WINDOW_WIDTH = 1200
MAIN_WINDOW_HEIGHT = 400



class MainWindow(QMainWindow):
    """
    Main program window

    Attributes
    -----------------------
    __models: ModelWrapper
        Wrapper for list and sum models
    __formLst : ListForm
        Internal list_form widget
    __actCreate : QAction
        The action of creating a new database
    __actOpen : QAction
        The action of logging in to a new database
    __actExport : QAction
        The action of saving the database to an external file
    __actClose : QAction
        Logs the user out

    Public methods
    -----------------------
    __init__()
        Constructor

    Private methods
    -----------------------
    __initForms()
        Inits the forms and the layout which contains them
    __initDialogs()
        Inits dialogs
    __initToolbar()
        Inits toolbar and the contained actions
    __initConnections()
        Inits form and dialog connections
    __initTbConnections()
        Inits connections of toolbar actions

    Private slots
    -----------------------
    __requestCreate()
        Attempts creation of database
    __requestOpen()
        Attempts to open existing database
    __requestExport()
        Collects filename from user and dumps database
    __closeDB()
        Closes current database

    Connections
    -----------------------
    __formLst.queryRequested[start, end]
        -> __models.updateModel(start, end)
    __actCreate.triggered
        -> __requestCreate()
    __actOpen.triggered
        -> __requestOpen()
    __actExport.triggered
        -> __requestExport()
    __actClose.triggered
        -> __closeDB()
    """

    def __init__(self):
        """
        Constructor
        """

        super().__init__()

        self.__models = None
        self.__formLst = None
        self.__actCreate = None
        self.__actOpen = None
        self.__actExport = None
        self.__actClose = None

        # set to narrow size by default
        self.resize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        # setting window title
        self.setWindowTitle('Simple Expense Manager')

        # initializing form
        self.__formLst = ListForm(self)
        # initializing toolbar
        self.__initToolbar()

        self.setCentralWidget(self.__formLst)

        self.__initConnections()
        self.__initTbConnections()



    def __initToolbar(self):
        """
        Inits toolbar and the contained actions
        """

        self.menuBar() = QToolBar(self)
        self.menuBar().setIconSize(QSize(30, 30))

        self.__actCreate = QAction(QIcon('resources/create.png'), 'Create', self)
        self.__actCreate.setToolTip('Create new database')

        self.__actOpen = QAction(QIcon('resources/open.png'), 'Open', self)
        self.__actOpen.setToolTip('Open existing database')

        self.__actExport = QAction(QIcon('resources/export.png'), 'Export', self)
        self.__actExport.setToolTip('Export database to CSV file')

        self.__actClose = QAction(QIcon('resources/close.png'), 'Close', self)
        self.__actClose.setToolTip('Close current database')

        self.__tb.addAction(self.__actCreate)
        self.__tb.addAction(self.__actOpen)
        self.__tb.addSeparator()
        self.__tb.addAction(self.__actExport)
        self.__tb.addSeparator()
        self.__tb.addAction(self.__actClose)



    def __initConnections(self):
        """
        Inits form and dialog connections
        """

        self.__formLst.queryRequested.connect(
                lambda s,e: __models.updateModel(s,e)
        )



    def __initTbConnections(self):
        """
        Inits connections of toolbar actions
        """

        # create action
        self.__actCreate.triggered.connect(
                self.__requestCreate
        )

        # open action
        self.__actOpen.triggered.connect(
                self.__requestOpen
        )

        # request exporting to CSV
        self.__actExport.triggered.connect(
                self.__requestExport
        )

        # close current database
        self.__actClose.triggered.connect(
                self.__closeDB
        )



    @QtCore.pyqtSlot()
    def __requestCreate(self):
        """
        Attempts creation of database
        """

        filename = QFileDialog.getSaveFileName(
                self,
                'Select name for new database',
        )[0]

        if (filename == ''):
            return

        try:
            self.__models.createDB(filename)
        except DatabaseError as err:
            ErrorMsg(err)
            return
        
        self.__models.initModel()



    @QtCore.pyqtSlot()
    def __requestOpen(self):
        """
        Attempts to open database
        """

        filename = QFileDialog.getOpenFileName(
                self,
                'Select database to access'
        )[0]

        if (filename == ''):
            return

        try:
            self.__models.openDB(filename)
        except DatabaseError as err:
            ErrorMsg(err)
            return

        self.__models.initModel()



    @QtCore.pyqtSlot()
    def __requestExport(self):
        """
        Collects filename from user and dumps database
        """

        filename = QFileDialog.getSaveFileName(
                self,
                'Specify file for exporting',
                None,
                'CSV files (*.csv)'
        )[0]

        if (filename == ''):
            return

        try:
            self.__models.saveCSV(filename)
        except DatabaseError as err:
            ErrorMsg(err)
            return



    @QtCore.pyqtSlot()
    def __closeDB(self):
        """
        Logs out from current database
        """

        self.__models.closeDB()
