def calculate_trip(llamas, total_gear_weight, trip_days, include_pellets):
    # If pellets are included, calculate them and add to the gear weight first
    pellets_weight = 0
    if include_pellets:
        pellets_weight = len(llamas) * 0.5 * trip_days
        total_gear_weight = total_gear_weight + pellets_weight

    total_llama_weight = 0
    for llama in llamas:
        total_llama_weight = total_llama_weight + llama["weight"]

    for llama in llamas:
        share = llama["weight"] / total_llama_weight
        llama["load"] = share * total_gear_weight

        safe_min = llama["weight"] * 0.20
        safe_max = llama["weight"] * 0.25

        if llama["load"] > safe_max:
            llama["status"] = "RED - Overloaded!"
        elif llama["load"] >= safe_min:
            llama["status"] = "YELLOW - Near Max"
        else:
            llama["status"] = "GREEN - Safe Load"

    return llamas, pellets_weight, total_gear_weight


# ---- Now let's actually use it ----

llamas = [
    {"name": "Kuzco", "weight": 160},
    {"name": "Paco", "weight": 140}
]

result_llamas, pellets, final_gear_weight = calculate_trip(
    llamas,
    total_gear_weight=25,
    trip_days=7,
    include_pellets=False
)

print("Pellets added:", pellets, "kg")
print("Total gear weight (including pellets):", final_gear_weight, "kg")
print()

for llama in result_llamas:
    print(llama["name"], "| load:", round(llama["load"], 1), "kg | status:", llama["status"])