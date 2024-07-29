# uncompyle6 version 3.2.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: /Volumes/LaCie/CLOUD/ALAN/WORK/SCRIPTS/MAYA/animBot_project/build/animBot/_api/widgets/sliderWidget.py
# Compiled at: 2018-11-21 07:08:57
from animBot._api.core import *
o__0__0_____o_____1_o__0___O____O___o_0_l__0_o_____l___l____l_____o_O_____o__O_____o = [5, 15, 50, 100]
o_____1___1____O__o_____o___o_____o_o_____l_____0_____l_____l___1___0____1_o___0____O___1__o____0_O____O__0___l____O_o____0_l___l = [105, 120, 150]
o___0_l_o__O_o_____l_____O___l___o = 200

class o__l____1__0__O___1(o_____1_0):
    o_____o_____1____l____O_____l__l = Signal()
    o___O_O____1_0___l___o___o___O__l_____l = Signal()

    def __init__(o_o____1_____l____1___O____l__O_1, value, sliderWidget, parentWidget, *args, **o_____O_1_O_____O___l____o_1):
        super(o__l____1__0__O___1, o_o____1_____l____1___O____l__O_1).__init__(*args, **o_____O_1_O_____O___l____o_1)
        o_o____1_____l____1___O____l__O_1.sliderWidget = sliderWidget
        o_o____1_____l____1___O____l__O_1.parentWidget = parentWidget
        o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1 = sliderWidget.o___O_____o_1_o____O____o_____1
        o_o____1_____l____1___O____l__O_1.o_____l__O____o____o_0____0___0 = '%s_dot_f' % o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.o_l__0___l_o____1_____0
        o____0___o_____O__O__l__0 = '%s_dot_b' % o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.o_l__0___l_o____1_____0
        o_o____1_____l____1___O____l__O_1.value = value
        o_O_1____l___0___O___1____o_____O = o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.config.get('o_O_1____l___0___O___1____o_____O', None) or [5, 15, 50, 100]
        o__o__O_____0___l__l = [o_O_1____l___0___O___1____o_____O[-1], o_O_1____l___0___O___1____o_____O[-1] * -1]
        o_o____1_____l____1___O____l__O_1.o___o___l___l_o___o = str(value).replace('.', '').replace('-', 'neg')
        o_o____1_____l____1___O____l__O_1.icon = o_o____1_____l____1___O____l__O_1.o_____l__O____o____o_0____0___0 if value in o__o__O_____0___l__l else o____0___o_____O__O__l__0
        o_o____1_____l____1___O____l__O_1.setMinimumWidth(5)
        o_o____1_____l____1___O____l__O_1.setMaximumHeight(24)
        o_o____1_____l____1___O____l__O_1.setIcon(QIcon(o__1___l_1____1_l__o__0(o_o____1_____l____1___O____l__O_1.icon)))
        o_o____1_____l____1___O____l__O_1.setFlat(True)
        o_o____1_____l____1___O____l__O_1.setIconSize(QSize(22, 22))
        o_o____1_____l____1___O____l__O_1.__o___1__o___1____l_o___1_____o___o___l()
        o_o____1_____l____1___O____l__O_1.clicked.connect(o_o____1_____l____1___O____l__O_1.o_1___o_____O___l_O)
        o_o____1_____l____1___O____l__O_1.middleClicked.connect(o_o____1_____l____1___O____l__O_1.o_1___o_____O___l_O)
        o_o____1_____l____1___O____l__O_1.o___O_O____1_0___l___o___o___O__l_____l.connect(o_o____1_____l____1___O____l__O_1.__o_O____0__O_0____0_O__0_o)
        o_o____1_____l____1___O____l__O_1.o_____o_____1____l____O_____l__l.connect(o_o____1_____l____1___O____l__O_1.__o__l__O)
        return

    def __o___1__o___1____l_o___1_____o___o___l(o_o____1_____l____1___O____l__O_1):
        o___o_____O___o_____l____O_l = CORE.color.o_o(o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.o_l__0___l_o____1_____0)
        o_o____1_____l____1___O____l__O_1.setStyleSheet('QPushButton:checked {background-color: %s; border: black 2px} QPushButton:pressed {background-color: %s; border: black 2px}' % (o___o_____O___o_____l____O_l, o___o_____O___o_____l____O_l))

    def __o_O____0__O_0____0_O__0_o(o_o____1_____l____1___O____l__O_1):
        o_o____1_____l____1___O____l__O_1.sliderWidget.o__O____O___o____O_l___O(o_o____1_____l____1___O____l__O_1.parentWidget)

    def __o__l__O(o_o____1_____l____1___O____l__O_1):
        o_o____1_____l____1___O____l__O_1.sliderWidget.o_____O____o_o___0____0_1_____0___l__1(o_o____1_____l____1___O____l__O_1.parentWidget)

    def o_1___o_____O___l_O(o_o____1_____l____1___O____l__O_1):
        CORE.moduleBot.o_____O___1_____1_____o(o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.o____0____o____1___O_____0_O___1)
        o_o____1_____l____1___O____l__O_1.clicked.disconnect()
        o_o____1_____l____1___O____l__O_1.middleClicked.disconnect()
        o_o____1_____l____1___O____l__O_1.clicked.connect(o_o____1_____l____1___O____l__O_1.trigger)
        o_o____1_____l____1___O____l__O_1.clicked.emit()

    def trigger(o_o____1_____l____1___O____l__O_1):
        mode = o_o____1_____l____1___O____l__O_1.parentWidget.o_____o__1___o_____l_0
        try:
            action = CORE.actions['%s_%s_%s_click' % (o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.o____0____o____1___O_____0_O___1, mode, o_o____1_____l____1___O____l__O_1.o___o___l___l_o___o)]
            action.trigger()
        except:
            print 'CORE.%s_%s_%s_click' % (o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.o____0____o____1___O_____0_O___1, mode, o_o____1_____l____1___O____l__O_1.o___o___l___l_o___o), 'preset method does not exist'
            o____1_O_1___0('Not implemented yet.')

    def setWorldSpace(o_o____1_____l____1___O____l__O_1, isWorldSpace):
        o_o____1_____l____1___O____l__O_1.icon = isWorldSpace and '%s_world_small' % o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.o_l__0___l_o____1_____0 if 1 else o_o____1_____l____1___O____l__O_1.o_____l__O____o____o_0____0___0
        o_o____1_____l____1___O____l__O_1.setIcon(QIcon(o__1___l_1____1_l__o__0(o_o____1_____l____1___O____l__O_1.icon)))

    def enterEvent(o_o____1_____l____1___O____l__O_1, event):
        super(o__l____1__0__O___1, o_o____1_____l____1___O____l__O_1).enterEvent(event)
        o____l_0_O(o_o____1_____l____1___O____l__O_1.o__l__0____0_____l_1__0_l__0(), o____O___0____o_1___0=True)

    def leaveEvent(o_o____1_____l____1___O____l__O_1, event):
        super(o__l____1__0__O___1, o_o____1_____l____1___O____l__O_1).leaveEvent(event)
        o____l_0_O.o__l____o____O____0()

    def mousePressEvent(o_o____1_____l____1___O____l__O_1, event):
        o_____O___l___O____o__1__O = event.button() == Qt.MiddleButton
        o____o__0_____0__O____O_1_O__0__l____O = event.button() == Qt.LeftButton
        if o_____O___l___O____o__1__O:
            o_o____1_____l____1___O____l__O_1.o_____o_____1____l____O_____l__l.emit()
            o____l___1____0__o_____O_____1__o_O = QMouseEvent(event.type(), event.pos(), Qt.LeftButton, Qt.LeftButton, event.modifiers())
            event = o____l___1____0__o_____O_____1__o_O
        else:
            if o____o__0_____0__O____O_1_O__0__l____O:
                o_o____1_____l____1___O____l__O_1.o___O_O____1_0___l___o___o___O__l_____l.emit()
        super(o__l____1__0__O___1, o_o____1_____l____1___O____l__O_1).mousePressEvent(event)

    def mouseReleaseEvent(o_o____1_____l____1___O____l__O_1, event):
        o_____O___l___O____o__1__O = event.button() == Qt.MiddleButton
        o____o__0_____0__O____O_1_O__0__l____O = event.button() == Qt.LeftButton
        if o_____O___l___O____o__1__O:
            o_o____1_____l____1___O____l__O_1.o_____o_____1____l____O_____l__l.emit()
            o____l___1____0__o_____O_____1__o_O = QMouseEvent(event.type(), event.pos(), Qt.LeftButton, Qt.LeftButton, event.modifiers())
            event = o____l___1____0__o_____O_____1__o_O
        else:
            if o____o__0_____0__O____O_1_O__0__l____O:
                o_o____1_____l____1___O____l__O_1.o___O_O____1_0___l___o___o___O__l_____l.emit()
        super(o__l____1__0__O___1, o_o____1_____l____1___O____l__O_1).mouseReleaseEvent(event)

    def o__l__0____0_____l_1__0_l__0(o_o____1_____l____1___O____l__O_1):
        o____0____O_1_1____O__o__1___o____l = '%s_%s' % (o_o____1_____l____1___O____l__O_1.parent().parent.o_____o__1___o_____l_0, o_o____1_____l____1___O____l__O_1.o___o___l___l_o___o)
        o___O_____o_1_o____O____o_____1 = o__O___l_____o_l__l___o__1__1.o___1____l____l_____0_o__O___1___l____1(o____0____O_1_1____O__o__1___o____l)
        if o___O_____o_1_o____O____o_____1 is not None:
            return o___O_____o_1_o____O____o_____1
        o____0____O_1_1____O__o__1___o____l = '%s_%s' % (o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.o____1, o_o____1_____l____1___O____l__O_1.o___o___l___l_o___o)
        o___O_____o_1_o____O____o_____1 = o__O___l_____o_l__l___o__1__1.o___1____l____l_____0_o__O___1___l____1(o____0____O_1_1____O__o__1___o____l)
        if o___O_____o_1_o____O____o_____1 is not None:
            return o___O_____o_1_o____O____o_____1
        return o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1


class o___l____O___o_____l___o_l____l_____l___1(o_____1_0):

    def __init__(o_o____1_____l____1___O____l__O_1, *args, **o_____O_1_O_____O___l____o_1):
        super(o___l____O___o_____l___o_l____l_____l___1, o_o____1_____l____1___O____l__O_1).__init__(*args, **o_____O_1_O_____O___l____o_1)
        o_o____1_____l____1___O____l__O_1.icon = 'white_dot_f'
        o_o____1_____l____1___O____l__O_1.setMinimumWidth(5)
        o_o____1_____l____1___O____l__O_1.setMaximumHeight(24)
        o_o____1_____l____1___O____l__O_1.setIcon(QIcon(o__1___l_1____1_l__o__0(o_o____1_____l____1___O____l__O_1.icon)))
        o_o____1_____l____1___O____l__O_1.setFlat(True)
        o_o____1_____l____1___O____l__O_1.setIconSize(QSize(22, 22))


class Slider(QSlider, CORE.toolWidgets.o___l_1___o____l_o_o___l, o____1_O_____0__l____0_____o____1):
    o_____o____O____O____0_o = Signal(str, int)
    o_____1___1___1 = Signal(float)
    o___0____1_O__O_____1_____o = Signal(str, tuple)
    o__l_o___O_O = Signal(float, str)
    o_____o_____1____l____O_____l__l = Signal()
    o___O_O____1_0___l___o___o___O__l_____l = Signal()
    kLeft = 0
    kRight = 1

    def __init__(o_o____1_____l____1___O____l__O_1, o___O_____o_1_o____O____o_____1, *args, **o_____O_1_O_____O___l____o_1):
        super(Slider, o_o____1_____l____1___O____l__O_1).__init__(*args, **o_____O_1_O_____O___l____o_1)
        o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1 = o___O_____o_1_o____O____o_____1
        o_o____1_____l____1___O____l__O_1.setOrientation(Qt.Horizontal)
        o_o____1_____l____1___O____l__O_1.setMinimumWidth(26)
        o_o____1_____l____1___O____l__O_1.setMaximumWidth(26)
        o_o____1_____l____1___O____l__O_1.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        o_o____1_____l____1___O____l__O_1.setContextMenuPolicy(Qt.CustomContextMenu)
        o_o____1_____l____1___O____l__O_1.customContextMenuRequested.connect(o_o____1_____l____1___O____l__O_1.parent().o__O_o__0____o___o__0__0____o)
        o_o____1_____l____1___O____l__O_1.o___l___o____0____0_____1____l___l___l()
        o_o____1_____l____1___O____l__O_1.sliderReleased.connect(o_o____1_____l____1___O____l__O_1.o__O___l_O___1___l_O___0_____o)
        o_o____1_____l____1___O____l__O_1.valueChanged.connect(o_o____1_____l____1___O____l__O_1.o____l_O____o__0__l___0_0____1)
        o_o____1_____l____1___O____l__O_1.sliderPressed.connect(o_o____1_____l____1___O____l__O_1.o_1___o_____O___l_O)

    def o_1___o_____O___l_O(o_o____1_____l____1___O____l__O_1):
        CORE.moduleBot.o_____O___1_____1_____o(o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.o____0____o____1___O_____0_O___1)
        o_o____1_____l____1___O____l__O_1.sliderPressed.disconnect()
        o_o____1_____l____1___O____l__O_1.sliderPressed.connect(o_o____1_____l____1___O____l__O_1.o____l__1____o_1_0___O___l)
        o_o____1_____l____1___O____l__O_1.sliderPressed.emit()

    def __o___o_l_1_1__0_0___1____O__l_____O(o_o____1_____l____1___O____l__O_1, o_O___l_____0__O_____1___l____0__0_____o___O):
        o_o____1_____l____1___O____l__O_1.o___l__0____0___o = o_O___l_____0__O_____1___l____0__0_____o___O
        o_o____1_____l____1___O____l__O_1.repaint()

    def paintEvent(o_o____1_____l____1___O____l__O_1, event):
        super(Slider, o_o____1_____l____1___O____l__O_1).paintEvent(event)
        painter = QPainter(o_o____1_____l____1___O____l__O_1)
        o_____O____1_____o___0 = 26
        o____O____l__0_l__l___O___0____l____1_0 = float(o_o____1_____l____1___O____l__O_1.sliderPosition() + o_o____1_____l____1___O____l__O_1.maximum())
        o_____o_O_0___1__0_o = o_o____1_____l____1___O____l__O_1.maximum() * 2.0
        center = o____O____l__0_l__l___O___0____l____1_0 / o_____o_O_0___1__0_o * (o_o____1_____l____1___O____l__O_1.width() - o_____O____1_____o___0)
        o____o_0__0____o___0__0____o_0 = 1 if o_o____1_____l____1___O____l__O_1.o__l___l____0____l_0____O____o_____l____0 else 0
        if o_o____1_____l____1___O____l__O_1.isEnabled():
            icon = o__1___l_1____1_l__o__0(o_o____1_____l____1___O____l__O_1.currentIcon(), hover=o_o____1_____l____1___O____l__O_1.o___l__0____0___o).toImage()
            painter.drawImage(center + o____o_0__0____o___0__0____o_0 + 1, o____o_0__0____o___0__0____o_0 + 1, icon.scaled(22, 22, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        if o_o____1_____l____1___O____l__O_1.o__l___l____0____l_0____O____o_____l____0:
            textValue = '%.2f' % o_o____1_____l____1___O____l__O_1.o_1___O___0_l()
            o___l_0__0___o = o_o____1_____l____1___O____l__O_1.o_____l__1__O_____0____1_0_1___1 - QCursor.pos().x()
            o_l__o_0_O___0____o = o___l_0__0___o <= 0
            align = Qt.AlignLeft if o_l__o_0_O___0____o else Qt.AlignRight
            rect = QRect(10, 6, o_o____1_____l____1___O____l__O_1.parent().width() - 20, o_o____1_____l____1___O____l__O_1.parent().height())
            painter.begin(o_o____1_____l____1___O____l__O_1)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setFont(QFont('Decorative', 12))
            painter.setPen(QColor(CORE.color.darkWhite))
            painter.drawText(rect, align, textValue)
        painter.end()

    def o_____l_____O_o____1___o_l__O(o_o____1_____l____1___O____l__O_1, value):
        o_o____1_____l____1___O____l__O_1.setSliderPosition(value)

    def o____l_O____o__0__l___0_0____1(o_o____1_____l____1___O____l__O_1, value):
        if not o_o____1_____l____1___O____l__O_1.o__l___l____0____l_0____O____o_____l____0:
            o_o____1_____l____1___O____l__O_1.o_____l_____O_o____1___o_l__O(0)
            return
        if value == 0 and not o_o____1_____l____1___O____l__O_1.o___O_l___1_____o_____l_0:
            return
        if not o_o____1_____l____1___O____l__O_1.o___O_l___1_____o_____l_0 and abs(o_o____1_____l____1___O____l__O_1.o_____l__1__O_____0____1_0_1___1 - QCursor.pos().x()) <= 5:
            o_o____1_____l____1___O____l__O_1.o_____l_____O_o____1___o_l__O(0)
            return
        o_o____1_____l____1___O____l__O_1.o___O_l___1_____o_____l_0 = True
        if (o_o____1_____l____1___O____l__O_1.o_1_0____0____1___0__O == Slider.kRight or o_o____1_____l____1___O____l__O_1.o_1_0____0____1___0__O is None) and o_o____1_____l____1___O____l__O_1.o_1___O___0_l() < 0:
            o___1__1____l_l___l____l = Slider.kLeft
        else:
            if (o_o____1_____l____1___O____l__O_1.o_1_0____0____1___0__O == Slider.kLeft or o_o____1_____l____1___O____l__O_1.o_1_0____0____1___0__O is None) and o_o____1_____l____1___O____l__O_1.o_1___O___0_l() > 0:
                o___1__1____l_l___l____l = Slider.kRight
            else:
                o___1__1____l_l___l____l = None
        if o___1__1____l_l___l____l is not None:
            if o_o____1_____l____1___O____l__O_1.o_1_0____0____1___0__O is not None:
                o_o____1_____l____1___O____l__O_1.o_____o____O____O____0_o.emit(o_o____1_____l____1___O____l__O_1.parent().o_____o__1___o_____l_0, o___1__1____l_l___l____l)
            o_o____1_____l____1___O____l__O_1.o_1_0____0____1___0__O = o___1__1____l_l___l____l
            o_o____1_____l____1___O____l__O_1.parent().o_____O_O____0.o_O_1___1.o____1____1____0_____l____O___l = o___1__1____l_l___l____l
            o_o____1_____l____1___O____l__O_1.parent().o_____O_O____0.o_O_1___1.repaint()
        o_o____1_____l____1___O____l__O_1.o_____1___1___1.emit(o_o____1_____l____1___O____l__O_1.o_1___O___0_l())
        return

    def o____l__1____o_1_0___O___l(o_o____1_____l____1___O____l__O_1):
        o_1 = o_o____1_____l____1___O____l__O_1.parent().o_____O_O____0.o_O_1___1.o_1
        o__0_____0____o__l_0_l___0 = o_o____1_____l____1___O____l__O_1.parent().o_____O_O____0.o_O_1___1.o__0_____0____o__l_0_l___0
        o_o____1_____l____1___O____l__O_1.o___0____1_O__O_____1_____o.emit(o_o____1_____l____1___O____l__O_1.parent().o_____o__1___o_____l_0, (o_1, o__0_____0____o__l_0_l___0))
        o_o____1_____l____1___O____l__O_1.o_____l__1__O_____0____1_0_1___1 = QCursor.pos().x()
        o_o____1_____l____1___O____l__O_1.o___O_l___1_____o_____l_0 = False
        o_o____1_____l____1___O____l__O_1.o__l___O_1__O_____O_____1__l(True)
        o_o____1_____l____1___O____l__O_1.setMaximumWidth(o___0_l_o__O_o_____l_____O___l___o)
        o_o____1_____l____1___O____l__O_1.__o_____l____l_____1____O___0___o____o__1__O___0()
        o_o____1_____l____1___O____l__O_1.o___l___o____0____0_____1____l___l___l(highlight=True)
        o_o____1_____l____1___O____l__O_1.o_1_0____0____1___0__O = None
        o_o____1_____l____1___O____l__O_1.parent().o_____O_O____0.o_O_1___1.o____1____1____0_____l____O___l = o_o____1_____l____1___O____l__O_1.o_1_0____0____1___0__O
        sliderWidget = o_o____1_____l____1___O____l__O_1.parent().o_____O_O____0.o_O_1___1.o___l___l__O or o_o____1_____l____1___O____l__O_1.parent().o_____O_O____0.o_O_1___1.o_____o_0__l__0____1
        o___0____o___0_1____o_0_l_1____0 = sliderWidget.o__1___o___O___1_____0__O____0___0 or False
        o_o____1_____l____1___O____l__O_1.parent().o_____O_O____0.o_O_1___1.o____1___l_____o_____1____O____0_1__l_____1____0(o___0____o___0_1____o_0_l_1____0)
        o_o____1_____l____1___O____l__O_1.parent().o_____O_O____0.o_O_1___1.repaint()
        return

    def o__O___l_O___1___l_O___0_____o(o_o____1_____l____1___O____l__O_1):
        o_o____1_____l____1___O____l__O_1.o__l___O_1__O_____O_____1__l(False)
        o_o____1_____l____1___O____l__O_1.o__l_o___O_O.emit(o_o____1_____l____1___O____l__O_1.o_1___O___0_l(), o_o____1_____l____1___O____l__O_1.parent().o_____o__1___o_____l_0)
        o_o____1_____l____1___O____l__O_1.__o_____O___l____0_o__o___1___l()
        CORE.deferBot.o_0____o_O____o____l__0(o_o____1_____l____1___O____l__O_1.__o_____O___l____0_o__o___1___l)

    def __o_____O___l____0_o__o___1___l(o_o____1_____l____1___O____l__O_1):
        o_o____1_____l____1___O____l__O_1.setMaximumWidth(26)
        o_o____1_____l____1___O____l__O_1.__o_____l____l_____1____O___0___o____o__1__O___0()
        o_o____1_____l____1___O____l__O_1.o___l___o____0____0_____1____l___l___l(highlight=False)
        o_o____1_____l____1___O____l__O_1.parent().o_O_0_____1_1___l__0___l(o_o____1_____l____1___O____l__O_1.parent().o_____O_O____0.o_1_O__1___0____l())
        o_o____1_____l____1___O____l__O_1.parent().o_____O_O____0.o_O_1___1.o____1____1____0_____l____O___l = None
        o_o____1_____l____1___O____l__O_1.parent().o_____O_O____0.o_O_1___1.repaint()
        return

    def o__l___O_1__O_____O_____1__l(o_o____1_____l____1___O____l__O_1, state):
        o_o____1_____l____1___O____l__O_1.o__l___l____0____l_0____O____o_____l____0 = state

    def o__O_o_1____o_l____O(o_o____1_____l____1___O____l__O_1):
        return ('\n        ::groove:horizontal {{\n            background-color: {0};\n            height: {1}px;\n            border-radius: {2}px;\n        }}\n        ::handle:horizontal {{\n            width: {1}px;\n            border: {3}px solid {4};\n            background-color: {5};\n            border-radius: {2}px;\n        }}\n    ').format(CORE.color.gray, 24, 5, 1, CORE.color.darkGray, o_o____1_____l____1___O____l__O_1.backgroundColor)

    def currentIcon(o_o____1_____l____1___O____l__O_1):
        return o_o____1_____l____1___O____l__O_1.o_1____O_____1__0____O_____o_____1____1 or o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.icon

    def o_____o_o_O__O_____o(o_o____1_____l____1___O____l__O_1, o___0_____1__1___0___0_o__o__o__O____0):
        o_o____1_____l____1___O____l__O_1.o_1____O_____1__0____O_____o_____1____1 = o___0_____1__1___0___0_o__o__o__O____0

    def o___l___o____0____0_____1____l___l___l(o_o____1_____l____1___O____l__O_1, highlight=False):
        o___o_____O___o_____l____O_l = CORE.color.o_o(o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.o_l__0___l_o____1_____0)
        o_o____1_____l____1___O____l__O_1.backgroundColor = CORE.color.lightGray if not highlight else o___o_____O___o_____l____O_l
        o_o____1_____l____1___O____l__O_1.setStyleSheet(o_o____1_____l____1___O____l__O_1.o__O_o_1____o_l____O())

    def o_1___O___0_l(o_o____1_____l____1___O____l__O_1):
        sliderValue = o_o____1_____l____1___O____l__O_1.value()
        if not o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.config.get('linearValue', None):
            o__l___l___1_____0__o___0 = o_o____1_____l____1___O____l__O_1.maximum() if sliderValue > 0 else o_o____1_____l____1___O____l__O_1.minimum()
            sliderValue = sliderValue * sliderValue / o__l___l___1_____0__o___0
        return sliderValue / 1000.0

    def __o_____l____l_____1____O___0___o____o__1__O___0(o_o____1_____l____1___O____l__O_1):
        o_o____1_____l____1___O____l__O_1.setValue(0)

    def enterEvent(o_o____1_____l____1___O____l__O_1, event):
        super(Slider, o_o____1_____l____1___O____l__O_1).enterEvent(event)
        o_o____1_____l____1___O____l__O_1.__o___o_l_1_1__0_0___1____O__l_____O(True)
        o____l_0_O(o_o____1_____l____1___O____l__O_1.o__l__0____0_____l_1__0_l__0())

    def leaveEvent(o_o____1_____l____1___O____l__O_1, event):
        super(Slider, o_o____1_____l____1___O____l__O_1).leaveEvent(event)
        o_o____1_____l____1___O____l__O_1.__o___o_l_1_1__0_0___1____O__l_____O(False)
        o____l_0_O.o__l____o____O____0()

    def mousePressEvent(o_o____1_____l____1___O____l__O_1, event):
        o_____O___l___O____o__1__O = event.button() == Qt.MiddleButton
        o____o__0_____0__O____O_1_O__0__l____O = event.button() == Qt.LeftButton
        if o_____O___l___O____o__1__O:
            o_o____1_____l____1___O____l__O_1.o_____o_____1____l____O_____l__l.emit()
            o____l___1____0__o_____O_____1__o_O = QMouseEvent(event.type(), event.pos(), Qt.LeftButton, Qt.LeftButton, event.modifiers())
            event = o____l___1____0__o_____O_____1__o_O
        else:
            if o____o__0_____0__O____O_1_O__0__l____O:
                o_o____1_____l____1___O____l__O_1.o___O_O____1_0___l___o___o___O__l_____l.emit()
        super(Slider, o_o____1_____l____1___O____l__O_1).mousePressEvent(event)

    def mouseReleaseEvent(o_o____1_____l____1___O____l__O_1, event):
        o_____O___l___O____o__1__O = event.button() == Qt.MiddleButton
        o____o__0_____0__O____O_1_O__0__l____O = event.button() == Qt.LeftButton
        if o_____O___l___O____o__1__O:
            o_o____1_____l____1___O____l__O_1.o_____o_____1____l____O_____l__l.emit()
        else:
            if o____o__0_____0__O____O_1_O__0__l____O:
                o_o____1_____l____1___O____l__O_1.o___O_O____1_0___l___o___o___O__l_____l.emit()
        super(Slider, o_o____1_____l____1___O____l__O_1).mouseReleaseEvent(event)

    def o__l__0____0_____l_1__0_l__0(o_o____1_____l____1___O____l__O_1):
        o___O_____o_1_o____O____o_____1 = o__O___l_____o_l__l___o__1__1.o___1____l____l_____0_o__O___1___l____1(o_o____1_____l____1___O____l__O_1.parent().o_____o__1___o_____l_0)
        if o___O_____o_1_o____O____o_____1 is not None:
            return o___O_____o_1_o____O____o_____1
        return o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1


class o_O____1(CORE.toolWidgets.o___l_1___o____l_o_o___l, QWidget, o_o___o___o_O____1_____O_O):
    o____o_1__1____1_____0_____0_____o___o = Signal(str)

    def __init__(o_o____1_____l____1___O____l__O_1, o___O_____o_1_o____O____o_____1, *args):
        super(o_O____1, o_o____1_____l____1___O____l__O_1).__init__(o___O_____o_1_o____O____o_____1, *args)
        QWidget.__init__(o_o____1_____l____1___O____l__O_1, *args)
        exec 'CORE.%sWidgets = CORE.%sWidgets or []' % (o_o____1_____l____1___O____l__O_1.o____0____o____1___O_____0_O___1, o_o____1_____l____1___O____l__O_1.o____0____o____1___O_____0_O___1)
        exec 'CORE.%sWidgets.append(o_o____1_____l____1___O____l__O_1)' % o_o____1_____l____1___O____l__O_1.o____0____o____1___O_____0_O___1
        o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1 = o___O_____o_1_o____O____o_____1
        o_o____1_____l____1___O____l__O_1.o____o_0_0___l_____o__o__o_____l___O = o_o____1_____l____1___O____l__O_1.parent()
        o_o____1_____l____1___O____l__O_1.o_l__1___l___O___O__l = o_o____1_____l____1___O____l__O_1.parent().parent()
        o_o____1_____l____1___O____l__O_1.o___o____0_l = o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.config.get('mod', None)
        o_o____1_____l____1___O____l__O_1.o_o_____l__1__0 = o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.config.get('o_____O___l___O____o__1__O', None)
        o_o____1_____l____1___O____l__O_1.o_____o__1___o_____l_0 = o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.o____1
        o_o____1_____l____1___O____l__O_1.o__1___o___O___1_____0__O____0___0 = o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.config.get('o__1___o___O___1_____0__O____0___0', None)
        o_o____1_____l____1___O____l__O_1.isWorldSpace = o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.config.get('isWorldSpace', False)
        o_o____1_____l____1___O____l__O_1.setContentsMargins(2, 0, 2, 0)
        o_o____1_____l____1___O____l__O_1.setMinimumHeight(24)
        o_o____1_____l____1___O____l__O_1.setMinimumWidth(o___0_l_o__O_o_____l_____O___l___o)
        o_o____1_____l____1___O____l__O_1.setMaximumWidth(o___0_l_o__O_o_____l_____O___l___o)
        o_o____1_____l____1___O____l__O_1.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        o____1_o_O = QHBoxLayout()
        o____1_o_O.setContentsMargins(0, 0, 0, 0)
        o____1_o_O.setSpacing(0)
        o__O_l__1____l___O_l____0__o = QHBoxLayout()
        o__O_l__1____l___O_l____0__o.setContentsMargins(0, 0, 0, 0)
        o__O_l__1____l___O_l____0__o.setSpacing(0)
        o____1_o_O.addLayout(o__O_l__1____l___O_l____0__o)
        o_o____1_____l____1___O____l__O_1.o_l_o____o = Slider(o___O_____o_1_o____O____o_____1, o_o____1_____l____1___O____l__O_1)
        o__O_l__1____l___O_l____0__o.addWidget(o_o____1_____l____1___O____l__O_1.o_l_o____o, 1)
        o_o____1_____l____1___O____l__O_1.__o_____0__O____o_____0_o()
        o_o____1_____l____1___O____l__O_1.setLayout(o____1_o_O)
        o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_O_1___1.o_____o_0__l__0____1 = o_o____1_____l____1___O____l__O_1
        o_o____1_____l____1___O____l__O_1.o_l_o____o.o___O_O____1_0___l___o___o___O__l_____l.connect(o_o____1_____l____1___O____l__O_1.o__O____O___o____O_l___O)
        o_o____1_____l____1___O____l__O_1.o_l_o____o.o_____o_____1____l____O_____l__l.connect(o_o____1_____l____1___O____l__O_1.o_____O____o_o___0____0_1_____0___l__1)
        o_o____1_____l____1___O____l__O_1.o_l_o____o.o___0____1_O__O_____1_____o.connect(o_o____1_____l____1___O____l__O_1.__o__l____0_____1____o____1____O____l___o_0)
        o_o____1_____l____1___O____l__O_1.show()
        return

    @o_____0_____o____O
    def sliderWidgets(o_o____1_____l____1___O____l__O_1):
        return eval('CORE.%sWidgets' % o_o____1_____l____1___O____l__O_1.o____0____o____1___O_____0_O___1)

    @o_____0_____o____O
    def o____l____O__l(o_o____1_____l____1___O____l__O_1):
        buttons = o_o____1_____l____1___O____l__O_1.o__1_____l__O_____0__o_____l.o__l____O_____0__O___l____o____l__1__1___0 + o_o____1_____l____1___O____l__O_1.o__1_____l__O_____0__o_____l.o__l___0__0____o__1____0____1____o__l + o_o____1_____l____1___O____l__O_1.o_____O___O_____O___1____o.o__l____O_____0__O___l____o____l__1__1___0 + o_o____1_____l____1___O____l__O_1.o_____O___O_____O___1____o.o__l___0__0____o__1____0____1____o__l
        return [ button for button in buttons ]

    def show(o_o____1_____l____1___O____l__O_1, *args):
        super(o_O____1, o_o____1_____l____1___O____l__O_1).show(*args)
        o_o____1_____l____1___O____l__O_1.o__1_____l__O_____0__o_____l = o____l___O___l(o_o____1_____l____1___O____l__O_1, o____l___O___l.kLeft, o_o____1_____l____1___O____l__O_1)
        o_o____1_____l____1___O____l__O_1.o_____O___O_____O___1____o = o____l___O___l(o_o____1_____l____1___O____l__O_1, o____l___O___l.kRight, o_o____1_____l____1___O____l__O_1)
        o_o____1_____l____1___O____l__O_1.setOvershootMode(False)

    def __o__O_____l____l____O__O__O____l_____l_1(o_o____1_____l____1___O____l__O_1):
        if o_o____1_____l____1___O____l__O_1.menu:
            return o_o____1_____l____1___O____l__O_1.menu
        o_o____1_____l____1___O____l__O_1.o_0_O_____O___1_1_____0_____l__l____1 = {}
        menu = QMenu(o_o____1_____l____1___O____l__O_1)
        actionGroup = QActionGroup(o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.parentWidget, exclusive=True, objectName='sliderModeActionGroup')
        action = QAction('Sliders', menu)
        action.setSeparator(True)
        action.setActionGroup(actionGroup)
        menu.addAction(action)
        for _o_0____0__O_____1_O_0 in o_o____1_____l____1___O____l__O_1.o_l__1___l___O___O__l.toolWidgets:
            if _o_0____0__O_____1_O_0.o___O_____o_1_o____O____o_____1.o____0_l__l_1_____O_o != 'o_O____1':
                continue
            if _o_0____0__O_____1_O_0.o___O_____o_1_o____O____o_____1.separator:
                menu.addSeparator()
            o____O_____o_0___l__0___O = o_O_____0____1___l(_o_0____0__O_____1_O_0.widget.o___o____0_l).o__0__l____0___O_____l____0()
            if _o_0____0__O_____1_O_0.widget.o_o_____l__1__0:
                o_____1___0____1__0 = '+MidClick' if 1 else ''
                o___1____0_O__O___O_0 = '%s\t%s%s' % (_o_0____0__O_____1_O_0.o___O_____o_1_o____O____o_____1.o___1____0_O__O___O_0, o____O_____o_0___l__0___O, o_____1___0____1__0)
                action = QAction(QIcon(o__1___l_1____1_l__o__0(_o_0____0__O_____1_O_0.o___O_____o_1_o____O____o_____1.icon)), o___1____0_O__O___O_0, menu)
                o_o____1_____l____1___O____l__O_1.o_0_O_____O___1_1_____0_____l__l____1[_o_0____0__O_____1_O_0.o___O_____o_1_o____O____o_____1.o____1] = action
                action.setActionGroup(actionGroup)
                action.setCheckable(True)
                action.triggered.connect(lambda o____o_0_0___l_____o__o__o_____l___O=_o_0____0__O_____1_O_0, *args: o_o____1_____l____1___O____l__O_1.__o_____l___l___1___l__o__o___o_____1_0(o____o_0_0___l_____o__o__o_____l___O))
                menu.addAction(action)

        return menu

    def __o____l_o____1____o(o_o____1_____l____1___O____l__O_1):
        if not o_o____1_____l____1___O____l__O_1.o_0_O_____O___1_1_____0_____l__l____1:
            return
        for _o_0____0__O_____1_O_0 in o_o____1_____l____1___O____l__O_1.o_l__1___l___O___O__l.toolWidgets:
            o_0_O_____O___1_1_____0_____l__l____1 = _o_0____0__O_____1_O_0.widget.o_0_O_____O___1_1_____0_____l__l____1
            if not o_0_O_____O___1_1_____0_____l__l____1:
                continue
            for _o___o____0__O___1____O_o____O____o____o in o_o____1_____l____1___O____l__O_1.o_l__1___l___O___O__l.toolWidgets:
                action = o_0_O_____O___1_1_____0_____l__l____1.get(_o___o____0__O___1____O_o____O____o____o.o___O_____o_1_o____O____o_____1.o____1, None)
                if not action:
                    continue
                if not o_o____1_____l____1___O____l__O_1.o_l__1___l___O___O__l.o____O_____0___1():
                    action.setVisible(False)
                    continue
                else:
                    action.setVisible(True)
                if not action:
                    continue
                isEnabled = not _o___o____0__O___1____O_o____O____o____o.o___0____l___l_____o__l____1()
                action.setEnabled(isEnabled)
                isChecked = o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.o____1 == _o___o____0__O___1____O_o____O____o____o.o___O_____o_1_o____O____o_____1.o____1
                if action.isChecked != isChecked:
                    action.setChecked(isChecked)

        return

    def o__O_o__0____o___o__0__0____o(o_o____1_____l____1___O____l__O_1):
        if o_o____1_____l____1___O____l__O_1.menu and o_o____1_____l____1___O____l__O_1.menu.isTearOffMenuVisible():
            o_o____1_____l____1___O____l__O_1.menu.close()
        o_o____1_____l____1___O____l__O_1.menu = o_o____1_____l____1___O____l__O_1.__o__O_____l____l____O__O__O____l_____l_1()
        o_o____1_____l____1___O____l__O_1.__o____l_o____1____o()
        o_o____1_____l____1___O____l__O_1.menu.exec_(QCursor.pos())

    def setOvershootMode(o_o____1_____l____1___O____l__O_1, o___o_____0_____1_0_____o):
        o_____0_1__1_____O_1_____o_____1_____1___O = o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.config.get('o____1_____1_____1_____1____1__O_0____l_0___0', o_____1___1____O__o_____o___o_____o_o_____l_____0_____l_____l___1___0____1_o___0____O___1__o____0_O____O__0___l____O_o____0_l___l)[-1]
        o_____l_1___o__O_____0___O___o___0_o = o_____0_1__1_____O_1_____o_____1_____1___O * 1000 if o___o_____0_____1_0_____o else 100000
        o_o____1_____l____1___O____l__O_1.o__o__o____o___1 = o___o_____0_____1_0_____o
        o_o____1_____l____1___O____l__O_1.__setPresetOvershootButonsVisible(o___o_____0_____1_0_____o)
        o_o____1_____l____1___O____l__O_1.o_l_o____o.setMinimum(o_____l_1___o__O_____0___O___o___0_o * -1)
        o_o____1_____l____1___O____l__O_1.o_l_o____o.setMaximum(o_____l_1___o__O_____0___O___o___0_o)

    def setWorldSpaceMode(o_o____1_____l____1___O____l__O_1, o_____1____0___0_O__1____o___O):
        o_o____1_____l____1___O____l__O_1.o_____1____0___0_O__1____o___O = o_____1____0___0_O__1____o___O
        worldSpace = o_____1____0___0_O__1____o___O and o_o____1_____l____1___O____l__O_1.isWorldSpace
        o_o____1_____l____1___O____l__O_1.o__1_____l__O_____0__o_____l.o__l____O_____0__O___l____o____l__1__1___0[-1].setWorldSpace(worldSpace)
        o_o____1_____l____1___O____l__O_1.o_____O___O_____O___1____o.o__l____O_____0__O___l____o____l__1__1___0[-1].setWorldSpace(worldSpace)

    def __o_____0__O____o_____0_o(o_o____1_____l____1___O____l__O_1):
        o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_O_1___1 = o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_O_1___1 or o_____1__l_____1_1____1_____O_O__0_____0(o_o____1_____l____1___O____l__O_1.o_____O_O____0)

    def __o_____l___l___1___l__o__o___o_____1_0(o_o____1_____l____1___O____l__O_1, o__o__1___o___0__l):
        if o__o__1___o___0__l.o___0____l___l_____o__l____1():
            return
        o__o__1___o___0__l.o_O____O_____0__l__o(True)
        o_o____1_____l____1___O____l__O_1.o____o_0_0___l_____o__o__o_____l___O.o_O____O_____0__l__o(False)
        o__o__1___o___0__l.widget.o____O_0___0()

    def __o__O_o__l_____l_O___1__1_____0_l(o_o____1_____l____1___O____l__O_1):
        if o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_O_1___1.o__O_l_l__1___l__O:
            return
        if QApplication.mouseButtons() != Qt.NoButton:
            return
        o_o____1_____l____1___O____l__O_1.__o_1_____o____l__0__0_____O(True)
        o_o____1_____l____1___O____l__O_1.__o_____0__o__O____1____1____O__o_____o_____1(False)
        o_o____1_____l____1___O____l__O_1.o_____o__1___o_____l_0 = o_o____1_____l____1___O____l__O_1.o___O_____o_1_o____O____o_____1.o____1
        o_o____1_____l____1___O____l__O_1.o_l_o____o.o_____o_o_O__O_____o(None)
        o_o____1_____l____1___O____l__O_1.o_l_o____o.o___l___o____0____0_____1____l___l___l()
        o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_O_1___1.o___l___l__O = None
        o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_O_1___1.o____1___l_____o_____1____O____0_1__l_____1____0(False)
        if o_o____1_____l____1___O____l__O_1.o__1___o___O___1_____0__O____0___0:
            o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_O_1___1.o____1___l_____o_____1____O____0_1__l_____1____0(True)
            o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_O_1___1.o____0_O__o____O___1_____1(False)
        return

    def __o___l___O_____0___1___O__o__0_____0____O(o_o____1_____l____1___O____l__O_1, o__o__1___o___0__l, click=None):
        if QApplication.mouseButtons() != Qt.NoButton and not click:
            return
        if not click:
            o_o____1_____l____1___O____l__O_1.__o_1_____o____l__0__0_____O(False)
            o_o____1_____l____1___O____l__O_1.__o_____0__o__O____1____1____O__o_____o_____1(True, o__o__1___o___0__l)
        o_o__l__O_0 = o__o__1___o___0__l.o___O_____o_1_o____O____o_____1.icon
        o_o____1_____l____1___O____l__O_1.o_____o__1___o_____l_0 = o__o__1___o___0__l.o___O_____o_1_o____O____o_____1.o____1
        o_o____1_____l____1___O____l__O_1.o_l_o____o.o_____o_o_O__O_____o(o_o__l__O_0)
        o_o____1_____l____1___O____l__O_1.o_l_o____o.o___l___o____0____0_____1____l___l___l()
        o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_O_1___1.o___l___l__O = o__o__1___o___0__l
        o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_O_1___1.o____1___l_____o_____1____O____0_1__l_____1____0(False)
        if o__o__1___o___0__l.o__1___o___O___1_____0__O____0___0:
            o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_O_1___1.o____1___l_____o_____1____O____0_1__l_____1____0(True)
            o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_O_1___1.o____0_O__o____O___1_____1(False)

    def o_O_0_____1_1___l__0___l(o_o____1_____l____1___O____l__O_1, o____O_____o_0___l__0___O):
        if o____O_____o_0___l__0___O == '':
            o_o____1_____l____1___O____l__O_1.__o__O_o__l_____l_O___1__1_____0_l()
            return
        for _o_0____0__O_____1_O_0 in o_o____1_____l____1___O____l__O_1.sliderWidgets:
            if _o_0____0__O_____1_O_0.o___o____0_l == o____O_____o_0___l__0___O and not _o_0____0__O_____1_O_0.o_o_____l__1__0:
                o_o____1_____l____1___O____l__O_1.__o___l___O_____0___1___O__o__0_____0____O(_o_0____0__O_____1_O_0)
                break

    def __o_1_____o____l__0__0_____O(o_o____1_____l____1___O____l__O_1, isVisible):
        for _o_____1__1____O in [o_o____1_____l____1___O____l__O_1.o__1_____l__O_____0__o_____l, o_o____1_____l____1___O____l__O_1.o_____O___O_____O___1____o]:
            _o_____1__1____O.setVisible(isVisible)

    def __o___O_o_____0_l_o___0(o_o____1_____l____1___O____l__O_1):
        o_o____1_____l____1___O____l__O_1.__o_1_____o____l__0__0_____O(True)

    def __o__l____0_____1____o____1____O____l___o_0(o_o____1_____l____1___O____l__O_1, *args):
        o_o____1_____l____1___O____l__O_1.__o_1_____o____l__0__0_____O(False)
        for _o_____1__1____O in [o_o____1_____l____1___O____l__O_1.o_o_____o__1__0____0___1___o, o_o____1_____l____1___O____l__O_1.o___1_l___O]:
            if _o_____1__1____O is not None:
                _o_____1__1____O.lower()

        return

    def __o_____0__o__O____1____1____O__o_____o_____1(o_o____1_____l____1___O____l__O_1, isVisible, o__o__1___o___0__l=None):
        for _o_____1__1____O in [o_o____1_____l____1___O____l__O_1.o_o_____o__1__0____0___1___o, o_o____1_____l____1___O____l__O_1.o___1_l___O]:
            if _o_____1__1____O is not None:
                _o_____1__1____O.deleteLater()

        o_o____1_____l____1___O____l__O_1.o_o_____o__1__0____0___1___o = None
        o_o____1_____l____1___O____l__O_1.o___1_l___O = None
        o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_O_1___1.o___l___l__O = None
        if isVisible:
            o_o____1_____l____1___O____l__O_1.o_o_____o__1__0____0___1___o = o____l___O___l(o__o__1___o___0__l, o____l___O___l.kLeft, o_o____1_____l____1___O____l__O_1)
            o_o____1_____l____1___O____l__O_1.o___1_l___O = o____l___O___l(o__o__1___o___0__l, o____l___O___l.kRight, o_o____1_____l____1___O____l__O_1)
        return

    def __setPresetOvershootButonsVisible(o_o____1_____l____1___O____l__O_1, isVisible):
        for _o_____1__1____O in [o_o____1_____l____1___O____l__O_1.o__1_____l__O_____0__o_____l, o_o____1_____l____1___O____l__O_1.o_____O___O_____O___1____o]:
            _o_____1__1____O.setPresetOvershootButtonsVisible(isVisible)

    def paintEvent(o_o____1_____l____1___O____l__O_1, event):
        painter = QPainter()
        painter.begin(o_o____1_____l____1___O____l__O_1)
        painter.setPen(QPen(QColor(CORE.color.gray), 10, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(7, o_o____1_____l____1___O____l__O_1.height() / 2, o_o____1_____l____1___O____l__O_1.width() - 7, o_o____1_____l____1___O____l__O_1.height() / 2)
        painter.end()

    def enterEvent(o_o____1_____l____1___O____l__O_1, event):
        if o_o____1_____l____1___O____l__O_1.o____O_____o___O___0__1_l____o___1:
            return
        super(o_O____1, o_o____1_____l____1___O____l__O_1).enterEvent(event)
        o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_O_1___1.o_____o_0__l__0____1 = o_o____1_____l____1___O____l__O_1
        if o_o____1_____l____1___O____l__O_1.o__1___o___O___1_____0__O____0___0:
            o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_O_1___1.o____1___l_____o_____1____O____0_1__l_____1____0(True)
            o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_O_1___1.o____0_O__o____O___1_____1(False)
            o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_O_1___1.repaint()
        o____o__0__o_____1 = o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_1_O__1___0____l()
        if o____o__0__o_____1 != '':
            o_o____1_____l____1___O____l__O_1.o_O_0_____1_1___l__0___l(o____o__0__o_____1)

    def leaveEvent(o_o____1_____l____1___O____l__O_1, event):
        super(o_O____1, o_o____1_____l____1___O____l__O_1).leaveEvent(event)
        o_o____1_____l____1___O____l__O_1.__o__O_o__l_____l_O___1__1_____0_l()
        o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_O_1___1.o____1___l_____o_____1____O____0_1__l_____1____0(False)

    def o___O___l___o_O___1(o_o____1_____l____1___O____l__O_1, event):
        if not o_o____1_____l____1___O____l__O_1.o____O_____o___O___0__1_l____o___1:
            return
        o____O_____o_0___l__0___O = CORE.animBotToolbar.o___l_____l___o(event)
        if o____O_____o_0___l__0___O == '':
            o_o____1_____l____1___O____l__O_1.__o__O_o__l_____l_O___1__1_____0_l()
        o_o____1_____l____1___O____l__O_1.o_O_0_____1_1___l__0___l(o____O_____o_0___l__0___O)

    def o_____1_____O__0(o_o____1_____l____1___O____l__O_1, event):
        if not o_o____1_____l____1___O____l__O_1.o____O_____o___O___0__1_l____o___1:
            return
        o____O_____o_0___l__0___O = CORE.animBotToolbar.o___l_____l___o(event)
        o_o____1_____l____1___O____l__O_1.o_O_0_____1_1___l__0___l(o____O_____o_0___l__0___O)

    def o__O____O___o____O_l___O(o_o____1_____l____1___O____l__O_1, parentWidget=None):
        o___O___O__O_o____l__O__0 = parentWidget or o_o____1_____l____1___O____l__O_1
        o___O___O__O_o____l__O__0.__o____0____1____1___1_____0_l(False)

    def o_____O____o_o___0____0_1_____0___l__1(o_o____1_____l____1___O____l__O_1, parentWidget=None):
        o___O___O__O_o____l__O__0 = parentWidget or o_o____1_____l____1___O____l__O_1
        o___O___O__O_o____l__O__0.__o____0____1____1___1_____0_l(True)

    def __o____0____1____1___1_____0_l(o_o____1_____l____1___O____l__O_1, o___o_____l__o__1__O_____1_o):
        o____o__0__o_____1 = o_o____1_____l____1___O____l__O_1.o_____O_O____0.o_1_O__1___0____l()
        if o____o__0__o_____1 == '':
            return
        for _o_0____0__O_____1_O_0 in o_o____1_____l____1___O____l__O_1.sliderWidgets:
            if _o_0____0__O_____1_O_0.o___o____0_l == o____o__0__o_____1 and o___o_____l__o__1__O_____1_o and _o_0____0__O_____1_O_0.o_o_____l__1__0:
                o_o____1_____l____1___O____l__O_1.__o___l___O_____0___1___O__o__0_____0____O(_o_0____0__O_____1_O_0, click=True)
                break
            if _o_0____0__O_____1_O_0.o___o____0_l == o____o__0__o_____1 and not o___o_____l__o__1__O_____1_o and not _o_0____0__O_____1_O_0.o_o_____l__1__0:
                o_o____1_____l____1___O____l__O_1.__o___l___O_____0___1___O__o__0_____0____O(_o_0____0__O_____1_O_0, click=True)
                break


class o_____1__l_____1_1____1_____O_O__0_____0(QWidget, o____1_O_____0__l____0_____o____1):

    def __init__(o_o____1_____l____1___O____l__O_1, o_____O_O____0, *args, **o_____O_1_O_____O___l____o_1):
        super(o_____1__l_____1_1____1_____O_O__0_____0, o_o____1_____l____1___O____l__O_1).__init__(o_____O_O____0, *args, **o_____O_1_O_____O___l____o_1)
        o_o____1_____l____1___O____l__O_1.o__O_____O__0_____l = CORE.o_O__O__1__o_o____l___l
        o_o____1_____l____1___O____l__O_1.o___l___l____1____0_____O____o___1___o = 12
        o_o____1_____l____1___O____l__O_1.leftMargin = 11
        o_o____1_____l____1___O____l__O_1.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        o_o____1_____l____1___O____l__O_1.setMouseTracking(True)
        o_o____1_____l____1___O____l__O_1.o_____O_O____0 = o_____O_O____0
        o_o____1_____l____1___O____l__O_1.o_1 = o_o____1_____l____1___O____l__O_1.o__O_1____O____o_____0__1____1____l_____0__1()
        o_o____1_____l____1___O____l__O_1.o__0_____0____o__l_0_l___0 = o_o____1_____l____1___O____l__O_1.o____1_O____1___O____O_____l___o()
        o_o____1_____l____1___O____l__O_1.o_____0__O_____1____o___O()
        o_o____1_____l____1___O____l__O_1.o____1___l_____o_____1____O____0_1__l_____1____0(False)
        o_o____1_____l____1___O____l__O_1.o____0_O__o____O___1_____1(False)
        o_o____1_____l____1___O____l__O_1.o_____O_O____0.o__O____O_0__0_____O_____O_____0____O__o.connect(o_o____1_____l____1___O____l__O_1.o____l__1__O__o)

    @o_____0_____o____O
    def color(o_o____1_____l____1___O____l__O_1):
        return CORE.color.white

    def o____0_o_1_l_O(o_o____1_____l____1___O____l__O_1):
        if o_o____1_____l____1___O____l__O_1.o____1____1____0_____l____O___l == Slider.kLeft or o_o____1_____l____1___O____l__O_1.o____1____1____0_____l____O___l is None:
            return o_o____1_____l____1___O____l__O_1.color
        return CORE.color.darkGray

    def o_____0____O_0__0_____o_____l____0(o_o____1_____l____1___O____l__O_1):
        if o_o____1_____l____1___O____l__O_1.o____1____1____0_____l____O___l == Slider.kRight or o_o____1_____l____1___O____l__O_1.o____1____1____0_____l____O___l is None:
            return o_o____1_____l____1___O____l__O_1.color
        return CORE.color.darkGray

    def o__O_1____O____o_____0__1____1____l_____0__1(o_o____1_____l____1___O____l__O_1):
        return int(cmds.playbackOptions(q=True, min=True))

    def o____1_O____1___O____O_____l___o(o_o____1_____l____1___O____l__O_1):
        return int(cmds.playbackOptions(q=True, max=True))

    def o__o____1__l__l___l___l____1___o_____o_____1(o_o____1_____l____1___O____l__O_1):
        if o_o____1_____l____1___O____l__O_1.o__O_____O__0_____l is not None:
            o_0____1___0_o_____O = o_o____1_____l____1___O____l__O_1.o__O_____O__0_____l.width() - o_o____1_____l____1___O____l__O_1.o__1_1____O___O_____O_o_____0___0_1__1() * 2
        else:
            o_0____1___0_o_____O = 1
        o____1_1_____o__o___O_____o_1_____1___0__0 = o_o____1_____l____1___O____l__O_1.o____1_O____1___O____O_____l___o() - o_o____1_____l____1___O____l__O_1.o__O_1____O____o_____0__1____1____l_____0__1() + 1
        return o_0____1___0_o_____O * 1.0 / o____1_1_____o__o___O_____o_1_____1___0__0

    def o__1_1____O___O_____O_o_____0___0_1__1(o_o____1_____l____1___O____l__O_1):
        o___o_l_l__o___o_O_o = CORE.o___0___0_____l_O.width() if CORE.o___0___0_____l_O.width() >= 600 else 600
        leftMargin = (o___o_l_l__o___o_O_o - 600) * 0.0065
        return leftMargin

    def paintEvent(o_o____1_____l____1___O____l__O_1, event):
        super(o_____1__l_____1_1____1_____O_O__0_____0, o_o____1_____l____1___O____l__O_1).paintEvent(event)
        sliderWidget = o_o____1_____l____1___O____l__O_1.o___l___l__O or o_o____1_____l____1___O____l__O_1.o_____o_0__l__0____1
        if not sliderWidget or not sliderWidget.o__1___o___O___1_____0__O____0___0:
            return
        painter = QPainter(o_o____1_____l____1___O____l__O_1)
        painter.begin(o_o____1_____l____1___O____l__O_1)
        painter.setRenderHint(QPainter.Antialiasing)
        o____l_____o__1_____1__O___O_1_1 = o_o____1_____l____1___O____l__O_1.o_____O_O____0.height()
        o_____1___l____o___0 = o_o____1_____l____1___O____l__O_1.o_____o_0__l__0____1.o__1_____l__O_____0__o_____l.o__O__1___1__O_1___0___O__l_0___O if not (o_o____1_____l____1___O____l__O_1.o___l___l__O and o_o____1_____l____1___O____l__O_1.o_____o_0__l__0____1.o_o_____o__1__0____0___1___o) else o_o____1_____l____1___O____l__O_1.o_____o_0__l__0____1.o_o_____o__1__0____0___1___o.o__O__1___1__O_1___0___O__l_0___O
        o__0_0_____l____0___o__O__o_____l = o_o____1_____l____1___O____l__O_1.o_____o_0__l__0____1.o_____O___O_____O___1____o.o__O__1___1__O_1___0___O__l_0___O if not (o_o____1_____l____1___O____l__O_1.o___l___l__O and o_o____1_____l____1___O____l__O_1.o_____o_0__l__0____1.o___1_l___O) else o_o____1_____l____1___O____l__O_1.o_____o_0__l__0____1.o___1_l___O.o__O__1___1__O_1___0___O__l_0___O
        if o_____1___l____o___0 is None or o__0_0_____l____0___o__O__o_____l is None:
            return
        o__1____1___l___O = o_____1___l____o___0.mapTo(o_o____1_____l____1___O____l__O_1.o_____O_O____0, QPoint(0, 0))
        o____O___1_1_l__l____o_____l_o_____o_____l = o__1____1___l___O.x() + o_____1___l____o___0.width() / 2 + 1
        o___l__O_O_l___l = o__1____1___l___O.y() + o_____1___l____o___0.height() / 2
        o__0____l___1____1___1_____o = o__0_0_____l____0___o__O__o_____l.mapTo(o_o____1_____l____1___O____l__O_1.o_____O_O____0, QPoint(0, 0))
        o__o____0___1_____l___o___0___O____o____0__o = o__0____l___1____1___1_____o.x() + o__0_0_____l____0___o__O__o_____l.width() / 2 + 1
        o_o__l____O_____l_____1____0_0_____0 = o__0____l___1____1___1_____o.y() + o__0_0_____l____0___o__O__o_____l.height() / 2
        o____l_____o = (o_o____1_____l____1___O____l__O_1.o_1 - o_o____1_____l____1___O____l__O_1.o__O_1____O____o_____0__1____1____l_____0__1()) * o_o____1_____l____1___O____l__O_1.o__o____1__l__l___l___l____1___o_____o_____1() + o_o____1_____l____1___O____l__O_1.o__1_1____O___O_____O_o_____0___0_1__1() + o_o____1_____l____1___O____l__O_1.leftMargin
        o__o____0_o_____l_O___1 = (o_o____1_____l____1___O____l__O_1.o__0_____0____o__l_0_l___0 - o_o____1_____l____1___O____l__O_1.o__O_1____O____o_____0__1____1____l_____0__1()) * o_o____1_____l____1___O____l__O_1.o__o____1__l__l___l___l____1___o_____o_____1() + o_o____1_____l____1___O____l__O_1.o__1_1____O___O_____O_o_____0___0_1__1() + o_o____1_____l____1___O____l__O_1.leftMargin
        o_____o____l___1____o____1___O___o_1__1_l = o____l_____o + o_o____1_____l____1___O____l__O_1.o__o____1__l__l___l___l____1___o_____o_____1() / 2
        o_____l_1__1___o____l_1_0 = o__o____0_o_____l_O___1 + o_o____1_____l____1___O____l__O_1.o__o____1__l__l___l___l____1___o_____o_____1() / 2
        o____0_____1_O_____0__l__0_0____o___O____l = 8
        lineSize = 30
        lineWidth = 25
        border = lineWidth * 0.01
        o__O_0___1__0 = o____l_____o__1_____1__O___O_1_1 - 27
        if o_o____1_____l____1___O____l__O_1.o__O_l_l__1___l__O and o_o____1_____l____1___O____l__O_1.o__1_o_1___O:
            o__l____0_____o = o_o____1_____l____1___O____l__O_1.o__1_o_1___O + o_o____1_____l____1___O____l__O_1.o__o____1__l__l___l___l____1___o_____o_____1() / 2
            if o_o____1_____l____1___O____l__O_1.o__0___O_____0_____O == Slider.kLeft:
                o____l_____o = o_o____1_____l____1___O____l__O_1.o__1_o_1___O
                o_____o____l___1____o____1___O___o_1__1_l = o__l____0_____o
            else:
                o__o____0_o_____l_O___1 = o_o____1_____l____1___O____l__O_1.o__1_o_1___O
                o_____l_1__1___o____l_1_0 = o__l____0_____o
        o____l_0____O____l__o__l_____O = QLine(o____l_____o, o____l_____o__1_____1__O___O_1_1, o____l_____o + o_o____1_____l____1___O____l__O_1.o__o____1__l__l___l___l____1___o_____o_____1(), o____l_____o__1_____1__O___O_1_1)
        o___O__O___0____0___0__O_o_O = QLine(o__o____0_o_____l_O___1, o____l_____o__1_____1__O___O_1_1, o__o____0_o_____l_O___1 + o_o____1_____l____1___O____l__O_1.o__o____1__l__l___l___l____1___o_____o_____1(), o____l_____o__1_____1__O___O_1_1)
        painter.setPen(QPen(QColor(o_o____1_____l____1___O____l__O_1.o____0_o_1_l_O()), 10, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(o____l_0____O____l__o__l_____O)
        painter.setPen(QPen(QColor(o_o____1_____l____1___O____l__O_1.o_____0____O_0__0_____o_____l____0()), 10, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(o___O__O___0____0___0__O_o_O)
        o__O___O_____O = (
         4320, 1440)
        o___o___1_____o____l__0 = (2880, 1440)
        painter.setPen(QPen(QColor(o_o____1_____l____1___O____l__O_1.o____0_o_1_l_O()), 1, Qt.SolidLine, Qt.SquareCap))
        o_____o_____0__1__o____l_____l__0_____0____1_1 = o_____o____l___1____o____1___O___o_1__1_l < o____O___1_1_l__l____o_____l_o_____o_____l
        arc = o__O___O_____O if o_____o_____0__1__o____l_____l__0_____0____1_1 else o___o___1_____o____l__0
        o___1_o____0_____l__0__o___0 = -20 if o_____o_____0__1__o____l_____l__0_____0____1_1 else 0
        o__o____1__0____o__O = -10 if o_____o_____0__1__o____l_____l__0_____0____1_1 else 10
        painter.drawLine(o____O___1_1_l__l____o_____l_o_____o_____l, o___l__O_O_l___l, o____O___1_1_l__l____o_____l_o_____o_____l, o____l_____o__1_____1__O___O_1_1 - 10)
        painter.drawLine(o____O___1_1_l__l____o_____l_o_____o_____l + o__o____1__0____o__O, o____l_____o__1_____1__O___O_1_1, o_____o____l___1____o____1___O___o_1__1_l, o____l_____o__1_____1__O___O_1_1)
        painter.drawArc((o____O___1_1_l__l____o_____l_o_____o_____l + o___1_o____0_____l__0__o___0), (o____l_____o__1_____1__O___O_1_1 - 20), 20, 20, *arc)
        painter.setPen(QPen(QColor(o_o____1_____l____1___O____l__O_1.o_____0____O_0__0_____o_____l____0()), 1, Qt.SolidLine, Qt.SquareCap))
        o_____o_____0__1__o____l_____l__0_____0____1_1 = o_____l_1__1___o____l_1_0 < o__o____0___1_____l___o___0___O____o____0__o
        arc = o__O___O_____O if o_____o_____0__1__o____l_____l__0_____0____1_1 else o___o___1_____o____l__0
        o___1_o____0_____l__0__o___0 = -20 if o_____o_____0__1__o____l_____l__0_____0____1_1 else 0
        o__o____1__0____o__O = -10 if o_____o_____0__1__o____l_____l__0_____0____1_1 else 10
        painter.drawLine(o__o____0___1_____l___o___0___O____o____0__o, o_o__l____O_____l_____1____0_0_____0, o__o____0___1_____l___o___0___O____o____0__o, o____l_____o__1_____1__O___O_1_1 - 10)
        painter.drawLine(o__o____0___1_____l___o___0___O____o____0__o + o__o____1__0____o__O, o____l_____o__1_____1__O___O_1_1, o_____l_1__1___o____l_1_0, o____l_____o__1_____1__O___O_1_1)
        painter.drawArc((o__o____0___1_____l___o___0___O____o____0__o + o___1_o____0_____l__0__o___0), (o____l_____o__1_____1__O___O_1_1 - 20), 20, 20, *arc)
        if o_o____1_____l____1___O____l__O_1.o__O_l_l__1___l__O and o_o____1_____l____1___O____l__O_1.o__1_o_1___O:
            painter.setPen(QPen(QColor(CORE.color.white), 0))
            painter.setBrush(QColor(CORE.color.white))
            o___l_____O____0__o_____O = QPolygon([QPoint(o__l____0_____o - o____0_____1_O_____0__l__0_0____o___O____l - lineSize - border, o__O_0___1__0),
             QPoint(o__l____0_____o - lineSize - border, o__O_0___1__0 - o____0_____1_O_____0__l__0_0____o___O____l),
             QPoint(o__l____0_____o - lineSize - border, o__O_0___1__0 + o____0_____1_O_____0__l__0_0____o___O____l)])
            painter.drawPolygon(o___l_____O____0__o_____O)
            o__o___0 = QPolygon([QPoint(o__l____0_____o + o____0_____1_O_____0__l__0_0____o___O____l + lineSize + border, o__O_0___1__0),
             QPoint(o__l____0_____o + lineSize + border, o__O_0___1__0 - o____0_____1_O_____0__l__0_0____o___O____l),
             QPoint(o__l____0_____o + lineSize + border, o__O_0___1__0 + o____0_____1_O_____0__l__0_0____o___O____l)])
            painter.drawPolygon(o__o___0)
            painter.setPen(QPen(QColor(CORE.color.darkWhite), lineWidth, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(o__l____0_____o - lineSize / 2, o__O_0___1__0, o__l____0_____o + lineSize / 2, o__O_0___1__0)
            rect = QRect(o__l____0_____o - lineSize / 2, o__O_0___1__0 - lineWidth / 2, lineSize, lineWidth)
            painter.setPen(QColor(CORE.color.white))
            painter.drawText(rect, Qt.AlignCenter, str(o_o____1_____l____1___O____l__O_1.o____1___0___l__1_1____l___l____l))
        o__1_O_O__1_____o___1 = o__1____1___l___O.y() - 8
        lineWidth = 15
        if o_o____1_____l____1___O____l__O_1.o__0___O_____0_____O != Slider.kLeft and o_o____1_____l____1___O____l__O_1.o____1____1____0_____l____O___l != Slider.kRight:
            o__l___o____l____1__o = o____O___1_1_l__l____o_____l_o_____o_____l
            painter.setPen(QPen(QColor(CORE.color.darkWhite), lineWidth, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(o__l___o____l____1__o - lineSize / 2, o__1_O_O__1_____o___1, o__l___o____l____1__o + lineSize / 2, o__1_O_O__1_____o___1)
            rect = QRect(o__l___o____l____1__o - lineSize / 2, o__1_O_O__1_____o___1 - lineWidth / 2, lineSize, lineWidth)
            painter.setPen(QColor(o_o____1_____l____1___O____l__O_1.o____0_o_1_l_O()))
            painter.drawText(rect, Qt.AlignCenter, str(o_o____1_____l____1___O____l__O_1.o_1))
        if o_o____1_____l____1___O____l__O_1.o__0___O_____0_____O != Slider.kRight and o_o____1_____l____1___O____l__O_1.o____1____1____0_____l____O___l != Slider.kLeft:
            o__l___o____l____1__o = o__o____0___1_____l___o___0___O____o____0__o
            painter.setPen(QPen(QColor(CORE.color.darkWhite), lineWidth, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(o__l___o____l____1__o - lineSize / 2, o__1_O_O__1_____o___1, o__l___o____l____1__o + lineSize / 2, o__1_O_O__1_____o___1)
            rect = QRect(o__l___o____l____1__o - lineSize / 2, o__1_O_O__1_____o___1 - lineWidth / 2, lineSize, lineWidth)
            painter.setPen(QColor(o_o____1_____l____1___O____l__O_1.o_____0____O_0__0_____o_____l____0()))
            painter.drawText(rect, Qt.AlignCenter, str(o_o____1_____l____1___O____l__O_1.o__0_____0____o__l_0_l___0))
        painter.end()
        return

    def o____1___l_____o_____1____O____0_1__l_____1____0(o_o____1_____l____1___O____l__O_1, isVisible):
        if o_o____1_____l____1___O____l__O_1.o__O_l_l__1___l__O:
            return
        o_____O___o____l_l_0_l = 0 if isVisible else 1000
        o_o____1_____l____1___O____l__O_1.move(0, o_____O___o____l_l_0_l)
        o_o____1_____l____1___O____l__O_1.raise_()
        o_o____1_____l____1___O____l__O_1.lower()
        o_o____1_____l____1___O____l__O_1.repaint()

    def o__O__l____l_____O____o(o_o____1_____l____1___O____l__O_1):
        o_o____1_____l____1___O____l__O_1.o____1___l_____o_____1____O____0_1__l_____1____0(True)
        o_o____1_____l____1___O____l__O_1.o____0_O__o____O___1_____1(True, Slider.kLeft)

    def o_o___O__0__o(o_o____1_____l____1___O____l__O_1):
        o_o____1_____l____1___O____l__O_1.o____1___l_____o_____1____O____0_1__l_____1____0(True)
        o_o____1_____l____1___O____l__O_1.o____0_O__o____O___1_____1(True, Slider.kRight)

    def o____0_O__o____O___1_____1(o_o____1_____l____1___O____l__O_1, o___0_o_l_____1____O_o, o_1_____o_____o____O_o_l_____O=None):
        o_o____1_____l____1___O____l__O_1.o__O_l_l__1___l__O = o___0_o_l_____1____O_o
        o_o____1_____l____1___O____l__O_1.o____1___0___l__1_1____l___l____l = None
        o_o____1_____l____1___O____l__O_1.o__1_o_1___O = None
        o_o____1_____l____1___O____l__O_1.o__0___O_____0_____O = None
        if o___0_o_l_____1____O_o:
            o_o____1_____l____1___O____l__O_1.raise_()
            o_o____1_____l____1___O____l__O_1.o__0___O_____0_____O = o_1_____o_____o____O_o_l_____O
            o_____l__o__l__0____o____o_____l = MAnimControl()
            o_o____1_____l____1___O____l__O_1.o_____0____O_____0___1_____l____o_o____o = int(o_____l__o__l__0____o____o_____l.currentTime().value())
            o_o____1_____l____1___O____l__O_1.o____0_1_____o__0__o = o_____o_o___1____l___1__l_____1__1____1__0().o_l_____0____O
            o_o____1_____l____1___O____l__O_1.o____O__0____l___o_1___O__1___1____1 = o_o____1_____l____1___O____l__O_1.mapFromGlobal(QCursor.pos())
            o_o____1_____l____1___O____l__O_1.o___l_____o____O___o__o_____o____l_O(o_o____1_____l____1___O____l__O_1.o____O__0____l___o_1___O__1___1____1)
        else:
            o_o____1_____l____1___O____l__O_1.lower()
        o_o____1_____l____1___O____l__O_1.repaint()
        return

    def o_____o____l_0_____1_____l_____o___l____o_o(o_o____1_____l____1___O____l__O_1, *args):
        o_o____1_____l____1___O____l__O_1.o_____0__O_____1____o___O()

    def o_____0__O_____1____o___O(o_o____1_____l____1___O____l__O_1):
        o__o____1__l__l___l___l____1___o_____o_____1 = o_o____1_____l____1___O____l__O_1.o__o____1__l__l___l___l____1___o_____o_____1()
        o____0_____l_____0___0__1_____o_____O_1 = o_o____1_____l____1___O____l__O_1.o__O_1____O____o_____0__1____1____l_____0__1()
        o_o____1_____l____1___O____l__O_1.o__O____O___0__0____0 = [ (frame, (frame - o____0_____l_____0___0__1_____o_____O_1) * o__o____1__l__l___l___l____1___o_____o_____1 + o_o____1_____l____1___O____l__O_1.o__1_1____O___O_____O_o_____0___0_1__1() + o_o____1_____l____1___O____l__O_1.leftMargin) for frame in xrange(o_o____1_____l____1___O____l__O_1.o__O_1____O____o_____0__1____1____l_____0__1(), o_o____1_____l____1___O____l__O_1.o____1_O____1___O____O_____l___o() + 1)
                                                                  ]

    def o____l__1__O__o(o_o____1_____l____1___O____l__O_1, o____O__1):
        o_o____1_____l____1___O____l__O_1.setMinimumSize(o____O__1.width(), o____O__1.height())
        o_o____1_____l____1___O____l__O_1.o_____0__O_____1____o___O()

    def enterEvent(o_o____1_____l____1___O____l__O_1, event):
        o_o____1_____l____1___O____l__O_1.o_____0__O_____1____o___O()

    def leaveEvent(o_o____1_____l____1___O____l__O_1, event):
        CORE.timerBot.o_0____o_O____o____l__0(lambda : o_o____1_____l____1___O____l__O_1.o____1___l_____o_____1____O____0_1__l_____1____0(False), 300)

    def mouseMoveEvent(o_o____1_____l____1___O____l__O_1, event):
        if not o_o____1_____l____1___O____l__O_1.o__O_l_l__1___l__O:
            return
        o_o____1_____l____1___O____l__O_1.o___l_____o____O___o__o_____o____l_O(event.pos())

    def o___l_____o____O___o__o_____o____l_O(o_o____1_____l____1___O____l__O_1, pos):
        if not o_o____1_____l____1___O____l__O_1.o____1___0___l__1_1____l___l____l or abs(o_o____1_____l____1___O____l__O_1.o____O__0____l___o_1___O__1___1____1.x() - pos.x()) <= 10:
            for o____1___0___l__1_1____l___l____l, o__1_o_1___O in o_o____1_____l____1___O____l__O_1.o__O____O___0__0____0:
                if o____1___0___l__1_1____l___l____l == o_o____1_____l____1___O____l__O_1.o_____0____O_____0___1_____l____o_o____o:
                    break

        else:
            o____1___0__O__1 = False
            for o____1___0___l__1_1____l___l____l, o__1_o_1___O in o_o____1_____l____1___O____l__O_1.o__O____O___0__0____0:
                if o____1___0___l__1_1____l___l____l in o_o____1_____l____1___O____l__O_1.o____0_1_____o__0__o:
                    if pos.x() - 10 < o__1_o_1___O + o_o____1_____l____1___O____l__O_1.o__o____1__l__l___l___l____1___o_____o_____1() < pos.x() + 10:
                        o____1___0__O__1 = True
                        break

        if not o____1___0__O__1:
            for o____1___0___l__1_1____l___l____l, o__1_o_1___O in o_o____1_____l____1___O____l__O_1.o__O____O___0__0____0:
                if pos.x() < o__1_o_1___O + o_o____1_____l____1___O____l__O_1.o__o____1__l__l___l___l____1___o_____o_____1():
                    break

        if o__1_o_1___O != o_o____1_____l____1___O____l__O_1.o__1_o_1___O:
            o_o____1_____l____1___O____l__O_1.o__1_o_1___O = o__1_o_1___O
            o_o____1_____l____1___O____l__O_1.o____1___0___l__1_1____l___l____l = o____1___0___l__1_1____l___l____l
            o_o____1_____l____1___O____l__O_1.repaint()

    def mouseReleaseEvent(o_o____1_____l____1___O____l__O_1, *args, **o_____O_1_O_____O___l____o_1):
        if not o_o____1_____l____1___O____l__O_1.o__O_l_l__1___l__O:
            return
        if o_o____1_____l____1___O____l__O_1.o__0___O_____0_____O == Slider.kLeft:
            o_o____1_____l____1___O____l__O_1.o_1 = o_o____1_____l____1___O____l__O_1.o____1___0___l__1_1____l___l____l
        else:
            o_o____1_____l____1___O____l__O_1.o__0_____0____o__l_0_l___0 = o_o____1_____l____1___O____l__O_1.o____1___0___l__1_1____l___l____l
        o_o____1_____l____1___O____l__O_1.o____0_O__o____O___1_____1(False)


class o____l___O___l(QWidget, o____1_O_____0__l____0_____o____1):
    kLeft = 0
    kRight = 1

    def __init__(o_o____1_____l____1___O____l__O_1, sliderWidget, o_1_____o_____o____O_o_l_____O, parent, *args):
        super(o____l___O___l, o_o____1_____l____1___O____l__O_1).__init__(parent, *args)
        o_o____1_____l____1___O____l__O_1.sliderWidget = sliderWidget
        o_o____1_____l____1___O____l__O_1.o_1_____o_____o____O_o_l_____O = o_1_____o_____o____O_o_l_____O
        o_o____1_____l____1___O____l__O_1.parent = parent
        o_o____1_____l____1___O____l__O_1.setMinimumHeight(sliderWidget.height())
        o_o____1_____l____1___O____l__O_1.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        o_o____1_____l____1___O____l__O_1.setContentsMargins(0, 0, 0, 0)
        o_o____1_____l____1___O____l__O_1.setMinimumWidth((o___0_l_o__O_o_____l_____O___l___o - 32) / 2)
        o_o____1_____l____1___O____l__O_1.setMaximumWidth((o___0_l_o__O_o_____l_____O___l___o - 32) / 2)
        o____1_o_O = QHBoxLayout()
        o____1_o_O.setContentsMargins(0, 0, 0, 0)
        o____1_o_O.setSpacing(0)
        o_o____1_____l____1___O____l__O_1.setLayout(o____1_o_O)
        buttons = []
        o_o____1_____l____1___O____l__O_1.o__l____O_____0__O___l____o____l__1__1___0 = []
        o_o____1_____l____1___O____l__O_1.o__l___0__0____o__1____0____1____o__l = []
        o_O_1____l___0___O___1____o_____O = sliderWidget.o___O_____o_1_o____O____o_____1.config.get('o_O_1____l___0___O___1____o_____O', o__0__0_____o_____1_o__0___O____O___o_0_l__0_o_____l___l____l_____o_O_____o__O_____o)
        o____1_____1_____1_____1____1__O_0____l_0___0 = sliderWidget.o___O_____o_1_o____O____o_____1.config.get('o____1_____1_____1_____1____1__O_0____l_0___0', o_____1___1____O__o_____o___o_____o_o_____l_____0_____l_____l___1___0____1_o___0____O___1__o____0_O____O__0___l____O_o____0_l___l)
        o_l___l__1_0____l = -1 if o_1_____o_____o____O_o_l_____O == Slider.kLeft else 1
        for _o__l____1_0___O in o_O_1____l___0___O___1____o_____O:
            button = o__l____1__0__O___1(_o__l____1_0___O * o_l___l__1_0____l, sliderWidget, parent)
            o_o____1_____l____1___O____l__O_1.o__l____O_____0__O___l____o____l__1__1___0.append(button)
            buttons.append(button)

        for _o__l____1_0___O in o____1_____1_____1_____1____1__O_0____l_0___0:
            button = o__l____1__0__O___1(_o__l____1_0___O * o_l___l__1_0____l, sliderWidget, parent)
            o_o____1_____l____1___O____l__O_1.o__l___0__0____o__1____0____1____o__l.append(button)
            buttons.append(button)

        if sliderWidget.o__1___o___O___1_____0__O____0___0:
            o_o____1_____l____1___O____l__O_1.o__O__1___1__O_1___0___O__l_0___O = o___l____O___o_____l___o_l____l_____l___1(o_o____1_____l____1___O____l__O_1)
            buttons.append(o_o____1_____l____1___O____l__O_1.o__O__1___1__O_1___0___O__l_0___O)
            if o_1_____o_____o____O_o_l_____O == Slider.kLeft:
                o_o____1_____l____1___O____l__O_1.o__O__1___1__O_1___0___O__l_0___O.clicked.connect(o_o____1_____l____1___O____l__O_1.sliderWidget.o_____O_O____0.o_O_1___1.o__O__l____l_____O____o)
            else:
                o_o____1_____l____1___O____l__O_1.o__O__1___1__O_1___0___O__l_0___O.clicked.connect(o_o____1_____l____1___O____l__O_1.sliderWidget.o_____O_O____0.o_O_1___1.o_o___O__0__o)
        if o_1_____o_____o____O_o_l_____O == Slider.kLeft:
            buttons = list(reversed(buttons))
        for _o_o__0_o in buttons:
            o____1_o_O.addWidget(_o_o__0_o, 0)

        if not o_o____1_____l____1___O____l__O_1.sliderWidget.o__o__o____o___1:
            o_o____1_____l____1___O____l__O_1.setPresetOvershootButtonsVisible(False)
        o_o____1_____l____1___O____l__O_1.show()
        o_o____1_____l____1___O____l__O_1.__o___O____l___O__0_____o_0_0_____l____o___o()

    def __o___O____l___O__0_____o_0_0_____l____o___o(o_o____1_____l____1___O____l__O_1):
        if o_o____1_____l____1___O____l__O_1.o_1_____o_____o____O_o_l_____O == Slider.kLeft:
            rect = QRect(3, 0, o_o____1_____l____1___O____l__O_1.parent.width() / 2 - 10, o_o____1_____l____1___O____l__O_1.parent.height())
            o_o____1_____l____1___O____l__O_1.setGeometry(rect)
        else:
            rect = QRect(o_o____1_____l____1___O____l__O_1.parent.width() / 2 + 13, 0, o_o____1_____l____1___O____l__O_1.parent.width() / 2 - 10, o_o____1_____l____1___O____l__O_1.parent.height())
            o_o____1_____l____1___O____l__O_1.setGeometry(rect)

    def setPresetOvershootButtonsVisible(o_o____1_____l____1___O____l__O_1, isVisible):
        for _o_o__0_o in o_o____1_____l____1___O____l__O_1.o__l___0__0____o__1____0____1____o__l:
            _o_o__0_o.setVisible(isVisible)

    def o___l__0_____1__l(o_o____1_____l____1___O____l__O_1, isVisible):
        for _o_o__0_o in o_o____1_____l____1___O____l__O_1.o__l____O_____0__O___l____o____l__1__1___0:
            _o_o__0_o.setVisible(isVisible)


o_____o____O__O_____o_0___o__O_1__0 = str(base64.urlsafe_b64decode(str('bWFuaXB1bGF0b3JFeHRyYVRvb2xz')))
o__0___1__1_l___o_____o____o_O = 154281
o____l_l____O____O___1_____o = None
o__O = None
CORE.o____l_l____O____O___1_____o = CORE.o____l_l____O____O___1_____o or {}
if CORE.o____l_l____O____O___1_____o.get(o_____o____O__O_____o_0___o__O_1__0, None) is None:
    o____1_____1__O = int(os.path.getmtime(o__o___o____O_____1('%s.py' % o_____o____O__O_____o_0___o__O_1__0).filePath))
    o__l__o_1_l____l___0___l__1_____l = int(o____1_____1__O / 10000)
    CORE.o____l_l____O____O___1_____o[o_____o____O__O_____o_0___o__O_1__0] = o__l__o_1_l____l___0___l__1_____l
    if CORE.o__O is None:
        CORE.o__O = o__0___1__1_l___o_____o____o_O - CORE.o____l_l____O____O___1_____o[o_____o____O__O_____o_0___o__O_1__0]
o__0___1__1_l___o_____o____o_O = o__0___1__1_l___o_____o____o_O - CORE.o__O
if o__0___1__1_l___o_____o____o_O != CORE.o____l_l____O____O___1_____o[o_____o____O__O_____o_0___o__O_1__0]:
    CORE.actions = None
# okay decompiling sliderWidget.pyc
