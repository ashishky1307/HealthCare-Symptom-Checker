"""Load environment variables from root .env file."""

from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env from project root (parent directory)
root_dir = Path(__file__).parent.parent
env_path = root_dir / '.env'

if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Loaded environment from: {env_path}")
else:
    print(f"⚠️ Warning: .env file not found at {env_path}")
