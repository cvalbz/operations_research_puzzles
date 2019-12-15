import random

N = 4

def print_matrix(m):
    for row in m:
        print(row)

def stable_state(old, new, iterations, tolerance = 0.001):
    if iterations < 100:
        return False
    for i in range(N):
        for j in range(N):
            if abs(old[i][j] - new[i][j]) > tolerance:
                return False

    return True

def get_state_prob(state, iterations):
    assert iterations > 0
    return [[e / iterations for e in r] for r in state]

def make_new_state():
    return [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

def guard_walk(guard_decision, starting_position, iterations = 10**5):
    state = make_new_state()
    i, j = starting_position
    state[i][j] += 1

    old_state_prob = get_state_prob(state, 1)
    #print_matrix(state)

    for iter_number in range(2, iterations):
        #print(iter_number)
        x, y = guard_decision( (i, j) )
        state[x][y] += 1
        i, j = x, y
        #print_matrix(state)

        new_state_prob = get_state_prob(state, iter_number)
        if stable_state(old_state_prob, new_state_prob, iter_number):
            #print_matrix(new_state_prob)
            return new_state_prob, True
        old_state_prob = new_state_prob

    return new_state_prob, False

def make_guard(probs):
    up, down, left, right = probs
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    assert len(moves) == len(probs)

    def decision(position):
        i, j = position
        move = random.choices(moves, probs)[0]
        new_i, new_j = i + move[0], j + move[1]
        if 0 <= new_i < N and 0 <= new_j < N:
            return new_i, new_j
        else:
            return i, j

    return decision

def sum_matrix(a, b):
    result = [[None] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            result[i][j] = a[i][j] + b[i][j]

    return result

def find_guard_state_prob(move_probs):
    guard = make_guard(move_probs)

    res = make_new_state()
    N_iterations = 10 ** 2
    for nr_iter in range(N_iterations):
        i, j = random.choices(range(N), k = 2)
        state_prob, stable = guard_walk(guard, (i, j))
        if stable:
            res = sum_matrix(res, state_prob)

    return get_state_prob(res, N_iterations)

def main():
    guard_one = [0.2, 0.4, 0.2, 0.2]
    guard_one_state = find_guard_state_prob(guard_one)

    guard_two = [0.4, 0.1, 0.2, 0.3]
    guard_two_state = find_guard_state_prob(guard_two)

    combined = sum_matrix(guard_one_state, guard_two_state)

    escape = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (2, 3), (3, 3)]
    print("Escape route is: %s" % " -> ".join([str(1 + i*N + j) for i, j in escape]))

    prob = 0
    for i, j in reversed(escape):
        prob = combined[i][j] + (1 - combined[i][j]) * prob

    print("There is %s probability that we are caught." % prob)

if __name__ == "__main__":
    main()
