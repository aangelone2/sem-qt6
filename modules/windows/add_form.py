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
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton,\
        QCalendarWidget, QLabel, QGroupBox, QMessageBox,\
        QLineEdit
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout

from pandas import DataFrame

import modules.common as common



af_width = 400



class add_form(QWidget):
    """
    Form to obtain info about new elements

    Attributes
    -----------------------
    __cal : QCalendarWidget
        Calendar to select the date for the expense
    __txt_type : QLineEdit
        Textbox for the expense type
    __txt_amount : QLineEdit
        Textbox for the expense amount
    __txt_justif : QLineEdit
        Textbox for the expense justification
    __but_accept : QPushButton
        Button to accept specified details

    Public methods
    -----------------------
    __init__()
        Constructor

    Private methods
    -----------------------
    __init_widgets() -> QVboxLayout
        Initializes widget layout, sets up validators
    __init_connections()
        Sets up connections between widgets

    Signals
    -----------------------
    insertion_requested[DataFrame]
        Broadcasts record to add to the database
        Transmits a DataFrame containing the fields

    Private slots
    -----------------------
    __request_insertion():
        Fetches query details from widgets
        Emits signal passing details as dictionary
        Sets focus on the calendar

    Connections
    -----------------------
    __cal.selectionChanged()
        -> __txt_type.setFocus
    __txt_type.editingFinished()
        -> __txt_amount.setFocus
    __txt_amount.editingFinished()
        -> __txt_justif.setFocus
    __txt_justif.editingFinished()
        -> __but_accept.setFocus
    __but_accept.clicked()
        -> __request_insertion
        -> insertion_requested[data]
    """

    def __init__(self):
        """
        Constructor

        Arguments
        -----------------------
        conn
            Connection to table/database pair
        """

        super().__init__()

        self.__cal = None
        self.__txt_type = None
        self.__txt_amount = None
        self.__txt_justif = None
        self.__but_accept = None

        self.setMaximumWidth(af_width)

        self.setLayout(self.__init_widgets())

        self.__init_connections()



    def __init_widgets(self) -> QVBoxLayout:
        """
        Initializes widget layout, sets up validators

        Return value
        -----------------------
        Returns the layout with the initialized widgets
        """

        # calendar
        self.__cal = QCalendarWidget(self)
        self.__cal = common.lock_size(self.__cal)
        self.__cal = common.set_font_size(self.__cal, 18)

        # type textbox
        self.__txt_type = QLineEdit(self)

        # amount textbox
        self.__txt_amount = QLineEdit(self)

        # justification textbox
        self.__txt_justif = QLineEdit(self)

        self.__but_accept = QPushButton('Add expense', self)

        # new entry details
        lay_det = QVBoxLayout()
        lay_det.addWidget(self.__cal)
        lay_det.addSpacing(25)

        lab_type = QLabel('Type', self)
        lab_type.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay_det.addWidget(lab_type)
        lay_det.addSpacing(-25)
        lay_det.addWidget(self.__txt_type)
        lay_det.addSpacing(25)

        lab_amount = QLabel('Amount', self)
        lab_amount.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay_det.addWidget(lab_amount)
        lay_det.addSpacing(-25)
        lay_det.addWidget(self.__txt_amount)
        lay_det.addSpacing(25)

        lab_justif = QLabel('Justification', self)
        lab_justif.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay_det.addWidget(lab_justif)
        lay_det.addSpacing(-25)
        lay_det.addWidget(self.__txt_justif)

        gb = QGroupBox('Entry details', self)
        gb.setLayout(lay_det)

        # general layout
        lay = QVBoxLayout()
        lay.addWidget(gb)
        lay.addSpacing(50)
        lay.addWidget(self.__but_accept)

        return lay



    def __init_connections(self):
        """
        Inits connections
        """

        # each widget leaves focus to the following one
        self.__cal.selectionChanged.connect(
                self.__txt_type.setFocus
        )
        self.__txt_type.editingFinished.connect(
                self.__txt_amount.setFocus
        )
        self.__txt_amount.editingFinished.connect(
                self.__txt_justif.setFocus
        )
        self.__txt_justif.editingFinished.connect(
                self.__but_accept.setFocus
        )

        self.__but_accept.clicked.connect(
                self.__request_insertion
        )



    insertion_requested = pyqtSignal(DataFrame)
    """
        Broadcasts record to add to the database
        Transmits a DataFrame containing the fields
    """



    @QtCore.pyqtSlot()
    def __request_insertion(self):
        """
        Sets focus on the calendar
        Fetches query details from widgets
        Emits signal passing details as dictionary
        """

        self.__cal.setFocus()

        date = self.__cal.selectedDate().toString(
                format = Qt.DateFormat.ISODate
        )

        # single-row DataFrame, still works
        df = DataFrame({
            'date': [date],
            'type': [self.__txt_type.text()],
            'amount': [self.__txt_amount.text()],
            'justification': [self.__txt_justif.text()]
        })

        self.insertion_requested.emit(df)
