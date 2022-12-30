# Copyright (c) 2022 Adriano Angelone
# 
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the
# Software.
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
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QSize

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton,\
        QCalendarWidget, QTableWidget, QTableWidgetItem
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout,\
        QSizePolicy

import sqlite3
import pandas as pd
import logging

import modules.common as common




# form to display and summarize records
class list_form(QWidget):
    """
    Form to display and summarize records


    Attributes
    -----------------------
    __cal_start : QCalendarWidget
        QCalendarWidget used to select start date in queries
    __cal_end : QCalendarWidget
        QCalendarWidget used to select end date in queries
    __but_update : QPushButton
        Updates the tables based on selected dates.
        Also refreshes expense categories
    __tab_list : QTableWidget
        Contains the expenses with dates between the two
        selected dates, lists all fields
    __tab_sum : QTableWidget
        Contains the sum of the expenses with dates between the
        two selected dates, grouped by category


    Methods
    -----------------------
    __init_lay_cal() -> QVBoxLayout
        Returns the initialized calendar + button layout
    __init_lay_tab() -> QVBoxLayout
        Returns the initialized table layout, empty tables
    __init_connections() -> None
        Inits connections


    Signals
    -----------------------
    query_requested(str, str)
        Broadcasts expense list request


    Slots
    -----------------------
    __request_query(str, str)
        emits signal with start and end date as arguments

    update_tables(pd.DataFrame)
        updates the tables from a provided dataframe


    Application logic
    -----------------------
    __but_update.clicked
        -> __request_query()
        -> query_requested(start_date, end_date)
        -> ...
        -> update_tables(df)
    """


    def __init__(self):
        """
        Constructor
        """

        super().__init__()

        self.__cal_start = None
        self.__cal_end = None
        self.__but_update = None
        self.__tab_list = None
        self.__tab_sum = None

        lay_cal = self.__init_lay_cal()
        lay_tab = self.__init_lay_tab()
        self.__init_connections()

        # generating main layout
        lay_gen = QHBoxLayout()
        lay_gen.addSpacing(100)
        lay_gen.addLayout(lay_cal)
        lay_gen.addSpacing(100)
        lay_gen.addLayout(lay_tab)
        lay_gen.addSpacing(100)

        # no show(), will be loaded from the main
        self.setLayout(lay_gen)


    def __init_lay_cal(self) -> QVBoxLayout:
        """
        Returns the initialized calendar + button layout
        """

        # start date label
        lab_start = QLabel('Start date [included]', self)
        lab_start.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lab_start = common.set_font_size(lab_start, 20)

        # start date calendar
        self.__cal_start = QCalendarWidget(self)
        self.__cal_start = common.lock_size(self.__cal_start)
        self.__cal_start = common.set_font_size(self.__cal_start, 16)

        # end date label
        lab_end = QLabel('End date [included]', self)
        lab_end.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lab_end = common.set_font_size(lab_end, 20)

        # end date calendar
        self.__cal_end = QCalendarWidget(self)
        self.__cal_end = common.lock_size(self.__cal_end)
        self.__cal_end = common.set_font_size(self.__cal_end, 16)

        # update button (graphical setup)
        self.__but_update = QPushButton('Update', self)
        self.__but_update = common.set_font_size(self.__but_update, 20)

        # setting up layout
        lay = QVBoxLayout()
        lay.addSpacing(50)
        lay.addWidget(lab_start)
        lay.addWidget(self.__cal_start)
        lay.addSpacing(50)
        lay.addWidget(lab_end)
        lay.addWidget(self.__cal_end)
        lay.addSpacing(50)
        lay.addWidget(self.__but_update)
        lay.addSpacing(50)

        return lay


    def __init_lay_tab(self) -> QVBoxLayout:
        """
        Returns the initialized table layout, empty tables
        """

        # expense list table
        self.__tab_list = QTableWidget(0, 5, self)
        # hide record index number in the record table
        self.__tab_list.verticalHeader().hide()
        # set header names in the record table
        self.__tab_list.setHorizontalHeaderLabels(
            ['ID', 'Date', 'Type', 'Amount', 'Justification']
        )
        
        # column and font behavior
        self.__tab_list = common.set_tw_behavior(self.__tab_list, 'equal')
        self.__tab_list = common.set_font_size(self.__tab_list, 18)
        self.__tab_list.horizontalHeader().setStyleSheet(
                'QHeaderView {font-size: 20px}'
        )

        # label for sum table
        label = QLabel('Total', self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label = common.set_font_size(label, 20)

        # sum table
        self.__tab_sum = QTableWidget(1, 0, self)
        self.__tab_sum.setMaximumHeight(58)
        # hide record index number in the sum table
        self.__tab_sum.verticalHeader().hide()

        # column and font behavior
        self.__tab_sum = common.set_tw_behavior(self.__tab_sum, 'equal')
        self.__tab_sum = common.lock_height(self.__tab_sum)
        self.__tab_sum = common.set_font_size(self.__tab_sum, 18)
        self.__tab_sum.horizontalHeader().setStyleSheet(
                'QHeaderView {font-size: 20px}'
        )

        # setting up layout
        lay = QVBoxLayout()
        lay.addWidget(self.__tab_list)
        lay.addSpacing(50)
        lay.addWidget(label)
        lay.addSpacing(10)
        lay.addWidget(self.__tab_sum)

        return lay


    def __init_connections(self):
        """
        Inits connections
        """

        self.__but_update.clicked.connect(self.__request_query)


    ####################### SIGNALS #######################

    query_requested = pyqtSignal(str, str)
    """
    Broadcasts expense list request

    Arguments
    -----------------------
    start_date : str
        starting date for the requested query, 'yyyy-mm-dd'
    end_date : str
        ending date for the requested query, 'yyyy-mm-dd'
    """


    ####################### SLOTS #######################

    @QtCore.pyqtSlot()
    def __request_query(self):
        """
        Emits signal with start and end date as arguments
        """

        fmt = Qt.DateFormat.ISODate
        start_date = self.__cal_start.selectedDate().toString(fmt)
        end_date = self.__cal_end.selectedDate().toString(fmt)

        self.query_requested.emit(start_date, end_date)


    @QtCore.pyqtSlot(pd.DataFrame)
    def update_tables(self, df: pd.DataFrame):
        """
        updates the tables from a provided dataframe

        Arguments
        -----------------------
        df : pd.DataFrame
            dataframe used to fill the tables; __tab_sum will
            only contain categories present in df
        """

        logging.info('update_tables() -> in update_tables')

        # clearing expense list
        self.__tab_list.setRowCount(0)

        self.__tab_list = common.set_tw_behavior(self.__tab_list, 'auto')
        # sets last column in self.__tab_list to take all available space
        self.__tab_list.horizontalHeader().setStretchLastSection(True)

        # filling expense table
        for ir, row in df.iterrows():
            self.__tab_list.insertRow(ir)

            for ic, (field, val) in enumerate(row.items()):
                itm = QTableWidgetItem(str(val))
                if (field != 'justification'):
                    itm.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # greying odd rows
                if (ir % 2 == 1):
                    itm.setBackground(common.colors['lightgray'])

                self.__tab_list.setItem(ir, ic, itm)

        # clearing sum table
        self.__tab_sum.setColumnCount(0)

        # computing sums
        asum = df.groupby('type').sum()

        logging.info('{}'.format(asum))

        try:
            asum = asum['amount']

            # filling sum table
            for ic, val in enumerate(asum):
                self.__tab_sum.insertColumn(ic)

                itm = QTableWidgetItem(str(val))
                itm.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # greying odd columns
                if (ic % 2 == 1):
                    itm.setBackground(common.colors['lightgray'])

                self.__tab_sum.setItem(0, ic, itm)

            # setting header names to the ones in the current df
            self.__tab_sum.setHorizontalHeaderLabels(asum.index.to_list())
        except KeyError:
            # empty result set
            pass