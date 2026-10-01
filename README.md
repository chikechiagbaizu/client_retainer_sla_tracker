# Client Retainer & SLA Tracker

An Odoo module for tracking client retainer agreements at a consulting or service agency — hours allowance, usage, renewal status, and which account manager owns each relationship.

Built as a hands-on learning project to practice classical model inheritance on a *standard* Odoo model (`res.partner`), computed status fields, automated testing with `TransactionCase`, dynamic Kanban visibility, and row-level security scoped to an assigned manager.

## Features

- **Retainer tracking** — client, tier (Bronze/Silver/Gold), monthly hour allowance, hours used, and assigned account manager.
- **Automatic usage warnings** — a retainer's status flips to "Warning" automatically once 80% of the monthly hour allowance is used, with no manual step required.
- **Automatic renewal validation** — a computed renewal status flags a retainer as "Failed" if its renewal date isn't after its start date, or isn't in the future, surfaced visibly rather than silently.
- **Service line logging** — a running log of dated service entries against each retainer, with hours logged per entry.
- **Native Contacts integration** — client contact records show a "Retainers" smart button and count directly on their standard partner form, linking straight to that client's retainer history. No separate screen needed to find it.
- **Dynamic Kanban urgency indicators** — retainer cards are colored red/amber/green based on how close the renewal date is, so at-risk accounts are visible at a glance.
- **Role-based security**
  - **Agency Admins** — full CRUD on all retainers and service lines.
  - **Account Managers** — read-only access, scoped automatically to only the retainers they're assigned to manage.
  - All other users have no access to retainer data by default.
- **Tested** — core business logic (usage-warning threshold, renewal validation) is covered by `TransactionCase` unit tests, not just manual UI checks.

## Models

| Model | Purpose |
|---|---|
| `client.retainer` | A single client retainer agreement: tier, hours, dates, manager, computed status |
| `retainer.service.line` | A dated log entry of service hours against a retainer |
| `res.partner` (extended) | Adds a `retainer_ids` relation and retainer count, surfaced as a smart button on the standard contact form |

## Installation

1. Copy the module folder into your Odoo `addons` path.
2. Restart the Odoo server.
3. Activate developer mode, go to **Apps**, click **Update Apps List**.
4. Search for "Client Retainer & SLA Tracker" and click **Install**.

## Usage

1. Go to **Client Retainers → Retainers** to create a new retainer agreement — select the client, tier, hour allowance, dates, and account manager.
2. Log service work against a retainer from its **Service Log** tab as it happens.
3. Watch the **Hours** status and the Kanban card color update automatically as usage and renewal dates approach their thresholds — no manual flagging required.
4. Open any client's contact record in **Contacts** to see their retainer count and jump straight to their history via the smart button.
5. Assign users to the **Agency Admin** or **Account Manager** group (Settings → Users) to control what they can see and manage.

## Security model

| Group | Access |
|---|---|
| Agency Admin | Full CRUD on all retainers and service lines |
| Account Manager | Read-only, limited to retainers where they are the assigned `account_manager_id` |
| No group | No access |

## Testing

Run the module's test suite with:

```bash
odoo-bin -d your_database -i client_retainer_tracker --test-enable --stop-after-init
```

Tests cover:
- Usage status correctly stays "Normal" below the 80% threshold and flips to "Warning" at or above it.
- Renewal status correctly fails when the renewal date precedes the start date, fails when it isn't in the future, and succeeds on a genuinely valid future date.

## Folder structure

```
client_retainer_tracker/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── client_retainer.py
│   ├── retainer_service_line.py
│   └── res_partner.py
├── security/
│   ├── retainer_security_groups.xml
│   ├── ir.model.access.csv
│   └── retainer_rule.xml
├── views/
│   ├── client_retainer_views.xml
│   ├── client_retainer_actions.xml
│   ├── res_partner_views.xml
│   └── client_retainer_menus.xml
├── tests/
│   ├── __init__.py
│   ├── test_hours_used.py
│   └── test_renewal_date.py
└── static/
    └── description/
        └── icon.png
```

## Requirements

- Odoo 19.0+
- Depends on the standard `base` and `contacts` modules
- No external Python dependencies beyond Odoo core

## Category

Services/Consultancy

## License

LGPL-3

## Author

Chike Chiagbaizu