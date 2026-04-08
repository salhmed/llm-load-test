$pythonCmd = "python" # or 'py' or a specific virtualenv path depending on the environment

Write-Host "=========================================="
Write-Host "Running Load Test for Version 1 (flan-t5-small)"
Write-Host "=========================================="
& $pythonCmd load_test.py -c tests/watsonx_compare/config_v1.yaml

Write-Host ""
Write-Host "=========================================="
Write-Host "Running Load Test for Version 2 (flan-t5-base)"
Write-Host "=========================================="
& $pythonCmd load_test.py -c tests/watsonx_compare/config_v2.yaml

Write-Host ""
Write-Host "=========================================="
Write-Host "Comparison Results"
Write-Host "=========================================="

function Print-Summary($file, $versionName) {
    if (Test-Path $file) {
        $json = Get-Content $file | ConvertFrom-Json
        $summary = $json.summary
        
        Write-Host "$versionName Results:"
        Write-Host " - Total Requests: $($summary.total_requests)"
        Write-Host " - Failure Rate: $([math]::Round($summary.failure_rate, 2))%"
        Write-Host " - Throughput: $([math]::Round($summary.throughput, 2)) tokens/s"
        if ($summary.tpot) {
            Write-Host " - Median Time Per Output Token: $([math]::Round($summary.tpot.median, 2)) ms"
        }
        if ($summary.ttft) {
            Write-Host " - Median Time To First Token: $([math]::Round($summary.ttft.median, 2)) ms"
        }
        Write-Host ""
    } else {
        Write-Host "$versionName output not found. Looked for $file"
        Write-Host ""
    }
}

Print-Summary "tests/watsonx_compare/output/output-version-1.json" "Version 1 (flan-t5-small)"
Print-Summary "tests/watsonx_compare/output/output-version-2.json" "Version 2 (flan-t5-base)"
