param(
  [int]$Limit = 200,
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
  $resp = Invoke-WebRequest -Uri $Url -Method Get -UseBasicParsing
  return [string]$resp.Content
}

function Get-SkillNameFromFetchUrl([string]$FetchUrl) {
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

Ensure-Dir (Join-Path $RepoRoot ".agents")
Ensure-Dir $SkillsDir

$trendUrl = "https://skillshub.wtf/api/v1/skills/trending?limit=$Limit"
$trend = Invoke-RestMethod -Uri $trendUrl -Method Get

if (-not $trend.data) {
  Write-Host "No trending skills returned."
  exit 2
}

Write-Host ("Trending skills returned: {0}" -f $trend.data.Count)

$installed = 0
$skipped = 0
$failed = 0

foreach ($row in $trend.data) {
  # API returns skills; build fetchUrl from github owner/repo/slug
  $owner = $row.repo.githubOwner
  $repo = $row.repo.githubRepoName
  $slug = $row.slug
  if ([string]::IsNullOrWhiteSpace($owner) -or [string]::IsNullOrWhiteSpace($repo) -or [string]::IsNullOrWhiteSpace($slug)) {
    continue
  }
  $fetchUrl = ("https://skillshub.wtf/{0}/{1}/{2}" -f $owner, $repo, $slug) + "?format=md"
  try {
    if (Install-SkillFromFetchUrl $fetchUrl) { $installed++ } else { $skipped++ }
  } catch {
    $failed++
    Write-Warning ("Failed: {0}" -f $fetchUrl)
  }
}

Write-Host ("Done. installed={0} skipped={1} failed={2}" -f $installed, $skipped, $failed)
if ($failed -gt 0) { exit 1 }
exit 0

