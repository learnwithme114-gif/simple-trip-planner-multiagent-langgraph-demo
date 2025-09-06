from __future__ import annotations
from datetime import datetime, timedelta
import json
from typing import cast, Dict, Any

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from schemas import ParsedTrip, HotelsResponse
from state import TripState
import os

# Boot model
load_dotenv()
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    temperature=0
)

import time
from functools import wraps

def log_node(fn):
    @wraps(fn)
    def wrapper(state, *args, **kwargs):
        name = fn.__name__
        print(f"\n🧠 Entering {name} ...")
        t0 = time.time()
        result = fn(state, *args, **kwargs)
        dt = (time.time() - t0) * 1000
        # result is a delta (dict); show just keys to avoid huge prints
        print(f"📝 {name} wrote: {', '.join(result.keys())}  ({dt:.1f} ms)")
        return result
    return wrapper

# Orchestrator: parse free text into structured fields
@log_node
def orchestrator(state: TripState) -> Dict[str, Any]:
    parser_llm = llm.with_structured_output(ParsedTrip)
    prompt = (
        "Extract city, check_in (YYYY-MM-DD), nights, and budget_total_usd from this request. "
        "Return ONLY the structured object (no commentary).\n"
        f"Request: {state['request']}"
    )
    parsed: ParsedTrip = parser_llm.invoke(prompt)
    # Return only what changed
    return {"parsed": parsed.model_dump()}

# Flights agent (mock with heuristic)
@log_node
def flights_agent(state: TripState) -> Dict[str, Any]:
    p = cast(dict, state.get("parsed") or {})
    budget = int(p.get("budget_total_usd", 1200))
    city = p.get("city", "destination")
    estimate = max(250, int(budget * 0.55))
    return {"flight": f"Round-trip to {city} ~ ${estimate} (economy)"}

# Hotels agent: ask LLM for 3 hotels
@log_node
def hotels_agent(state: TripState) -> Dict[str, Any]:
    p = cast(dict, state.get("parsed") or {})
    hotel_llm = llm.with_structured_output(HotelsResponse)
    prompt = (
        "You are a travel assistant. Suggest exactly 3 realistic hotel options as structured JSON. "
        "Respect total budget and number of nights; prefer central or well-connected areas. "
        "Return ONLY JSON (no extra text).\n\n"
        f"city: {p.get('city')}\n"
        f"check_in: {p.get('check_in')}\n"
        f"nights: {p.get('nights')}\n"
        f"budget_total_usd: {p.get('budget_total_usd')}\n"
    )
    hotels: HotelsResponse = hotel_llm.invoke(prompt)
    return {"hotels": hotels.model_dump()}

# Calendar agent: compute travel window
@log_node
def calendar_agent(state: TripState) -> Dict[str, Any]:
    p = cast(dict, state.get("parsed") or {})
    try:
        start = datetime.strptime(p.get("check_in", ""), "%Y-%m-%d")
        end = start + timedelta(days=int(p.get("nights", 3)))
        nice = f"{start.date().isoformat()} → {end.date().isoformat()}"
    except Exception:
        nice = f"{p.get('check_in')} (+{p.get('nights')} nights)"
    return {"calendar_note": f"Blocked travel window: {nice}"}

# Integrator: stitch final itinerary
@log_node
def integrator(state: TripState) -> Dict[str, Any]:
    p = cast(dict, state.get("parsed") or {})
    city = p.get("city", "destination")
    nights = p.get("nights", 0)
    check_in = p.get("check_in", "YYYY-MM-DD")
    budget = p.get("budget_total_usd", 0)

    hotels_text = "No hotels"
    if state.get("hotels"):
        try:
            h = HotelsResponse(**state["hotels"])  # type: ignore[arg-type]
            lines = []
            for i, opt in enumerate(h.suggestions, 1):
                hi = ", ".join(opt.highlights[:2]) if opt.highlights else ""
                lines.append(
                    f"{i}. {opt.name} — ${opt.price_per_night_usd}/night — {opt.location} "
                    f"{'('+hi+')' if hi else ''}"
                )
            hotels_text = "\n".join(lines)
        except Exception:
            hotels_text = json.dumps(state["hotels"], indent=2)

    itinerary = (
        f"Trip Plan → {city}\n"
        f"- Check-in: {check_in}  |  Nights: {nights}  |  Budget: ${budget}\n\n"
        f"Flight:\n  {state.get('flight','')}\n\n"
        f"Hotels:\n{hotels_text}\n\n"
        f"Calendar:\n  {state.get('calendar_note','')}\n"
    )
    return {"itinerary": itinerary}
