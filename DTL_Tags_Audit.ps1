# DTL_tags_audit.ps1
# A lancer depuis le dossier du projet Git

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

Write-Host "Verification du depot..."
git rev-parse --show-toplevel | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erreur : ce dossier n'est pas un depot Git."
    exit 1
}

Write-Host "Verification GitHub CLI..."
gh repo view | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Avertissement : gh n'accede pas au depot GitHub."
    Write-Host "Le script continue avec les informations Git locales."
}

$tags = git for-each-ref refs/tags --format="%(refname:short)|%(objectname:short)|%(contents:subject)"

$rows = foreach ($line in $tags) {
    $parts = $line -split "\|", 3
    $tagName = $parts[0]
    $tagObject = $parts[1]
    $tagMessage = $parts[2]

    # Commit reellement pointe par le tag
    $commit = git rev-list -n 1 $tagName
    $commitShort = git rev-parse --short $commit
    $commitDate = git show -s --format="%cs" $commit
    $commitSubject = git show -s --format="%s" $commit

    [pscustomobject]@{
        DateCommit   = $commitDate
        Tag          = $tagName
        Commit       = $commitShort
        Description  = $tagMessage
        CommitResume = $commitSubject
    }
}

$rows = $rows | Sort-Object DateCommit

Write-Host ""
Write-Host "Historique des tags par date reelle du commit"
Write-Host "---------------------------------------------"
$rows | Format-Table DateCommit, Tag, Commit, Description, CommitResume -AutoSize

Write-Host ""
Write-Host "Propositions de correction"
Write-Host "--------------------------"

foreach ($row in $rows) {
    Write-Host ""
    Write-Host "Tag         : $($row.Tag)"
    Write-Host "Date commit : $($row.DateCommit)"
    Write-Host "Commit      : $($row.Commit)"
    Write-Host "Description : $($row.Description)"
    Write-Host "Resume Git  : $($row.CommitResume)"

    Write-Host ""
    Write-Host "Commande pour changer uniquement la description :"
    Write-Host "git tag -f -a $($row.Tag) $($row.Commit) -m `"NOUVELLE DESCRIPTION`""
    Write-Host "git push origin :refs/tags/$($row.Tag)"
    Write-Host "git push origin $($row.Tag)"
}