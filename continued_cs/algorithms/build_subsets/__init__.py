def build_subsets(superset):
    ''' Given a set, compute all subsets '''
    subsets = [set([])]
    while superset:
        item = superset.pop()
        subsets_plus_item = [one_set.union(set([item])) for one_set in subsets]
        subsets = subsets + subsets_plus_item

    return subsets


def build_subsets_recursive(superset):
    ''' Given a set, compute all subsets '''
    if not superset:
        return [set([])]

    item = superset.pop()
    subsets = build_subsets_recursive(superset)
    subsets_plus_item = [one_set.union(set([item])) for one_set in subsets]
    subsets = subsets + subsets_plus_item

    return subsets
