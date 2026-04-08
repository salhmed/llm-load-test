$outFile = "c:\Users\medsa\Documents\dev-projects\llm-load-test\datasets\mixed_load_test.jsonl"
$metadata = @{ name="load-test-mix"; version="0.0.1" }
($metadata | ConvertTo-Json -Compress) | Out-File -FilePath $outFile -Encoding utf8

for ($i = 0; $i -lt 250; $i++) {
    $is_rag = ($i % 5 -eq 0)
    if ($is_rag) {
        $context = ""
        for ($j=0; $j -lt 50; $j++) {
            $context += "The company performance in Q3 was exceptional due to cost cutting measures and successful product launches. "
        }
        $context = $context.TrimEnd()
        
        $question = "Based on the following context, summarize the key points. Question $i`nContext: $context"
        $system_prompt = "You are a knowledgeable assistant. Use the provided context to answer the user's question accurately."
        $tok_input_length = [math]::Floor($question.Length / 4)
        $tok_output_length = Get-Random -Minimum 50 -Maximum 100
    } else {
        $question = "Explain the theory of relativity to a 5-year old. Variation $i."
        $system_prompt = "You are a helpful and friendly AI assistant."
        $tok_input_length = [math]::Floor($question.Length / 4)
        $tok_output_length = Get-Random -Minimum 150 -Maximum 300
    }
    
    $record = [ordered]@{
        index = $i
        question = $question
        system_prompt = $system_prompt
        tok_input_length = $tok_input_length
        tok_output_length = $tok_output_length
    }
    
    $jsonline = ($record | ConvertTo-Json -Compress)
    # The backticks `n might be escaped differently in PS JSON but this creates a valid oneline json string.
    $jsonline = $jsonline -replace "\\u000a","\n" # sometimes PS compress misses standard escapes
    $jsonline | Out-File -FilePath $outFile -Append -Encoding ascii
}
Write-Output "Dataset generated at datasets/mixed_load_test.jsonl"
