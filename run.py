# run.py - single-click runner for TradeSentinelGPT
import sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from scanner.scan_runner import main
except Exception as e:
    print("[ERR] Could not import scanner. Make sure the folder structure is intact.")
    raise

if __name__ == "__main__":
    print("[INFO] Running TradeSentinelGPT scanner...")
    main()
    print("[INFO] Done.")
    python run.py
