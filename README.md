<div align="center">

# 💰 Azure FinOps Waste Cleaner

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PowerShell](https://img.shields.io/badge/PowerShell-7.4-5391FE?style=for-the-badge&logo=powershell&logoColor=white)](https://learn.microsoft.com/powershell/)
[![Azure Functions](https://img.shields.io/badge/Azure-Serverless_Function-0078D4?style=for-the-badge&logo=azurefunctions&logoColor=white)](https://azure.microsoft.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](./LICENSE)

<p align="center">
  <b>Automated serverless FinOps hygiene engine identifying orphaned disks, unattached public IPs, and zombie snapshots across multi-subscription enterprise Azure tenants.</b>
</p>

</div>

---

## 💡 Overview & Financial Impact

Enterprise cloud spend often suffers from silent waste caused by decommissioned VMs leaving behind unattached managed disks and orphaned static public IPs. 

This toolkit continuously audits subscriptions, calculates monthly leakage according to standard Azure rate cards, and pushes automated executive Slack/Teams cards with exact resource IDs and dollar values saved.

```
┌────────────────────────────┐
│ Azure EventGrid / Cron     │
└─────────────┬──────────────┘
              │ Triggers
              ▼
┌────────────────────────────────────────────────────────┐
│ Azure Function / Runbook (Python 3.11 / PowerShell 7)  │
│  - ComputeManagementClient.disks.list()                │
│  - NetworkManagementClient.public_ip_addresses.list()   │
└─────────────┬──────────────────────────────┬───────────┘
              │                              │
              ▼                              ▼
┌───────────────────────────┐  ┌─────────────────────────┐
│ Microsoft Teams Alert     │  │ CSV Export / FinOps Log │
│ (Dollar amounts & links)  │  │ (Automated Audit Trail) │
└───────────────────────────┘  └─────────────────────────┘
```

---

## 📊 Features

- **Orphaned Managed Disks**: Discovers Premium SSD, Standard SSD, and HDD disks with `managed_by == None`.
- **Idle Static Public IPs**: Finds public IPs reserved but not bound to any Network Interface or Gateway.
- **Cost Quantification Engine**: Calculates monthly run-rate waste in USD automatically.
- **Serverless & Local Execution**: Run as an Azure Function App or directly via PowerShell CLI.
- **Teams / Slack Actionable Cards**: Instant notifications to Cloud Economics and FinOps teams.

---

## 📁 Repository Structure

```
azure-finops-waste-cleaner/
├── .github/workflows/
│   └── ci.yml                  # Flake8 linting and dependency validation
├── src/                        # Python audit engine
│   ├── disk_cleaner.py         # Orphaned disk discovery & cost estimator
│   ├── ip_cleaner.py           # Unattached Public IP auditor
│   ├── teams_notifier.py       # Adaptive card webhook publisher
│   └── main.py                 # Multi-subscription runner
├── powershell/                 # PowerShell automation runbooks
│   └── Invoke-FinOpsAudit.ps1  # Single-command Az cmdlet scanner
├── terraform/                  # Serverless Azure Function deployment IaC
│   └── main.tf
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

```bash
# 1. Clone & Setup
git clone https://github.com/vishwjeetmehta-bot/azure-finops-waste-cleaner.git
cd azure-finops-waste-cleaner
pip install -r requirements.txt

# 2. Set Target Subscription & Run
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export TEAMS_OR_SLACK_WEBHOOK_URL="https://your-teams-webhook-url"
python src/main.py
```

---

## 👤 Author

**Vishwjeet Kumar Mehta**  
Senior DevOps & DevSecOps Consultant | Cloud & Infrastructure Architect  
- **LinkedIn**: [linkedin.com/in/vishwjeetmehta](https://linkedin.com/in/vishwjeetmehta)  
- **GitHub**: [@vishwjeetmehta-bot](https://github.com/vishwjeetmehta-bot)
