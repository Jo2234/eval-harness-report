"""Launch an unmodified Equity API with a fresh source-only corpus."""
import argparse
import os
from pathlib import Path
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--copilot', type=Path, required=True)
parser.add_argument('--state', type=Path, required=True)
parser.add_argument('--port', type=int, default=8766)
args = parser.parse_args()
if args.state.exists():
    raise SystemExit('Choose a fresh state directory, without existing companies or conversations')
args.state.mkdir(parents=True)
sys.path.insert(0, str(args.copilot.resolve() / 'backend'))
os.environ.update({
    'AIERC_DATA_DIR': str(args.state.resolve() / 'import-time-demo'),
    'AIERC_LLM_PROVIDER': 'local',
    'AIERC_LOCAL_MODEL_NAME': 'local-deterministic-grounded-v1',
    'AIERC_DEMO_MODE': 'false',
    'AIERC_EMBEDDING_DIMENSIONS': '128',
    'AIERC_CHUNK_TARGET_TOKENS': '800',
    'AIERC_CHUNK_OVERLAP_TOKENS': '80',
    'AIERC_RETRIEVAL_MIN_SCORE': '0.04',
    'AIERC_MAX_UPLOAD_MB': '10',
})
from ai_equity_research_copilot_backend.main import create_app
import uvicorn

# Importing main creates a seeded default app; isolate it from the measured app.
uvicorn.run(create_app(data_dir=args.state.resolve() / 'source-only', seed=False),
            host='127.0.0.1', port=args.port)
