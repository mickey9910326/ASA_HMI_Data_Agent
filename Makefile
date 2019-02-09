default: gui test

UItest:
	@py scripts/test_ui.py

test:
	@py main.py

gui:
	@ py scripts/pyuic_all_ui.py
