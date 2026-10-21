# ADR-0001: One web app for groomers and clients; no app-store apps in version 1

- Status: Accepted
- Date: 2026-10-19
- Decided by: Owner (the founder chose a browser-based app: "whatever is cheaper and faster")
- Confidence: High
- Change later: Moderate

## Context
Clients book from their phones; groomers work on a laptop or tablet at the salon (NFR-1). The founder wants a version that can be sold within about 3 months, is not a programmer, and builds with AI coding tools, so every extra codebase, toolchain and release process costs real time. Reminders reach clients by text or email, so clients do not need an installed app to get them.

## Options considered
1. **One responsive web app** (client booking page and groomer screens in the browser) — one codebase; instant updates; works on any phone, tablet or laptop; no store fees or app review / no App Store presence; notifications to groomers rely on email, text or web push rather than native app notifications.
2. **Store app for groomers, web booking page for clients** — native feel and notifications for groomers / a second codebase or cross-platform toolchain; Apple and Google developer accounts; app review on every release; signing and release management.
3. **Store apps for groomers and clients** — the most "app-like" / the most work; clients are unlikely to install an app for a groomer they visit every few weeks.

## Decision
Build one responsive web app. Clients use a mobile-first booking page in their phone's browser; groomers use the same app's groomer screens on a laptop or tablet, and can add it to their home screen. No App Store or Google Play apps in version 1.

## Why
- Matches where people already are: clients tap a link on their phone; groomers already have a laptop or tablet at the salon.
- The fastest and cheapest path to a sellable version in about 3 months: one codebase, no app review delays, no store fees.
- Store apps lost because they add a second release process that a non-programmer building with AI tools would have to manage, without a version 1 requirement that needs them.

## Consequences
- Good: one codebase; every groomer and client gets fixes the moment they ship.
- Costs and tradeoffs: no store listing to be discovered in; groomer notifications depend on email, text or web push.
- Follow-up work: design the booking page for phones first and the groomer screens for tablet and laptop; test on iPhone Safari, Android Chrome, iPad Safari and a desktop browser before each release.

## Evidence
- Apple Developer Program: "$99 annual membership" — https://developer.apple.com/programs/ (checked 2026-10-19)
- Google Play Console: "US$25 one-time registration fee" — https://support.google.com/googleplay/android-developer/answer/6112435 (checked 2026-10-19)

## Revisit when
- Several paying groomers ask for an installed app or for notifications the web cannot give them.
- Groomers need to work without signal (for example mobile groomers in vans), which a plain web app handles poorly.
