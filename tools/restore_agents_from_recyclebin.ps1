param(
  [string]$MatchPath = "E:\projects\github\1.Whiskey28\wmt_skills\.agents\"
)

$ErrorActionPreference = "Stop"

function Get-RecycleBinItems {
  $shell = New-Object -ComObject Shell.Application
  $rb = $shell.NameSpace(0xA)
  foreach ($item in $rb.Items()) {
    $originalPath = $rb.GetDetailsOf($item, 1)
    $name = $rb.GetDetailsOf($item, 0)
    $deletedOn = $rb.GetDetailsOf($item, 2)
    [pscustomobject]@{
      Item = $item
      Name = $name
      OriginalPath = $originalPath
      DeletedOn = $deletedOn
    }
  }
}

$items = @(Get-RecycleBinItems | Where-Object { $_.OriginalPath -like "*$MatchPath*" })

Write-Host ("Found {0} recycle bin items matching path: {1}" -f $items.Count, $MatchPath)

if ($items.Count -eq 0) {
  exit 2
}

$restored = 0
foreach ($it in $items) {
  try {
    # RESTORE verb moves item back to OriginalPath
    $it.Item.InvokeVerb("RESTORE")
    $restored++
  } catch {
    Write-Warning ("Failed to restore: {0} ({1})" -f $it.Name, $it.OriginalPath)
  }
}

Write-Host ("Restore attempted for {0} items." -f $restored)
exit 0

