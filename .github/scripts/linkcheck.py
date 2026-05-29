#!/usr/bin/env python3
"""DevForge static-site link checker — wrapper around canonical implementation.

This script is kept at .github/scripts/linkcheck.py for backward compatibility
with existing CI workflows. The canonical implementation lives in
.hermes/linkcheck.py and both resolve to the same code.
"""

import os
import sys

# Ensure .hermes is on the path
_HERMES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".hermes")
sys.path.insert(0, _HERMES)

from linkcheck import main  # noqa: E402

if __name__ == "__main__":
    # Remove this script's directory from argv to match the canonical CLI
    sys.exit(main())
