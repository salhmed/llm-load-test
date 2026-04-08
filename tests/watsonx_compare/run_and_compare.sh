#!/usr/bin/env bash

PYTHON_CMD=${PYTHON_CMD:-"python"}

echo "=========================================="
echo "Running Load Test for Version 1 (flan-t5-small)"
echo "=========================================="
$PYTHON_CMD load_test.py -c tests/watsonx_compare/config_v1.yaml

echo ""
echo "=========================================="
echo "Running Load Test for Version 2 (flan-t5-base)"
echo "=========================================="
$PYTHON_CMD load_test.py -c tests/watsonx_compare/config_v2.yaml

echo ""
echo "=========================================="
echo "Comparison Results"
echo "=========================================="

print_summary() {
    local file=$1
    local version_name=$2
    
    if [ -f "$file" ]; then
        echo "$version_name Results:"
        
        # We use grep/sed or python to parse the output JSON simply if jq is not available.
        # But expecting user has python, we directly use inline python to parse the json safely!
        $PYTHON_CMD -c "
import json
try:
    with open('$file') as f:
        data = json.load(f)
        summary = data.get('summary', {})
        print(f' - Total Requests: {summary.get(\"total_requests\")}')
        print(f' - Failure Rate: {round(summary.get(\"failure_rate\", 0), 2)}%')
        print(f' - Throughput: {round(summary.get(\"throughput\", 0), 2)} tokens/s')
        if 'tpot' in summary:
            print(f' - Median Time Per Output Token: {round(summary[\"tpot\"].get(\"median\", 0), 2)} ms')
        if 'ttft' in summary:
            print(f' - Median Time To First Token: {round(summary[\"ttft\"].get(\"median\", 0), 2)} ms')
except Exception as e:
    print(f'Could not parse {e}')
"
        echo ""
    else
        echo "$version_name output not found. Looked for $file"
        echo ""
    fi
}

print_summary "tests/watsonx_compare/output/output-version-1.json" "Version 1 (flan-t5-small)"
print_summary "tests/watsonx_compare/output/output-version-2.json" "Version 2 (flan-t5-base)"
