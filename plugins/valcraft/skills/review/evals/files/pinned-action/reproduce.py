from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


sys.dont_write_bytecode = True
revision = "0123456789abcdef0123456789abcdef01234567"
source = Path(__file__).parent / "action-captures" / revision / "action.py"
spec = spec_from_file_location("pinned_retry_action", source)
module = module_from_spec(spec)
spec.loader.exec_module(module)
print(module.run())
