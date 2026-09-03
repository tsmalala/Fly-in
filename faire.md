# Fly-in Drones — Sprint Tasks

## Project Goal

Build an object-oriented Python 3.10+ application that routes multiple drones from a start zone to an end zone while respecting:

* Zone capacities
* Connection capacities
* Movement costs
* Restricted zones
* Blocked zones
* Priority zones
* Simultaneous movements
* Waiting
* Multi-drone conflicts
* Turn minimization

The project must pass `flake8` and `mypy`, a Makefile, documentation, and a visual terminal representation.

---

# Sprint 0 — Project Setup

**Estimated time:** 2–3 hours

**Goal:** Create a clean project foundation before implementing any algorithm.

## Tasks

* [x] Create the Git repository
* [x] Create the Python project structure
* [x] Create a virtual environment
* [x] Create `.gitignore`
* [x] Create `README.md`
* [x] Create `Makefile`
* [x] Create `main.py`
* [x] Create `src/` package
* [x] Configure Python 3.10+
* [x] Install `flake8`
* [x] Install `mypy`
* [x] Verify `python --version`
* [x] Verify `flake8`
* [x] Verify `mypy`
* [x] Add basic `make install`
* [x] Add basic `make run`
* [x] Add basic `make debug`
* [x] Add basic `make clean`
* [x] Add basic `make lint`
* [x] Test the Makefile

## Expected structure

```text
fly-in/
├── main.py
├── Makefile
├── README.md
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── zone.py
│   ├── connection.py
│   ├── drone.py
│   ├── graph.py
│   ├── parser.py
│   ├── pathfinder.py
│   ├── scheduler.py
│   ├── simulation.py
│   └── display.py
└── maps/
```

## Definition of Done

* [x] Project launches
* [x] Makefile works
* [x] `flake8` runs
* [x] `mypy` runs
* [x] No unnecessary dependencies

---

# Sprint 1 — Domain Model

**Estimated time:** 2–3 hours

**Goal:** Create the object-oriented model of the problem.

## Zone

* [x] Create `Zone` class
* [x] Add zone name
* [x] Add coordinates
* [x] Add zone type
* [x] Add color
* [x] Add maximum drone capacity
* [x] Add current occupancy
* [x] Implement capacity checking
* [x] Implement entering a zone
* [x] Implement leaving a zone
* [x] Add type hints
* [x] Add docstrings

## Connection

* [x] Create `Connection` class
* [x] Store both connected zones
* [x] Store maximum link capacity
* [x] Track drones currently using the connection
* [x] Implement capacity checking
* [x] Implement connection traversal
* [x] Add type hints
* [x] Add docstrings

## Drone

* [x] Create `Drone` class
* [x] Add unique drone ID
* [x] Add current zone
* [x] Add current path
* [x] Add path position
* [x] Add drone state
* [x] Define states such as:
  * [ ] `AT_ZONE`
  * [ ] `IN_FLIGHT`
  * [ ] `DELIVERED`
* [x] Add type hints
* [x] Add docstrings

## Graph

* [x] Create `Graph` class
* [x] Store zones
* [x] Store connections
* [x] Build adjacency lists
* [x] Add zones
* [x] Add connections
* [x] Retrieve a zone by name
* [x] Retrieve neighbours
* [ ] Check whether a zone exists
* [ ] Check whether a connection exists

## Definition of Done

* [x] All domain objects exist
* [x] No business logic in `main.py`
* [x] Classes are properly typed
* [x] `mypy` passes

---

# Sprint 2 — Parser

**Estimated time:** 10–12 hours

**Goal:** Parse the complete map format and reject invalid input cleanly.

## Basic parsing

* [x] Parse `nb_drones`
* [x] Parse `start_hub`
* [x] Parse `end_hub`
* [x] Parse regular `hub`
* [x] Parse `connection`
* [x] Ignore comments
* [x] Ignore empty lines if appropriate

## Zone metadata

* [x] Parse `zone=normal`
* [x] Parse `zone=blocked`
* [x] Parse `zone=restricted`
* [x] Parse `zone=priority`
* [x] Parse `color=...`
* [x] Parse `max_drones=...`
* [x] Apply default values
* [x] Support metadata in any order

## Connection metadata

* [x] Parse `max_link_capacity`
* [x] Apply default capacity of 1

## Validation

* [x] Validate positive drone count
* [x] Validate unique zone names
* [x] Validate integer coordinates
* [x] Validate exactly one start zone
* [x] Validate exactly one end zone
* [x] Validate zone types
* [x] Validate positive capacities
* [x] Validate connection endpoints
* [x] Reject duplicate connections
* [x] Reject invalid metadata
* [x] Reject malformed lines
* [x] Reject forbidden zone-name syntax
* [x] Report a useful error message

## Tests

* [x] Valid simple map
* [x] Invalid drone count
* [x] Missing start
* [x] Missing end
* [x] Multiple starts
* [x] Multiple ends
* [x] Duplicate zone
* [x] Unknown zone in connection
* [x] Duplicate connection
* [x] Invalid zone type
* [x] Invalid capacity
* [x] Duplicate coordinates
* [x] Invalid metadata
* [x] Comments
* [x] Empty lines

## Definition of Done

* [x] All provided map formats parse correctly
* [x] Invalid maps fail gracefully
* [x] Error messages include line and cause
* [x] Parser tests pass

---

# Sprint 3 — Graph & Pathfinding

**Estimated time:** 8–10 hours

**Goal:** Find valid and efficient paths without using graph libraries.

## Graph

* [X] Build bidirectional connections
* [X] Build adjacency list
* [X] Ignore blocked zones during traversal
* [x] Detect missing paths
* [x] Prevent infinite loops on cycles

## Movement cost

Implement:

```text
normal     = 1
priority   = 1
restricted = 2
blocked    = impossible
```

Tasks:

* [x] Create movement-cost logic
* [x] Verify cost depends on destination zone
* [x] Prevent movement into blocked zones
* [x] Handle restricted destinations

## Bellman Ford

* [x] Implement pathfinder manually
* [x] Reconstruct the final path
* [x] Handle unreachable destinations
* [x] Add tests for shortest paths
* [x] Test cycles
* [x] Test multiple possible paths
* [x] Test restricted zones
* [x] Test blocked zones

## Definition of Done

Given:

```text
START → A → B → END
```

the pathfinder returns:

```text
START → A → B → END
```

with the correct total movement cost.

---

# Sprint 4 — Single-Drone Simulation

**Estimated time:** 4–5 hours

**Goal:** Build a correct simulation for one drone.

## Simulation engine

* [x] Create `Simulation` class
* [x] Initialize simulation state
* [x] Create one drone
* [x] Execute turns
* [x] Move drone between zones
* [x] Track current turn
* [x] Stop when drone reaches end

## Movement

* [x] Normal movement
* [ ] Priority movement
* [ ] Restricted movement
* [ ] Waiting
* [ ] Blocked movement prevention

## Restricted zones

* [ ] Detect restricted destination
* [ ] Apply 2-turn movement
* [ ] Put drone into `IN_FLIGHT`
* [ ] Prevent unnecessary waiting during restricted traversal
* [ ] Complete movement on the correct turn

## Output

Implement:

```text
D1-zone
```

and:

```text
D1-connection
```

for restricted traversal where required.

## Definition of Done

A single drone can travel from start to end correctly on all basic maps.

---

# Sprint 5 — Multi-Drone Simulation

**Estimated time:** 6–8 hours

**Goal:** Correctly simulate multiple drones simultaneously.

## Drone initialization

* [ ] Create all drones
* [ ] Assign unique IDs
* [ ] Place all drones at start
* [ ] Allow unlimited initial occupancy at start

## Zone capacity

* [ ] Check destination capacity
* [ ] Count drones leaving the zone
* [ ] Free capacity before validating incoming drones
* [ ] Allow multiple drones in zones with sufficient capacity
* [ ] Allow unlimited drones at end

## Connection capacity

* [ ] Track connection occupancy
* [ ] Validate `max_link_capacity`
* [ ] Prevent excessive simultaneous traversal
* [ ] Release connection capacity correctly

## Simultaneous movement

Implement a two-phase turn:

```text
1. Calculate movements
2. Validate movements
3. Apply movements
```

Tasks:

* [ ] Calculate candidate moves
* [ ] Detect zone conflicts
* [ ] Detect connection conflicts
* [ ] Account for drones leaving zones
* [ ] Apply all valid movements simultaneously
* [ ] Handle drones that must wait

## Waiting

* [ ] Allow a drone to stay in place
* [ ] Ensure waiting does not violate rules
* [ ] Avoid unnecessary waiting

## Delivery

* [ ] Remove delivered drones from active simulation
* [ ] Keep end-zone occupancy unlimited
* [ ] Detect completion when all drones arrive

## Definition of Done

* [ ] Multiple drones can run simultaneously
* [ ] No zone capacity violation
* [ ] No connection capacity violation
* [ ] No invalid collisions
* [ ] Simulation terminates correctly

---

# Sprint 6 — Scheduling & Optimization

**Estimated time:** 6–10 hours

**Goal:** Minimize the total number of simulation turns.

This is the main optimization sprint.

## Baseline scheduler

* [ ] Create `Scheduler` class
* [ ] Generate candidate movement for each drone
* [ ] Rank possible movements
* [ ] Detect conflicts
* [ ] Resolve conflicts
* [ ] Decide which drones wait
* [ ] Avoid deadlocks

## Multiple paths

* [ ] Find several possible routes
* [ ] Compare path costs
* [ ] Calculate path capacities
* [ ] Identify bottlenecks
* [ ] Distribute drones between routes

Example:

```text
Path A:
START → A → B → END

Path B:
START → C → D → END
```

Distribute drones according to:

* [ ] Path length
* [ ] Zone capacity
* [ ] Connection capacity
* [ ] Restricted zones
* [ ] Current congestion
* [ ] Priority zones

## Congestion

* [ ] Detect congested zones
* [ ] Detect congested connections
* [ ] Penalize congested paths
* [ ] Prefer less congested paths

## Dynamic scheduling

* [ ] Re-evaluate blocked movements
* [ ] Allow waiting strategically
* [ ] Re-route drones when useful
* [ ] Avoid unnecessary recalculation
* [ ] Prevent deadlocks

## Performance

* [ ] Benchmark easy maps
* [ ] Benchmark medium maps
* [ ] Benchmark hard maps
* [ ] Record number of turns
* [ ] Record average drone turns
* [ ] Record total path cost
* [ ] Compare against subject targets

## Definition of Done

The scheduler produces valid simulations and improves upon the naïve shortest-path-per-drone approach.

---

# Sprint 7 — Visualisation

**Estimated time:** 15–20 hours

**Goal:** Make the simulation understandable during execution.

## Graphical representation

* [ ] Display map information
* [ ] Display zones
* [ ] Display connections
* [ ] Display drone positions
* [ ] Display current turn
* [ ] Display delivered drones
* [ ] Display occupancy

## Colours

* [ ] Start colour
* [ ] End colour
* [ ] Normal zone colour
* [ ] Restricted zone colour
* [ ] Priority zone colour
* [ ] Blocked zone colour
* [ ] Drone colour

## Definition of Done

A peer can understand the simulation by the visualizer.

---

# Sprint 8 — Testing, Quality & Submission

**Estimated time:** 5–7 hours

**Goal:** Make the project evaluation-ready.

## Unit tests

* [ ] Zone tests
* [ ] Connection tests
* [ ] Drone tests
* [ ] Graph tests
* [ ] Parser tests
* [ ] Pathfinding tests
* [ ] Scheduler tests
* [ ] Simulation tests
* [ ] Display tests where useful

## Edge cases

* [ ] One drone
* [ ] Many drones
* [ ] No path
* [ ] One possible path
* [ ] Multiple paths
* [ ] Blocked route
* [ ] Restricted route
* [ ] Priority route
* [ ] Zone capacity = 1
* [ ] Zone capacity > 1
* [ ] Connection capacity = 1
* [ ] Connection capacity > 1
* [ ] Cyclic graph
* [ ] Dead end
* [ ] Multiple bottlenecks
* [ ] Start connected directly to end
* [ ] Large drone count

## Static analysis

* [ ] Run `flake8 .`
* [ ] Fix all flake8 errors
* [ ] Run required mypy command
* [ ] Fix all mypy errors
* [ ] Remove unnecessary `# type: ignore`
* [ ] Add missing type hints
* [ ] Check return types
* [ ] Check class attributes

## Exception handling

* [ ] Handle invalid input
* [ ] Handle missing map file
* [ ] Handle invalid simulation state
* [ ] Handle no-path situations
* [ ] Prevent unhandled crashes
* [ ] Use context managers for file access

## Documentation

* [ ] Complete README
* [ ] Add project description
* [ ] Add installation instructions
* [ ] Add execution instructions
* [ ] Explain map format
* [ ] Explain architecture
* [ ] Explain pathfinding
* [ ] Explain scheduling
* [ ] Explain optimization
* [ ] Explain complexity
* [ ] Explain visualisation
* [ ] Add benchmark results
* [ ] Add resources
* [ ] Document AI usage
* [ ] Ensure README is in English
* [ ] Verify required first line

## Peer-review preparation

Be able to explain:

* [ ] Why the project is object-oriented
* [ ] Why you chose your pathfinding algorithm
* [ ] How movement costs work
* [ ] How restricted zones work
* [ ] How zone capacity works
* [ ] How connection capacity works
* [ ] How simultaneous movement works
* [ ] How waiting works
* [ ] How deadlocks are avoided
* [ ] How drones are distributed
* [ ] How paths are cached
* [ ] Time complexity
* [ ] Memory complexity
* [ ] Why your scheduler is efficient

## Final checks

* [ ] `make install`
* [ ] `make run`
* [ ] `make debug`
* [ ] `make lint`
* [ ] `make clean`
* [ ] Test every provided map
* [ ] Check Git status
* [ ] Remove temporary files
* [ ] Verify only required project files are committed

---

# Recommended Development Order

Do NOT implement everything at once.

Follow this order:

```text
Domain Model
     ↓
Parser
     ↓
Graph
     ↓
Bellman Ford
     ↓
1 Drone
     ↓
Multiple Drones
     ↓
Capacity Management
     ↓
Scheduler
     ↓
Multiple Paths
     ↓
Optimization
     ↓
Visualisation
     ↓
Tests
     ↓
README
```

The most important rule is:

> **First make it correct, then make it fast.**

Do not try to beat the 45-turn Challenger map before the basic simulation is completely reliable.
