
compile:
	@pyinstaller -F -w main.py

compile2:
	@pyinstaller -w main.py

gui:
	@pyuic5 mainwindow.ui -o pyqtwindow.py

test:
	@make gui
	@py main.py
