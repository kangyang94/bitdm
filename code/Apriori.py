###################################
####----------2018 4-17--------####
####-------By Liu Yuanpei------####
###################################

from collections import defaultdict, Iterable
import itertools

"""
class description:
    conduct FIM(Frequent Item Mining) and then ARM(Association Rule Mining) by the Apriori algorithm
class variables description:
    minSup: the minimum support
    minConf: the minimum confidence
    dataset: the dataset to be analysed
    transList: the list of transactions
    freqList: the list of item sets and their 
    itemset: the item sets
    highSupportList: the list of high support item sets
    numItems: the number of items
    remove_skyl:  whether removing the skyline
    F: the frequent item sets
"""
class Apriori:
    def __init__(self, data, minSup, minConf):
        self.minSup = minSup
        self.minConf = minConf
        self.dataset = data
        self.transList = defaultdict(list)
        self.freqList = defaultdict(int)
        self.itemset = set()
        self.highSupportList = list()
        self.numItems = 0
        self.remove_skyl = True
        self.prep_data()  # initialize the above collections

        self.F = defaultdict(list)

    # generate associations
    def gen_associations(self):
        candidate = {}
        count = {}

        self.F[1] = self.first_pass(self.freqList, 1)
        k = 2
        while len(self.F[k - 1]) != 0:
            candidate[k] = self.gen_candidate(self.F[k - 1], k)
            for t in self.transList.items():
                for c in candidate[k]:
                    if set(c).issubset(t[1]):
                        self.freqList[c] += 1

            self.F[k] = self.pruning(candidate[k], k)
            if k > 2 and self.remove_skyl:
                self.rem_skyline(k, k - 1)
            k += 1

        return self.F

    # remove the skyline
    def rem_skyline(self, k, kPrev):
        for item in self.F[k]:
            subsets = self.gen_subsets(item)
            for subset in subsets:
                if subset in (self.F[kPrev]):
                    self.F[kPrev].remove(subset)

        subsets = self.gen_subsets

    # conduct the pruning
    def pruning(self, items, k):
        f = []
        for item in items:
            count = self.freqList[item]
            support = self.support(count)
            if support >= .95:
                self.highSupportList.append(item)
            elif support >= self.minSup:
                f.append(item)

        return f

    # generate the candidate item sets
    def gen_candidate(self, items, k):
        candidate = []

        if k == 2:
            candidate = [tuple(sorted([x, y])) for x in items for y in items if len((x, y)) == k and x != y]
        else:
            candidate = [tuple(set(x).union(y)) for x in items for y in items if len(set(x).union(y)) == k and x != y]

        for c in candidate:
            subsets = self.gen_subsets(c)
            if any([x not in items for x in subsets]):
                candidate.remove(c)

        return set(candidate)

    # generate the subsets
    def gen_subsets(self, item):
        subsets = []
        for i in range(1, len(item)):
            subsets.extend(itertools.combinations(item, i))
        return subsets

    # generate the rules
    def gen_rules(self, F):
        H = []

        for k, itemset in F.items():
            if k >= 2:
                for item in itemset:
                    subsets = self.gen_subsets(item)
                    for subset in subsets:
                        if len(subset) == 1:
                            subCount = self.freqList[subset[0]]
                        else:
                            subCount = self.freqList[subset]
                        itemCount = self.freqList[item]
                        if subCount != 0:
                            confidence = self.confidence(subCount, itemCount)
                            if confidence >= self.minConf:
                                support = self.support(self.freqList[item])
                                rhs = self.difference(item, subset)
                                if len(rhs) == 1:
                                    support_rhs = self.support(self.freqList[rhs[0]])
                                else:
                                    support_rhs = self.support(self.freqList[rhs])
                                if support_rhs == 0:
                                    print(rhs)
                                    lift = 'Inf'
                                else:
                                    lift = confidence / support_rhs

                                H.append((subset, rhs, support, confidence, lift))

        return H

    # calculate the difference
    def difference(self, item, subset):
        return tuple(x for x in item if x not in subset)

    # calculate the confidence
    def confidence(self, subCount, itemCount):
        return float(itemCount) / subCount

    # calculate the support
    def support(self, count):
        return float(count) / self.numItems

    # the first pass
    def first_pass(self, items, k):
        f = []
        for item, count in items.items():
            support = self.support(count)
            if support == 1:
                self.highSupportList.append(item)
            elif support >= self.minSup:
                f.append(item)

        return f

    # prepare the data
    def prep_data(self):
        key = 0
        for basket in self.dataset:
            self.numItems += 1
            key = basket[0]
            if key != '':
                # for i, item in enumerate(basket):
                # print(basket[1].strip(',').split(','))
                basket[1] = basket[1].replace("]","")
                basket[1] = basket[1].replace("[", "")
                list_basket = basket[1].strip(',').split(',')
                list_basket = {}.fromkeys(list_basket).keys()
                for i, item in enumerate(list_basket):
                        self.transList[key].append(item.strip())
                        self.itemset.add(item.strip())
                        self.freqList[(item.strip())] += 1