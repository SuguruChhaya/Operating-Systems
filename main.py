
TOTAL_MEMORY = 20 
MAX = 38
class Job:
    def __init__(self, job_id, start, size, duration, end_state):
        self.id = job_id
        self.start = start
        self.size = size
        self.duration = duration
        self.remaining = duration
        self.end_state = end_state
        self.start_addr = None


class MemoryManager:
    def __init__(self):
        self.memory = [(0, TOTAL_MEMORY, None)]

    def free_blocks(self):
        blocks = []
        for block in self.memory:
            if block[2] is None:
                blocks.append(block)
        return blocks

    def allocate(self, job, strategy):
        free = self.free_blocks()
        # first-fit uses original order
        if strategy == "best":
            free.sort(key=lambda b: b[1])
        elif strategy == "worst":
            free.sort(key=lambda b: b[1], reverse=True)
        
        for start, size, _ in free:
            if size >= job.size:
                self.place_block(job, start, size)
                return True

        return False

    def place_block(self, job, start, size):
        new_mem = []

        for b_start, b_size, owner in self.memory:
            if b_start == start and owner is None:
                new_mem.append((start, job.size, job.id))
                if b_size > job.size:
                    new_mem.append((start + job.size, b_size - job.size, None))
            else:
                new_mem.append((b_start, b_size, owner))

        self.memory = new_mem
        job.start_addr = start

    def deallocate(self, job):
        updated = []

        for start, size, owner in self.memory:
            if owner == job.id:
                updated.append((start, size, None))
            else:
                updated.append((start, size, owner))

        self.memory = self.merge_free(updated)

    def merge_free(self, blocks):
        blocks.sort()
        merged = [blocks[0]]

        for block in blocks[1:]:
            last = merged[-1]
            if last[2] is None and block[2] is None and last[0] + last[1] == block[0]:
                merged[-1] = (last[0], last[1] + block[1], None)
            else:
                merged.append(block)

        return merged

    def ensure_space(self, job, sleeping, active, strategy):
        while not self.allocate(job, strategy):
            if sleeping:
                victim = sleeping.pop(0)
                print(f"Replacing sleeping Job {victim.id}")
                self.deallocate(victim)
            elif active:
                victim = active.pop(0)
                print(f"Replacing active Job {victim.id}")
                self.deallocate(victim)
            else:
                return False
        return True

    def print_memory(self):
        view = []
        for _, size, owner in self.memory:
            symbol = "." if owner is None else str(owner)
            for _ in range(size):
                view.append(symbol)
        print("Memory:", " ".join(view))


def run_simulation(jobs, strategy):
    print(f"\n{strategy.upper()} FIT")

    mem = MemoryManager()
    time = 0

    active = []
    sleeping = []

    while time < MAX:
        time += 1
        print(f"\n--- Time {time} ---")

        for job in list(jobs):
            if job.start == time:
                print(f"Job {job.id} arrives ({job.size} KB)")
                if not mem.ensure_space(job, sleeping, active, strategy):
                    print("Allocation failed")
                    return
                active.append(job)
                jobs.remove(job)

        for job in list(active):
            job.remaining -= 1
            if job.remaining == 0:
                if job.end_state == "End":
                    print(f"Job {job.id} ends -> deallocated")
                    mem.deallocate(job)
                else:
                    print(f"Job {job.id} sleeps")
                    sleeping.append(job)
                active.remove(job)

        mem.print_memory()


jobs = [
    Job(1, 1, 2, 7, "End"),
    Job(2, 2, 3, 8, "Sleep"),
    Job(3, 3, 4, 6, "End"),
    Job(4, 4, 3, 6, "Sleep"),
    Job(5, 5, 2, 9, "Sleep"),
    Job(6, 6, 3, 6, "Sleep"),
    Job(7, 7, 2, 6, "Sleep"),
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
    run_simulation(copy.deepcopy(jobs), fit)
