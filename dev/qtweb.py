import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
class qtweb(QWebEngineView):
    def __init__(self,*args,**kwargs):
        super(qtweb,self).__init__(*args,**kwargs)
        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.onCookieAdd)
class window(Qwidget):
    def __init__(self):
        super().__init__()
        self.setup()
    def setup(self):
        pass
app=QApplication(sys.argv)
