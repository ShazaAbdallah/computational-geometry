from SweepLine import sweep_line
from Utility import input_read

def crashes(segments):
    try:
        sweep_line(segments)
        return False  # no crash
    except Exception as e:
        # Uncomment to see exception during minimization:
        print("Crash:", e)
        return True

def delta_minimize(segments):
    """
    Given a failing input (segments list), repeatedly reduces it
    until the smallest failing subset is found.
    """

    n = 2  # number of partitions
    failing = segments[:]   # start with the full failing input

    while len(failing) >= 2:
        chunk_size = len(failing) // n
        if chunk_size == 0:
            break

        reduced = None

        for i in range(n):
            # try each partition by removing one chunk
            start = i * chunk_size
            end   = (i + 1) * chunk_size
            test = failing[:start] + failing[end:]

            if crashes(test):
                # Found a smaller failing input
                reduced = test
                break

        if reduced:
            failing = reduced
            n = 2  # restart with 2 partitions
        else:
            if n >= len(failing):
                break
            n = min(len(failing), n * 2)

    return failing

def save_segments(segments, filename="reduced.txt"):
    with open(filename, "w") as f:
        f.write(str(len(segments)) + "\n")
        for s in segments:
            f.write(f"{s.p.x} {s.p.y}   {s.q.x} {s.q.y}\n")
        f.write("-1\n")


# Load your large failing test case into "all_segments"...
# Then:

all_segments = input_read("bug.txt")[0]  # adjust filename and index as needed
minimal = delta_minimize(all_segments)

print("Original:", len(all_segments))
print("Reduced to:", len(minimal))

save_segments(minimal)
