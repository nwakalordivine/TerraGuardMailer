import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))
from app.main import handler as app
# Vercel will look for 'app' in this file
