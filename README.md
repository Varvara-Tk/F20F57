# Explore Linz

> The city begins as a secret. Every step makes it yours.

Explore Linz is a map-based walking experience in which the city is hidden
behind a grey veil. The user starts with a tiny island of visible streets—just
100 metres around their position. As they move, the map opens around them,
leaving a bright trail through the places they have discovered.

This repository contains a polished, self-contained demonstration of that
idea. Choose a destination and a simulated visitor walks along mapped
pedestrian roads and walkways. The first journey begins at Hauptplatz; every
later journey begins exactly where the user marker currently stands. The user marker moves, the veil recedes,
the travelled path grows, and the percentage of Linz explored ticks upward in
real time.

## The experience

The first screen makes the game rule visible immediately:

- **100 m at the start** — only the area surrounding the user is visible.
- **100 m while walking** — each new position reveals another circle of city.
- **One shared goal** — uncover 100% of Linz.

The interface deliberately keeps the world mysterious. Grey areas are not
disabled map tiles; they are unexplored territory. Under the veil, the
OpenStreetMap basemap is already present and waiting to be uncovered.

Amber points above the veil are upcoming event-location hints sourced from a
small snapshot of the open Boudicca Events Search API. They give the player
reasons to explore without revealing the streets beneath the fog. Past events
are filtered out in the browser. The snapshot keeps the static demo reliable
because the public Search service does not currently advertise browser CORS
access.

When the user comes within 100 metres of one of these hints, an event card
appears with the event title and venue. Each discovery is shown once per page
session and can be dismissed without interrupting the walk. Event points in an
already revealed area can also be clicked to reopen their information. Where
the source provides a URL, the card links to the original event page; points
outside the revealed area remain anonymous hints.

### Demo journeys

The journeys are artificial location simulations and require no GPS permission.
The current choices are Mariendom, Landestheater Linz, and Linz Hauptbahnhof.
Initial route geometry is bundled with the demo. When a new destination is
chosen, the app asks the open Valhalla pedestrian router for a street-following
route from the marker's current coordinates, so the user never jumps back to
Hauptplatz.

```text
Hauptplatz
    ↓
Hofgasse and pedestrian walkways
    ↓
Herrenstraße
    ↓
Domplatz
    ↓
Mariendom
```

The route uses 61 coordinates from an open pedestrian routing result. It is
approximately 855 metres long and includes the small turns and bends needed to
follow the mapped street network. For presentation speed, the complete walk is
compressed into roughly sixteen seconds.

During the simulation:

1. The camera stays centred on the moving user.
2. A bright user marker advances between consecutive route coordinates.
3. A lime trail grows behind the marker.
4. A softly feathered 100 m circle clears the grey mask.
5. Distance, explored area, and percentage update continuously.
6. Mariendom remains visible as the destination.

The demo can be paused or continued. After reaching a destination, the user can
choose another journey from their current position or finish the trip. The
finish screen summarizes distance, area, exploration percentage, destinations,
events, and named streets. Short place and street histories come from Linz
Tourism, the destination operators, and the City of Linz street-name dataset.

## How the reveal works

The hidden-city effect is made from a semi-transparent canvas laid over the
map. Each accepted user position cuts a circular opening into that canvas.

The edge of every opening uses a radial gradient rather than a hard boundary.
The mask is refreshed up to 20 times per second, which makes the grey veil melt
away smoothly as the marker travels.

Exploration progress is calculated independently from the visual mask:

- Linz is represented by a lightweight city-boundary polygon.
- The polygon is sampled as a grid of 100 m cells.
- A cell becomes explored when its centre falls within a reveal circle.
- Explored percentage is `explored cells ÷ all city cells × 100`.
- Explored area is `explored cells × 0.01 km²`.

This gives the prototype a stable, understandable score without needing a
database or spatial backend.

## Controls

| Control | Behaviour |
| --- | --- |
| **Walk to…** | Starts the artificial journey to the selected destination |
| **Choose destination** | Selects Mariendom, Landestheater, or Hauptbahnhof |
| **Right-click map** | Pins any point inside Linz as a custom walking destination |
| **Pause demo** | Freezes the simulated user at the current position |
| **Continue demo** | Resumes from the paused position |
| **Walk somewhere again** | Opens destination choice after arrival |
| **Finish trip** | Opens the trip summary after completing a route |
| **City overview** | Frames the full Linz game area |
| **Follow me** | Centres the map on the latest user position |
| **+ / −** | Changes map zoom |

## Technology

- **CesiumJS** renders the interactive map, user, destination, boundary, and
  growing trail.
- **OpenStreetMap** supplies the open basemap tiles.
- **Boudicca Events** supplies the Linz event-location hints shown above the
  unexplored map.
- **City of Linz street-name data** supplies historical context for streets
  recorded by the pedestrian router.
- **Linz-only clipping** limits the Cesium globe and basemap requests to the
  configured Linz bounding area.
- **Canvas masking** creates the fog-of-exploration effect.
- **Vanilla HTML, CSS, and JavaScript** keep the demo portable and dependency
  free at build time.

No access token, application server, or database is needed at runtime. An
internet connection is required for CesiumJS, map tiles, and new pedestrian
routes, which are loaded from public services.

## Run the project

Build the distributable page:

```bash
python3 build_cesium_linz.py
```

Start a local server:

```bash
python3 -m http.server 4173 --directory dist
```

Open [http://127.0.0.1:4173/](http://127.0.0.1:4173/) in a browser.

Serving the file through HTTP is important. Opening `dist/index.html` directly
may prevent browser location access and can cause restrictions on remote map
resources.

## Project structure

```text
.
├── src/
│   ├── linz-map.html       # Editable application source
│   └── routes.js           # Embedded pedestrian route geometry
├── dist/
│   ├── index.html          # Generated, ready-to-serve demo
│   └── routes.js           # Generated route data
├── build_cesium_linz.py    # Copies source into dist
└── README.md               # This guide
```

Edit `src/linz-map.html`, then run the build command again. Do not edit the
generated `dist/index.html` directly because the next build replaces it.

## Important implementation constants

The prototype is intentionally concentrated in one source file. Search for
these values when tuning the experience:

| Constant or value | Current purpose |
| --- | --- |
| `CITY` | Simplified boundary used for the exploration goal |
| `START` | Demo starting position at Hauptplatz |
| `DEMO` | Detailed pedestrian route to Mariendom |
| `GRID = 100` | Progress-cell size in metres |
| `100` in `move()` | Reveal radius in metres |
| `duration = 16000` | Complete demo duration in milliseconds |
| `lastRevealAt < 50` | Maximum mask-update frequency |

## Prototype boundaries

This is a presentation-ready proof of concept, not yet a production tracker.

- Progress lasts for the current page session and is not persisted.
- The city outline is simplified rather than an official municipal boundary.
- A newly selected destination is routed from the marker's current location;
  this requires the public Valhalla service to be available.
- External CDN and OpenStreetMap availability affect the basemap.

A production version would use the official Linz boundary, persistent user
progress, GPS accuracy filtering, route-aware map matching, offline handling,
and a privacy-first consent flow.

## The idea in one sentence

Explore Linz turns an ordinary city map into a personal record of movement:
**you do not merely view the city—you earn the right to see it, one walk at a
time.**
