#!/usr/bin/env python

import csv
import random
import re
import sys
from collections import defaultdict

# Add the names of any projects you want to remove from the running here.
disqualified = []

pat = re.compile(r"^(.*?) - (.*?)$")

prefs = {
    "first choice": 1,
    "second choice": 2,
    "third choice": 3,
}


def load_data(filename):
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        return [parse_ballot(b) for b in reader]


def parse_ballot(raw_ballot):
    ballot = defaultdict(dict)
    for column, project in raw_ballot.items():
        if m := pat.match(column):
            category = m.group(1)
            pref = m.group(2)
            ballot[category][prefs[pref]] = project
    return ballot


def current_score(category_votes):
    all_candidate = {c for v in category_votes for c in v.values()}

    s = {c: 0 for c in all_candidate}

    total_votes = 0
    for v in category_votes:
        if 1 in v:
            s[v[1]] += 1
            total_votes += 1
    return s, total_votes


def bottom(score):
    lowest = min(score.values())
    return {k for k in score if score[k] == lowest}


def winners(score, total_votes):
    r = []
    for proj, votes in score.items():
        if votes >= total_votes / 2:
            r.append(proj)
    return r


def show_votes(votes):
    print("\nAdjusted ballots:")
    for v in votes:
        print(v)
    print()


def show_scores(s, total_votes):
    print(f"\nFirst place votes (total: {total_votes}):\n")
    for k, v in sorted(s.items(), key=lambda x: x[1], reverse=True):
        print(f"{k:.<32s} {v} ({v/total_votes:.0%})")


def category_results(votes, n):
    print(f"\nRound {n}")
    show_votes(votes)
    s, total_votes = current_score(votes)
    show_scores(s, total_votes)
    if w := winners(s, total_votes):
        return w
    else:
        least_votes = bottom(s)
        # There are various choices what to do when there is a tie at the
        # bottom. We take an easy one and pick one at random to eliminate. But
        # updated_ballots takes a set in case we wanted to do something else
        # more efficient.
        to_eliminate = {random.choice(list(least_votes))}
        print(f"\nEliminated: {to_eliminate}")
        return category_results(updated_ballots(votes, to_eliminate), n + 1)


def updated_ballots(votes, eliminated):
    return [renumber(eliminate(v, eliminated)) for v in votes]


def eliminate(v, eliminated):
    return {k: v for k, v in v.items() if v not in eliminated}


def renumber(v):
    return {i + 1: t[1] for i, t in enumerate(sorted(v.items()))}


def categories(ballots):
    return ballots[0].keys()


def tally_category(c, ballots):
    for_category = [b[c] for b in ballots]
    votes = updated_ballots(for_category, {""} | set(disqualified))
    return category_results(votes, 1)


if __name__ == "__main__":

    ballots = load_data(sys.argv[1])

    results = []

    for c in categories(ballots):
        print(f"\nTallying category '{c}'")
        r = tally_category(c, ballots)
        print(f"\nCategory winner '{c}': {r}")
        results.append((c, r))

    print("\nFinal results:\n")

    for c, r in results:
        print(f"Winner '{c}': {r}")
