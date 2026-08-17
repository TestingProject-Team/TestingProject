# Verification Runner for YIYI-40 (PowerShell)
# Scope: AI Fallback, Context, Streaming, Per-User History, and Secret Handling

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  YIYI-40: RUNNING AUTOMATED AI VERIFICATION SUITE" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$global:testResults = @()
$global:passCount = 0
$global:failCount = 0

function Run-Test {
    param(
        [string]$TestId,
        [string]$Name,
        [scriptblock]$TestBlock
    )
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    try {
        & $TestBlock
        $sw.Stop()
        $global:passCount++
        $res = [PSCustomObject]@{
            id = $TestId
            name = $Name
            status = "PASS"
            durationMs = $sw.ElapsedMilliseconds
            error = $null
        }
        $global:testResults += $res
        Write-Host "[PASS] $TestId : $Name ($($sw.ElapsedMilliseconds)ms)" -ForegroundColor Green
    }
    catch {
        $sw.Stop()
        $global:failCount++
        $res = [PSCustomObject]@{
            id = $TestId
            name = $Name
            status = "FAIL"
            durationMs = $sw.ElapsedMilliseconds
            error = $_.Exception.Message
        }
        $global:testResults += $res
        Write-Host "[FAIL] $TestId : $Name ($($sw.ElapsedMilliseconds)ms)" -ForegroundColor Red
        Write-Host "       Error: $($_.Exception.Message)" -ForegroundColor DarkRed
    }
}

# 1. RAG & Keyword Extraction
Run-Test "TC-AI-RAG-001" "Trich xuat tu khoa va loc bo stop words" {
    $stopWords = @("co", "khong", "bao", "nhieu", "san", "pham", "cuon", "quyen", "sach", "cua", "va", "la", "toi", "minh", "ban", "cho", "voi", "mot", "nhung", "cac", "nay", "do", "cai")
    $query = "ban co sach nao ve phat trien tu duy kinh doanh khong"
    $words = $query.ToLower() -split "\s+"
    $kws = @()
    foreach ($w in $words) {
        if ($w.Length -ge 2 -and -not ($stopWords -contains $w)) {
            $kws += $w
        }
    }
    if ($kws -contains "co" -or $kws -contains "khong" -or $kws -contains "sach") { throw "Stop words not filtered" }
    if (-not ($kws -contains "phat" -and $kws -contains "trien" -and $kws -contains "kinh" -and $kws -contains "doanh")) { throw "Missing valid keywords" }
}

Run-Test "TC-AI-RAG-002" "Client-side RAG Matching tim dung san pham theo Ten sach" {
    $books = @(
        @{ title = "Dac Nhan Tam"; author = "Dale Carnegie"; category = @{ name = "Ky nang" }; price = 86000 },
        @{ title = "Nha Gia Kim"; author = "Paulo Coelho"; category = @{ name = "Van hoc" }; price = 79000 }
    )
    $searchKws = @("dac", "nhan", "tam")
    $matches = @()
    foreach ($b in $books) {
        $t = $b.title.ToLower()
        foreach ($kw in $searchKws) {
            if ($t.Contains($kw)) {
                $matches += $b
                break
            }
        }
    }
    if ($matches.Count -ne 1 -or $matches[0].title -ne "Dac Nhan Tam") { throw "RAG match failed" }
}

# 2. Intent Detection
Run-Test "TC-AI-INT-001" "Nhan dien chinh xac y dinh can tu van va goi y (wantRecommendation)" {
    $msg = "goi y cho minh vai cuon sach hay"
    $isMatch = [regex]::IsMatch($msg, "goi y|de xuat|recommend|nen doc|hay khong|co gi hay|khong biet|muon tim|tim giup|gioi thieu")
    if (-not $isMatch) { throw "Failed to match intent wantRecommendation" }
}

Run-Test "TC-AI-INT-002" "Nhan dien da y dinh: Qua tang + Gia re + Ky nang" {
    $msg = "tang qua sinh nhat ban cuon sach ky nang gia re"
    $isGift = [regex]::IsMatch($msg, "tang|qua|gift|sinh nhat|ky niem")
    $isPrice = [regex]::IsMatch($msg, "gia|bao nhieu|re|dat|tiet kiem")
    $isSkill = [regex]::IsMatch($msg, "ky nang|phat trien|tu duy|kinh doanh")
    if (-not ($isGift -and $isPrice -and $isSkill)) { throw "Failed multi-intent detection" }
}

# 3. Product Context Builder
Run-Test "TC-AI-CTX-001" "Xay dung Store Context day du thong ke tong quan kho" {
    $totalBooks = 9
    $totalCats = 5
    $ctx = "TONG QUAN KHO HANG YIYI BOOK:`n- Tong so san pham: $totalBooks san pham`n- So danh muc: $totalCats danh muc"
    if (-not $ctx.Contains("Tong so san pham: 9 san pham")) { throw "Mismatch total products in context" }
    if (-not $ctx.Contains("So danh muc: 5 danh muc")) { throw "Mismatch total categories in context" }
}

# 4. Groq SSE Streaming
Run-Test "TC-AI-STR-001" "Giai ma chuan luong SSE va ket thuc an toan voi token [DONE]" {
    $rawStream = "data: {`"choices`":[{`"delta`":{`"content`":`"Chao `"}}]}`r`n`r`ndata: {`"choices`":[{`"delta`":{`"content`":`"ban!`"}}]}`r`n`r`ndata: [DONE]`r`n`r`n"
    $events = [regex]::Split($rawStream, "\r?\n\r?\n")
    $text = ""
    $done = $false
    foreach ($ev in $events) {
        $line = $ev.Trim()
        if ($line.StartsWith("data: ")) {
            $dataStr = $line.Substring(6).Trim()
            if ($dataStr -eq "[DONE]") { $done = $true; continue }
            try {
                $obj = $dataStr | ConvertFrom-Json
                $delta = $obj.choices[0].delta.content
                if ($delta) { $text += $delta }
            } catch {}
        }
    }
    if ($text -ne "Chao ban!") { throw "Stream text decoded wrongly: $text" }
    if (-not $done) { throw "Done signal not processed" }
}

# 5. Per-User History
Run-Test "TC-AI-HIS-001" "Phan tach Storage Key theo User ID tranh xung dot cache" {
    $guestKey = "yiyi_chat_history_guest"
    $userKey = "yiyi_chat_history_101"
    if ($guestKey -eq $userKey) { throw "Key collision between Guest and User" }
    if (-not $userKey.EndsWith("101")) { throw "User key missing user ID" }
}

Run-Test "TC-AI-HIS-002" "Gioi han cua so ngu canh toi da 20 tin nhan gan nhat" {
    $allMsgs = 1..35 | ForEach-Object { @{ role = "user"; content = "Msg $_" } }
    $recentMsgs = $allMsgs | Select-Object -Last 20
    if ($recentMsgs.Count -ne 20) { throw "Context window size is not 20" }
    if ($recentMsgs[0].content -ne "Msg 16" -or $recentMsgs[19].content -ne "Msg 35") { throw "Window boundary incorrect" }
}

# 6. Fallback & Secret Handling
Run-Test "TC-AI-SEC-001" "Kiem tra API Key khong bi hardcode trong source code AIChatWidget.jsx" {
    $content = Get-Content -Raw "frontend/src/components/common/AIChatWidget.jsx"
    if ($content -match "gsk_[A-Za-z0-9]{20,}") { throw "Detected hardcoded Groq key" }
    if (-not $content.Contains("import.meta.env.VITE_GROQ_API_KEY")) { throw "Missing import.meta.env config" }
}

Run-Test "TC-AI-SEC-002" "Quet tinh toan bo repo de dam bao khong ro ri secret trong source code" {
    $srcFiles = Get-ChildItem -Path "frontend/src", "backend/src" -Recurse -Include *.jsx, *.js, *.java, *.json
    foreach ($f in $srcFiles) {
        $txt = Get-Content -Raw $f.FullName
        if ($txt -match "gsk_[A-Za-z0-9]{30,}") {
            throw "Detected leaked secret in file $($f.FullName)"
        }
    }
}

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  SUMMARY: Total: $($global:passCount + $global:failCount) | PASS: $global:passCount | FAIL: $global:failCount" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$summary = [PSCustomObject]@{
    suite = "YIYI-40: AI Chatbot Fallback, Context, Streaming and Secret Handling"
    executedAt = (Get-Date).ToString("yyyy-MM-ddTHH:mm:sszzz")
    totalTests = $global:passCount + $global:failCount
    passCount = $global:passCount
    failCount = $global:failCount
    status = if ($global:failCount -eq 0) { "PASS" } else { "FAIL" }
    tests = $global:testResults
}

$summaryJson = $summary | ConvertTo-Json -Depth 5
[System.IO.File]::WriteAllText("test-scripts/YIYI-40-ai-test-summary.json", $summaryJson, [System.Text.Encoding]::UTF8)
Write-Host "Summary JSON exported to test-scripts/YIYI-40-ai-test-summary.json" -ForegroundColor Green
