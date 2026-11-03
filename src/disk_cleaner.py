def scan_unattached_disks(compute_client):
    """Identifies unmanaged/managed disks not attached to any running VM."""
    orphaned = []
    total_waste = 0.0

    # Approximate baseline cost per GB for Standard/Premium SSD
    cost_per_gb_ssd = 0.10

    disks = compute_client.disks.list()
    for disk in disks:
        if disk.managed_by is None:
            size_gb = disk.disk_size_gb or 0
            cost = size_gb * cost_per_gb_ssd
            total_waste += cost
            orphaned.append({
                "name": disk.name,
                "resource_group": disk.id.split("/")[4],
                "size_gb": size_gb,
                "tier": disk.sku.name if disk.sku else "Unknown",
                "monthly_cost": round(cost, 2)
            })

    return orphaned, round(total_waste, 2)
