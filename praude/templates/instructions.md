# Claude Instructions: `{{ title }}`

## Context

The current task is part of the {{ organization_name }} bug bounty program, hosted on {{ platform_name }} (program slug: `{{ program_slug }}`).

{% if business_description %}
Quick description of the activity, given by the organization:
{{ business_description }}
{% endif %}

- Program Name: {{ title }}
- Program Type: {{ program_type }}
- Managed by: {{ organization_name }}
{% if report_language %}
- Report language: {{ report_language }}
{% endif %}

## Objective

Identify and report exploitable vulnerabilities within the defined scope.
Prioritize critical/high impact findings, in accordance with the program's rules of engagement.

## Scope

Assets are listed with their criticality (as defined by the program). Prioritize testing effort on CRITICAL and HIGH criticality assets first.

### In-scope assets

| Target | Type | Criticality | Reports |
|------|--------|-------|-------|
{% for asset in in_scope -%}
| {{ asset.target }} | {{ asset.type }} | {{ asset.criticality }} | {{ asset.reports }} |
{% endfor %}

### Out-of-scope assets

{% if out_of_scope %}
{% for item in out_of_scope -%}
- {{ item }}
{% endfor %}
{% else %}
No out-of-scope assets defined for this program.
{% endif %}

## Test accounts

{% if accounts %}
The following accounts are provisioned for testing. When multiple accounts are available, use them to test authorization flaws (IDOR, privilege escalation, broken access control) by attempting to access or modify resources owned by another account.

| Scope | Label | Username / Email | Password | Notes |
|-------|-------|-------------------|----------|-------|
{% for account in accounts -%}
| {{ account.scope or "All in-scope assets" }} | {{ account.label }} | {{ account.username }} | {{ account.password }} | {% if account.role %}({{ account.role }}) {% endif %}{{ account.notes }} |
{% endfor %}
{% elif account_access %}
No test accounts were provisioned directly for this program. Refer to the Account Access section below for how to obtain valid credentials.
{% else %}
No test accounts were provisioned for this program. Testing must be limited to unauthenticated / publicly accessible functionality.
{% endif %}

## Email aliases

{% if email_aliases %}
The following YesWeHack email aliases belong to the hunter account. They are not necessarily accounts (though some may already be registered), and any mail sent to them reaches the hunter inbox. Use them to self-register on in-scope assets when credentials are needed and the program allows self-registration (they also receive confirmation links, OTPs and password-reset emails).

{% for alias in email_aliases -%}
- `{{ alias }}`
{% endfor %}

You can also use temporary / disposable email addresses if needed.
{% else %}
No email aliases are attached to the hunter account. You can use temporary / disposable email addresses if you need to self-register.
{% endif %}

## Vulnerability types

The vulnerabilities are divided into two categories:
- The qualifying vulnerabilities, which are eligible for rewards
- The non-qualifying vulnerabilities, which are not eligible for rewards on this program

### Qualifying vulnerabilities

{% if qualifying_vulnerabilities %}
The qualifying vulnerabilities for this program are:
{% for vuln in qualifying_vulnerabilities -%}
- {{ vuln }}
{% endfor %}
{% else %}
No qualifying vulnerability list was specified by the program.
{% endif %}

### Non-qualifying vulnerabilities

{% if non_qualifying_vulnerabilities %}
The non-qualifying vulnerabilities for this program are:
{% for vuln in non_qualifying_vulnerabilities -%}
- {{ vuln }}
{% endfor %}
{% else %}
No non-qualifying vulnerability list was specified by the program.
{% endif %}

{% if rules %}
## Program specific rules (organization's defined)

{{ rules }}
{% endif %}

{% if user_agent or vpn_proxy_url or account_access %}
## Hunting requirements

To hunt on this program, some requirements apply.

{% if user_agent %}
### User Agent

All requests to the in-scope assets need to have this specific user-agent suffix: `{{ user_agent }}`.
{% endif %}

{% if vpn_proxy_url %}
### VPN

All requests must pass through this proxy in order to go through the YesWeHack VPN: `{{ vpn_proxy_url }}`.
{% endif %}

{% if account_access %}
### Account Access

The program defines these rules for the accounts:

{{ account_access }}
{% endif %}
{% endif %}
