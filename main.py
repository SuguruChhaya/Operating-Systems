TOTAL_MEMORY_KB = 20
PAGE_SIZE_KB = 1
TOTAL_PAGES = TOTAL_MEMORY_KB // PAGE_SIZE_KB


class Job:
    def __init__(self, job_id, start, size, duration, end_state):
        self.id = job_id
        self.start = start
        self.size = size                 
        self.remaining = duration
        self.end_state = end_state
        self.pages = []                  


class MemoryManager:
    def __init__(self):
        self.memory = [None] * TOTAL_PAGES

    def free_pages(self):
        free_pages = []
        for index in range(len(self.memory)):
            if self.memory[index] is None:
                free_pages.append(index)

        return free_pages

    def allocate(self, job, strategy):
        free = self.free_pages()

        if len(free) < job.size:
            return False

        if strategy == "first":
            chosen = free[:job.size]

        elif strategy == "best":
            # free array is already sorted
            chosen = free[:job.size] 

        elif strategy == "worst":
            chosen = free[-job.size:]

        for page in chosen:
            self.memory[page] = job.id
            job.pages.append(page)

        return True

    def deallocate(self, job):
        for page in job.pages:
            self.memory[page] = None
        job.pages.clear()

    def replace(self, active_jobs):
        if not active_jobs:
            return
        victim = active_jobs.pop(0)
        print(f"Page replacement: removing Job {victim.id}")
        self.deallocate(victim)

    def print_memory(self):
        state = []

        for page in self.memory:
            if page is None:
                state.append(".")
            else:
                state.append(str(page))

        print("Memory:", " ".join(state))


def run_simulation(jobs, strategy):
    print(f"\n{strategy.upper()} FIT SIMULATION")
    manager = MemoryManager()
    time = 0
    active = []

    while jobs or active:
        time += 1
        print(f"\n--- Time {time} ---")

        for job in list(jobs):
            if job.start == time:
                print(f"Job {job.id} arrives (needs {job.size} pages)")
                if not manager.allocate(job, strategy):
                    manager.replace(active)
                    manager.allocate(job, strategy)
                active.append(job)
                jobs.remove(job)

        for job in list(active):
            job.remaining -= 1
            if job.remaining == 0:
                if job.end_state == "End":
                    print(f"Job {job.id} ends -> deallocated")
                    manager.deallocate(job)
                else:
                    print(f"Job {job.id} sleeps -> remains in memory")
                active.remove(job)

        manager.print_memory()

    print("\nSimulation completed.\n")


jobs_set_1 = [
    Job(1, 1, 2, 7, "End"),
    Job(2, 2, 3, 8, "Sleep"),
    Job(3, 3, 4, 6, "End"),
    Job(4, 4, 3, 6, "Sleep"),
    Job(5, 5, 2, 9, "Sleep"),
    Job(6, 6, 3, 6, "Sleep"),
    Job(7, 7, 2, 6, "Sleep"),
]

jobs_set_2 = [
    Job(8, 8, 3, 4, "Sleep"),
    Job(9, 9, 5, 5, "Sleep"),
    Job(10, 10, 2, 8, "Sleep"),
    Job(11, 11, 4, 6, "End"),
    Job(12, 12, 6, 5, "Sleep"),
    Job(2, 13, 3, 6, "End"),
    Job(4, 13, 3, 4, "Sleep"),
    Job(13, 13, 5, 3, "End"),
    Job(7, 13, 2, 3, "End"),
    Job(9, 17, 4, 4, "Sleep"),
    Job(10, 19, 2, 11, "End"),
    Job(6, 19, 3, 6, "End"),
    Job(5, 20, 2, 10, "Sleep"),
    Job(4, 21, 3, 12, "Sleep"),
    Job(12, 22, 6, 13, "End"),
    Job(8, 22, 3, 9, "End"),
    Job(9, 28, 5, 11, "End"),
    Job(5, 33, 2, 3, "Sleep"),
    Job(4, 34, 3, 10, "End"),
    Job(5, 38, 2, 10, "End"),
]

import copy

for fit in ["first", "best", "worst"]:
    all_jobs = copy.deepcopy(jobs_set_1 + jobs_set_2)
    run_simulation(all_jobs, fit)
