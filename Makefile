test:
	@make gui
	@py main.py

gui:
	@pyuic5 mainwindow.ui -o pyqtwindow.py
