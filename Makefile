
compile:
	@pyinstaller -F -w test.py

gui:
	@pyuic5 mainwindow.ui -o pyqtwindow.py
