import requests


def send_finops_alert(webhook_url: str, disks: list, ips: list, monthly_savings: float):
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0076D7",
        "summary": "Azure FinOps Optimization Report",
        "sections": [{
            "activityTitle": "💰 Azure FinOps Waste Cleaner - Executive Summary",
            "activitySubtitle": "Automated Infrastructure Resource Hygiene",
            "facts": [
                {"name": "Orphaned Disks:", "value": str(len(disks))},
                {"name": "Unattached Public IPs:", "value": str(len(ips))},
                {"name": "Estimated Monthly Waste:", "value": f"${monthly_savings:,.2f}"},
                {"name": "Annualized Savings Potential:", "value": f"${monthly_savings * 12:,.2f}"}
            ],
            "markdown": True
        }]
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to post FinOps alert to Teams webhook: {e}")
