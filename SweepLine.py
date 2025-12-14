import Utility
import sys
from bintrees import AVLTree
from sortedcontainers import SortedSet


def print_sweep_status(sweep_status):
    print("Sweep Status:")
    for seg in sweep_status:
        print(seg)
    print("End of Sweep Status\n")

def get_prev_next(sweep_status, segment):
    try:
        prev_seg = sweep_status.prev_key(segment)
    except KeyError:
        prev_seg = None
    
    try:
        next_seg = sweep_status.succ_key(segment)
    except KeyError:
        next_seg = None

    return prev_seg, next_seg

def sweep_line(segments):

    event_queue = Utility.CG24PriorityQueue(False, True, False)
    sweep_status = AVLTree()
    seen_intersections = SortedSet()

    for seg in segments:
        start = Utility.Event(seg.p, 0, seg)  # Start event
        end = Utility.Event(seg.q, 2, seg)    # End event
        event_queue.insert(start, seg.p.x, seg.p.y, 0)  # Insert start point
        event_queue.insert(end, seg.q.x, seg.q.y, 2)  # Insert end point
 
    

    count_intersections = 0

    while not event_queue.empty():
        event = event_queue.pop()

        if event.etype == 0:  # Start point
            Utility.current_sweep_x = event.point.x  # Update global sweep line position
            sweep_status.insert(event.seg1, None)
            prev_seg, next_seg = get_prev_next(sweep_status, event.seg1)

            # Check for intersections with neighbors
            if prev_seg and Utility.intersects(event.seg1, prev_seg):
                inter_point = Utility.intersection(event.seg1, prev_seg)
                if inter_point and inter_point.x >= Utility.current_sweep_x and not(seen_intersections.__contains__((inter_point.x, inter_point.y))):
                    inter_event = Utility.Event(inter_point, 1, prev_seg, event.seg1)
                    event_queue.insert(inter_event, inter_point.x, inter_point.y, 1)
                    seen_intersections.add((inter_point.x, inter_point.y))
            
            if next_seg and Utility.intersects(event.seg1, next_seg):
                inter_point = Utility.intersection(event.seg1, next_seg)
                if inter_point and inter_point.x >= Utility.current_sweep_x and not(seen_intersections.__contains__((inter_point.x, inter_point.y))):
                    inter_event = Utility.Event(inter_point, 1, event.seg1, next_seg)
                    event_queue.insert(inter_event, inter_point.x, inter_point.y, 1)
                    seen_intersections.add((inter_point.x, inter_point.y))
        
        elif event.etype == 1:  # Intersection point
            count_intersections += 1
            seg1 = event.seg1
            seg2 = event.seg2

            # Swap segments in sweep status
            Utility.current_sweep_x = event.point.x - 1e-9
            sweep_status.remove(seg1)
            sweep_status.remove(seg2)
            #seg2.breaker = 0
            #seg1.breaker = 1
            Utility.current_sweep_x = event.point.x + 1e-9  # Update global sweep line position
            sweep_status.insert(seg1, None)
            sweep_status.insert(seg2, None)
            #print_sweep_status(sweep_status)
            #seg2.breaker = 0
            #seg1.breaker = 1


            # Check for new intersections with neighbors
            prev_seg = get_prev_next(sweep_status, seg2)[0]
            if prev_seg and Utility.intersects(seg2, prev_seg):
                inter_point = Utility.intersection(seg2, prev_seg)
                if inter_point and inter_point.x >= Utility.current_sweep_x and not(seen_intersections.__contains__((inter_point.x, inter_point.y))):
                    inter_event = Utility.Event(inter_point, 1, prev_seg, seg2)
                    event_queue.insert(inter_event, inter_point.x, inter_point.y, 1)
                    seen_intersections.add((inter_point.x, inter_point.y))

            next_seg = get_prev_next(sweep_status, seg1)[1]
            if next_seg and Utility.intersects(seg1, next_seg):
                inter_point = Utility.intersection(seg1, next_seg)
                if inter_point and inter_point.x >= Utility.current_sweep_x and not(seen_intersections.__contains__((inter_point.x, inter_point.y))):
                    inter_event = Utility.Event(inter_point, 1, seg1, next_seg)
                    event_queue.insert(inter_event, inter_point.x, inter_point.y, 1)
                    seen_intersections.add((inter_point.x, inter_point.y))
            
            


        elif event.etype == 2:  # End point
            Utility.current_sweep_x = max(event.point.x, Utility.current_sweep_x)  # Update global sweep line position
            prev_seg, next_seg = get_prev_next(sweep_status, event.seg1)
            sweep_status.remove(event.seg1)

            # Check for intersection between neighbors
            if prev_seg and next_seg and Utility.intersects(prev_seg, next_seg):
                inter_point = Utility.intersection(prev_seg, next_seg)
                if inter_point and inter_point.x >= Utility.current_sweep_x and not(seen_intersections.__contains__((inter_point.x, inter_point.y))):
                    inter_event = Utility.Event(inter_point, 1, prev_seg, next_seg)
                    event_queue.insert(inter_event, inter_point.x, inter_point.y, 1)
                    seen_intersections.add((inter_point.x, inter_point.y))

        #event_queue.print_queue()
            


    return count_intersections


def naive_count_intersections(segments):
    count = 0
    n = len(segments)
    for i in range(n):
        for j in range(i + 1, n):
            if Utility.intersects(segments[i], segments[j]):
                inter_point = Utility.intersection(segments[i], segments[j])
                if inter_point.x >= segments[i].p.x and inter_point.x <= segments[i].q.x:
                    count += 1
    return count
            




    
    
    

def main_bug(argv):
    if len(argv) < 2:
        print("Usage: python SweepLine.py <input_file>")
        return

    print(f"processing {argv[1]}")
    input_file = argv[1]
    test_cases = Utility.input_read(input_file)

    naive=[]
    #print("the naive algorithm outputs:")
    for i, test in enumerate(test_cases):
        #print(f"test {i} , intersection = {naive_count_intersections(test)}")
        naive.append(naive_count_intersections(test))


    #print(sweep_line(test_cases[24]))
    sweep=[]
    print("the sweep line algorithm outputs:")
    for i, test in enumerate(test_cases):
        #print(f"test {i}, intersection = {sweep_line(test)} ")
        sweep.append(sweep_line(test))
    
    for i in range (len(naive)):
        if naive[i]!=sweep[i]:
            print(f"mismatch in test {i}: naive={naive[i]} ,sweep={sweep[i]}")


    print("Finished processing all test cases.")

def main(argv):
    if len(argv) < 2:
        print("Usage: python SweepLine.py <input_file>")
        return

    input_file = argv[1]
    test_cases = Utility.input_read(input_file)


    for i, test in enumerate(test_cases):
        print(sweep_line(test))


if __name__ == "__main__":
    main(sys.argv)

