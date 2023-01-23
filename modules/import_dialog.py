# Copyright (c) 2023 Adriano Angelone
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


import pandas as pd
from pandas import DataFrame as dataframe

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QWidget, QDialog,\
        QDialogButtonBox, QFileDialog
from PyQt6.QtWidgets import QVBoxLayout

import modules.common as common
import modules.db as db
from modules.cqwidgets import CQTableWidget


isd_width = 800
isd_height = 500




class import_dialog(QDialog):
    """
    Form to display imported CSV files

    Attributes
    -----------------------
    __df : dataframe
        Stores the imported data
    __table : QTableWidget
        Table showing the imported data
    __buttons : QDialogButtonBox
        Ok/Cancel buttons

    Methods
    -----------------------
    __init__(parent: QWidget)
        Constructor
    __init_widgets() -> QVBoxLayout
        Sets up widgets, returns the layout containing them

    Signals
    -----------------------
    import_requested[dataframe]
        Broadcasts the request for importing in the database

    Slots
    -----------------------
    load()
        Allows the user to select a CSV file,
        loads it in the member dataframe
        and displays it in the table
    accept()
        Emits `import_requested` with the stored dataframe

    Connections
    -----------------------
    __buttons.accepted
        -> accept()
        -> import_requested[self.__df]
    __buttons.rejected -> reject()
    """

    def __init__(self, parent: QWidget):
        """
        Constructor
        """

        super().__init__(parent)

        self.__df = None
        self.__table = None
        self.__buttons = None

        self.resize(isd_width, isd_height)

        lay = self.__init_widgets()

        self.__init_connections()

        self.setLayout(lay)




    def __init_widgets(self) -> QVBoxLayout:
        """
        Sets up widgets and layouts

        Return value
        -----------------------
        Returns the layout with the initialized widgets
        """

        self.__table = CQTableWidget(self)

        self.__buttons = QDialogButtonBox(
                QDialogButtonBox.StandardButton.Ok
                | QDialogButtonBox.StandardButton.Cancel
        )

        lay = QVBoxLayout()
        lay.addWidget(self.__table)
        lay.addWidget(self.__buttons)

        return lay




    def __init_connections(self):
        """
        Inits connections
        """

        self.__buttons.accepted.connect(self.accept)
        self.__buttons.rejected.connect(self.reject)




    import_requested = pyqtSignal(dataframe)
    """
    Broadcasts import request

    Arguments
    -----------------------
    df : dataframe
        The dataframe to bulk-import in the database
    """




    @QtCore.pyqtSlot()
    def load(self):
        """
        Allows the user to select a CSV file,
        loads it in the member dataframe
        and displays it in the table
        """

        filename = QFileDialog.getOpenFileName(
                self,
                'Select file to import',
                None,
                'CSV files (*.csv)'
        )[0]

        if (filename == ''):
            return

        self.show()

        try:
            self.__df = db.parse_csv(filename)
        except db.DatabaseError:
            common.ErrorMsg('file error')

        self.__table.fill(self.__df)




    @QtCore.pyqtSlot()
    def accept(self):
        """
        Emits a signal carrying the stored dataframe
        for importing in the database
        """
        self.import_requested.emit(self.__df)
        self.hide()