import sys
from pathlib import Path
from collections import deque
from PySide6.QtGui import QImage
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterSingletonType
from PySide6.QtCore import QUrl ,QObject, Signal, Slot, QBuffer, QByteArray ,QTimer
from PySide6.QtLocation import QGeoServiceProvider

import numpy as np
from qt_backend import BackendAPI

backend = BackendAPI()

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    qmlRegisterSingletonType(QUrl.fromLocalFile("/home/saeed/work1/colcon_ws/src/my_first_pkg/my_first_pkg/Style.qml"), "Style", 1, 0, "Style")

    engine.rootContext().setContextProperty("backend", backend)
    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())