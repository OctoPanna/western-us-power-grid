best_score = -float("inf")
best_params = None

for i in range(100):  # number of random samples to try

    # pick random parameter values
    trip_threshold = random.uniform(0.05, 0.5)
    capacity_factor = random.uniform(1.0, 2.0)
    num_failures = random.randint(1, max(1, int(0.1 * G.number_of_edges())))
    initial_failed_edges = random.sample(list(G.edges()), num_failures)
    max_iterations = random.randint(5, 50)
    redistribution_factor = random.uniform(0.5, 1.0)
    random_seed = random.randint(0, 10000)
    stop_on_disconnect = random.choice([True, False])

    # run your simulation capacity_factor=capacity_factor, num_failures=num_failures,initial_failed_edges=initial_failed_edges, max_iterations=max_iterations,   redistribution_factor=redistribution_factor, random_seed=random_seed, stop_on_disconnect=stop_on_disconnect
    result = cascade_simulation(G0=G, trip_threshold=trip_threshold)

    # your objective metric
    score = result["load_served_fraction"]

    # update best
    if score > best_score:
        best_score = score
        best_params = {"threshold": threshold, "capacity_factor": capacity_factor, "num_failures":num_failures, "initial_failed_edges":initial_failed_edges, "max_iteration":max_iterations, "redistribution_factor":redistribution_factor, "random_seed":random_seed, "stop_on_disconnect":stop_on_disconnect}
print("Best parameters found:", best_params)
print("Best score:", best_score) 