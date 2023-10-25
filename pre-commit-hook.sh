echo '#!/bin/bash

pytest -v' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
