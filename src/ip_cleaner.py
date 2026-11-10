def scan_idle_public_ips(network_client):
    """Finds Static or Dynamic Public IPs not associated with any NIC or Gateway."""
    idle = []
    idle_ip_cost = 3.65  # Average cost per unused static IP/month

    public_ips = network_client.public_ip_addresses.list_all()
    for ip in public_ips:
        if ip.ip_configuration is None:
            idle.append({
                "name": ip.name,
                "resource_group": ip.id.split("/")[4],
                "ip_address": ip.ip_address or "Allocated",
                "sku": ip.sku.name if ip.sku else "Basic",
                "monthly_cost": idle_ip_cost
            })

    total_waste = len(idle) * idle_ip_cost
    return idle, round(total_waste, 2)
