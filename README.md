# An Ethical Simulated Phishing Study: Assessing Behavioral Susceptibility in an SME Context and the Implementation of a Targeted phishing Awareness

**Author:** Jesufemi Dada
**Date:** May 2026
**Status:** Completed

## Overview

An ethical, consent-based simulated phishing study conducted with 17
SME-employed participants. The study investigated behavioural and cognitive
factors contributing to phishing susceptibility, and implemented a custom
just-in-time awareness training programme for participants who clicked.

## Executive Summary

This project presents a consent-based, ethically governed simulated phishing
study conducted in May 2026 with 17 SME-employed participants aged 26 to 34.
The study was designed to investigate the behavioural and cognitive factors
that cause individuals to fall for phishing emails, and to implement an
immediate, targeted awareness training response for those who clicked.

A simulated phishing email was deployed via GoPhish hosted on a DigitalOcean
VPS, delivered through Brevo authenticated SMTP. Participants who clicked were
directed to an ethical disclosure page, an anonymous behavioural survey, and a
custom five-module phishing awareness training programme hosted on Google
Classroom.

**12 of 17 participants clicked the simulation link — a 70.6% click rate,
2.9 times the KnowBe4 2025 SME industry baseline of 24.6%.** Analysis of
the behavioural survey revealed that curiosity was the dominant click
motivator (54.5%), followed by genuine belief in the email's legitimacy
(45.5%). 

Time-to-click analysis showed that 75% of participants clicked more than 30 minutes after delivery, confirming that susceptibility was driven by the quality of the social engineering rather than momentary inattention.

The most significant finding was the Overconfidence Paradox: 54.5% of
respondents rated themselves as highly confident in their ability to detect
phishing before the study — and every one of them clicked. This directly
reflects the Dunning-Kruger effect (Kruger and Dunning, 1999) and
demonstrates that security awareness training must target confident
employees, not just those who self-identify as uncertain.

The study concludes that SME phishing susceptibility is more of a behavioural and cognitive challenge, not just a technical one. Effective mitigation requires recurring simulation, just-in-time embedded training, and confidence calibration exercises designed to close the metacognitive gap that leaves the most self-assured employees the most exposed.

# Behavioural Security Study Infrastructure

This repository also documents the infrastructure setup used for a controlled behavioural security study. The environment was built to support a web application, email delivery, DNS configuration, and a hosted lab server for campaign-style testing in a closed setting. Full deployment steps, sensitive configuration values, and end-to-end operational instructions are **intentionally withheld** from this documentation.

##The project used:
- Namecheap for domain registration and DNS management.
- DigitalOcean for hosting the virtual private server.
- Brevo for transactional email delivery.
- GoPhish as the study platform for controlled campaign tracking and reporting.
- PowerShell on the local workstation for remote administration and setup tasks.

A cloud-hosted phishing awareness lab built for **personal security research and behavioural study**. The environment was designed to be accessible on **any network from any location** — no shared physical network required between researcher and participants.

## Namecheap

Namecheap was used to register the study domain and manage the domain’s ownership and DNS configuration. Its role in the setup was to provide a public-facing domain name that could be mapped to the hosted server and used consistently in study communications.

### Purpose
- Register and hold the domain.
- Provide a central place for DNS management.
- Support TXT records used for domain verification and email authentication.

## DigitalOcean

DigitalOcean was used to host the Linux server that ran the study platform. The server provided the public IP address, network access, and the runtime environment needed to keep the service online.

### Purpose
- Host the application on a VPS.
- Provide a stable public endpoint for the domain.
- Run the study service continuously so it remained available even when the local laptop was closed.

### DNS and Hosting Connection
The domain was pointed to the DigitalOcean server by updating DNS records so the public hostname resolved to the VPS. This made the service reachable through the domain name rather than by raw IP address.

## Brevo

Brevo was used as the transactional email provider. Its purpose was to send the study emails reliably through authenticated SMTP delivery, rather than sending mail directly from the server.

### Purpose
- Send outgoing mail through a trusted mail relay.
- Improve deliverability and reduce the chance of mail being rejected.
- Provide logs for delivery status and troubleshooting.
- Support sender/domain verification for authenticated sending.

## PowerShell Administration

PowerShell was used as the local administration tool for remote server management. It helped connect to the VPS, run setup commands, and manage the service from a Windows workstation.

### Purpose
- Open an SSH session to the server.
- Run setup and maintenance commands remotely.
- Verify service status and restart the application when needed.

## GoPhish Setup

GoPhish was installed on the VPS and configured as the study platform. The service was set up to run continuously in the background and automatically restart if the server rebooted.

### Service Persistence
A system service was created so the application would start automatically on boot. This ensured the study environment stayed available without manual intervention after reboots or server maintenance.

## What Worked Well

The final setup achieved the following:
- The domain resolved correctly to the hosted server.
- The email sending service was authenticated and working.
- The server remained online independently without shared network between participant and researcher.
- The application started automatically and stayed running.
- Domain verification succeeded for mail-related tooling.
- The study environment became stable enough for consented participant testing.

## Operational Notes

The environment was structured so each service had a separate responsibility:
- Namecheap handled the domain.
- DigitalOcean handled hosting.
- Brevo handled email delivery.
- GoPhish handled study delivery and tracking.

This separation made the setup easier to manage and troubleshoot, while keeping the infrastructure reliable for the project work.
