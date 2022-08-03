from .common_settings import *
import os

if os.environ.get("ENV_NAME") == 'Production':
    from .prod_settings import *
else:
    from .dev_settings import *