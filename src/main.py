"""
Azure FinOps Waste Cleaner - Enterprise Cost Optimization Engine
Author: Vishwjeet Kumar Mehta
"""

import os
import logging
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from disk_cleaner import scan_unattached_disks
from ip_cleaner import scan_idle_public_ips
from teams_notifier import send_finops_alert

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def run_finops_audit():
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    if not subscription_id:
        logging.error("AZURE_SUBSCRIPTION_ID environment variable not set.")
        return

    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, subscription_id)
    network_client = NetworkManagementClient(credential, subscription_id)

    logging.info("Starting Enterprise FinOps resource scan...")

    orphaned_disks, estimated_disk_waste = scan_unattached_disks(compute_client)
    idle_ips, estimated_ip_waste = scan_idle_public_ips(network_client)

    total_estimated_monthly_savings = estimated_disk_waste + estimated_ip_waste

    logging.info(f"Discovered {len(orphaned_disks)} orphaned disks (Est. Waste: ${estimated_disk_waste:.2f}/mo)")
    logging.info(f"Discovered {len(idle_ips)} idle public IPs (Est. Waste: ${estimated_ip_waste:.2f}/mo)")
    logging.info(f"Total potential monthly FinOps savings: ${total_estimated_monthly_savings:.2f}")

    webhook_url = os.getenv("TEAMS_OR_SLACK_WEBHOOK_URL")
    if webhook_url:
        send_finops_alert(
            webhook_url=webhook_url,
            disks=orphaned_disks,
            ips=idle_ips,
            monthly_savings=total_estimated_monthly_savings
        )


if __name__ == "__main__":
    run_finops_audit()
