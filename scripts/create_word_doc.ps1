# PowerShell script to convert Markdown/HTML report to Word (.docx / .doc)

$mdPath = "g:\KI HE NAM 3\TestingProject\docs\BVA_EP_TEST_REPORT_VAN_THIEN.md"
$docxPath = "g:\KI HE NAM 3\TestingProject\docs\BVA_EP_TEST_REPORT_VAN_THIEN.docx"
$docPath = "g:\KI HE NAM 3\TestingProject\docs\BVA_EP_TEST_REPORT_VAN_THIEN.doc"

$mdContent = Get-Content -Path $mdPath -Raw -Encoding UTF8

# Convert Markdown tables and headers to clean HTML for Word
$html = @"
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body { font-family: 'Calibri', 'Segoe UI', Arial, sans-serif; margin: 30px; color: #222; font-size: 11pt; line-height: 1.5; }
    h1 { color: #1a365d; font-size: 18pt; border-bottom: 2px solid #2b6cb0; padding-bottom: 5px; }
    h2 { color: #2c5282; font-size: 14pt; margin-top: 20px; border-bottom: 1px solid #e2e8f0; padding-bottom: 3px; }
    h3 { color: #2b6cb0; font-size: 12pt; margin-top: 15px; }
    table { border-collapse: collapse; width: 100%; margin: 15px 0; font-size: 9.5pt; }
    th { background-color: #2b6cb0; color: white; border: 1px solid #1a365d; padding: 8px; text-align: left; font-weight: bold; }
    td { border: 1px solid #cbd5e0; padding: 6px 8px; text-align: left; vertical-align: top; }
    tr:nth-child(even) { background-color: #f7fafc; }
    code, pre { font-family: 'Consolas', 'Courier New', monospace; background-color: #edf2f7; color: #805ad5; font-size: 9pt; }
    pre { padding: 10px; border-radius: 4px; border: 1px solid #e2e8f0; overflow-x: auto; white-space: pre-wrap; }
    .status-pass { color: #276749; font-weight: bold; background-color: #c6f6d5; padding: 2px 6px; border-radius: 3px; }
    blockquote { border-left: 4px solid #4299e1; padding-left: 10px; color: #4a5568; font-style: italic; }
</style>
</head>
<body>
"@

# Helper to process markdown lines
$lines = $mdContent -split "\r?\n"
$inTable = $false
$inCode = $false

foreach ($line in $lines) {
    if ($line.StartsWith("```")) {
        if ($inCode) {
            $html += "</pre>`n"
            $inCode = $false
        } else {
            $html += "<pre>"
            $inCode = $true
        }
        continue
    }

    if ($inCode) {
        $encoded = [System.Web.HttpUtility]::HtmlEncode($line)
        $html += "$encoded`n"
        continue
    }

    if ($line.StartsWith("# ")) {
        $text = $line.Substring(2)
        $html += "<h1>$text</h1>`n"
    } elseif ($line.StartsWith("## ")) {
        $text = $line.Substring(3)
        $html += "2. <h2>$text</h2>`n"
    } elseif ($line.StartsWith("### ")) {
        $text = $line.Substring(4)
        $html += "3. <h3>$text</h3>`n"
    } elseif ($line.StartsWith("|")) {
        if (-not $inTable) {
            $html += "<table>`n"
            $inTable = $true
            $isHeader = $true
        }

        if ($line -match "^\s*\|(?:\s*:?-+:?\s*\|)+\s*$") {
            # Skip separator line | :--- | :--- |
            continue
        }

        $cells = $line.Trim('|').Split('|')
        $html += "<tr>"
        foreach ($cell in $cells) {
            $cText = $cell.Trim()
            # Format bold, pass tag
            $cText = $cText -replace "\*\*(.*?)\*\*", "<b>`$1</b>"
            $cText = $cText -replace "`"(.*?)`"", "<code>`$1</code>"
            $cText = $cText -replace "\bPASS\b", "<span class='status-pass'>PASS</span>"
            $cText = $cText -replace "<br>", "<br/>"

            if ($isHeader) {
                $html += "<th>$cText</th>"
            } else {
                $html += "<td>$cText</td>"
            }
        }
        $html += "</tr>`n"
        $isHeader = $false
    } else {
        if ($inTable) {
            $html += "</table>`n"
            $inTable = $false
        }
        if ($line.Trim() -ne "") {
            $pText = $line -replace "\*\*(.*?)\*\*", "<b>`$1</b>"
            $pText = $pText -replace "`"(.*?)`"", "<code>`$1</code>"
            $html += "<p>$pText</p>`n"
        }
    }
}

if ($inTable) { $html += "</table>`n" }
if ($inCode) { $html += "</pre>`n" }

$html += "</body></html>"

# Save HTML doc
Add-Type -AssemblyName System.Web
[System.IO.File]::WriteAllText($docPath, $html, [System.Text.Encoding]::UTF8)

# Try using Word COM object to save as native .docx if MS Word is installed
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $doc = $word.Documents.Open($docPath)
    $doc.SaveAs([ref]$docxPath, [ref]16) # 16 = wdFormatDocumentDefault (.docx)
    $doc.Close()
    $word.Quit()
    Write-Host "Successfully generated native .docx file at $docxPath"
} catch {
    Write-Host "MS Word COM not available, saved Word-compatible document at $docPath"
}
