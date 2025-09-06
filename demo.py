from graph import app
from state import TripState

if __name__ == "__main__":
    user_request = input("Enter your trip request (e.g., 'Paris under $1500, 3 nights, 2025-10-12'): ")

    init: TripState = {
        "request": user_request,
        "parsed": None,
        "flight": "",
        "hotels": None,
        "calendar_note": "",
        "itinerary": ""
    }

    print("\n⏳ Planning your trip... (streaming trace below)\n")

    # Stream deltas as each node writes to state
    for update in app.stream(init, stream_mode="updates"):
        # update is a dict like {"orchestrator": {"parsed": {...}}}
        for node_name, delta in update.items():
            written_keys = ", ".join(delta.keys())
            print(f"➡️  [{node_name}] wrote: {written_keys}")

    # Get the final state (or read the last event you captured)
    out = app.invoke(init)
    print("\n✅ Final itinerary:\n")
    print(out["itinerary"])
