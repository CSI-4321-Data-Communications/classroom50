#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

def run_autograder():
    score = 0
    feedback = "No valid input"
    compiled_successfully = False

    try:
        result = subprocess.run(
            ["cargo", "run", "--quiet"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            compiled_successfully = True
            if "Hello, world!" in result.stdout.strip():
                score = 100
                feedback = "success!"
            else:
                score = 0
                feedback = f"output is wrong. expect: 'Hello, world!'，actual: '{result.stdout.strip()}'"
    except Exception as e:
        compiled_successfully = False

    if not compiled_successfully:
        main_rs_path = Path("src/main.rs")
        if main_rs_path.exists():
            source_code = main_rs_path.read_text()
            if 'println!("Hello, world!");' in source_code or 'Hello, world!' in source_code:
                score = 50
                feedback = "Compile error"
            else:
                score = 0
                feedback = "Compile error, no key word"
        else:
            score = 0
            feedback = "failed to find src/main.rs"

    result_json = {
        "schema": "classroom50/result/v1",
        "score": score,
        "max-score": 100,
        "tests": [
            {
                "test-name": "Hello World Check",
                "passed": score > 0,
                "score": score,
                "max-score": 100,
                "feedback": feedback
            }
        ]
    }

    print(json.dumps(result_json, indent=2))

if __name__ == "__main__":
    run_autograder()
