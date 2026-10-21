# ADR-0007: Photo storage on Cloudflare R2

- Status: Accepted
- Date: 2026-10-19 (photo backup added the same day after the review panel)
- Decided by: Product owner, approving the recommended architecture package on 2026-10-19.
- Confidence: High
- Change later: Easy

## Context
Renters and vendors attach photos taken inside homes (FR-1, FR-4). Photos will be most of the stored data, are viewed by staff, vendors and renters, can carry location data, and arrive from iPhones in HEIC format. Uploads must work on phone connections (NFR-1).

## Options considered
1. **Cloudflare R2** — $0.015 per GB a month, no download (egress) fees, S3-compatible API / one more vendor account to secure.
2. **Amazon S3** — the most established / download fees on every photo view.
3. **Disk on the app servers** — rejected: tied to one instance and lost on redeploys.

## Decision
- A private R2 bucket per environment for photos; nothing is public.
- Browsers upload directly to R2 using short-lived pre-signed upload links limited by size (15 MB) and type, so uploads do not tie up web instances.
- A background job checks each upload, converts HEIC and other formats to JPEG, removes all metadata (including location), makes a thumbnail, and deletes the original upload. Only processed photos are ever shown. The job runs on the `media` worker, which holds no email, text or Stripe credentials (ADR-0005), with a pixel limit (Pillow's decompression-bomb guard) and a per-image time limit.
- Photos are shown through pre-signed links that expire after 10 minutes.
- Only the `media` app talks to R2 (through django-storages and its S3 backend).
- Photos are backed up too: the nightly backup job copies new photos to a bucket in a separate Cloudflare account, and photos deleted from the main bucket stay in the backup for 30 days (architecture.md › Operations).

## Why
- Cheapest storage with free downloads, which matters because every photo is viewed several times.
- The S3-compatible API keeps an exit path to Amazon S3 or another provider.

## Consequences
- Good: storage stays a few dollars a month at launch (architecture.md › Cost).
- Costs and tradeoffs: cross-origin settings must allow direct uploads from the app's domain only; deletion for departing companies (FR-22) must cover photos.
- Follow-up work: bucket settings and the processing job in M1.

## Evidence
- [Cloudflare R2 pricing](https://developers.cloudflare.com/r2/pricing/) (checked 2026-10-19) — $0.015/GB-month; Class A $4.50 and Class B $0.36 per million operations; free egress; free tier 10 GB.

## Revisit when
- Stored photos pass 5 TB, or image resizing at view time is needed.
- A customer requires Canadian data residency for photos.
