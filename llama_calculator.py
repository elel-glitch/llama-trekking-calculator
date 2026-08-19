def calculate_trip(llamas, total_gear_weight, trip_days, include_pellets):
    pellets_total = 0
    if include_pellets:
        pellets_total = len(llamas) * 0.5 * trip_days

    starting_gear_weight = total_gear_weight + pellets_total

    total_llama_weight = 0
    for llama in llamas:
        total_llama_weight = total_llama_weight + llama["weight"]

    herd_percent = (starting_gear_weight / total_llama_weight) * 100

    for llama in llamas:
        share = llama["weight"] / total_llama_weight
        safe_min = llama["weight"] * 0.20
        safe_max = llama["weight"] * 0.25

        starting_load = share * starting_gear_weight
        llama["load"] = starting_load

        if starting_load > safe_max:
            llama["status"] = "🔴 Overloaded"
        elif starting_load >= safe_min:
            llama["status"] = "🟡 Standard Pack Load"
        else:
            llama["status"] = "🟢 Optimal Pack Load"

    # Check if ANY llama is overloaded (checking one is enough, since % is shared, but this stays safe even if that changes later)
    any_overloaded = False
    for llama in llamas:
        if llama["status"] == "🔴 Overloaded":
            any_overloaded = True

    herd_insight = None

    if any_overloaded:
        herd_insight = (
            "⚠️ Warning: The herd is overloaded. Consider adding another llama, removing non-essential gear,"
            "or shortening the trek duration to reduce supply weight."
        )

    elif llamas[0]["status"] == "🟢 Optimal Pack Load":
        herd_insight = "✅ The herd is comfortably within the optimal load zone for this entire trip."

    elif include_pellets and llamas[0]["status"] == "🟡 Standard Pack Load":
        transition_day = None
        for day in range(1, trip_days + 1):
            pellets_eaten_so_far = len(llamas) * 0.5 * day
            remaining_pellets = pellets_total - pellets_eaten_so_far
            if remaining_pellets < 0:
                remaining_pellets = 0

            gear_on_this_day = total_gear_weight + remaining_pellets
            herd_percent_on_this_day = (gear_on_this_day / total_llama_weight) * 100

            if herd_percent_on_this_day < 20:
                transition_day = day
                break

        if transition_day:
            herd_insight = (
                "The herd is carrying a normal working load. With pellet consumption enabled, "
                "the pack load will enter the 🟢 Optimal Zone on Day " + str(transition_day) + "."
            )
        else:
            herd_insight = (
                "The herd will remain in the 🟡 Standard Zone for the entire duration of the trip."
            )

    return llamas, pellets_total, herd_insight, herd_percent


# ---- Test it ----

llamas = [
    {"name": "Kuzco", "weight": 160},
    {"name": "Paco", "weight": 140}
]

total_gear_weight = 25
trip_days = 8

result_llamas, pellets, herd_insight, herd_percent = calculate_trip(
    llamas,
    total_gear_weight=total_gear_weight,
    trip_days=trip_days,
    include_pellets=True
)

if pellets > 0:
    print("Total Load:", total_gear_weight, "kg gear +", pellets, "kg pellets =", total_gear_weight + pellets, "kg")
else:
    print("Total Load:", total_gear_weight, "kg gear (no pellets included)")

print("Herd load:", round(herd_percent, 1), "% of body weight each")
print()

for llama in result_llamas:
    print("🦙", llama["name"], "(" + str(llama["weight"]) + " kg Llama)")
    print("  Current Load:", round(llama["load"], 1), "kg")
    print("  Status:", llama["status"])
    print()

if herd_insight:
    print("Smart Insight:", herd_insight)