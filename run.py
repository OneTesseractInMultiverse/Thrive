import os
from thrive import app

__author__ = "Pedro Guzman (pedro@subvertic.com)"
__version__ = "1.0.0"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8190))
    app.run(host='0.0.0.0', port=port)
