s = "Anna went to see civic racecar stats"
def same_start_end(s):
    words = s.split()
    return [w for w in words if len(w) > 1 and w[0].lower() == w[-1].lower()]
same_start_end(s)