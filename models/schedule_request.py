class WorkerScheduleRequest:
    def __init__(self, num_workers, num_shifts, num_days):
        self.num_workers = num_workers
        self.num_shifts = num_shifts
        self.num_days = num_days

    @staticmethod
    def from_dict(data):
        return WorkerScheduleRequest(
            num_workers=data.get("num_workers"),
            num_shifts=data.get("num_shifts"),
            num_days=data.get("num_days"),
        )
