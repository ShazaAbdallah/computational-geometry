import random
import math

def generate_point(xmin=-10000, xmax=10000, ymin=-10000, ymax=10000):
    """Generate a well-separated random point with 2-decimal precision."""
    x = round(random.uniform(xmin, xmax), 2)
    y = round(random.uniform(ymin, ymax), 2)
    return x, y


def generate_segment():
    """Generate a random segment with:
       - no verticality
       - well-separated endpoints
       - random orientation (x1 may be > x2)
    """
    while True:
        x1, y1 = generate_point()
        x2, y2 = generate_point()

        # avoid vertical segments
        if abs(x1 - x2) < 1e-6:
            continue

        # avoid tiny segments (too close → causes numerical issues)
        if math.hypot(x1 - x2, y1 - y2) < 1.0:
            continue

        return x1, y1, x2, y2


def generate_test_set(num_segments):
    """Generate one test set with num_segments segments."""
    segments = []

    for _ in range(num_segments):
        seg = generate_segment()
        segments.append(seg)

    return segments


def write_tests(filename, num_sets=10, max_segments=1000, add_spacing=True):
    """Generate many test sets into a file, following the required format."""
    with open(filename, "w") as f:
        f.write(str(num_sets) + "\n")

        for _ in range(num_sets):
            m = random.randint(1, max_segments)
            f.write("\n" if add_spacing else "")
            f.write(str(m) + "\n")

            for x1, y1, x2, y2 in generate_test_set(m):
                f.write(f"{x1:.2f} {y1:.2f}   {x2:.2f} {y2:.2f}\n")

        f.write("-1\n")


# -------------------------------
# Example usage
# -------------------------------
# Generates 5 sets, each up to 100 segments, into "tests.txt"
write_tests("tests.txt", num_sets=25, max_segments=1000)
