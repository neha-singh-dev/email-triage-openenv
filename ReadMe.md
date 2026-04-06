---
title: Email Triage OpenEnv
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_file: inference.py
pinned: false
---
# Email Triage OpenEnv Environment

## Overview
This environment simulates a real-world email triage system where an AI agent must classify emails and generate appropriate responses.

## Tasks

### Easy
- Classify emails as `spam` or `not_spam`

### Medium
- Classify emails into:
  - spam
  - promotion
  - important

### Hard
- Classify email AND generate appropriate response

## Action Space
- label: classification label
- response: optional text response (used in hard task)

## Observation Space
- email_text: content of the email

## Reward Design
- Easy/Medium:
  - Correct classification → 1.0
  - Wrong → 0.0

- Hard:
  - Classification reward + Response reward
  - Final = average (0.0 to 1.0)

## Setup

```bash
docker build -t email-env .
docker run email-env