# Performance Improvements Design

## Problem

A 4-device installation makes ~33 HTTP roundtrips per 60s poll cycle, with ~16 of those being redundant session-alive checks. Startup creates 4 separate login sessions for the same account.

## Fix 1: Cache `is_session_active()` (HIGH impact)

The `@logged_in` decorator calls `is_session_active()` before every API method, each costing one HTTP roundtrip. With 4 devices making ~4 API calls each per poll, that's ~16 wasted calls.

**Change**: Add a `_session_active_cache` tuple `(result, timestamp)` on the client. `is_session_active()` returns the cached result if it's less than 30 seconds old. Reset the cache on login, logout, or session error.

**Files**: `client.py` — `is_session_active()` method + `_login()` + `log_out()`

**Expected savings**: ~16 HTTP calls/poll → ~1 per poll cycle.

## Fix 2: Share `FusionSolarClient` across config entries (HIGH impact)

Each config entry creates its own client, even when multiple entries use the same username+subdomain. A 4-device setup means 4 login ceremonies at startup and 4x session maintenance.

**Change**: In `__init__.py`, key clients by `(username, subdomain)` instead of `entry.entry_id`. The first config entry with a given credential pair creates the client; subsequent entries reuse it. Reference-count so the client is only logged out when the last entry using it is unloaded.

**Data structure**: `hass.data[DOMAIN]["_clients"]` = `{(username, subdomain): {"client": FusionSolarClient, "ref_count": int}}`

Individual entries still store their own coordinator, handler, and device_info — only the client is shared.

**Files**: `__init__.py` — `async_setup_entry()` + `async_unload_entry()`

**Expected savings**: N-1 login ceremonies eliminated. Session maintenance overhead reduced by ~75%.

## Fix 3: Only query existing battery modules (MEDIUM impact)

Battery handler always queries modules 1-4 regardless of how many exist. Each query includes a `@logged_in` session check. With the session cache fix, the session check overhead goes away, but the module queries themselves are still wasted.

**Change**: In `battery/sensor.py`, after fetching the first module, check if it returned data. Stop iterating when a module returns empty. Store discovered module count for subsequent polls.

**Files**: `battery/sensor.py` — `_async_get_data()`

**Expected savings**: 1-3 fewer HTTP calls per battery poll for most installations.
