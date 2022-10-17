import pandas as pd
import math
from decimal import Decimal


# Question a
def sim_distanceManhattan(person1, person2):
    distance = 0
    for (movie, rating) in person1.items():
        if not (pd.isna(person2[movie]) or pd.isna(rating)):
            distance += abs(rating - person2[movie])
        else:
            distance += 0
    return distance


def sim_distanceEuclidienne(person1, person2):
    distance = 0
    for (movie, rating) in person1.items():
        if not (pd.isna(person2[movie]) or pd.isna(rating)):
            distance += pow((rating - person2[movie]), 2)
        else:
            distance += 0
    return pow(distance, 0.5)


# Question 2b
def recommendNearestNeighbor(nouveauCritique, Critiques):
    nearest_neighbor = computeNearestNeighbor(nouveauCritique, Critiques)[0][1]
    movie1 = dict([i for i in Critiques[nearest_neighbor].items() if not pd.isna(i[1])])
    movie2 = dict([i for i in Critiques[nouveauCritique].items() if pd.isna(i[1])])
    return [(i, movie1[i]) for i in movie1 if i in movie2]


def computeNearestNeighbor(nouveauCritique, Critiques):
    distances = []
    for critique in Critiques:
        if critique != nouveauCritique:
            distance = sim_distanceManhattan(Critiques[critique], Critiques[nouveauCritique])
            distances.append((distance, critique))
    distances.sort()
    return distances


# Question 2c
def unwatchlist(person, critiques):
    return [i[0] for i in critiques[person].items() if pd.isna(i[1])]


def global_score(person, movie, critiques):
    total_score = 0
    s_score = 0
    for critique in critiques.items():
        if not pd.isna(critique[1][movie]):
            total_score += critique[1][movie] / (1+sim_distanceManhattan(critiques[person], critique[1]))
            s_score += 1 / (1+sim_distanceManhattan(critiques[person], critique[1]))
    return total_score / s_score


def global_score_exp(person, movie, critiques):
    total_score = 0
    s_score = 0
    for critique in critiques.items():
        if not pd.isna(critique[1][movie]):
            total_score += critique[1][movie] * pow(math.e, -1*sim_distanceManhattan(critiques[person], critique[1]))
            s_score += pow(math.e, -1*sim_distanceManhattan(critiques[person], critique[1]))
    return total_score / s_score


def Bestrecommend(person, critiques):
    recommend = [(global_score(person, movie, critiques), movie) for movie in unwatchlist(person, critiques)]
    if recommend:
        return sorted(recommend)[-1]
    return None


def BestrecommendwithExp(person, critiques):
    recommend = [(global_score_exp(person, movie, critiques), movie) for movie in unwatchlist(person, critiques)]
    if recommend:
        return sorted(recommend)[-1]
    return None


# Question 2d
def pearson(person1, person2):
    sum_xy = 0
    sum_x, sum_y = 0, 0
    sum_x2, sum_y2 = 0, 0
    n = 0
    for key in person1:
        if key in person2:
            n += 1
            if not (pd.isna(person1[key]) or pd.isna(person2[key])):
                x, y = person1[key], person2[key]
                sum_xy += x*y
                sum_x += x
                sum_y += y
                sum_x2 += x**2
                sum_y2 += y**2
            else:
                continue
    denominator = pow(sum_x2 - (sum_x**2) / n, 0.5) * pow(sum_y2 - (sum_y**2) / n, 0.5)
    if denominator == 0:
        return 0
    else:
        return (sum_xy - (sum_x * sum_y) / n) / denominator


def global_score_pearson(person, movie, critiques):
    total_score = 0
    s_score = 0
    for critique in critiques.items():
        if not pd.isna(critique[1][movie]):
            total_score += critique[1][movie] / (1+pearson(critiques[person], critique[1]))
            s_score += 1 / (1+pearson(critiques[person], critique[1]))
    return total_score / s_score


def PearsonRecommend(person, critiques):
    recommend = [(global_score_pearson(person, movie, critiques), movie) for movie in unwatchlist(person, critiques)]
    if recommend:
        return sorted(recommend)[-1]
    return None


# Question 2e
def cosine(person1, person2):
    sum_xy = 0
    sum_x2, sum_y2 = 0, 0
    n = 0
    for key in person1:
        if key in person2:
            n += 1
            if not (pd.isna(person1[key]) or pd.isna(person2[key])):
                x, y = person1[key], person2[key]
                sum_xy += x*y
                sum_x2 += x**2
                sum_y2 += y**2
            else:
                continue
    denominator = pow(sum_x2, 0.5) * pow(sum_y2, 0.5)
    if denominator == 0:
        return 0
    else:
        return sum_xy / denominator


def global_score_cosine(person, movie, critiques):
    total_score = 0
    s_score = 0
    for critique in critiques.items():
        if not pd.isna(critique[1][movie]):
            total_score += critique[1][movie] / (1+cosine(critiques[person], critique[1]))
            s_score += 1 / (1+cosine(critiques[person], critique[1]))
    return total_score / s_score


def CosineRecommend(person, critiques):
    recommend = [(global_score_cosine(person, movie, critiques), movie) for movie in unwatchlist(person, critiques)]
    if recommend:
        return sorted(recommend)[-1]
    return None


def global_score_euclidienne(person, movie, critiques):
    total_score = 0
    s_score = 0
    for critique in critiques.items():
        if not pd.isna(critique[1][movie]):
            total_score += critique[1][movie] / (1+sim_distanceEuclidienne(critiques[person], critique[1]))
            s_score += 1 / (1+sim_distanceEuclidienne(critiques[person], critique[1]))
    return total_score / s_score


def EuclidienneRecommend(person, critiques):
    recommend = [(global_score_cosine(person, movie, critiques), movie) for movie in unwatchlist(person, critiques)]
    if recommend:
        return sorted(recommend)[-1]
    return None


def nth_root(value, n_root):
    root_value = 1 / float(n_root)
    return round(Decimal(value) ** Decimal(root_value), 3)


def minkowski_distance(x, y, p_value):
    return nth_root(sum(pow(abs(a - b), p_value) for a, b in zip(x, y)), p_value)


def minkowski(person1, person2, p_value=3):
    movie_1 = dict([movie for movie in person1.items() if not pd.isna(movie[1])])
    movie_2 = dict([movie for movie in person2.items() if not pd.isna(movie[1])])
    movie_12 = [movie for movie in movie_1 if movie in movie_2]
    rating_1 = [round(person1[movie]) for movie in movie_12]
    rating_2 = [round(person2[movie]) for movie in movie_12]
    return minkowski_distance(rating_1, rating_2, p_value)


def global_score_minkowski(person, movie, critiques):
    total_score = 0
    s_score = 0
    for critique in critiques.items():
        if not pd.isna(critique[1][movie]):
            total_score += critique[1][movie] / (1+minkowski(critiques[person], critique[1]))
            s_score += 1 / (1+minkowski(critiques[person], critique[1]))
    return total_score / s_score


def MinkowskiRecommend(person, critiques):
    recommend = [(global_score_cosine(person, movie, critiques), movie) for movie in unwatchlist(person, critiques)]
    if recommend:
        return sorted(recommend)[-1]
    return None


if __name__ == '__main__':
    critiques = pd.read_csv("rating.csv", index_col=0).to_dict()
    # print(critiques)

    # Question 2a
    print("For Question 2a:")
    print("The Euclidean distance between Lisa and Gene is")
    print(sim_distanceEuclidienne(critiques['Lisa'], critiques['Gene']))

    print()
    print("=========================================")

    # Question 2b
    print("For Question 2b:")

    print("Lisa's Nearest Nerighbor is \n {}".format(computeNearestNeighbor('Lisa', critiques)))
    print("Lisa's Recommend Nearest Nerighbor is \n {}".format(recommendNearestNeighbor('Lisa', critiques)))

    print()

    print("Toby's Nearest Nerighbor is \n {}".format(computeNearestNeighbor('Toby', critiques)))
    print("Toby's Recommend Nearest Nerighbor is \n {}".format(recommendNearestNeighbor('Toby', critiques)))

    print()
    print("=========================================")

    # Question 2ci
    print("For Question 2ci:")
    print("By using Manhattan distances,")
    print("Suggest to Anne:")
    print(Bestrecommend('Anne', critiques))

    print()

    print("By using Euclidean distances,")
    print("Suggest to Anne:")
    print(EuclidienneRecommend('Anne', critiques))

    print()
    print("=========================================")

    # For Question 2cii
    print("For Question 2cii:")
    print("By using Manhattan distances and replacing the weights,")
    print("Suggest to Anne:")
    print(BestrecommendwithExp('Anne', critiques))

    print()
    print("=========================================")
    # Question 2d
    print("For Question 2d:")
    print("By using Pearson correlation coefficient,")
    print("Suggest to Anne:")
    print(PearsonRecommend('Anne', critiques))

    print()
    print("=========================================")
    # Question 2e
    print("For Question 2d:")
    print("By using Cosine correlation coefficient,")
    print("Suggest to Anne:")
    print(CosineRecommend('Anne', critiques))

    # Question 3
    print("For Question 3:")
    music = pd.read_csv("music.csv", index_col=0).to_dict()
    # print(music)

    print("For Veronica:")
    print("By using Manhattan distances,")
    print("Suggest to Veronica:")
    print(Bestrecommend("Veronica", music))
    print()

    print("By using Euclidean distances,")
    print("Suggest to Veronica:")
    print(EuclidienneRecommend('Veronica', music))
    print()

    print("By using Manhattan distances and replacing the weights,")
    print("Suggest to Veronica:")
    print(BestrecommendwithExp("Veronica", music))
    print()

    print("By using Pearson correlation coefficient,")
    print("Suggest to Veronica:")
    print(PearsonRecommend("Veronica", music))
    print()

    print("By using Cosine correlation coefficient,")
    print("Suggest to Veronica:")
    print(CosineRecommend("Veronica", music))
    print()
    print("=========================================")

    print("For Hailey:")
    print("By using Manhattan distances,")
    print("Suggest to Hailey:")
    print(Bestrecommend("Hailey", music))
    print()

    print("By using Euclidean distances,")
    print("Suggest to Hailey:")
    print(EuclidienneRecommend("Hailey", music))
    print()

    print("By using Manhattan distances and replacing the weights,")
    print("Suggest to Hailey:")
    print(BestrecommendwithExp("Hailey", music))
    print()

    print("By using Pearson correlation coefficient,")
    print("Suggest to Hailey:")
    print(PearsonRecommend("Hailey", music))
    print()

    print("By using Cosine correlation coefficient,")
    print("Suggest to Hailey:")
    print(CosineRecommend("Hailey", music))
    print()
    print("=========================================")

    # Question 4
    print("For Question 4:")
    random_matrix = pd.read_csv("random_matrix.csv", index_col=0).to_dict()

    print("By using Manhattan distances,")
    print("Suggest to Person 1:")
    print(Bestrecommend("Person 1", random_matrix))
    print()

    print("By using Euclidean distances,")
    print("Suggest to Person 1:")
    print(EuclidienneRecommend("Person 1", random_matrix))
    print()

    print("By using Pearson correlation coefficient,")
    print("Suggest to Person 1:")
    print(PearsonRecommend("Person 1", random_matrix))
    print()

    print("By using Cosine correlation coefficient,")
    print("Suggest to Person 1:")
    print(CosineRecommend("Person 1", random_matrix))
    print()

    print("By using Minkowski distances,")
    print("Suggest to Person 1:")
    print(MinkowskiRecommend("Person 1", random_matrix))
    print()