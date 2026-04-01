param(
  [string]$RepoRoot = "E:\projects\github\1.Whiskey28\wmt_skills",
  [string]$SkillsDir = "E:\projects\github\1.Whiskey28\wmt_skills\.agents\skills"
)

$ErrorActionPreference = "Stop"

function Ensure-Dir([string]$Path) {
  if (-not (Test-Path -LiteralPath $Path)) {
    New-Item -ItemType Directory -Path $Path -Force | Out-Null
  }
}

function Fetch-Text([string]$Url) {
  # Use Invoke-WebRequest to get raw markdown (Skillshub returns text/markdown)
  $resp = Invoke-WebRequest -Uri $Url -Method Get -UseBasicParsing
  return [string]$resp.Content
}

function Get-SkillNameFromFetchUrl([string]$FetchUrl) {
  # Example: https://skillshub.wtf/anthropics/skills/docx?format=md
  $noQuery = $FetchUrl.Split('?')[0]
  return ($noQuery.TrimEnd('/') -split '/')[ -1 ]
}

function Install-SkillFromFetchUrl([string]$FetchUrl) {
  $name = Get-SkillNameFromFetchUrl $FetchUrl
  if ([string]::IsNullOrWhiteSpace($name)) { return $false }

  $dst = Join-Path $SkillsDir $name
  $skillFile = Join-Path $dst "SKILL.md"

  if (Test-Path -LiteralPath $skillFile) { return $false }

  Ensure-Dir $dst
  $md = Fetch-Text $FetchUrl
  Set-Content -LiteralPath $skillFile -Value $md -Encoding UTF8
  return $true
}

function Get-FetchUrlsFromNavFiles {
  $navFiles = Get-ChildItem -LiteralPath (Join-Path $RepoRoot "roles") -Recurse -Filter "NAV.md" -File
  $urls = New-Object System.Collections.Generic.HashSet[string]
  foreach ($f in $navFiles) {
    $text = Get-Content -LiteralPath $f.FullName -Raw -Encoding UTF8
    # Parse YAML block inside NAV_DATA: collect lines like "url: https://skillshub.wtf/..."
    foreach ($m in [regex]::Matches($text, "^\s*url:\s*(https?://\S+)\s*$", "Multiline")) {
      [void]$urls.Add($m.Groups[1].Value)
    }
  }
  # Return as an enumerable of strings
  return $urls
}

function Get-RepoSkillsFetchUrls([string]$Owner, [string]$RepoName) {
  $page = 1
  $limit = 50
  $all = @()
  while ($true) {
    $u = "https://skillshub.wtf/api/v1/skills/search?owner=$Owner&repo=$RepoName&limit=$limit&page=$page"
    $res = Invoke-RestMethod -Uri $u -Method Get
    foreach ($s in $res.data) {
      $slug = $s.slug
      if (-not [string]::IsNullOrWhiteSpace($slug)) {
        $all += ("https://skillshub.wtf/{0}/{1}/{2}" -f $Owner, $RepoName, $slug) + "?format=md"
      }
    }
    if (-not $res.hasMore) { break }
    $page++
  }
  return $all | Select-Object -Unique
}

Ensure-Dir (Join-Path $RepoRoot ".agents")
Ensure-Dir $SkillsDir

Write-Host "Collecting fetchUrls from roles/*/NAV.md ..."
$navUrls = @(Get-FetchUrlsFromNavFiles)
Write-Host ("Found {0} unique Skillshub fetchUrls in NAV files." -f $navUrls.Count)

$coreRepos = @(
  @{ owner = "anthropics"; repo = "skills" },
  @{ owner = "obra"; repo = "superpowers" }
)

Write-Host "Collecting core repo skills (anthropics/skills, obra/superpowers) ..."
$coreUrls = @()
foreach ($r in $coreRepos) {
  $coreUrls += Get-RepoSkillsFetchUrls -Owner $r.owner -RepoName $r.repo
}
$coreUrls = $coreUrls | Select-Object -Unique
Write-Host ("Found {0} core fetchUrls." -f $coreUrls.Count)

$allUrls = @($navUrls + $coreUrls) | Select-Object -Unique
Write-Host ("Installing {0} skills into {1} ..." -f $allUrls.Count, $SkillsDir)

$installed = 0
$skipped = 0
$failed = 0

foreach ($u in $allUrls) {
  try {
    if (Install-SkillFromFetchUrl $u) { $installed++ } else { $skipped++ }
  } catch {
    $failed++
    Write-Warning ("Failed: {0}" -f $u)
  }
}

Write-Host ("Done. installed={0} skipped={1} failed={2}" -f $installed, $skipped, $failed)
if ($failed -gt 0) { exit 1 }
exit 0

