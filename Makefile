default: gui test


UItest:
	@py UItest.py

test:
	@py main0.py

gui:
	@pyuic5 ui/mainwindow.ui -o ui_mainwindow.py
	@pyuic5 ui/hmi.ui -o ui_hmi.py
	@pyuic5 ui/avrdude.ui -o ui_avrdude.py
	@pyuic5 ui/asa_prog.ui -o ui_asa_prog.py
