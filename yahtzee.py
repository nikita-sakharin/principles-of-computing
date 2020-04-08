import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    answer_set = set([()])
    for _ in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def score(hand):
    max_score = 0
    for item in hand:
        max_score = max(max_score, item * hand.count(item))
    return max_score

def expected_value(held_dice, num_die_sides, num_free_dice):
    outcomes = [num + 1 for num in range(num_die_sides)]
    all_sequences = gen_all_sequences(outcomes, num_free_dice)
    expected = 0.0
    for hand in all_sequences:
        expected += score(held_dice + hand)
    return expected / len(all_sequences)

def gen_all_holds(hand):
    all_holds = [()]
    for item in hand:
        for hold in all_holds:
            all_holds = all_holds + [hold + (item,)]
    return set(all_holds)

def strategy(hand, num_die_sides):
    all_holds = gen_all_holds(hand)
    max_expected = 0.0
    max_hand = ()
    for temp_hand in all_holds:
        temp_expected = expected_value(temp_hand, num_die_sides,
            len(hand) - len(temp_hand))
        if temp_expected > max_expected:
            max_expected = temp_expected
            max_hand = temp_hand
    return (max_expected, max_hand)

# import poc_holds_testsuite
# poc_holds_testsuite.run_suite(gen_all_holds)
