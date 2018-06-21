default: gui test

UItest:
	@py UItest.py

test:
	@py main.py

gui:
	@pyuic5 ui/mainwindow.ui -o asa_hmi_data_agent/ui/ui_mainwindow.py
	@pyuic5 ui/hmi.ui -o asa_hmi_data_agent/ui/ui_hmi.py
	@pyuic5 ui/avrdude.ui -o asa_hmi_data_agent/ui/ui_avrdude.py
	@pyuic5 ui/asa_prog.ui -o asa_hmi_data_agent/ui/ui_asa_prog.py
	@pyuic5 ui/bit_selector.ui -o asa_hmi_data_agent/ui/ui_bit_selector.py
	@pyuic5 ui/hmi_save_dialog.ui -o asa_hmi_data_agent/ui/ui_hmi_save_dialog.py
	@pyuic5 ui/hmi_load_dialog.ui -o asa_hmi_data_agent/ui/ui_hmi_load_dialog.py
