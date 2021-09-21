import os
import sys
import traceback

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMenuBar
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QRect
from PyQt6 import uic
from tabulate import tabulate


from harp_helper import constants
from harp_helper.harps import Harmonica
from harp_helper import music


MAX_FILE_LABEL_TEXT = 65
WINDOW_MARGIN = 20
WINDOW_FOOTER = 20

current_path = os.path.dirname(__file__)
main_ui = os.path.join(current_path, 'ui', 'main_window.ui')
explorer_ui = os.path.join(current_path, 'ui', 'explorer_widget.ui')
message_ui = os.path.join(current_path, 'ui', 'message_widget.ui')


class HarpHelperUi(QMainWindow):

    app = QApplication(sys.argv)

    def gui_exception_handler(func):
        """Decorator for showing exceptions in a message box"""
        def exception_wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except:
                self.open_message(
                    "FATAL ERROR: Traceback",
                    traceback.format_exc()
                )
        return exception_wrapper

    def __init__(self):
        super().__init__()
        uic.loadUi(main_ui, self)
        self.last_dir = os.getenv('HOME')
        self._tab_source_file_name = ""

        # Main Window Appearance
        self.setWindowTitle(constants.FULL_RELEASE_NAME)
        self.add_menu_bar()
        self.update_harps()
        self.chartBox.addItems(('Tune', 'Transpose'))
        self.sourceKeyCheckBox.setChecked(False)
        self.update_tab_source_keys()
        self.outputComboBox.addItems(('table', 'csv'))

        # Perform connections
        self.main_window_connections()

        # Placeholders for child windows
        self.explorer = None
        self.message = None

    @classmethod
    def exec(cls):
        sys.exit(cls.app.exec())

    def add_menu_bar(self):

        # Exit
        exitAction = QAction("Depart", self)
        exitAction.setShortcut("Ctrl+D")
        exitAction.setStatusTip(f"Exit App")
        exitAction.triggered.connect(self.menu_exit)

        # Save Output
        saveAction = QAction("&Save Output", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setStatusTip("Save the current output to a file")
        saveAction.triggered.connect(self.save_output_dialog)

        # HelpNotation
        notationAction = QAction("Notation", self)
        notationAction.setStatusTip("Music expression notation help")
        notationAction.triggered.connect(self.help_notation_message)

        self.statusBar()

        mainMenu = QMenuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(saveAction)
        helpMenu = mainMenu.addMenu('Help')
        helpMenu.addAction(notationAction)
        self.setMenuBar(mainMenu)

    def main_window_connections(self):
        # Chart Widgets
        self.generateChartButton.clicked.connect(self.report_button_click)
        # Tab Widgets
        self.goButton.clicked.connect(self.go_button_click)
        self.sourceExpressionButton.clicked.connect(self.update_source_music_group)
        self.sourceFileButton.clicked.connect(self.tab_file_radio_button_click)
        self.sourceKeyCheckBox.stateChanged.connect(self.update_tab_source_keys)
        self.fileExplorerButton.clicked.connect(self.open_file_dialog)
        # --- Keep source key sync'd with harp key if unchecked!
        self.harpKeyBox.currentIndexChanged.connect(self.update_tab_source_keys)
        # General Widgets
        self.typeBox.currentTextChanged.connect(self.update_harp_keys)

    def resizeEvent(self, *args, **kwargs):
        """Override the main window resizeEvent to resize window contents"""

        # Call the event to perform the main window resize
        QMainWindow.resizeEvent(self, *args, **kwargs)

        # Recenter the harp widgets
        self.harpGroupBox.setGeometry(QRect(
            (self.geometry().width() - self.harpGroupBox.geometry().width()) // 2,
            self.harpGroupBox.geometry().y(),
            self.harpGroupBox.geometry().width(),
            self.harpGroupBox.geometry().height()
        ))

        # Resize the tabWidget
        self.tabWidget.setGeometry(QRect(
            WINDOW_MARGIN,
            self.tabWidget.geometry().y(),
            self.geometry().width() - WINDOW_MARGIN * 2,
            self.geometry().height() - self.tabWidget.geometry().y() - WINDOW_MARGIN - WINDOW_FOOTER))

        # Recenter the chart widgets
        self.chartWidgetGroupBox.setGeometry(QRect(
            (self.tabWidget.geometry().width() - self.chartWidgetGroupBox.geometry().width()) // 2,
            self.chartWidgetGroupBox.geometry().y(),
            self.chartWidgetGroupBox.geometry().width(),
            self.chartWidgetGroupBox.geometry().height()
        ))
        # Resize the Chart Browser
        self.chartBrowser.setGeometry(QRect(
            WINDOW_MARGIN,
            self.chartBrowser.geometry().y(),
            self.tabWidget.geometry().width() - WINDOW_MARGIN * 2,
            self.tabWidget.geometry().height() - self.chartBrowser.geometry().y() - WINDOW_MARGIN - WINDOW_FOOTER
        ))

        # Recenter the tablature widgets
        self.tabWidgetGroupBox.setGeometry(QRect(
            (self.tabWidget.geometry().width() - self.tabWidgetGroupBox.geometry().width()) // 2,
            self.tabWidgetGroupBox.geometry().y(),
            self.tabWidgetGroupBox.geometry().width(),
            self.tabWidgetGroupBox.geometry().height()
        ))
        # Resize the tablature Browser
        self.tabBrowser.setGeometry(QRect(
            WINDOW_MARGIN,
            self.tabBrowser.geometry().y(),
            self.tabWidget.geometry().width() - WINDOW_MARGIN * 2,
            self.tabWidget.geometry().height() - self.tabBrowser.geometry().y() - WINDOW_MARGIN - WINDOW_FOOTER
        ))

    def update_harps(self):
        self.typeBox.clear()
        for harp_type in Harmonica.types():
            harp = Harmonica(harp_type, 'c')
            self.typeBox.addItem(harp.harmonica_description, harp_type)
        self.update_harp_keys()

    def update_source_music_group(self):
        if self.sourceExpressionButton.isChecked():
            self.expressionEdit.setEnabled(True)
        else:
            self.expressionEdit.setEnabled(False)
            self.expressionEdit.setText("")

    def update_harp_keys(self):
        self.harpKeyBox.clear()
        harp_type = self.typeBox.currentData()
        for key in Harmonica(harp_type, 'c').keys_available:
            self.harpKeyBox.addItem(music.NoteParser(key).musical_name, key)
        self.update_tab_source_keys()

    def update_tab_source_keys(self):
        # all_notes = set(music.FLAT_NOTE_ORDER + music.SHARP_NOTE_ORDER)
        self.sourceKeyBox.clear()
        if self.sourceKeyCheckBox.isChecked():
            for key in music.KEYS:
                self.sourceKeyBox.addItem(
                    music.NoteParser(key).musical_name,
                    key
                )
            self.sourceKeyBox.setEnabled(True)
            self.transposeDirectionRadioButtons.setEnabled(True)
        else:
            self.sourceKeyBox.addItem(
                self.harpKeyBox.currentText(),
                self.harpKeyBox.currentData()
            )
            self.sourceKeyBox.setEnabled(False)
            self.transposeDirectionRadioButtons.setEnabled(False)

    # \\\\\\\ signal handlers ///////

    @gui_exception_handler
    def go_button_click(self, *args):

        self.tabBrowser.clear()

        harp = Harmonica(
            harmonica_type=self.typeBox.currentData(),
            harmonica_key=self.harpKeyBox.currentData()
        )

        details = []
        for source_notes in self.generate_tab_notation_from_source():

            expression = music.MusicExpression(source_notes, key=self.sourceKeyBox.currentData())

            if self.transposeSpinner.value() != 0:
                expression.transpose_half_steps(self.transposeSpinner.value())

            if self.transposeDownButton.isChecked():
                direction = "down"
            elif self.transposeUpButton.isChecked():
                direction = "up"
            else:
                direction = "closest"
            if self.sourceKeyCheckBox.isChecked():
                expression.transpose_to_key(
                    key=self.harpKeyBox.currentData(),
                    direction=direction
                )

            # Create the notation
            phrase = " &diams; ".join(harp.get_notation(expression.notation_list))
            details.append(phrase.replace("<", "&lt;"))

        self.tabBrowser.setText("\n<br>\n".join(details))

    @gui_exception_handler
    def report_button_click(self, *args):
        chart_type = self.chartBox.currentText()
        if chart_type == "Tune":
            harp = Harmonica(
                harmonica_type=self.typeBox.currentData(),
                harmonica_key=self.harpKeyBox.currentData()
            )
            output = harp.tuning_chart(output_format=self.outputComboBox.currentText())
        else:
            output = self.create_transposing_charts()
        self.chartBrowser.setText(output)


    @gui_exception_handler
    def tab_file_radio_button_click(self, *args):
        if not self.sourceFileLabel.text().strip():
            self.open_file_dialog()
        if not self.sourceFileLabel.text().strip():
            self.sourceExpressionButton.setChecked(True)

    @gui_exception_handler
    def menu_save(self, *args):
        raise NotImplementedError("Feature 'Save Output' not supported")

    def menu_exit(self):
        self.close()

    @gui_exception_handler
    def help_notation_message(self):
        self.open_message(title="Help: Music Notation", message=constants.NOTATION_HELP, html=True)

    # \\\\\\\ Helper Functions For Main Window ///////

    def generate_tab_notation_from_source(self):
        """Generator for yielding tab notation"""
        if self.sourceExpressionButton.isChecked():
            yield self.expressionEdit.text()
        else:
            with open(self._tab_source_file_name, "r") as fh:
                line = fh.readline()
                while line:
                    notation = line.partition("#")[0].strip()
                    if len(notation) > 0:
                        yield line.strip()
                    line = fh.readline()

    def update_file_source_label(self, label_text):
        """Updates tab source file (concatenates as needed)"""
        if len(label_text) <= MAX_FILE_LABEL_TEXT:
            self.sourceFileLabel.setText(label_text)
            return
        source_dir = os.path.dirname(label_text)
        source_base = os.path.basename(label_text)
        if len(source_base) > MAX_FILE_LABEL_TEXT - 4:
            self.sourceFileLabel.setText(f".../{source_base}")
            return
        concat_dir = source_dir[:MAX_FILE_LABEL_TEXT - len(source_base) - 3]
        self.sourceFileLabel.setText(f"{concat_dir}.../{source_base}")

    def create_transposing_charts(self) -> str:
        chart_outputs = []
        for key in music.KEYS:
            harp = Harmonica(
                harmonica_type=self.typeBox.currentData(),
                harmonica_key=key
            )
            chart_outputs.append(f"Source music: {music.NoteParser(key).musical_name}")
            chart_outputs.append(harp.tuning_chart(output_format=self.outputComboBox.currentText()))
            chart_outputs.append("")
        return "\n".join(chart_outputs)

    # \\\\\\\ File Dialog ///////

    def open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select Music File",
            directory=self.last_dir
        )
        if not filename:
            return
        self.last_dir = os.path.dirname(filename)
        self._tab_source_file_name = filename
        self.update_file_source_label(filename)
        self.sourceFileButton.setChecked(True)
        if not self.sourceFileLabel.text():
            self.sourceExpressionButton.setChecked(True)

    def save_output_dialog(self):
        filename, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save output",
            directory=self.last_dir
        )
        if not filename:
            print("cancelled")
            return
        self.last_dir = os.path.dirname(filename)
        tabs = (self.chartBrowser, self.tabBrowser)
        with open(filename, "w") as fh:
            fh.write(tabs[self.tabWidget.currentIndex()].toPlainText())

    # \\\\\\\ Scrolling Message Box ///////

    def open_message(self, title: str = "MESSAGE", message: str = "?", html: bool = False):
        self.message = QWidget()
        uic.loadUi(message_ui, self.message)
        self.message.okButton.clicked.connect(self.close_message)
        self.message.setWindowTitle(title)
        if html:
            self.message.textBrowser.setHtml(message)
        else:
            self.message.textBrowser.setText(message)
        self.message.resizeEvent = self.message_window_resize
        self.message.show()

    def message_window_resize(self, *args, **kwargs):
        QMainWindow.resizeEvent(self, *args, **kwargs)

        #  Relocate Ok button
        self.message.okButton.setGeometry(QRect(
            (self.message.geometry().width() - self.message.okButton.geometry().width()) // 2,
            self.message.geometry().height() - self.message.okButton.geometry().height() - WINDOW_MARGIN - WINDOW_FOOTER,
            self.message.okButton.geometry().width(),
            self.message.okButton.geometry().height()
        ))

        # Text Browser
        self.message.textBrowser.setGeometry(QRect(
            WINDOW_MARGIN,
            WINDOW_MARGIN,
            self.message.geometry().width() - WINDOW_MARGIN * 2,
            self.message.okButton.geometry().y() - WINDOW_MARGIN * 2
        ))

    def close_message(self):
        self.message.close()
        self.message = None


def main():
    harp_helper = HarpHelperUi()
    harp_helper.show()
    harp_helper.exec()


if __name__ == "__main__":
    main()
