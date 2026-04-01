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

$page = 1
$perPage = 50
$installed = 0
$skipped = 0
$failed = 0
$processed = 0

Write-Host ("Installing top {0} skills by GitHub stars..." -f $Limit)

while ($processed -lt $Limit) {
  $remaining = $Limit - $processed
  $limitThis = [Math]::Min($perPage, $remaining)
  $u = "https://skillshub.wtf/api/v1/skills/search?sort=stars&limit=$limitThis&page=$page"
  $res = Invoke-RestMethod -Uri $u -Method Get
  if (-not $res.data -or $res.data.Count -eq 0) { break }

  foreach ($row in $res.data) {
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

  $processed += $res.data.Count
  if (-not $res.hasMore) { break }
  $page++
}

Write-Host ("Done. processed={0} installed={1} skipped={2} failed={3}" -f $processed, $installed, $skipped, $failed)
if ($failed -gt 0) { exit 1 }
exit 0

