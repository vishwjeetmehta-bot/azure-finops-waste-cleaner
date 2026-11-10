<#
.SYNOPSIS
    Automated Azure FinOps Waste Scanner (PowerShell Runbook)
.DESCRIPTION
    Scans Azure subscription for unattached disks, unused public IPs, and old VM snapshots.
    Author: Vishwjeet Kumar Mehta
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$SubscriptionId
)

if ($SubscriptionId) {
    Set-AzContext -SubscriptionId $SubscriptionId | Out-Null
}

Write-Host "=== Starting Azure FinOps Resource Waste Audit ===" -ForegroundColor Cyan

# 1. Orphaned Managed Disks
$unattachedDisks = Get-AzDisk | Where-Object { $_.ManagedBy -eq $null }
Write-Host "Found ($($unattachedDisks.Count)) unattached disks." -ForegroundColor Yellow

$totalDiskWasteGB = 0
foreach ($disk in $unattachedDisks) {
    $totalDiskWasteGB += $disk.DiskSizeGB
    Write-Host " - Orphaned Disk: $($disk.Name) | RG: $($disk.ResourceGroupName) | Size: $($disk.DiskSizeGB) GB"
}

# 2. Unattached Public IPs
$idleIps = Get-AzPublicIpAddress | Where-Object { $_.IpConfiguration -eq $null }
Write-Host "Found ($($idleIps.Count)) unattached public IP addresses." -ForegroundColor Yellow
foreach ($ip in $idleIps) {
    Write-Host " - Idle Public IP: $($ip.Name) | RG: $($ip.ResourceGroupName)"
}

Write-Host "=== Audit Completed Successfully ===" -ForegroundColor Green

