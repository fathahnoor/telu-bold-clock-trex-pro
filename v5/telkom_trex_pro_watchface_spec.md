# Telkom University Watch Face — Amazfit T-Rex Pro
## Visual & Functional Specification for Implementation Harness

**Status:** implementation specification based on the approved visual reference  
**Target device:** Amazfit T-Rex Pro  
**Canvas:** 360 × 360 px, circular AMOLED display  
**Primary language:** English  
**Primary theme:** Telkom University — black / white / red / dark gray  
**Reference image:** provide the approved PNG together with this Markdown to the harness.

---

## 1. Goal

Recreate the supplied Telkom University watch face as closely as possible while keeping the interface readable on the actual 360 × 360 px Amazfit T-Rex Pro display.

The design is intentionally:

- dark and high-contrast for AMOLED,
- symmetrical,
- dominated by the central time,
- strongly branded with Telkom University,
- information-dense without looking like a generic dashboard,
- built around curved red/gray elements inspired by the Telkom University visual identity.

The implementation should prioritize **visual similarity to the supplied reference PNG** over inventing new styling.

---

## 2. Device Constraints

Use a **360 × 360 px circular canvas**.

Recommended rules:

- Design origin: `(0,0)` at the top-left.
- Center point: `(180,180)`.
- Treat the outermost ~8–12 px as a visual safety zone.
- Avoid important text touching the circular crop.
- Use anti-aliased raster/vector assets where supported.
- Keep the background almost pure black to benefit the AMOLED panel.
- Do not place a rectangular panel behind the layout.
- All elements must visually belong to the circular watch face.

### Safe Areas

Suggested working zones:

| Zone | Approx. area |
|---|---|
| Outer decorative ring | radius 168–178 px |
| Main content safe area | radius ≤ 165 px |
| Critical text/data area | radius ≤ 150 px |
| Bottom campus silhouette | y ≈ 270–325 px |
| Bottom brand text | y ≈ 323–342 px |

Coordinates in this document are **implementation guides**, not a substitute for matching the supplied visual reference.

---

## 3. Visual Identity

### 3.1 Background

Primary background:

```text
#000000
```

Subtle charcoal areas may use:

```text
#111111
#1A1A1A
#242424
#323232
```

Avoid bright gray backgrounds.

---

## 3.2 Main Accent Colors

Suggested palette sampled/approximated from the approved concept:

```text
Telkom-style red / main accent:   #FF2029
Bright red highlight:             #FF3038
Deep red:                         #C90F18

Primary white:                    #FFFFFF
Secondary white:                  #F1F1F1
Medium gray:                      #8B8B8B
Dark gray:                        #353535

Weather yellow:                   #FFD21A
Heart accent:                     #FF0057
```

The design should remain visually dominated by:

1. black,
2. white,
3. Telkom red,
4. gray.

Weather yellow and heart magenta are secondary functional accents only.

---

## 3.3 Telkom University Logo

At the top center:

- use the **official Telkom University logo/wordmark asset** if available,
- do **not** redraw the "Telkom University" wordmark using a random system font if an official raster/vector asset exists,
- retain the red upper mark and metallic/dark-gray "U" appearance from the reference.

Approximate center:

```text
x = 180
y = 50
```

Approximate region:

```text
x = 135–225
y = 12–100
```

The logo is a major visual anchor and must not be replaced by plain text.

---

## 3.4 Typography

The reference uses a clean, geometric, slightly condensed sans-serif appearance.

Recommended priority:

1. official Telkom-related font if legally/technically available,
2. a geometric condensed sans,
3. a neutral fallback such as Roboto Condensed / Inter / similar.

Typography hierarchy:

| Element | Weight | Style |
|---|---:|---|
| Main hour/minute | Extra Bold / Black | condensed |
| Date | Bold | clean sans |
| Metric values | Bold | condensed or geometric |
| Labels | Regular/Medium | uppercase with tracking |
| Motto | Light/Regular | uppercase with wide tracking |
| Bottom "TELKOM UNIVERSITY" | Medium | uppercase with wide tracking |

### Important

Small labels should use increased letter spacing.

Examples:

```text
STEPS
BPM
POWER
KCAL
SUNRISE
SUNSET
CLOUDY
```

---

# 4. Layout Overview

The design is vertically divided into five layers:

```text
┌──────────────────────────────────────┐
│ TOP BRAND / MOTTO / WEATHER          │
│                                      │
│              DATE                    │
│                                      │
│ STEPS       LARGE TIME        BPM    │
│                  AM/PM               │
│                                      │
│ POWER       SOLAR EVENT       KCAL   │
│                                      │
│       TEL-U CAMPUS SILHOUETTE        │
│          TELKOM UNIVERSITY           │
└──────────────────────────────────────┘
```

The layout should look **radial and symmetrical**, not grid-like.

---

# 5. Component Specification

## 5.1 Top Left — Telkom University Values

Content:

```text
HARMONY
EXCELLENCE
INTEGRITY
```

Style:

- three stacked lines,
- uppercase,
- light gray / white,
- generous tracking,
- small red horizontal underline,
- no enclosing box.

Approximate anchor:

```text
x ≈ 65
y ≈ 73
```

This is a static branding element.

---

## 5.2 Top Center — Telkom University Logo

Use logo asset described above.

It should be visually centered on the vertical axis of the watch.

Do not let the motto or weather panel compete with it.

---

## 5.3 Top Right — Weather

Display:

```text
[weather icon] 29°C
CLOUDY
```

Data:

- current weather icon,
- current temperature,
- short weather condition.

Preferred formatting:

```text
29°C
CLOUDY
```

Temperature should be more prominent than the condition label.

### Weather condition text

Use uppercase, preferably a short label:

```text
SUNNY
CLOUDY
RAIN
STORM
FOG
SNOW
WINDY
```

If the source condition is longer, map it to a shorter display label rather than shrinking the font excessively.

### Icon

Use a compact icon visually consistent with the reference.

Weather colors may differ by condition, but avoid making the entire watch face colorful.

Approximate anchor:

```text
x ≈ 285
y ≈ 74
```

---

# 6. Date

Centered above the main time.

Reference format:

```text
Friday, 12 Sep
```

Required format:

```text
dddd, DD MMM
```

Examples:

```text
Monday, 01 Jan
Friday, 12 Sep
Sunday, 30 Nov
```

Do not display the year.

Approximate center:

```text
x = 180
y ≈ 120
```

Use white bold text.

---

# 7. Main Time

This is the strongest visual element.

Example:

```text
10:28
AM
```

## 7.1 Time Format

Use **12-hour time** with separate AM/PM indicator.

Hour and minute must be visually differentiated:

```text
10     → white
28     → red
:      → red
```

Recommended color rule:

```text
Hour    = #FFFFFF
Colon   = Telkom red
Minute  = Telkom red
AM/PM   = gray/white
```

The colon should visually belong to the minute/red side.

### Examples

```text
07:05 AM
10:28 AM
12:45 PM
09:13 PM
```

Leading zero behavior may follow the reference implementation capability, but the preferred appearance is:

```text
07:05
```

rather than:

```text
7:05
```

if enough width is available.

---

## 7.2 AM / PM

Centered directly below the main time.

Example:

```text
AM
```

Add subtle horizontal divider lines to the left and right, matching the reference.

Approximate center:

```text
x = 180
y ≈ 205
```

---

# 8. Steps — Left Middle Circular Gauge

Display:

```text
[shoe icon]
8,426
STEPS
```

Approximate center:

```text
x ≈ 60
y ≈ 155
```

## Gauge

Use:

- dark gray base ring,
- Telkom-red progress arc,
- circular/partial circular geometry,
- red progress should visually move clockwise.

The gauge should not dominate the time.

### Data formatting

Examples:

```text
826
8,426
12,580
```

Use a thousands separator.

If a step goal is available:

```text
progress = steps / step_goal
```

Clamp:

```text
0.0 ≤ progress ≤ 1.0
```

If the platform has no step-goal value, use a configured design goal such as 10,000 steps **only if explicitly needed by the implementation**.

---

# 9. Heart Rate — Right Middle Circular Gauge

Display:

```text
[heart icon]
72
BPM
```

Approximate center:

```text
x ≈ 300
y ≈ 155
```

Heart icon:

- bright red / magenta,
- centered.

BPM value:

- white,
- bold.

If live/current BPM is unavailable, use the most recent valid heart-rate value supported by the watch face API.

### Invalid data fallback

Prefer:

```text
--
BPM
```

Do not show a fake numeric heart rate.

---

# 10. Battery / Power — Lower Left

Display:

```text
[battery icon]
82%
POWER
```

Approximate center:

```text
x ≈ 82
y ≈ 238
```

Circular gauge:

- dark gray base,
- red progress arc,
- approximately proportional to battery percentage.

Examples:

```text
100%
82%
34%
9%
```

Optional low-battery behavior:

```text
<= 15% → stronger red emphasis
```

Do not introduce green; maintain the Telkom theme.

---

# 11. Calories — Lower Right

Display:

```text
[flame icon]
560
KCAL
```

Approximate center:

```text
x ≈ 278
y ≈ 238
```

The kcal module is visually paired with POWER.

Use:

- red flame icon,
- white numeric value,
- uppercase gray `KCAL`,
- same circular gauge language as the other metric modules.

If a calorie goal is available:

```text
progress = kcal / kcal_goal
```

Otherwise, a decorative/static partial ring is acceptable if the platform cannot bind a calorie goal.

---

# 12. Dynamic Sunrise / Sunset Module

## 12.1 Critical Requirement

**SUNRISE and SUNSET must NOT appear simultaneously.**

There is only **one centered solar-event module**.

Approximate center:

```text
x = 180
y ≈ 239
```

It occupies the bottom-center position between POWER and KCAL.

---

## 12.2 Runtime Logic

Use local watch/device time.

Pseudocode:

```pseudo
now = current local datetime
sunrise = today's sunrise
sunset = today's sunset

if now < sunrise:
    event_type = "SUNRISE"
    event_time = sunrise
    icon = sunrise_icon

else if now < sunset:
    event_type = "SUNSET"
    event_time = sunset
    icon = sunset_icon

else:
    event_type = "SUNRISE"
    event_time = tomorrow's sunrise
    icon = sunrise_icon
```

Equivalent interpretation:

```text
Before today's sunrise:
    show today's SUNRISE

After sunrise but before sunset:
    show today's SUNSET

After sunset:
    show next SUNRISE
```

At the event boundary:

```text
now >= sunrise → switch to SUNSET
now >= sunset  → switch to next SUNRISE
```

---

## 12.3 Solar Event Appearance

### Sunrise state

Example:

```text
[sunrise icon]
05:47
SUNRISE
```

### Sunset state

Example:

```text
[sunset icon]
18:02
SUNSET
```

Use red iconography to stay within the Telkom theme.

Time should be white.

Label should be gray/light gray with letter spacing.

### Very Important

Do **not** keep two permanent blocks like:

```text
05:47 SUNRISE | 18:02 SUNSET
```

That earlier layout has been rejected.

The approved behavior is one dynamic event only.

---

# 13. Bottom Campus Silhouette

Use a dark grayscale silhouette inspired by the supplied image.

Visual content:

- Telkom University campus/building silhouette,
- centered,
- dark gray,
- partially blended into the black background,
- tree/foliage silhouettes may be included.

Approximate region:

```text
y ≈ 267–322
```

The building should remain subordinate to the data.

It must not reduce the readability of the solar-event module above it.

---

# 14. Bottom Text

Display:

```text
TELKOM UNIVERSITY
```

Style:

- curved or visually following the lower arc,
- uppercase,
- wide letter spacing,
- white/light gray,
- small red dash accents on left and right.

Approximate center:

```text
x = 180
y ≈ 334
```

This is decorative branding and should never collide with the display edge.

---

# 15. Outer Decorative Frame

The perimeter contains a set of red and dark-gray curved accent pieces inspired by Telkom University's shape language.

Requirements:

- preserve the circular feel,
- use mirrored left/right curves,
- use short red accents near the top,
- use larger red/gray vertical curves on the lower sides,
- do not turn these into functional gauges unless explicitly desired.

These accents should frame the interface without reducing data legibility.

---

# 16. Circular Metric Gauge Style

STEPS, BPM, POWER, and KCAL share a common visual grammar.

Base:

```text
dark circular ring
```

Progress:

```text
thick red arc
```

Interior:

```text
black
```

Each module contains:

```text
icon
value
label
```

Suggested priority:

```text
value > icon > label
```

Avoid fully enclosing the module with a bright red ring.

Partial rings are preferred.

---

# 17. Data Binding Model

Suggested abstract data model for the harness:

```json
{
  "time": {
    "hour12": "10",
    "minute": "28",
    "ampm": "AM"
  },
  "date": {
    "weekday": "Friday",
    "day": "12",
    "monthShort": "Sep"
  },
  "activity": {
    "steps": 8426,
    "stepGoal": 10000,
    "caloriesKcal": 560,
    "calorieGoal": 800
  },
  "health": {
    "heartRateBpm": 72
  },
  "battery": {
    "percent": 82
  },
  "weather": {
    "temperatureC": 29,
    "condition": "CLOUDY",
    "icon": "partly_cloudy"
  },
  "solar": {
    "sunriseToday": "05:47",
    "sunsetToday": "18:02",
    "sunriseTomorrow": "05:47"
  }
}
```

This structure is conceptual. Map it to the exact data fields supported by the chosen T-Rex Pro watch-face toolchain.

---

# 18. Reference State A — Before Sunrise

Example current time:

```text
04:35 AM
```

Data:

```text
Date        : Friday, 12 Sep
Steps       : 220
Heart Rate  : 64 BPM
Battery     : 94%
Calories    : 35 KCAL
Weather     : 21°C CLEAR
Sunrise     : 05:47
Sunset      : 18:02
```

The solar module MUST display:

```text
05:47
SUNRISE
```

Conceptual layout:

```text
 HARMONY                ☀ 21°C
 EXCELLENCE              CLEAR
 INTEGRITY

             Friday, 12 Sep

 STEPS        04:35        BPM
  220           AM          64

 POWER       [SUNRISE]     KCAL
  94%          05:47         35
              SUNRISE

        [TEL-U CAMPUS]
        TELKOM UNIVERSITY
```

---

# 19. Reference State B — Daytime / After Sunrise

Example current time:

```text
10:28 AM
```

Data:

```text
Date        : Friday, 12 Sep
Steps       : 8,426
Heart Rate  : 72 BPM
Battery     : 82%
Calories    : 560 KCAL
Weather     : 29°C CLOUDY
Sunrise     : 05:47
Sunset      : 18:02
```

Because sunrise has already passed but sunset has not:

```text
18:02
SUNSET
```

This is the state represented by the approved visual reference.

Conceptual layout:

```text
 HARMONY               ⛅ 29°C
 EXCELLENCE              CLOUDY
 INTEGRITY

             Friday, 12 Sep

 STEPS        10:28        BPM
 8,426           AM          72

 POWER        [SUNSET]      KCAL
  82%           18:02        560
               SUNSET

        [TEL-U CAMPUS]
        TELKOM UNIVERSITY
```

---

# 20. Reference State C — After Sunset

Example current time:

```text
09:13 PM
```

Data:

```text
Date        : Friday, 12 Sep
Steps       : 11,734
Heart Rate  : 78 BPM
Battery     : 61%
Calories    : 790 KCAL
Weather     : 24°C CLOUDY
Today's sunset       : 18:02
Tomorrow's sunrise   : 05:47
```

Because today's sunset has passed, display the next relevant solar event:

```text
05:47
SUNRISE
```

The solar module is therefore conceptually the **next event**, not a fixed daily pair.

---

# 21. Reference State D — Low Battery / Missing Heart Rate

Example:

```text
06:20 PM
```

Data:

```text
Steps       : 13,405
Heart Rate  : unavailable
Battery     : 9%
Calories    : 905 KCAL
Weather     : 25°C RAIN
Sunset      : 18:02
Next sunrise: 05:47
```

Expected:

```text
Heart Rate:
--
BPM
```

Battery:

```text
9%
POWER
```

Since sunset has passed:

```text
05:47
SUNRISE
```

Do not invent unavailable health data.

---

# 22. Formatting Rules

## Steps

```text
8426 → 8,426
```

## Temperature

```text
29 → 29°C
```

No space before `°C`.

## Battery

```text
82 → 82%
```

## Calories

```text
560 → 560
label → KCAL
```

## Heart Rate

```text
72
BPM
```

## Solar time

Prefer 24-hour notation:

```text
05:47
18:02
```

even though the main clock is 12-hour with AM/PM.

This matches the approved visual.

---

# 23. Visual Priority

When space or platform constraints force a compromise, preserve this priority order:

1. Main time
2. Date
3. Telkom University logo / identity
4. Steps
5. Heart rate
6. Battery
7. Calories
8. Dynamic sunrise/sunset
9. Weather
10. Decorative motto / campus / outer accents

Do not shrink the main time merely to preserve a decorative element.

---

# 24. Scaling Strategy

The supplied reference image is larger than the physical 360 × 360 display.

Do not simply resize all typography uniformly.

Instead:

1. reproduce the composition,
2. place elements using the 360 × 360 coordinate system,
3. adjust font sizes until readable on-device,
4. keep the time dominant,
5. simplify micro-details that disappear at 360 × 360.

A detail that looks excellent at 1200 px but becomes visual noise at 360 px should be simplified.

---

# 25. Suggested 360 × 360 Anchor Map

Approximate component centers:

```text
                 x
        0       180       360
        ┌──────────────────┐
 y  0   │                  │
        │      LOGO        │  ~50
        │ VALUES     WX    │  ~75
        │      DATE        │  ~120
        │                  │
        │STEPS  TIME   BPM │  ~155–180
        │       AM/PM      │  ~205
        │                  │
        │POWER  SOLAR KCAL │  ~235
        │                  │
        │ CAMPUS SILHOUETTE│  ~290
        │ TELKOM UNIVERSITY│  ~334
 y360   └──────────────────┘
```

More explicit anchors:

```text
Logo             ≈ (180, 50)
Values            ≈ (67, 75)
Weather           ≈ (287, 75)
Date              ≈ (180, 120)

Steps             ≈ (60, 155)
Main time         ≈ (180, 166)
Heart rate        ≈ (300, 155)
AM/PM             ≈ (180, 205)

Power             ≈ (82, 238)
Solar event       ≈ (180, 238)
Kcal              ≈ (278, 238)

Campus            ≈ (180, 292)
Bottom branding   ≈ (180, 334)
```

These are starting points only.

Match the reference image visually after rendering.

---

# 26. State Transition Rules

The watch face should update relevant values without visible layout jumps.

### Every minute

Update:

```text
hour
minute
AM/PM
solar-event selection when crossing sunrise/sunset
```

### At date change

Update:

```text
weekday
day
month
sunrise/sunset data
```

### When activity data changes

Update:

```text
steps
step progress
calories
calorie progress
```

### When health data changes

Update:

```text
heart rate
```

### When battery changes

Update:

```text
battery percentage
battery gauge
```

### When weather refreshes

Update:

```text
weather icon
temperature
condition
```

---

# 27. Solar Logic Test Cases

Harness should explicitly test these cases.

Assume:

```text
sunrise = 05:47
sunset  = 18:02
```

| Current time | Display |
|---|---|
| 00:10 | `05:47 SUNRISE` |
| 05:46 | `05:47 SUNRISE` |
| 05:47 | `18:02 SUNSET` |
| 10:28 | `18:02 SUNSET` |
| 18:01 | `18:02 SUNSET` |
| 18:02 | `05:47 SUNRISE` of next day |
| 23:59 | next `SUNRISE` |

The design must never display both solar events at once.

---

# 28. Missing Solar Data

If sunrise/sunset data is temporarily unavailable, preferred fallback:

```text
--:--
SUN EVENT
```

or hide the module cleanly if the platform supports conditional visibility.

Do not fabricate sunrise or sunset times.

If only today's sunrise and sunset are available and the watch face cannot access tomorrow's sunrise after sunset, acceptable fallback priority:

```text
1. use platform-provided next sunrise if available
2. use a supported "next solar event" field
3. otherwise show SUNRISE with unavailable time "--:--"
```

Do not show the already-passed sunset as if it were upcoming.

---

# 29. Weather Failure State

If weather is unavailable:

Preferred:

```text
[neutral weather icon]
--°
WEATHER
```

Alternative:

hide the weather content but retain visual balance.

Never display fake weather data.

---

# 30. Always-On Display (Optional)

The T-Rex Pro supports Always-On Display.

If an AOD variant is implemented, simplify aggressively.

Recommended AOD:

```text
10:28
FRI 12
82%
```

Optional small Telkom symbol.

Avoid:

- weather graphics,
- campus silhouette,
- four full gauges,
- bright large red areas.

The full active watch face remains the primary design.

---

# 31. Implementation Guidance

Depending on the selected T-Rex Pro watch-face toolchain, runtime conditional logic may be supported differently.

Possible implementation strategies for the solar event:

### Strategy A — Native conditional visibility

Create:

```text
sunrise_group
sunset_group
```

Then bind visibility to time ranges.

Only one group may be visible at any moment.

### Strategy B — Computed "next solar event"

At runtime compute:

```text
nextSolarType
nextSolarTime
```

Bind one icon, one time text, and one label.

This is the preferred logical model.

### Strategy C — Toolchain-limited fallback

If arbitrary runtime code is not available:

- use the watch-face format's built-in sunrise/sunset expressions if available,
- or generate mutually exclusive layers based on supported time-range conditions.

Do not revert to displaying both events merely because conditional logic is inconvenient.

---

# 32. Asset List

The harness should prepare or locate these assets:

```text
telkom_university_logo
weather_icons
shoe_icon
heart_icon
battery_icon
flame_icon
sunrise_icon
sunset_icon
campus_silhouette
outer_red_gray_frame_elements
```

Recommended:

- PNG with transparency or vector-compatible asset,
- high-contrast,
- clean edges,
- minimal tiny detail.

---

# 33. Acceptance Checklist

The implementation is accepted when all of the following are true:

- [ ] Canvas is designed for 360 × 360 circular AMOLED.
- [ ] Main background is black.
- [ ] Telkom University visual identity is immediately recognizable.
- [ ] Official/approved Telkom University logo asset is used where possible.
- [ ] Date is centered above the main time.
- [ ] Main time uses white hour + red colon/minute.
- [ ] AM/PM appears below the main time.
- [ ] Steps appear on the left.
- [ ] Heart rate appears on the right.
- [ ] Battery/POWER appears lower-left.
- [ ] KCAL appears lower-right.
- [ ] Weather + temperature appear upper-right.
- [ ] `HARMONY / EXCELLENCE / INTEGRITY` appears upper-left.
- [ ] Campus silhouette appears at the bottom.
- [ ] Bottom text reads `TELKOM UNIVERSITY`.
- [ ] Sunrise and sunset are combined into ONE center-bottom module.
- [ ] Before sunrise → show SUNRISE.
- [ ] After sunrise → show SUNSET.
- [ ] After sunset → show the next SUNRISE.
- [ ] Sunrise and sunset are never simultaneously visible.
- [ ] Missing sensor data is not fabricated.
- [ ] No critical text is clipped by the circular screen.
- [ ] Final output remains legible at actual 360 × 360 resolution.

---

# 34. Approved Reference State

The approved reference image represents this data state:

```text
Date        : Friday, 12 Sep
Time        : 10:28 AM
Steps       : 8,426
Heart Rate  : 72 BPM
Battery     : 82%
Calories    : 560 KCAL
Weather     : 29°C CLOUDY
Sunrise     : 05:47
Sunset      : 18:02
```

Because the current time is **10:28 AM**, sunrise has already passed and sunset is still upcoming.

Therefore the center-bottom solar module must display:

```text
18:02
SUNSET
```

This behavior is part of the design specification, not merely a visual example.

---

## Final Instruction to the Implementation Harness

Use the supplied reference image as the primary visual target and this Markdown as the behavioral specification.

Do not reinterpret the composition into a generic smartwatch layout.

Preserve:

```text
Telkom University identity
black/red/white palette
radial symmetry
dominant central time
four surrounding metric modules
single dynamic solar-event module
campus silhouette
outer curved Telkom-style accents
```

When a visual conflict occurs, prioritize actual watch readability at **360 × 360** while keeping the result as close as possible to the approved reference image.
