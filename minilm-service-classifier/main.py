# main.py
import sys
import os
import json
from router import route_query
from config import ENFORCE_PARAMS, THRESHOLD

def batch_process(input_file, output_file="results.txt", enforce_params=ENFORCE_PARAMS, threshold=THRESHOLD):
    if not os.path.exists(input_file):
        print(f"❌ Input file '{input_file}' not found.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    results = []
    for line in lines:
        result = route_query(line, enforce_params=enforce_params, threshold=threshold)
        confidence = result.pop("confidence", None)
        ordered_result = {
            "input": line,
            "route": result.get("route"),
            "intent": result.get("intent"),
            "confidence": confidence,
            "params": result.get("params", result.get("recognized", {}))
        }
        if "missing_params" in result:
            ordered_result["missing_params"] = result["missing_params"]
        results.append(ordered_result)

    with open(output_file, "w", encoding="utf-8") as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n\n")

    print(f"✅ Batch processing complete. Results written to '{output_file}'.")

if __name__ == "__main__":
    # CLI flags
    enforce_params = ENFORCE_PARAMS
    threshold = THRESHOLD

    if "--no-params" in sys.argv:
        enforce_params = False
        print("⚡ Running in classification-only mode (no required parameter enforcement).")
        sys.argv.remove("--no-params")
    else:
        print("🔒 Running in full mode (parameters enforced).")

    if "--threshold" in sys.argv:
        idx = sys.argv.index("--threshold")
        if idx + 1 < len(sys.argv):
            try:
                threshold = float(sys.argv[idx + 1])
                print(f"🎯 Using custom classification threshold: {threshold}")
                sys.argv.pop(idx)
                sys.argv.pop(idx)
            except ValueError:
                print("⚠️ Invalid threshold value, using default 0.8.")

    # Batch or interactive mode
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else "results.txt"
        batch_process(input_path, output_path, enforce_params=enforce_params, threshold=threshold)
    else:
        print("🤖 Interactive assistant (type 'exit' to quit)")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            result = route_query(user_input, enforce_params=enforce_params, threshold=threshold)
            print("🔍 Debug info:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
