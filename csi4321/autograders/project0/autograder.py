import json
import subprocess
import os

def grade():
    score = 0
    max_score = 100
    msg = "No output"
    
    result = subprocess.run(["cargo", "run", "--quiet"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    output = result.stdout.strip()
    has_compile_error = result.returncode != 0
    
    if output == "Hello, world!":
        if not has_compile_error:
            score = 100
            msg = "Perfect! Correct output and compiled cleanly."
        else:
            score = 50
            msg = "Correct output, but contained syntax/compiler errors."
    else:
        score = 0
        msg = "Incorrect output or failed to run."

    result_json = {
        "schema": "classroom50/result/v1",
        "score": score,
        "max-score": max_score,
        "tests": [
            {
                "test-name": "test1",
                "passed": score == 100,
                "score": score,
                "max-score": max_score,
                "output": msg
            }
        ]
    }

    with open("result.json", "w") as f:
        json.dump(result_json, f, indent=2)

if __name__ == "__main__":
    grade()
