# PostFlow — Wireframes

**Status:** Low-fidelity structural wireframes  
**Related specification:** [UI_UX_SPECIFICATION.md](../UI_UX_SPECIFICATION.md)  
**Interactive prototype:** [Open prototype](./prototype/index.html)

These wireframes define hierarchy and task flow, not final pixel-perfect styling. The prototype is a static front-end concept using representative data; it does not connect to the FastAPI backend or real social/AI providers.

## 1. Application shell

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ POSTFLOW   [Workspace ▾] [Brand ▾]                     Search       Help   Notifications  ● │
├───────────────┬─────────────────────────────────────────────────────────────────────────────┤
│               │                                                                             │
│  OVERVIEW     │  Page title                                      [Primary action]           │
│  Calendar     │  Supporting description                                                   │
│               │  ┌───────────────────────────────────────────────────────────────────────┐ │
│  CREATE       │  │ Context banner / runtime status / account warning                    │ │
│  Content      │  └───────────────────────────────────────────────────────────────────────┘ │
│  Composer     │                                                                             │
│               │  Main content area                                                         │
│  ASSETS       │                                                                             │
│  Media        │                                                                             │
│               │                                                                             │
│  PUBLISHING   │                                                                             │
│  Accounts     │                                                                             │
│  Queue        │                                                                             │
│               │                                                                             │
│  INTELLIGENCE │                                                                             │
│  AI Providers │                                                                             │
│  Analytics    │                                                                             │
│               │                                                                             │
│  SYSTEM       │                                                                             │
│  Settings     │                                                                             │
│               │                                                                             │
│  ● API online │                                                                             │
│  ● Worker on  │                                                                             │
└───────────────┴─────────────────────────────────────────────────────────────────────────────┘
```

## 2. Overview

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ Overview                                                          [ + Create post ]         │
│ Your publishing workspace at a glance                                                       │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ [ Scheduled 08 ] [ Awaiting approval 03 ] [ Published 24 ] [ Needs attention 02 ]          │
├───────────────────────────────────────────────────────────────┬─────────────────────────────┤
│ Upcoming                                                     │ Account health              │
│ ┌───────────────────────────────────────────────────────────┐ │ ┌─────────────────────────┐ │
│ │ 10:30  LinkedIn   Product launch                           │ │ │ LinkedIn  Connected     │ │
│ │ 13:00  Instagram  Tutorial carousel                         │ │ │ Instagram Reauthorize   │ │
│ │ Tomorrow         X          Release notes                   │ │ │ AI provider 2/3 ready   │ │
│ └───────────────────────────────────────────────────────────┘ │ └─────────────────────────┘ │
│                                                               │ Quick actions               │
│ Recent activity                                               │ [Connect account]            │
│ ┌───────────────────────────────────────────────────────────┐ │ [Create content]             │
│ │ Draft updated · 4 min ago                                  │ │ [Open queue]                 │
│ │ Job published · LinkedIn · Yesterday                       │ │                             │
│ └───────────────────────────────────────────────────────────┘ │                             │
└───────────────────────────────────────────────────────────────┴─────────────────────────────┘
```

## 3. Composer — source plus destination variants

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ ← Content library   New post                      Saved · 10:42 AM       [Save draft] [Next] │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ SOURCE CONTENT                                      DESTINATIONS                              │
│ ┌───────────────────────────────────────────────┐  ┌───────────────────────────────────────┐ │
│ │ Internal title                                 │  │ [✓ LinkedIn] [✓ Instagram] [ ] X      │ │
│ │                                               │  │                                       │ │
│ │ Source text                                   │  │ LinkedIn variant                      │ │
│ │                                               │  │ ┌───────────────────────────────────┐ │ │
│ │                                               │  │ │ Platform-specific copy            │ │ │
│ │                                               │  │ │                                   │ │ │
│ │                                               │  │ └───────────────────────────────────┘ │ │
│ │                                               │  │ 214 / capability limit               │ │
│ │                                               │  │ [Generate] [Preview] [Validate]       │ │
│ └───────────────────────────────────────────────┘  │                                       │ │
│ [AI assist] [Attach media] [Brand voice]           │ Instagram variant                     │
│                                                    │ [Edit] [Preview] [Validate]            │
│                                                    └───────────────────────────────────────┘ │
│ Approval is tied to the exact revision. Editing after approval requires re-approval.         │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 4. Calendar

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ Calendar                     [Month] [Week] [List]              [Today] [ + Schedule ]      │
│ [‹]  9–15 November 2026  [›]          Filters: [All platforms ▾] [All statuses ▾]             │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ MON 9       TUE 10       WED 11       THU 12       FRI 13       SAT 14       SUN 15           │
│ ┌────────┐  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐      │
│ │10:00   │  │11:30   │   │        │   │09:00   │   │14:00   │   │        │   │        │      │
│ │LinkedIn│  │Insta   │   │        │   │X       │   │LinkedIn│   │        │   │        │      │
│ │Launch  │  │Carousel│   │        │   │Release │   │Update  │   │        │   │        │      │
│ └────────┘  └────────┘   └────────┘   └────────┘   └────────┘   └────────┘   └────────┘      │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ Local desktop scheduler: PostFlow and the worker must be running at the scheduled time.       │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 5. Publishing queue and job detail

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ Publishing queue                                                                            │
│ [Scheduled 8] [Running 1] [Failed 2] [Needs reconciliation 1] [Published]                   │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ Content             Destination       Scheduled          State                 Action       │
│ Launch announcement LinkedIn / Page   Nov 10, 10:30       Scheduled             Open         │
│ Product teaser      Instagram         Nov 10, 13:00       Failed                Diagnose     │
│ Feature update     X                 Nov 11, 09:00       Unknown outcome       Reconcile    │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ Selected job detail                                                                         │
│ State: NEEDS RECONCILIATION                                                                  │
│ Last attempt: timeout after request sent                                                    │
│ [Attempt timeline]                                                                          │
│ Do not retry until platform state is reconciled.                                            │
│ [Check platform status] [Mark manually resolved]                                            │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 6. Social accounts

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ Social accounts                                                     [ + Connect account ]   │
│ Manage connected destinations and permission health                                        │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ [LinkedIn icon]  DevSpire Company Page       Connected · Verified 5 min ago   [Manage]       │
│ [Instagram icon] @devspirehub                Reauthorization required         [Reconnect]    │
│ [X icon]         @devspirehub                Connected · Limited capability   [Manage]       │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 7. Media library

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ Media library                                                      [ Upload media ]         │
│ [Search assets...] [All types ▾] [Processing ▾]                                              │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐                              │
│ │ Thumbnail  │  │ Thumbnail  │  │ Thumbnail  │  │ Thumbnail  │                              │
│ │ campaign   │  │ tutorial   │  │ logo       │  │ reel       │                              │
│ │ Ready      │  │ Ready      │  │ Ready      │  │ Processing │                              │
│ └────────────┘  └────────────┘  └────────────┘  └────────────┘                              │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 8. Responsive transformations

- At 1200 px: collapse sidebar; keep composer columns only if both remain usable.
- At 900 px: stack composer source and destination panels; inspectors become drawers.
- At 768 px: calendar defaults to list; tables become cards.
- At 640 px: navigation becomes a drawer; actions wrap into a compact toolbar.
- At all widths: retain visible status text, keyboard focus and access to primary actions.
