---
title: Email Triage OpenEnv
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
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
  - Correct classification → 0.8
  - Wrong → 0.2

- Hard:
  - Classification (0.6 or 0.2) + Response bonus (0.1–0.3)
  - Final score always between 0 and 1 (never 0 or 1)

## Setup

```bash
docker build -t email-env .
docker run email-env