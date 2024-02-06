# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QPushButton, QSizePolicy,
    QStackedWidget, QTextEdit, QVBoxLayout, QWidget)

from modules.pages.exporter import Exporter
from modules.pages.generator import Generator
from widgets.image_viewer.ImageViewer import ImageViewer
from .resources_rc import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(940, 716)
        MainWindow.setMinimumSize(QSize(940, 560))
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.styleSheet.setFont(font)
        self.styleSheet.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"\n"
"SET APP STYLESHEET - FULL STYLES HERE\n"
"DARK THEME - DRACULA COLOR BASED\n"
"\n"
"# BY: WANDERSON M.PIMENTA\n"
"# PROJECT MADE WITH: Qt Designer and PySide6\n"
"# V: 1.0.0\n"
"#\n"
"# This project can be used freely for all uses, as long as they maintain the\n"
"# respective credits only in the Python scripts, any information in the visual\n"
"# interface (GUI) can be modified without any implication.\n"
"#\n"
"# There are limitations on Qt licenses if you want to use your products\n"
"# commercially, I recommend reading them on the official website:\n"
"# https://doc.qt.io/qtforpython/licenses.html\n"
"\n"
"///////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"\n"
"QWidget{\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"QStackedWidget > QWidget{\n"
"	background : transparent;\n"
"}\n"
"\n"
"/* //////////////////////////"
                        "///////////////////////////////////////////////////////////////////////\n"
"Tooltip */\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(33, 37, 43, 180);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid #6cbfcf;\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Bg App */\n"
"#bgApp {	\n"
"	background-color: #282c34;\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Left Menu */\n"
"#leftMenuBg {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#topLogo {\n"
"	background-color: rgb(33, 37, 43);\n"
"	background-position: centered;\n"
"	background-repeat: no-repeat;\n"
"}\n"
"#titleLeftApp { font: 63 12pt \"Segoe U"
                        "I Semibold\"; }\n"
"#titleLeftDescription { font: 8pt \"Segoe UI\"; color: #8cbfca; }\n"
"\n"
"/* MENUS */\n"
"#topMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#topMenu .QPushButton:hover {\n"
"	background-color: #282c34;\n"
"}\n"
"#topMenu .QPushButton:pressed {	\n"
"	background-color: #8cbfca;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#bottomMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#bottomMenu .QPushButton:hover {\n"
"	background-color: #282c34;\n"
"}\n"
"#bottomMenu .QPushButton:pressed {	\n"
"	background-color: #8cbfca;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#leftMenuFrame{\n"
"	border-top: 3"
                        "px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Toggle Button */\n"
"#toggleButton {\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color: rgb(37, 41, 48);\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	color: rgb(113, 126, 149);\n"
"}\n"
"#toggleButton:hover {\n"
"	background-color: #282c34;\n"
"}\n"
"#toggleButton:pressed {\n"
"	background-color: #8cbfca;\n"
"}\n"
"\n"
"/* Title Menu */\n"
"#titleRightInfo { padding-left: 10px; }\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Extra Tab */\n"
"#extraLeftBox {	\n"
"	background-color: rgb(44, 49, 58);\n"
"}\n"
"#extraTopBg{	\n"
"	background-color: #8cbfca\n"
"}\n"
"\n"
"/* Icon */\n"
"#extraIcon {\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"	background-image: url(:/icons/images/icons/icon_settings.png);\n"
"}\n"
"\n"
"/* Label */\n"
"#extraLabel { color: "
                        "rgb(255, 255, 255); }\n"
"\n"
"/* Btn Close */\n"
"#extraCloseColumnBtn { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#extraCloseColumnBtn:hover { background-color: #80c5d3; border-style: solid; border-radius: 4px; }\n"
"#extraCloseColumnBtn:pressed { background-color: #7bcdde; border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Extra Content */\n"
"#extraContent{\n"
"	border-top: 3px solid #282c34;\n"
"}\n"
"\n"
"/* Extra Top Menus */\n"
"#extraTopMenu .QPushButton {\n"
"background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#extraTopMenu .QPushButton:hover {\n"
"	background-color: #282c34;\n"
"}\n"
"#extraTopMenu .QPushButton:pressed {	\n"
"	background-color: #8cbfca;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* ///////////////////////////////////////////////////////////////////////////////////"
                        "//////////////\n"
"Content App */\n"
"#contentTopBg{	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#contentBottom{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Top Buttons */\n"
"#rightButtons .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#rightButtons .QPushButton:hover { background-color: rgb(44, 49, 57); border-style: solid; border-radius: 4px; }\n"
"#rightButtons .QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Theme Settings */\n"
"#extraRightBox { background-color: rgb(44, 49, 58); }\n"
"#themeSettingsTopDetail { background-color: #8cbfca; }\n"
"\n"
"/* Bottom Bar */\n"
"#bottomBar { background-color: rgb(44, 49, 58); }\n"
"#bottomBar QLabel { font-size: 11px; color: rgb(113, 126, 149); padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }\n"
"\n"
"/* CONTENT SETTINGS */\n"
"/* MENUS */\n"
"#contentSettings .QPushButton {	\n"
"	background-position: left cente"
                        "r;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#contentSettings .QPushButton:hover {\n"
"	background-color: #282c34;\n"
"}\n"
"#contentSettings .QPushButton:pressed {	\n"
"	background-color: #8cbfca;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"QTableWidget */\n"
"QTableWidget {	\n"
"	background-color: transparent;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: #8cbfca;\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: rgb(33, 37, 43);\n"
"	max-width: 30px;\n"
"	"
                        "border: 1px solid rgb(44, 49, 58);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(33, 37, 43);\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"LineEdit */\n"
"QLineEdit {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: #6cbfcf;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: "
                        "2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"PlainTextEdit */\n"
"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: #6cbfcf;\n"
"}\n"
"QPlainTextEdit  QScrollBar:vertical {\n"
"    width: 8px;\n"
" }\n"
"QPlainTextEdit  QScrollBar:horizontal {\n"
"    height: 8px;\n"
" }\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ScrollBars */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: #8cbfca;\n"
"    m"
                        "in-width: 25px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: #8c"
                        "bfca;\n"
"    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CheckBox */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width"
                        ": 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	background-image: url(:/icons/images/icons/cil-check-alt.png);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"RadioButton */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ComboBox "
                        "*/\n"
"QComboBox{\n"
"	background-color: rgb(52, 59, 72);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/images/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: repeat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: #6cbfcf;	\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Sliders */\n"
"QSl"
                        "ider::groove:horizontal {\n"
"    border-radius: 5px;\n"
"    height: 10px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: #8cbfca;\n"
"    border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: #9bf5ff;\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: #6cbfcf;\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 5px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: #8cbfca;\n"
"	border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
""
                        "    background-color: #9bf5ff;\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: #6cbfcf;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CommandLinkButton */\n"
"QCommandLinkButton {	\n"
"	color: #6cbfcf;\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"}\n"
"QCommandLinkButton:hover {	\n"
"	color: #aaf5ff;\n"
"	background-color: rgb(44, 49, 60);\n"
"}\n"
"QCommandLinkButton:pressed {	\n"
"	color: #8cbfca;\n"
"	background-color: rgb(52, 58, 71);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Button */\n"
"#pagesContainer QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"#pagesContainer QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"#pagesContainer QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49"
                        ");\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ListWidget */\n"
"#pagesContainer QListWidget {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Disabled */\n"
"\n"
"#pagesContainer QPushButton:disabled {\n"
"	color: rgb(132, 134, 137);\n"
"	background-color: rgb(59, 64, 75);\n"
"}\n"
"#pagesContainer QLabel:disabled {\n"
"	color: rgb(132, 134, 137);\n"
"}\n"
"#pagesContainer QComboBox:disabled {\n"
"	color: rgb(132, 134, 137);\n"
"	background-color: rgb(59, 64, 75);\n"
"}\n"
"#pagesContainer QComboBox QAbstractItemView:disabled {\n"
"	color: rgb(132, 134, 137);\n"
"	background-color: rgb(59, 64, 75);\n"
"}\n"
"#pagesContainer QSlider:disabled {\n"
"	background-color: rgb(59, 64, 75);\n"
"}\n"
"#pagesCont"
                        "ainer QSlider::groove:disabled {\n"
"	background-color: rgb(59, 64, 75);\n"
"}\n"
"#pagesContainer QSlider::handle:disabled {\n"
"	background-color: rgb(59, 64, 75);\n"
"}\n"
"#pagesContainer QScrollBar:disabled {\n"
"	background-color: rgb(59, 64, 75);\n"
"}\n"
"#pagesContainer QScrollBar::handle:disabled {\n"
"	background-color: rgb(59, 64, 75);\n"
"}\n"
"#pagesContainer QCheckBox:disabled {\n"
"	color: rgb(132, 134, 137);\n"
"}\n"
"#pagesContainer QRadioButton:disabled {\n"
"	color: rgb(132, 134, 137);\n"
"}\n"
"#pagesContainer QPlainTextEdit:disabled {\n"
"	color: rgb(132, 134, 137);\n"
"	background-color: rgb(59, 64, 75);\n"
"}\n"
"#pagesContainer QLineEdit:disabled {\n"
"	color: rgb(132, 134, 137);\n"
"	background-color: rgb(59, 64, 75);\n"
"}\n"
"#pagesContainer QListWidget:disabled {\n"
"	color: rgb(132, 134, 137);\n"
"	background-color: rgb(59, 64, 75);\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.gridLayout_3 = QGridLayout(self.styleSheet)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setFrameShape(QFrame.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Raised)
        self.appLayout = QHBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName(u"appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.leftMenuBg = QFrame(self.bgApp)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setMinimumSize(QSize(60, 0))
        self.leftMenuBg.setMaximumSize(QSize(60, 16777215))
        self.leftMenuBg.setFrameShape(QFrame.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.leftMenuBg)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.topLogoInfo = QFrame(self.leftMenuBg)
        self.topLogoInfo.setObjectName(u"topLogoInfo")
        self.topLogoInfo.setMinimumSize(QSize(0, 50))
        self.topLogoInfo.setMaximumSize(QSize(16777215, 50))
        self.topLogoInfo.setFrameShape(QFrame.NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.Raised)
        self.topLogo = QFrame(self.topLogoInfo)
        self.topLogo.setObjectName(u"topLogo")
        self.topLogo.setGeometry(QRect(10, 5, 42, 42))
        self.topLogo.setMinimumSize(QSize(42, 42))
        self.topLogo.setMaximumSize(QSize(42, 42))
        self.topLogo.setStyleSheet(u"background-color: rgb(33, 37, 43);\n"
"background-image: url(:/images/images/images/microRep.png);\n"
"background-position: centered;\n"
"background-repeat: no-repeat;")
        self.topLogo.setFrameShape(QFrame.NoFrame)
        self.topLogo.setFrameShadow(QFrame.Raised)
        self.titleLeftApp = QLabel(self.topLogoInfo)
        self.titleLeftApp.setObjectName(u"titleLeftApp")
        self.titleLeftApp.setGeometry(QRect(70, 8, 160, 20))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI Semibold"])
        font1.setPointSize(12)
        font1.setBold(False)
        font1.setItalic(False)
        self.titleLeftApp.setFont(font1)
        self.titleLeftApp.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.titleLeftDescription = QLabel(self.topLogoInfo)
        self.titleLeftDescription.setObjectName(u"titleLeftDescription")
        self.titleLeftDescription.setGeometry(QRect(70, 27, 160, 16))
        self.titleLeftDescription.setMaximumSize(QSize(16777215, 16))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(8)
        font2.setBold(False)
        font2.setItalic(False)
        self.titleLeftDescription.setFont(font2)
        self.titleLeftDescription.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_3.addWidget(self.topLogoInfo)

        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        self.leftMenuFrame.setFrameShape(QFrame.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Raised)
        self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.verticalMenuLayout.setSpacing(0)
        self.verticalMenuLayout.setObjectName(u"verticalMenuLayout")
        self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.toggleBox = QFrame(self.leftMenuFrame)
        self.toggleBox.setObjectName(u"toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.toggleBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.toggleButton = QPushButton(self.toggleBox)
        self.toggleButton.setObjectName(u"toggleButton")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleButton.sizePolicy().hasHeightForWidth())
        self.toggleButton.setSizePolicy(sizePolicy)
        self.toggleButton.setMinimumSize(QSize(0, 45))
        self.toggleButton.setFont(font)
        self.toggleButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LeftToRight)
        self.toggleButton.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_menu.png);")

        self.verticalLayout_4.addWidget(self.toggleButton)


        self.verticalMenuLayout.addWidget(self.toggleBox)

        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.topMenu)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.btn_home = QPushButton(self.topMenu)
        self.btn_home.setObjectName(u"btn_home")
        sizePolicy.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
        self.btn_home.setSizePolicy(sizePolicy)
        self.btn_home.setMinimumSize(QSize(0, 45))
        self.btn_home.setFont(font)
        self.btn_home.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_home.setLayoutDirection(Qt.LeftToRight)
        self.btn_home.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-home.png);")

        self.verticalLayout_8.addWidget(self.btn_home)

        self.btn_generator = QPushButton(self.topMenu)
        self.btn_generator.setObjectName(u"btn_generator")
        sizePolicy.setHeightForWidth(self.btn_generator.sizePolicy().hasHeightForWidth())
        self.btn_generator.setSizePolicy(sizePolicy)
        self.btn_generator.setMinimumSize(QSize(0, 45))
        self.btn_generator.setFont(font)
        self.btn_generator.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_generator.setLayoutDirection(Qt.LeftToRight)
        self.btn_generator.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-image1.png);")

        self.verticalLayout_8.addWidget(self.btn_generator)

        self.btn_classic = QPushButton(self.topMenu)
        self.btn_classic.setObjectName(u"btn_classic")
        sizePolicy.setHeightForWidth(self.btn_classic.sizePolicy().hasHeightForWidth())
        self.btn_classic.setSizePolicy(sizePolicy)
        self.btn_classic.setMinimumSize(QSize(0, 45))
        self.btn_classic.setFont(font)
        self.btn_classic.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_classic.setLayoutDirection(Qt.LeftToRight)
        self.btn_classic.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-media-play.png);")

        self.verticalLayout_8.addWidget(self.btn_classic)

        self.btn_webcam = QPushButton(self.topMenu)
        self.btn_webcam.setObjectName(u"btn_webcam")
        sizePolicy.setHeightForWidth(self.btn_webcam.sizePolicy().hasHeightForWidth())
        self.btn_webcam.setSizePolicy(sizePolicy)
        self.btn_webcam.setMinimumSize(QSize(0, 45))
        self.btn_webcam.setFont(font)
        self.btn_webcam.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_webcam.setLayoutDirection(Qt.LeftToRight)
        self.btn_webcam.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-camera.png);")

        self.verticalLayout_8.addWidget(self.btn_webcam)

        self.btn_exp = QPushButton(self.topMenu)
        self.btn_exp.setObjectName(u"btn_exp")
        sizePolicy.setHeightForWidth(self.btn_exp.sizePolicy().hasHeightForWidth())
        self.btn_exp.setSizePolicy(sizePolicy)
        self.btn_exp.setMinimumSize(QSize(0, 45))
        self.btn_exp.setFont(font)
        self.btn_exp.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_exp.setLayoutDirection(Qt.LeftToRight)
        self.btn_exp.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-magnifying-glass.png);")

        self.verticalLayout_8.addWidget(self.btn_exp)


        self.verticalMenuLayout.addWidget(self.topMenu, 0, Qt.AlignTop)

        self.bottomMenu = QFrame(self.leftMenuFrame)
        self.bottomMenu.setObjectName(u"bottomMenu")
        self.bottomMenu.setFrameShape(QFrame.NoFrame)
        self.bottomMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.bottomMenu)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.toggleLeftBox = QPushButton(self.bottomMenu)
        self.toggleLeftBox.setObjectName(u"toggleLeftBox")
        sizePolicy.setHeightForWidth(self.toggleLeftBox.sizePolicy().hasHeightForWidth())
        self.toggleLeftBox.setSizePolicy(sizePolicy)
        self.toggleLeftBox.setMinimumSize(QSize(0, 45))
        self.toggleLeftBox.setFont(font)
        self.toggleLeftBox.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggleLeftBox.setLayoutDirection(Qt.LeftToRight)
        self.toggleLeftBox.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_settings.png);")

        self.verticalLayout_9.addWidget(self.toggleLeftBox)


        self.verticalMenuLayout.addWidget(self.bottomMenu, 0, Qt.AlignBottom)


        self.verticalLayout_3.addWidget(self.leftMenuFrame)


        self.appLayout.addWidget(self.leftMenuBg)

        self.extraLeftBox = QFrame(self.bgApp)
        self.extraLeftBox.setObjectName(u"extraLeftBox")
        self.extraLeftBox.setMinimumSize(QSize(0, 0))
        self.extraLeftBox.setMaximumSize(QSize(0, 16777215))
        self.extraLeftBox.setFrameShape(QFrame.NoFrame)
        self.extraLeftBox.setFrameShadow(QFrame.Raised)
        self.extraColumLayout = QVBoxLayout(self.extraLeftBox)
        self.extraColumLayout.setSpacing(0)
        self.extraColumLayout.setObjectName(u"extraColumLayout")
        self.extraColumLayout.setContentsMargins(0, 0, 0, 0)
        self.extraTopBg = QFrame(self.extraLeftBox)
        self.extraTopBg.setObjectName(u"extraTopBg")
        self.extraTopBg.setMinimumSize(QSize(0, 50))
        self.extraTopBg.setMaximumSize(QSize(16777215, 50))
        self.extraTopBg.setFrameShape(QFrame.NoFrame)
        self.extraTopBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.extraTopBg)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.extraTopLayout = QGridLayout()
        self.extraTopLayout.setObjectName(u"extraTopLayout")
        self.extraTopLayout.setHorizontalSpacing(10)
        self.extraTopLayout.setVerticalSpacing(0)
        self.extraTopLayout.setContentsMargins(10, -1, 10, -1)
        self.extraIcon = QFrame(self.extraTopBg)
        self.extraIcon.setObjectName(u"extraIcon")
        self.extraIcon.setMinimumSize(QSize(20, 0))
        self.extraIcon.setMaximumSize(QSize(20, 20))
        self.extraIcon.setFrameShape(QFrame.NoFrame)
        self.extraIcon.setFrameShadow(QFrame.Raised)

        self.extraTopLayout.addWidget(self.extraIcon, 0, 0, 1, 1)

        self.extraLabel = QLabel(self.extraTopBg)
        self.extraLabel.setObjectName(u"extraLabel")
        self.extraLabel.setMinimumSize(QSize(150, 0))

        self.extraTopLayout.addWidget(self.extraLabel, 0, 1, 1, 1)

        self.extraCloseColumnBtn = QPushButton(self.extraTopBg)
        self.extraCloseColumnBtn.setObjectName(u"extraCloseColumnBtn")
        self.extraCloseColumnBtn.setMinimumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setMaximumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/icon_close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.extraCloseColumnBtn.setIcon(icon)
        self.extraCloseColumnBtn.setIconSize(QSize(20, 20))

        self.extraTopLayout.addWidget(self.extraCloseColumnBtn, 0, 2, 1, 1)


        self.verticalLayout_5.addLayout(self.extraTopLayout)


        self.extraColumLayout.addWidget(self.extraTopBg)

        self.extraContent = QFrame(self.extraLeftBox)
        self.extraContent.setObjectName(u"extraContent")
        self.extraContent.setFrameShape(QFrame.NoFrame)
        self.extraContent.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.extraContent)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.extraCenter = QFrame(self.extraContent)
        self.extraCenter.setObjectName(u"extraCenter")
        self.extraCenter.setFrameShape(QFrame.NoFrame)
        self.extraCenter.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.extraCenter)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.textEdit = QTextEdit(self.extraCenter)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMinimumSize(QSize(222, 0))
        self.textEdit.setFrameShape(QFrame.NoFrame)
        self.textEdit.setReadOnly(True)

        self.verticalLayout_10.addWidget(self.textEdit)


        self.verticalLayout_12.addWidget(self.extraCenter)

        self.extraBottom = QFrame(self.extraContent)
        self.extraBottom.setObjectName(u"extraBottom")
        self.extraBottom.setFrameShape(QFrame.NoFrame)
        self.extraBottom.setFrameShadow(QFrame.Raised)

        self.verticalLayout_12.addWidget(self.extraBottom)


        self.extraColumLayout.addWidget(self.extraContent)


        self.appLayout.addWidget(self.extraLeftBox)

        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName(u"contentBox")
        self.contentBox.setFrameShape(QFrame.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.contentTopBg = QFrame(self.contentBox)
        self.contentTopBg.setObjectName(u"contentTopBg")
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.contentTopBg.setFrameShape(QFrame.NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.leftBox = QFrame(self.contentTopBg)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy1)
        self.leftBox.setFrameShape(QFrame.NoFrame)
        self.leftBox.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u"titleRightInfo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(sizePolicy2)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        self.titleRightInfo.setFont(font)
        self.titleRightInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)


        self.horizontalLayout.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTopBg)
        self.rightButtons.setObjectName(u"rightButtons")
        self.rightButtons.setMinimumSize(QSize(0, 28))
        self.rightButtons.setFrameShape(QFrame.NoFrame)
        self.rightButtons.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightButtons)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.settingsTopBtn = QPushButton(self.rightButtons)
        self.settingsTopBtn.setObjectName(u"settingsTopBtn")
        self.settingsTopBtn.setMinimumSize(QSize(28, 28))
        self.settingsTopBtn.setMaximumSize(QSize(28, 28))
        self.settingsTopBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/cil-info.png", QSize(), QIcon.Normal, QIcon.Off)
        self.settingsTopBtn.setIcon(icon1)
        self.settingsTopBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.settingsTopBtn)

        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/icon_minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.minimizeAppBtn.setIcon(icon2)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)

        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setStyleStrategy(QFont.PreferDefault)
        self.maximizeRestoreAppBtn.setFont(font3)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/icons/icon_maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.maximizeRestoreAppBtn.setIcon(icon3)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.closeAppBtn.setIcon(icon)
        self.closeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.closeAppBtn)


        self.horizontalLayout.addWidget(self.rightButtons, 0, Qt.AlignRight)


        self.verticalLayout_2.addWidget(self.contentTopBg)

        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName(u"contentBottom")
        self.contentBottom.setFrameShape(QFrame.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.contentBottom)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.NoFrame)
        self.content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pagesContainer = QFrame(self.content)
        self.pagesContainer.setObjectName(u"pagesContainer")
        self.pagesContainer.setFrameShape(QFrame.NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.pagesContainer)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(1, 1, 1, 1)
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setEnabled(True)
        self.webcam_page = QWidget()
        self.webcam_page.setObjectName(u"webcam_page")
        self.gridLayout_344 = QGridLayout(self.webcam_page)
        self.gridLayout_344.setObjectName(u"gridLayout_344")
        self.gridLayout_344.setContentsMargins(9, 9, 9, 9)
        self.webcam = QWidget(self.webcam_page)
        self.webcam.setObjectName(u"webcam")
        self.label_live_file = ImageViewer(self.webcam)
        self.label_live_file.setObjectName(u"label_live_file")
        self.label_live_file.setGeometry(QRect(9, 9, 804, 565))
        self.label_commands = ImageViewer(self.webcam)
        self.label_commands.setObjectName(u"label_commands")
        self.label_commands.setGeometry(QRect(9, 9, 804, 565))
        self.label_rep = ImageViewer(self.webcam)
        self.label_rep.setObjectName(u"label_rep")
        self.label_rep.setGeometry(QRect(9, 9, 804, 565))
        self.label_markers = ImageViewer(self.webcam)
        self.label_markers.setObjectName(u"label_markers")
        self.label_markers.setGeometry(QRect(9, 9, 804, 565))

        self.gridLayout_344.addWidget(self.webcam, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.webcam_page)
        self.classic_page = QWidget()
        self.classic_page.setObjectName(u"classic_page")
        self.gridLayout_3411 = QGridLayout(self.classic_page)
        self.gridLayout_3411.setObjectName(u"gridLayout_3411")
        self.gridLayout_3411.setContentsMargins(9, 9, 9, 9)
        self.classic = QWidget(self.classic_page)
        self.classic.setObjectName(u"classic")

        self.gridLayout_3411.addWidget(self.classic, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.classic_page)
        self.experiment_page = QWidget()
        self.experiment_page.setObjectName(u"experiment_page")
        self.gridLayout_341 = QGridLayout(self.experiment_page)
        self.gridLayout_341.setObjectName(u"gridLayout_341")
        self.gridLayout_341.setContentsMargins(9, 9, 9, 9)
        self.experiment = QWidget(self.experiment_page)
        self.experiment.setObjectName(u"experiment")

        self.gridLayout_341.addWidget(self.experiment, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.experiment_page)
        self.home_page = QWidget()
        self.home_page.setObjectName(u"home_page")
        self.home_page.setStyleSheet(u"background-image: url(:/images/images/images/microRep_vertical.png);\n"
"background-position: center;\n"
"background-repeat: no-repeat;")
        self.gridLayout_342 = QGridLayout(self.home_page)
        self.gridLayout_342.setObjectName(u"gridLayout_342")
        self.gridLayout_342.setContentsMargins(9, 9, 9, 9)
        self.home = QWidget(self.home_page)
        self.home.setObjectName(u"home")

        self.gridLayout_342.addWidget(self.home, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.home_page)
        self.exporter_page = QWidget()
        self.exporter_page.setObjectName(u"exporter_page")
        self.gridLayout_343 = QGridLayout(self.exporter_page)
        self.gridLayout_343.setObjectName(u"gridLayout_343")
        self.gridLayout_343.setContentsMargins(9, 9, 9, 9)
        self.exporter = Exporter(self.exporter_page)
        self.exporter.setObjectName(u"exporter")
        self.gridLayoutWidget_3 = QWidget(self.exporter)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(410, 70, 421, 421))
        self.gridLayout_11 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(9, 9, 9, 9)
        self.frame_mappings = QFrame(self.gridLayoutWidget_3)
        self.frame_mappings.setObjectName(u"frame_mappings")
        self.frame_mappings.setFrameShape(QFrame.WinPanel)
        self.frame_mappings.setLineWidth(2)
        self.gridLayout_12 = QGridLayout(self.frame_mappings)
        self.gridLayout_12.setObjectName(u"gridLayout_12")

        self.gridLayout_11.addWidget(self.frame_mappings, 0, 0, 1, 1)

        self.layoutWidget2 = QWidget(self.exporter)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 160, 391, 221))
        self.gridLayout_8 = QGridLayout(self.layoutWidget2)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(9, 9, 9, 9)
        self.line_3 = QFrame(self.layoutWidget2)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShadow(QFrame.Plain)
        self.line_3.setFrameShape(QFrame.HLine)

        self.gridLayout_8.addWidget(self.line_3, 10, 0, 1, 2)

        self.comboBox_export_type = QComboBox(self.layoutWidget2)
        self.comboBox_export_type.addItem("")
        self.comboBox_export_type.addItem("")
        self.comboBox_export_type.addItem("")
        self.comboBox_export_type.addItem("")
        self.comboBox_export_type.setObjectName(u"comboBox_export_type")
        self.comboBox_export_type.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.gridLayout_8.addWidget(self.comboBox_export_type, 9, 1, 1, 1)

        self.entry_prefix = QLineEdit(self.layoutWidget2)
        self.entry_prefix.setObjectName(u"entry_prefix")
        self.entry_prefix.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.gridLayout_8.addWidget(self.entry_prefix, 8, 1, 1, 1)

        self.label_7 = QLabel(self.layoutWidget2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_8.addWidget(self.label_7, 9, 0, 1, 1)

        self.label_4 = QLabel(self.layoutWidget2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_8.addWidget(self.label_4, 8, 0, 1, 1)

        self.label_5 = QLabel(self.layoutWidget2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_8.addWidget(self.label_5, 0, 0, 1, 1)

        self.btn_apply_export_3 = QPushButton(self.layoutWidget2)
        self.btn_apply_export_3.setObjectName(u"btn_apply_export_3")
        self.btn_apply_export_3.setMinimumSize(QSize(0, 0))
        self.btn_apply_export_3.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.gridLayout_8.addWidget(self.btn_apply_export_3, 6, 0, 1, 1)

        self.entry_export_path = QLineEdit(self.layoutWidget2)
        self.entry_export_path.setObjectName(u"entry_export_path")
        self.entry_export_path.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.entry_export_path.setReadOnly(True)

        self.gridLayout_8.addWidget(self.entry_export_path, 6, 1, 1, 1)

        self.line = QFrame(self.layoutWidget2)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setFrameShape(QFrame.HLine)

        self.gridLayout_8.addWidget(self.line, 7, 0, 1, 2)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.btn_export_current = QPushButton(self.layoutWidget2)
        self.btn_export_current.setObjectName(u"btn_export_current")
        self.btn_export_current.setEnabled(False)
        self.btn_export_current.setMinimumSize(QSize(0, 50))
        self.btn_export_current.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.horizontalLayout_8.addWidget(self.btn_export_current)

        self.btn_export_all = QPushButton(self.layoutWidget2)
        self.btn_export_all.setObjectName(u"btn_export_all")
        self.btn_export_all.setEnabled(False)
        self.btn_export_all.setMinimumSize(QSize(0, 50))
        self.btn_export_all.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.horizontalLayout_8.addWidget(self.btn_export_all)


        self.gridLayout_8.addLayout(self.horizontalLayout_8, 12, 1, 1, 1)

        self.gridLayoutWidget_4 = QWidget(self.exporter)
        self.gridLayoutWidget_4.setObjectName(u"gridLayoutWidget_4")
        self.gridLayoutWidget_4.setGeometry(QRect(410, 490, 421, 81))
        self.gridLayout_14 = QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.widget = QWidget(self.gridLayoutWidget_4)
        self.widget.setObjectName(u"widget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy3)
        self.horizontalLayout_7 = QHBoxLayout(self.widget)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.btn_previous = QPushButton(self.widget)
        self.btn_previous.setObjectName(u"btn_previous")
        self.btn_previous.setMinimumSize(QSize(0, 50))
        self.btn_previous.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.horizontalLayout_7.addWidget(self.btn_previous)

        self.btn_next = QPushButton(self.widget)
        self.btn_next.setObjectName(u"btn_next")
        self.btn_next.setMinimumSize(QSize(0, 50))
        self.btn_next.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.horizontalLayout_7.addWidget(self.btn_next)


        self.gridLayout_14.addWidget(self.widget, 0, 0, 1, 1)

        self.verticalLayoutWidget_3 = QWidget(self.exporter)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 0, 401, 71))
        self.verticalLayout_22 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.label_9 = QLabel(self.verticalLayoutWidget_3)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_22.addWidget(self.label_9)

        self.line_6 = QFrame(self.verticalLayoutWidget_3)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShadow(QFrame.Plain)
        self.line_6.setFrameShape(QFrame.HLine)

        self.verticalLayout_22.addWidget(self.line_6)

        self.btn_export_6 = QPushButton(self.exporter)
        self.btn_export_6.setObjectName(u"btn_export_6")
        self.btn_export_6.setGeometry(QRect(150, 450, 91, 91))
        self.btn_export_6.setMinimumSize(QSize(0, 0))
        self.btn_export_6.setStyleSheet(u"border-radius: 45%;")
        icon4 = QIcon()
        icon4.addFile(u":/images/images/images/cil-arrow-circle-left.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_export_6.setIcon(icon4)
        self.btn_export_6.setIconSize(QSize(80, 80))

        self.gridLayout_343.addWidget(self.exporter, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.exporter_page)
        self.generator_page = QWidget()
        self.generator_page.setObjectName(u"generator_page")
        self.gridLayout_364 = QGridLayout(self.generator_page)
        self.gridLayout_364.setObjectName(u"gridLayout_364")
        self.gridLayout_364.setContentsMargins(9, 9, 9, 9)
        self.generator = Generator(self.generator_page)
        self.generator.setObjectName(u"generator")
        self.gridLayoutWidget = QWidget(self.generator)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(20, 70, 381, 411))
        self.gridLayout_5 = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(9, 9, 9, 9)
        self.frame_img = QFrame(self.gridLayoutWidget)
        self.frame_img.setObjectName(u"frame_img")
        self.frame_img.setFrameShape(QFrame.WinPanel)
        self.frame_img.setLineWidth(2)
        self.gridLayout_6 = QGridLayout(self.frame_img)
        self.gridLayout_6.setObjectName(u"gridLayout_6")

        self.gridLayout_5.addWidget(self.frame_img, 0, 0, 1, 1)

        self.btn_import = QPushButton(self.gridLayoutWidget)
        self.btn_import.setObjectName(u"btn_import")
        self.btn_import.setStyleSheet(u"")

        self.gridLayout_5.addWidget(self.btn_import, 1, 0, 1, 1)

        self.gridLayoutWidget_2 = QWidget(self.generator)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(420, 520, 411, 71))
        self.gridLayout_7 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(9, 9, 9, 9)
        self.btn_mapping = QPushButton(self.gridLayoutWidget_2)
        self.btn_mapping.setObjectName(u"btn_mapping")
        self.btn_mapping.setEnabled(True)
        self.btn_mapping.setMinimumSize(QSize(0, 45))
        self.btn_mapping.setStyleSheet(u"")

        self.gridLayout_7.addWidget(self.btn_mapping, 0, 0, 1, 1)

        self.verticalLayoutWidget_2 = QWidget(self.generator)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 0, 401, 71))
        self.verticalLayout_21 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.label_8 = QLabel(self.verticalLayoutWidget_2)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_21.addWidget(self.label_8)

        self.line_5 = QFrame(self.verticalLayoutWidget_2)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShadow(QFrame.Plain)
        self.line_5.setFrameShape(QFrame.HLine)

        self.verticalLayout_21.addWidget(self.line_5)

        self.mapping_frame = QFrame(self.generator)
        self.mapping_frame.setObjectName(u"mapping_frame")
        self.mapping_frame.setEnabled(False)
        self.mapping_frame.setGeometry(QRect(420, 10, 411, 521))
        self.mapping_frame.setFrameShape(QFrame.StyledPanel)
        self.mapping_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.mapping_frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame_grid = QGridLayout()
        self.frame_grid.setObjectName(u"frame_grid")
        self.frame_grid.setHorizontalSpacing(9)
        self.frame_grid.setContentsMargins(9, 9, 9, 9)
        self.btn_clear = QPushButton(self.mapping_frame)
        self.btn_clear.setObjectName(u"btn_clear")
        self.btn_clear.setStyleSheet(u"")

        self.frame_grid.addWidget(self.btn_clear, 8, 1, 1, 1)

        self.comboBox_finger = QComboBox(self.mapping_frame)
        self.comboBox_finger.addItem("")
        self.comboBox_finger.addItem("")
        self.comboBox_finger.addItem("")
        self.comboBox_finger.addItem("")
        self.comboBox_finger.setObjectName(u"comboBox_finger")

        self.frame_grid.addWidget(self.comboBox_finger, 1, 0, 1, 1)

        self.label_str_config = QLabel(self.mapping_frame)
        self.label_str_config.setObjectName(u"label_str_config")

        self.frame_grid.addWidget(self.label_str_config, 4, 0, 1, 3)

        self.comboBox_microgesture = QComboBox(self.mapping_frame)
        self.comboBox_microgesture.addItem("")
        self.comboBox_microgesture.addItem("")
        self.comboBox_microgesture.addItem("")
        self.comboBox_microgesture.addItem("")
        self.comboBox_microgesture.setObjectName(u"comboBox_microgesture")
        self.comboBox_microgesture.setStyleSheet(u"")

        self.frame_grid.addWidget(self.comboBox_microgesture, 2, 0, 1, 1)

        self.comboBox_charac = QComboBox(self.mapping_frame)
        self.comboBox_charac.addItem("")
        self.comboBox_charac.addItem("")
        self.comboBox_charac.addItem("")
        self.comboBox_charac.addItem("")
        self.comboBox_charac.addItem("")
        self.comboBox_charac.setObjectName(u"comboBox_charac")
        self.comboBox_charac.setStyleSheet(u"")

        self.frame_grid.addWidget(self.comboBox_charac, 2, 1, 1, 1)

        self.label_config_file = QLabel(self.mapping_frame)
        self.label_config_file.setObjectName(u"label_config_file")

        self.frame_grid.addWidget(self.label_config_file, 10, 0, 1, 2)

        self.label_10 = QLabel(self.mapping_frame)
        self.label_10.setObjectName(u"label_10")

        self.frame_grid.addWidget(self.label_10, 9, 1, 1, 1)

        self.btn_select = QPushButton(self.mapping_frame)
        self.btn_select.setObjectName(u"btn_select")
        self.btn_select.setStyleSheet(u"")

        self.frame_grid.addWidget(self.btn_select, 11, 3, 1, 1)

        self.btn_apply = QPushButton(self.mapping_frame)
        self.btn_apply.setObjectName(u"btn_apply")
        self.btn_apply.setStyleSheet(u"")

        self.frame_grid.addWidget(self.btn_apply, 4, 3, 1, 1)

        self.btn_add = QPushButton(self.mapping_frame)
        self.btn_add.setObjectName(u"btn_add")
        self.btn_add.setMinimumSize(QSize(0, 50))
        self.btn_add.setStyleSheet(u"")

        self.frame_grid.addWidget(self.btn_add, 1, 3, 2, 1)

        self.list_config = QListWidget(self.mapping_frame)
        self.list_config.setObjectName(u"list_config")

        self.frame_grid.addWidget(self.list_config, 6, 0, 1, 4)

        self.label = QLabel(self.mapping_frame)
        self.label.setObjectName(u"label")
        sizePolicy3.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy3)

        self.frame_grid.addWidget(self.label, 0, 0, 1, 4)

        self.label_3 = QLabel(self.mapping_frame)
        self.label_3.setObjectName(u"label_3")

        self.frame_grid.addWidget(self.label_3, 3, 0, 1, 4)

        self.btn_save_as = QPushButton(self.mapping_frame)
        self.btn_save_as.setObjectName(u"btn_save_as")
        self.btn_save_as.setStyleSheet(u"")

        self.frame_grid.addWidget(self.btn_save_as, 8, 3, 1, 1)

        self.label_2 = QLabel(self.mapping_frame)
        self.label_2.setObjectName(u"label_2")
        sizePolicy3.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy3)

        self.frame_grid.addWidget(self.label_2, 5, 0, 1, 3)

        self.btn_remove = QPushButton(self.mapping_frame)
        self.btn_remove.setObjectName(u"btn_remove")
        self.btn_remove.setStyleSheet(u"")

        self.frame_grid.addWidget(self.btn_remove, 5, 3, 1, 1)

        self.btn_reset = QPushButton(self.mapping_frame)
        self.btn_reset.setObjectName(u"btn_reset")
        self.btn_reset.setStyleSheet(u"")

        self.frame_grid.addWidget(self.btn_reset, 8, 0, 1, 1)

        self.entry_config = QLineEdit(self.mapping_frame)
        self.entry_config.setObjectName(u"entry_config")
        self.entry_config.setEnabled(False)
        self.entry_config.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.entry_config.setReadOnly(True)

        self.frame_grid.addWidget(self.entry_config, 11, 0, 1, 3)


        self.gridLayout.addLayout(self.frame_grid, 0, 0, 1, 1)

        self.btn_export_5 = QPushButton(self.generator)
        self.btn_export_5.setObjectName(u"btn_export_5")
        self.btn_export_5.setGeometry(QRect(160, 500, 91, 91))
        self.btn_export_5.setMinimumSize(QSize(0, 0))
        self.btn_export_5.setStyleSheet(u"border-radius: 45%;")
        icon5 = QIcon()
        icon5.addFile(u":/images/images/images/cil-arrow-circle-right.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_export_5.setIcon(icon5)
        self.btn_export_5.setIconSize(QSize(80, 80))
        self.widget_2 = QWidget(self.generator)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(269, 499, 111, 91))

        self.gridLayout_364.addWidget(self.generator, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.generator_page)

        self.verticalLayout_15.addWidget(self.stackedWidget)


        self.horizontalLayout_4.addWidget(self.pagesContainer)

        self.extraRightBox = QFrame(self.content)
        self.extraRightBox.setObjectName(u"extraRightBox")
        self.extraRightBox.setMinimumSize(QSize(0, 0))
        self.extraRightBox.setMaximumSize(QSize(0, 16777215))
        self.extraRightBox.setFrameShape(QFrame.NoFrame)
        self.extraRightBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.extraRightBox)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.themeSettingsTopDetail = QFrame(self.extraRightBox)
        self.themeSettingsTopDetail.setObjectName(u"themeSettingsTopDetail")
        self.themeSettingsTopDetail.setMaximumSize(QSize(16777215, 3))
        self.themeSettingsTopDetail.setFrameShape(QFrame.NoFrame)
        self.themeSettingsTopDetail.setFrameShadow(QFrame.Raised)

        self.verticalLayout_7.addWidget(self.themeSettingsTopDetail)

        self.contentSettings = QFrame(self.extraRightBox)
        self.contentSettings.setObjectName(u"contentSettings")
        self.contentSettings.setFrameShape(QFrame.NoFrame)
        self.contentSettings.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.contentSettings)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.topMenus = QFrame(self.contentSettings)
        self.topMenus.setObjectName(u"topMenus")
        self.topMenus.setFrameShape(QFrame.NoFrame)
        self.topMenus.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.topMenus)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.btn_author = QPushButton(self.topMenus)
        self.btn_author.setObjectName(u"btn_author")
        sizePolicy.setHeightForWidth(self.btn_author.sizePolicy().hasHeightForWidth())
        self.btn_author.setSizePolicy(sizePolicy)
        self.btn_author.setMinimumSize(QSize(0, 45))
        self.btn_author.setFont(font)
        self.btn_author.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_author.setLayoutDirection(Qt.LeftToRight)
        self.btn_author.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-user.png);")

        self.verticalLayout_14.addWidget(self.btn_author)

        self.btn_related = QPushButton(self.topMenus)
        self.btn_related.setObjectName(u"btn_related")
        sizePolicy.setHeightForWidth(self.btn_related.sizePolicy().hasHeightForWidth())
        self.btn_related.setSizePolicy(sizePolicy)
        self.btn_related.setMinimumSize(QSize(0, 45))
        self.btn_related.setFont(font)
        self.btn_related.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_related.setLayoutDirection(Qt.LeftToRight)
        self.btn_related.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-link.png);")

        self.verticalLayout_14.addWidget(self.btn_related)


        self.verticalLayout_13.addWidget(self.topMenus, 0, Qt.AlignTop)


        self.verticalLayout_7.addWidget(self.contentSettings)


        self.horizontalLayout_4.addWidget(self.extraRightBox)


        self.verticalLayout_6.addWidget(self.content)

        self.bottomBar = QFrame(self.contentBottom)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFrameShape(QFrame.NoFrame)
        self.bottomBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.creditsLabel = QLabel(self.bottomBar)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        font4.setBold(False)
        font4.setItalic(False)
        self.creditsLabel.setFont(font4)
        self.creditsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.creditsLabel)

        self.runningInfo = QLabel(self.bottomBar)
        self.runningInfo.setObjectName(u"runningInfo")
        self.runningInfo.setMaximumSize(QSize(16777215, 16))
        self.runningInfo.setFont(font4)
        self.runningInfo.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.runningInfo)

        self.version = QLabel(self.bottomBar)
        self.version.setObjectName(u"version")
        self.version.setMaximumSize(QSize(60, 16777215))
        self.version.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.version)

        self.frame_size_grip = QFrame(self.bottomBar)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_5.addWidget(self.frame_size_grip)


        self.verticalLayout_6.addWidget(self.bottomBar)


        self.verticalLayout_2.addWidget(self.contentBottom)


        self.appLayout.addWidget(self.contentBox)


        self.gridLayout_3.addWidget(self.bgApp, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)
        self.btn_select.clicked.connect(self.generator.select_file_config)
        self.btn_save_as.clicked.connect(self.generator.save_config_as_file)
        self.btn_clear.clicked.connect(self.generator.clear_config)
        self.btn_add.clicked.connect(self.generator.add_mapping)
        self.btn_apply.clicked.connect(self.generator.apply_config)
        self.btn_remove.clicked.connect(self.generator.remove_config)
        self.btn_reset.clicked.connect(self.generator.default_config)
        self.btn_mapping.clicked.connect(self.generator.lock_mappings)
        self.btn_import.clicked.connect(self.generator.import_image)
        self.btn_previous.clicked.connect(self.exporter.previous_rep)
        self.btn_next.clicked.connect(self.exporter.next_rep)
        self.btn_export_current.clicked.connect(self.exporter.export_current)
        self.btn_export_all.clicked.connect(self.exporter.export_all)
        self.btn_apply_export_3.clicked.connect(self.exporter.select_export_folder)
        self.btn_export_5.clicked.connect(self.generator.export_image_with_mappings)
        self.btn_export_6.clicked.connect(self.exporter.back_to_generator)

        self.stackedWidget.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.titleLeftApp.setText(QCoreApplication.translate("MainWindow", u"\u00b5Rep-PyGUI", None))
        self.titleLeftDescription.setText(QCoreApplication.translate("MainWindow", u"Microgesture representations", None))
#if QT_CONFIG(tooltip)
        self.toggleButton.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.toggleButton.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
#if QT_CONFIG(tooltip)
        self.btn_home.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
#if QT_CONFIG(tooltip)
        self.btn_generator.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.btn_generator.setText(QCoreApplication.translate("MainWindow", u"Generator", None))
#if QT_CONFIG(tooltip)
        self.btn_classic.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.btn_classic.setText(QCoreApplication.translate("MainWindow", u"Classic demo", None))
#if QT_CONFIG(tooltip)
        self.btn_webcam.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.btn_webcam.setText(QCoreApplication.translate("MainWindow", u"Webcam demo", None))
#if QT_CONFIG(tooltip)
        self.btn_exp.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.btn_exp.setText(QCoreApplication.translate("MainWindow", u"Experiment", None))
#if QT_CONFIG(tooltip)
        self.toggleLeftBox.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.toggleLeftBox.setText(QCoreApplication.translate("MainWindow", u"Options", None))
        self.extraLabel.setText(QCoreApplication.translate("MainWindow", u"Options", None))
#if QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close left box", None))
#endif // QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setText("")
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#8cbfca;\">\u00b5Rep - Options</span></p></body></html>", None))
        self.titleRightInfo.setText(QCoreApplication.translate("MainWindow", u"\u00b5Rep-PyGUI : Explore the representation of hand microgestures", None))
#if QT_CONFIG(tooltip)
        self.settingsTopBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Information", None))
#endif // QT_CONFIG(tooltip)
        self.settingsTopBtn.setText("")
#if QT_CONFIG(tooltip)
        self.minimizeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.closeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.closeAppBtn.setText("")
        self.label_live_file.setProperty("text", "")
        self.label_commands.setProperty("text", "")
        self.label_rep.setProperty("text", "")
        self.label_markers.setProperty("text", "")
        self.comboBox_export_type.setItemText(0, QCoreApplication.translate("MainWindow", u"SVG", None))
        self.comboBox_export_type.setItemText(1, QCoreApplication.translate("MainWindow", u"PNG", None))
        self.comboBox_export_type.setItemText(2, QCoreApplication.translate("MainWindow", u"JPG", None))
        self.comboBox_export_type.setItemText(3, QCoreApplication.translate("MainWindow", u"PDF", None))

        self.entry_prefix.setPlaceholderText(QCoreApplication.translate("MainWindow", u"myRep_", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Export as...", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"File prefix", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Export to folder...", None))
        self.btn_apply_export_3.setText(QCoreApplication.translate("MainWindow", u"Select folder", None))
        self.entry_export_path.setText("")
        self.entry_export_path.setPlaceholderText(QCoreApplication.translate("MainWindow", u"C:\\Users\\USER_NAME\\Downloads", None))
        self.btn_export_current.setText(QCoreApplication.translate("MainWindow", u"Export current", None))
        self.btn_export_all.setText(QCoreApplication.translate("MainWindow", u"Export all", None))
        self.btn_previous.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.btn_next.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">Export microgesture representations</span></p></body></html>", None))
        self.btn_export_6.setText("")
        self.btn_import.setText(QCoreApplication.translate("MainWindow", u"Import JPG...", None))
        self.btn_mapping.setText(QCoreApplication.translate("MainWindow", u"Unlock mappings", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">Export microgesture representations</span></p></body></html>", None))
        self.btn_clear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.comboBox_finger.setItemText(0, QCoreApplication.translate("MainWindow", u"Index", None))
        self.comboBox_finger.setItemText(1, QCoreApplication.translate("MainWindow", u"Middle", None))
        self.comboBox_finger.setItemText(2, QCoreApplication.translate("MainWindow", u"Ring", None))
        self.comboBox_finger.setItemText(3, QCoreApplication.translate("MainWindow", u"Pinky", None))

        self.label_str_config.setText("")
        self.comboBox_microgesture.setItemText(0, QCoreApplication.translate("MainWindow", u"Tap", None))
        self.comboBox_microgesture.setItemText(1, QCoreApplication.translate("MainWindow", u"Hold", None))
        self.comboBox_microgesture.setItemText(2, QCoreApplication.translate("MainWindow", u"Swipe", None))
        self.comboBox_microgesture.setItemText(3, QCoreApplication.translate("MainWindow", u"Flex", None))

        self.comboBox_charac.setItemText(0, QCoreApplication.translate("MainWindow", u"Tip", None))
        self.comboBox_charac.setItemText(1, QCoreApplication.translate("MainWindow", u"Middle", None))
        self.comboBox_charac.setItemText(2, QCoreApplication.translate("MainWindow", u"Base", None))
        self.comboBox_charac.setItemText(3, QCoreApplication.translate("MainWindow", u"Up", None))
        self.comboBox_charac.setItemText(4, QCoreApplication.translate("MainWindow", u"Down", None))

        self.label_config_file.setText(QCoreApplication.translate("MainWindow", u"Specific configuration file :", None))
        self.label_10.setText("")
        self.btn_select.setText(QCoreApplication.translate("MainWindow", u"Select file", None))
        self.btn_apply.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.btn_add.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Choose a microgesture to add to the mapping :", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Current microgesture mapping :", None))
        self.btn_save_as.setText(QCoreApplication.translate("MainWindow", u"Save as", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"List of microgesture mappings to consider :", None))
        self.btn_remove.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.btn_reset.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.entry_config.setPlaceholderText("")
        self.btn_export_5.setText("")
        self.btn_author.setText(QCoreApplication.translate("MainWindow", u"Author", None))
        self.btn_related.setText(QCoreApplication.translate("MainWindow", u"Related works", None))
        self.creditsLabel.setText(QCoreApplication.translate("MainWindow", u"By: Vincent Lambert", None))
        self.runningInfo.setText(QCoreApplication.translate("MainWindow", u"Running threads : 0", None))
        self.version.setText(QCoreApplication.translate("MainWindow", u"v0.0.1", None))
    # retranslateUi

