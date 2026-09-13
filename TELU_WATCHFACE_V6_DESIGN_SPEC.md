# TELKOM UNIVERSITY Watchface — V6 "Performance"
## Design & Implementation Specification for Amazfit T-Rex Pro

> **Target device:** Amazfit T-Rex Pro  
> **Display:** 360 × 360 px, circular AMOLED  
> **Base repository:** https://github.com/fathahnoor/telu-amazfit-trex-pro-watchface  
> **Baseline implementation:** current V5  
> **New visual reference:** the latest approved mockup with **white hour digits** and **light-gray minute digits**  
> **Primary goal:** make the time readable instantly from farther away while retaining a sporty, modern Telkom University identity.

---

## 1. Objective

Create a new V6 watchface based on the current working V5 codebase, but substantially redesign the visual hierarchy.

The V6 must prioritize:

1. **Hour and minute readability from a distance**
2. A **sporty / performance-oriented** aesthetic
3. Strong but not excessive **Telkom University branding**
4. High contrast on the T-Rex Pro AMOLED display
5. Preservation of the useful information already present in V5
6. Safe rendering on the physical 360 × 360 circular display
7. Compatibility with the existing repository build, pack, validation, and preview workflow

The watchface must look like a **sports instrument first**, and a university-branded watchface second.

The time is the hero.

---

## 2. Approved Visual Direction

The approved design has this hierarchy:

### Primary

- Large `HH`
- Large `MM`
- `HH` is **white**
- `MM` is **light gray**
- Hour and minute are stacked vertically
- No large conventional horizontal `HH:MM` row
- The time occupies most of the central area

Example:

```text
        10
        28
```

The hour and minute should visually dominate everything else by a large margin.

### Secondary

- Day
- Date
- AM/PM

### Tertiary

- Steps
- Heart rate
- Calories
- Battery
- Sunrise / sunset
- Current temperature / weather status

### Decorative / branding

- Tel-U logo or partial Tel-U visual language
- `HARMONY / EXCELLENCE / INTEGRITY`
- Campus silhouette
- Sport-style perimeter accents
- Tel-U red highlights

---

## 3. Design Philosophy

V5 uses multiple circular metric modules and a relatively balanced visual hierarchy.

V6 should feel more like:

- a running watch
- a motorsport dashboard
- a modern performance wearable
- a bold typographic sports UI

Avoid making every data point equally prominent.

The user's eye should follow this order:

```text
TIME
 ↓
DATE / AM-PM
 ↓
ACTIVITY + STATUS DATA
 ↓
BRANDING / DECORATION
```

At arm's length or farther, the user should still immediately recognize the hour and minute even if the smaller data is unreadable.

---

# 4. Color System

Use a predominantly black AMOLED background.

## Core colors

| Role | Recommended HEX | Notes |
|---|---|---|
| AMOLED background | `#000000` | Main background |
| Main white | `#F5F5F5` to `#FFFFFF` | Hour digits and important values |
| Minute light gray | `#D0D0D2` to `#D8D8DA` | **Minute digits only** |
| Tel-U red | `#ED1E28` | Official Tel-U primary red |
| Tel-U maroon | `#B6252A` | Optional low-intensity accent |
| Tel-U dark gray | `#55565B` | Secondary structural elements |
| Tel-U light gray | `#959597` | Secondary labels |
| Near-black panel | `#0A0A0C` to `#121316` | Side panels |
| Divider gray | `#55565B` at low visual weight | Lines / separators |

Official Telkom University logo palette includes:

- Red `#ED1E28`
- Maroon `#B6252A`
- Dark gray `#55565B`
- Light gray `#959597`

For V6, the minute digits should be **lighter than official Tel-U light gray** so they remain highly readable.

Recommended minute color:

```text
#D2D2D4
```

Do **not** return the minute digits to red.

Red is now an **accent color**, not a primary time color.

---

# 5. Time Typography

## 5.1 Hour

Example:

```text
10
```

Properties:

- Color: white
- Very bold
- Condensed or semi-condensed
- Sans serif
- Minimal internal detail
- Wide stroke
- No outline
- No glow
- No thin decorative effects

Preferred font direction:

- Montserrat ExtraBold / Black
- Inter Black
- another condensed sport-style font if it renders better at 360 × 360

The implementation may rasterize digits into sprites if required by the T-Rex Pro format.

## 5.2 Minute

Example:

```text
28
```

Properties:

- Same font family as hour
- Same or slightly smaller visual size
- Color: **light gray**
- Approx. `#D2D2D4`
- Must still be brighter than labels and structural gray

The purpose of the color difference is to create hierarchy without reducing minute legibility.

## 5.3 Relative scale

Target visual relationship:

```text
hour font height   ≈ 88–100 px
minute font height ≈ 88–100 px
```

Exact sprite dimensions may differ depending on the font.

The important criterion is visual dominance.

Combined hour + minute block should occupy approximately:

```text
45–55% of the visible dial area
```

---

# 6. Main Layout

All coordinates below are **starting targets for a 360 × 360 canvas**, not immutable pixel values.

The implementation must still pass circular-boundary and collision validators.

## 6.1 Coordinate system

```text
Top-left     = (0, 0)
Center       = (180, 180)
Bottom-right = (359, 359)
```

Maintain a practical safety radius inside the physical bezel.

Recommended important-content safe region:

```text
x ≈ 20..340
y ≈ 18..342
```

Avoid placing critical text at the extreme rim.

---

# 7. Proposed 360 × 360 Placement

## 7.1 Top branding zone

Approximate area:

```text
x = 120..240
y = 10..90
```

Contains:

- simplified Tel-U mark
- `Telkom University`

The logo does not have to use the full official logo.

It may use:

- the red open-book element
- the U / shield geometry
- only the upper crest
- a simplified monochrome version

Do not let the branding compete with the time.

Recommended height:

```text
Tel-U mark       ≈ 30–42 px
wordmark group   ≈ 20–30 px
```

---

## 7.2 Main time block

Approximate center:

```text
x ≈ 175–185
```

Suggested bounds:

```text
Hour:
x ≈ 112..247
y ≈ 100..188

Minute:
x ≈ 106..249
y ≈ 182..273
```

The hour and minute should almost touch visually but must not overlap.

Use optical centering rather than purely mathematical centering.

The digit pair must remain centered when the time changes, including:

```text
00
01
08
10
11
18
20
23
```

and minute combinations such as:

```text
00
01
08
10
11
28
44
58
59
```

---

## 7.3 AM/PM

Place beside the hour/minute block, approximately:

```text
x ≈ 245..285
y ≈ 155..185
```

Style:

- small
- gray
- uppercase
- optional short red underline

Example:

```text
AM
—
```

AM/PM must never visually compete with the time.

If firmware / format behavior makes AM/PM difficult, prioritize 24-hour mode compatibility.

---

# 8. Left Information Panel

Use a dark, irregular rounded sport panel instead of circular gauges.

Suggested bounds:

```text
x ≈ 20..108
y ≈ 102..275
```

Suggested contents:

### Section 1 — Steps

```text
[shoe icon]
8,426
STEPS
```

### Section 2 — Heart rate

```text
[heart icon] 72
             BPM
```

### Section 3 — Calories

```text
[flame icon] 560
             KCAL
```

Use thin separators.

Suggested value hierarchy:

```text
numeric value > icon > label
```

Do not use large circular progress rings around these values.

The side panel should visually support the central time rather than create competing focal points.

---

# 9. Right Information Panel

Suggested bounds:

```text
x ≈ 258..340
y ≈ 102..280
```

Contents:

### Section 1 — Battery

```text
[battery icon]
82%
POWER
```

or label:

```text
BATTERY
```

If the current implementation already uses `POWER`, it may be retained for consistency.

### Section 2 — Sunrise / Sunset

Single smart module:

```text
[sun icon]
18:02
SUNSET
```

or:

```text
[sunrise icon]
05:46
SUNRISE
```

### Section 3 — Weather

```text
[weather icon] 29°C
CLOUDY
```

Weather should remain tertiary and compact.

---

# 10. Smart Sunrise / Sunset Behaviour

Keep the behavior previously defined for the project.

Only **one solar event module** is displayed at a time.

## Rule

### Before today's sunrise

Display:

```text
SUNRISE
today's sunrise time
```

### After sunrise but before sunset

Display:

```text
SUNSET
today's sunset time
```

### After today's sunset

Display:

```text
SUNRISE
next sunrise time
```

Conceptual logic:

```python
if now < sunrise_today:
    event = SUNRISE_TODAY
elif now < sunset_today:
    event = SUNSET_TODAY
else:
    event = SUNRISE_NEXT
```

If the legacy watchface format cannot implement every transition perfectly, preserve the existing V5 mechanism and document the limitation rather than introducing an unsafe format change.

---

# 11. Date

Top-right area.

Suggested bounds:

```text
x ≈ 260..335
y ≈ 60..105
```

Example:

```text
FRI
12 SEP
```

Recommended styling:

- day in Tel-U red
- date in white or light gray
- bold
- compact
- left aligned

Do not use the previous long single-line date if it reduces balance.

The date must support all weekday and month combinations without clipping.

---

# 12. Tel-U Identity

The design must still be immediately recognizable as Telkom University themed, but branding should become more integrated into the sporty UI.

## Recommended elements

### Top

Simplified Tel-U emblem.

### Upper left

Small motto:

```text
HARMONY
EXCELLENCE
INTEGRITY
```

Color:

```text
#959597
```

Use wide tracking.

### Bottom

Dark campus silhouette inspired by the existing V5 artwork.

Recommended opacity / intensity:

```text
15–35% perceived brightness
```

It is decorative only.

It must never compete with the time.

### Bottom rim

Optional:

```text
TELKOM UNIVERSITY
```

Small tracked uppercase.

---

# 13. Campus Illustration

Reuse or adapt the current campus artwork from V5.

Change its role from a prominent graphic to a **low-contrast structural silhouette**.

Approximate bounds:

```text
x ≈ 55..305
y ≈ 275..325
```

Colors:

```text
dark gray
mid gray
near-black
```

The campus should appear almost like a watermark.

No bright white areas.

---

# 14. Sporty Perimeter

Use segmented accents around the outer ring.

Recommended segments:

- red at upper-left
- red at upper-right
- red at lower-left
- red at lower-right
- dark-gray segments between them

Do not create a full bright ring.

The red perimeter should visually echo:

- T-Rex ruggedness
- athletic UI
- Tel-U brand color

Keep the center visually calmer.

---

# 15. Background Texture

Base:

```text
#000000
```

Optional subtle texture:

- dark dotted pattern
- very dark red gradient
- faint diagonal mesh
- extremely faint Tel-U geometry

Maximum visual intensity should remain low.

The texture should almost disappear on the physical AMOLED display.

Avoid:

- bright gradients
- large red fills
- gray full-screen background
- decorative detail behind the digits

---

# 16. Icons

Recommended icon set:

- shoe → steps
- heart → BPM
- flame → kcal
- battery → power
- sunrise/sunset
- weather

Use the same Material Design Icons assets already used by the project where possible.

Icon colors:

```text
Primary metric icon      = Tel-U red
Battery outline          = white or red
Weather cloud            = white
Weather sun              = yellow only if already supported
Solar event icon         = Tel-U red
```

Avoid introducing multiple unrelated icon styles.

---

# 17. Information Priority

Use this size hierarchy.

| Level | Element | Relative importance |
|---|---|---:|
| 1 | Hour | 100% |
| 1 | Minute | 95–100% |
| 2 | Date | 35% |
| 2 | AM/PM | 25% |
| 3 | Steps / BPM / kcal / battery values | 25–35% |
| 3 | Solar time | 25–30% |
| 4 | Labels | 12–18% |
| 5 | Motto / bottom branding | 8–15% |
| 5 | Campus artwork | decorative |

If any secondary element forces the time to shrink, **shrink or remove the secondary element instead**.

---

# 18. Dynamic Data Requirements

V6 should display:

```text
Hour
Minute
AM/PM where available
Weekday
Date
Month
Steps
Heart rate
Calories
Battery
Temperature
Weather condition / icon
Sunrise or sunset time
Sunrise / sunset state
```

Do not add new metrics until the core layout is stable.

---

# 19. Long / Short Value Testing

The design must be tested with representative values.

## Steps

```text
0
7
99
999
8,426
9,999
10,000
```

## BPM

```text
0
72
99
120
220
```

## Calories

```text
0
9
99
560
999
1000
```

## Battery

```text
0%
1%
9%
82%
99%
100%
```

## Temperature

At minimum:

```text
-5°C
0°C
9°C
29°C
39°C
```

If negative temperature cannot be represented safely in the existing format, document it.

---

# 20. Time Stress Tests

Render at least:

```text
00:00
01:01
08:08
10:28
11:11
12:59
18:48
20:00
23:59
```

Important edge cases:

- `11` is visually narrow
- `00` is visually wide
- `28` uses different internal negative space
- hour and minute must remain optically centered

No visible horizontal jumping should occur between digit combinations.

---

# 21. Always-On Display

The V5 repository currently supports a full always-on representation.

For V6:

### Preferred

Keep the same major composition so the user's spatial memory remains intact.

At minimum retain:

```text
HH
MM
date
battery
```

### Ideal

Retain all V6 information, matching normal mode.

However, if battery consumption becomes excessive, the implementation may reduce:

- decorative perimeter
- weather icon
- campus illustration
- motto
- side separators

Do **not** reduce time visibility.

AOD hour and minute should remain:

```text
hour   = white or safe reduced white
minute = light gray
```

---

# 22. Implementation Strategy

Do **not** rewrite the project from scratch.

Use current V5 as the technical baseline.

Existing repository components already include:

```text
tools/gen_telu.py
tools/check_round.py
tools/check_layout.py
tools/pack_watchface.py
tools/verify_bin.py
tools/render_mockup.py
preview.html
```

The existing project already targets the T-Rex Pro 360 × 360 format and includes validation for circular bounds and layout collisions.

## Recommended development approach

Create V6 independently before replacing V5.

Suggested structure:

```text
v6/
design/
    v6-concept-gray-minute.png
docs/
    v6-design-spec.md
out/
    telu_university_v6.bin
```

If practical, preserve V5 artifacts so visual and device regressions can be compared.

---

# 23. Generator Changes

Prefer making the new UI declarative inside the existing asset-generation pipeline.

Potential tasks:

```text
1. Add V6 layout constants.
2. Generate giant hour sprites.
3. Generate giant light-gray minute sprites.
4. Generate left/right sport panels.
5. Reuse existing icons where possible.
6. Reuse the campus silhouette but reduce brightness.
7. Add date block.
8. Reposition weather.
9. Reposition solar event.
10. Rebuild and run all validators.
```

Avoid hand-editing final `.bin` assets unless necessary.

The Python generator should remain the source of truth.

---

# 24. Validation Requirements

Run the existing build and tests:

```powershell
python tools/build_all.py
python -m unittest discover -s tools -p "test_*.py"
```

V6 must pass:

- round-screen bounds
- no icon/text collision
- digit bounds
- date bounds
- largest supported values
- sprite validation
- `.bin` pack verification
- preview render
- AOD render
- physical-device test

Do not consider preview equivalence alone sufficient.

The final acceptance step is installation on the actual Amazfit T-Rex Pro.

---

# 25. Required Preview Scenarios

Generate previews for at least:

### A. Normal daytime

```text
10:28 AM
Fri, 12 Sep
8,426 steps
72 BPM
560 kcal
82% battery
29°C
18:02 sunset
```

### B. Before sunrise

```text
05:20 AM
SUNRISE 05:46
```

### C. After sunset

```text
20:30
next SUNRISE
```

### D. Maximum-width data

```text
23:59
10,000 steps
220 BPM
1000 kcal
100% battery
```

### E. Minimum-width data

```text
01:01
0 steps
0 BPM
0 kcal
1% battery
```

### F. Always-on

Render the same time and compare alignment with normal mode.

---

# 26. Visual Acceptance Criteria

The V6 design is accepted only if:

- the time can be recognized substantially faster than in V5
- `HH` and `MM` remain legible from farther away
- hour stays white
- minute stays light gray
- red is used primarily as an accent
- no metric panel visually competes with the time
- the watchface still feels recognizably Telkom University
- the design feels sporty rather than academic/formal
- the bottom campus silhouette remains subtle
- all elements remain inside the circular safe region
- no dynamic value causes overlap
- actual watch rendering is close to the preview

---

# 27. Non-Negotiable Design Decisions

These must not be changed without explicit approval:

```text
1. Hour and minute are the visual hero.
2. Hour is white.
3. Minute is light gray.
4. Minute must NOT be red.
5. Black AMOLED background.
6. Tel-U red is retained as an accent.
7. Use stacked HH / MM.
8. Keep steps, BPM, kcal, battery, weather, and sunrise/sunset.
9. Sunrise and sunset share one smart dynamic slot.
10. Retain Tel-U identity but branding must not dominate the time.
11. Maintain 360 × 360 T-Rex Pro compatibility.
12. Preserve the existing validated build/pack workflow whenever possible.
```

---

# 28. Things the Implementation Agent May Adjust

The implementation agent is allowed to fine-tune:

```text
± several pixels in element positions
font raster size
kerning
line thickness
panel curvature
icon size
campus brightness
separator length
perimeter segment length
date spacing
logo size
```

Only when needed for:

- optical centering
- collision prevention
- round-screen safety
- better physical readability

Do not make major composition changes merely because they are easier to code.

Match the approved mockup first.

---

# 29. Suggested V6 Naming

Internal:

```text
TELU Watchface V6 Performance
```

Possible user-facing name:

```text
TEL-U PERFORMANCE
```

or simply retain:

```text
TELKOM UNIVERSITY
```

Recommended output:

```text
out/telu_university_v6.bin
```

---

# 30. Final Instruction to the Coding Agent

Implement the attached approved V6 mockup as faithfully as possible using the existing repository as the technical baseline.

**Do not redesign it again.**

Priority order:

```text
1. Physical readability of HH/MM
2. Correct dynamic data
3. Round-screen safety
4. Device compatibility
5. Visual fidelity
6. Decorative details
```

If technical limitations require a compromise, preserve the giant time first and simplify decorative elements before reducing the size of the time.

The approved central time treatment is:

```text
HH = WHITE
MM = LIGHT GRAY
```

with Tel-U red reserved primarily for accents, icons, date emphasis, and sporty perimeter elements.
