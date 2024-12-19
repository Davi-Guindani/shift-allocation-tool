from ortools.sat.python import cp_model

def generate_schedule(request_data):
    model = cp_model.CpModel()

    num_workers = request_data.num_workers
    num_shifts = request_data.num_shifts
    num_days = request_data.num_days
    all_workers = range(num_workers)
    all_shifts = range(num_shifts)
    all_days = range(num_days)

    shifts = {}
    for n in all_workers:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d, s)] = model.NewBoolVar(f"shift_n{n}_d{d}_s{s}")

    for d in all_days:
        for s in all_shifts:
            model.AddExactlyOne(shifts[(n, d, s)] for n in all_workers)

    for n in all_workers:
        for d in all_days:
            model.AddAtMostOne(shifts[(n, d, s)] for s in all_shifts)

    min_shifts_per_worker = (num_shifts * num_days) // num_workers
    max_shifts_per_worker = min_shifts_per_worker + (1 if (num_shifts * num_days) % num_workers else 0)
    for n in all_workers:
        shifts_worked = [shifts[(n, d, s)] for d in all_days for s in all_shifts]
        model.Add(min_shifts_per_worker <= sum(shifts_worked))
        model.Add(sum(shifts_worked) <= max_shifts_per_worker)

    solver = cp_model.CpSolver()
    
    class SolutionPrinter(cp_model.CpSolverSolutionCallback):
        def __init__(self, shifts, num_workers, num_days, num_shifts):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self._shifts = shifts
            self._num_workers = num_workers
            self._num_days = num_days
            self._num_shifts = num_shifts
            self._solutions = []

        def on_solution_callback(self):
            solution = []
            for d in range(self._num_days):
                day_schedule = []
                for n in range(self._num_workers):
                    for s in range(self._num_shifts):
                        if self.Value(self._shifts[(n, d, s)]):
                            day_schedule.append({"worker": n, "shift": s})
                solution.append(day_schedule)
            self._solutions.append(solution)

        def get_solutions(self):
            return self._solutions

    solution_printer = SolutionPrinter(shifts, num_workers, num_days, num_shifts)
    solver.SearchForAllSolutions(model, solution_printer)

    return solution_printer.get_solutions()
