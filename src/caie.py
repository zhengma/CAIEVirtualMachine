import sys
from caie_vm import caie_vm
from caie_assembler import caie_assembler
from caie_ui import caie_ui


args = sys.argv

test_assemble = caie_assembler(args[1], int(args[2]), int(args[3]))
exe = test_assemble.generate()
test_run = caie_vm(int(args[2]), exe, ext=True)
test_ui = caie_ui(test_assemble, test_run)
test_ui.disp()