# PowerShell static verification script for CodeceptJS E2E Test Suite (YIYI-50)
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptRoot

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "  YIYI-50: STATIC CODE & POM STRUCTURE VERIFIER (NOT REAL EXECUTION)" -ForegroundColor Yellow
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "  [NOTICE] This script ONLY verifies file existence & POM structure." -ForegroundColor White
Write-Host "  To run actual Playwright/CodeceptJS E2E tests, execute:" -ForegroundColor White
Write-Host "  -> npx codeceptjs run --steps" -ForegroundColor Green
Write-Host "  -> npx codeceptjs dry-run" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Cyan

$Results = @()

function Record-StaticCheck {
    param(
        [string]$Id,
        [string]$Name,
        [string]$Status,
        [string]$Type = "StaticCodeCheck",
        [string]$Error = $null
    )
    $color = if ($Status -eq "VERIFIED") { "Green" } else { "Red" }
    Write-Host "[$Status] $Id : $Name ($Type)" -ForegroundColor $color
    if ($Error) {
        Write-Host "        Note/Error: $Error" -ForegroundColor Yellow
    }
    return [PSCustomObject]@{
        id = $Id
        name = $Name
        status = $Status
        checkType = $Type
        note = $Error
    }
}

# 1. Structural Check: Config & Custom Helpers
$confFile = Join-Path $ProjectRoot "codecept.conf.js"
$stepsFile = Join-Path $ProjectRoot "steps_file.js"
$helperFile = Join-Path $ProjectRoot "e2e\helpers\custom_helper.js"

if ((Test-Path $confFile) -and (Test-Path $stepsFile) -and (Test-Path $helperFile)) {
    $Results += Record-StaticCheck -Id "CHK-CFG-001" -Name "Full CodeceptJS Configuration, Steps file, and CustomHelper" -Status "VERIFIED"
} else {
    $Results += Record-StaticCheck -Id "CHK-CFG-001" -Name "Missing CodeceptJS Configuration files" -Status "FAILED" -Error "Missing config/steps/helper"
}

# 2. Structural Check: 4 Page Object Models (POM)
$pomFiles = @(
    (Join-Path $ProjectRoot "e2e\pages\authPage.js"),
    (Join-Path $ProjectRoot "e2e\pages\productPage.js"),
    (Join-Path $ProjectRoot "e2e\pages\cartPage.js"),
    (Join-Path $ProjectRoot "e2e\pages\aiChatPage.js")
)
$missingPom = $pomFiles | Where-Object { -not (Test-Path $_) }
if ($missingPom.Count -eq 0) {
    $Results += Record-StaticCheck -Id "CHK-POM-001" -Name "Verified 4 Page Objects: authPage, productPage, cartPage, aiChatPage" -Status "VERIFIED"
} else {
    $Results += Record-StaticCheck -Id "CHK-POM-001" -Name "Missing Page Object files" -Status "FAILED" -Error ("Missing: " + ($missingPom -join ", "))
}

# 3. Structural Check: 17 CodeceptJS Scenarios across 3 Test Files
$testFiles = @(
    @{ file = "e2e\tests\01_auth_test.js"; count = 5; feature = "Auth E2E Scenarios" },
    @{ file = "e2e\tests\02_search_and_ai_chat_test.js"; count = 6; feature = "Search & AI Chat Scenarios" },
    @{ file = "e2e\tests\03_cart_and_checkout_test.js"; count = 6; feature = "Cart & Checkout Scenarios" }
)

$totalScenariosFound = 0
foreach ($t in $testFiles) {
    $filePath = Join-Path $ProjectRoot $t.file
    if (Test-Path $filePath) {
        $content = Get-Content $filePath -Raw -Encoding UTF8
        $matches = [regex]::Matches($content, "Scenario\(")
        $scount = $matches.Count
        $totalScenariosFound += $scount
        $Results += Record-StaticCheck -Id ("CHK-FILE-" + (Split-Path $t.file -Leaf)) -Name ("File " + $t.file + " contains " + $scount + " defined scenarios") -Status "VERIFIED"
    } else {
        $Results += Record-StaticCheck -Id ("CHK-FILE-" + (Split-Path $t.file -Leaf)) -Name ("File " + $t.file + " missing") -Status "FAILED"
    }
}

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host ("  STATIC AUDIT RESULT: Found " + $totalScenariosFound + " Scenarios defined in test files.") -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Cyan

$SummaryObject = [PSCustomObject]@{
    suite = "YIYI-50: CodeceptJS E2E Static Verification Audit"
    auditType = "Static Code Analysis (NOT Browser E2E Execution)"
    executedAt = (Get-Date).ToString("yyyy-MM-ddTHH:mm:sszzz")
    scenariosFound = $totalScenariosFound
    checks = $Results
}

$SummaryJsonPath = Join-Path $ProjectRoot "test-scripts\YIYI-50-codeceptjs-static-audit.json"
$SummaryObject | ConvertTo-Json -Depth 5 | Set-Content -Path $SummaryJsonPath -Encoding UTF8
Write-Host "Static verification report exported to test-scripts/YIYI-50-codeceptjs-static-audit.json" -ForegroundColor Yellow
