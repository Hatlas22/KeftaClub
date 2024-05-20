

def friends(graph, user):
    """Returns a set of the friends of the given user, in the given graph"""
    return set(graph.neighbors(user))


def friends_of_friends(graph, user):
    """Returns a set of friends of friends of the given user, in the given graph.
    The result does not include the given user nor any of that user's friends.
    """
    user_friends = friends(graph, user)
    user_friends_of_friends = set()

    for friend in user_friends:
        user_friends_of_friends.update(friends(graph, friend) - user_friends)

    return user_friends_of_friends - {user}


def common_friends(graph, user1, user2):
    """Returns the set of friends that user1 and user2 have in common."""
    return friends(graph, user1).intersection(friends(graph, user2))


def number_of_common_friends_map(graph, user):
    """Returns a map from each user U to the number of friends U has in common with the given user.
    The map keys are the users who have at least one friend in common with the
    given user, and are neither the given user nor one of the given user's friends.
    Take a graph G for example:
        - A and B have two friends in common
        - A and C have one friend in common
        - A and D have one friend in common
        - A and E have no friends in common
        - A is friends with D
    number_of_common_friends_map(G, "A")  =>   { 'B':2, 'C':1 }
    """
    common_friends_map = {}
    user_friends = friends_of_friends(graph, user)

    for friend in user_friends:
        length = len(common_friends(graph, user, friend))
        if length >= 1:
            common_friends_map[friend] = length / len(friends(graph, friend))

    return common_friends_map

def number_of_common_friends_ratio_map(graph, user):
    """Returns a map from each user U to the ratio between U common friends with the given user / U total number of friends
    The map keys are the users who have at least one friend in common with the
    given user, and are neither the given user nor one of the given user's friends.
    Take a graph G for example:
        - A and B have 1/5 friends in common
        - A and C have 1/10 friends in common
        - A and D have 5/100 friends in common
    number_of_common_friends_map(G, "A")  =>   { 'B': 0.2, 'C': 0.1 }
    """
    common_friends_map = {}
    user_friends = friends_of_friends(graph, user)

    for friend in user_friends:
        length = len(common_friends(graph, user, friend))
        if length >= 1:
            common_friends_map[friend] = round((length/ len(friends(graph, friend))), 4)

    return common_friends_map


def number_map_to_sorted_list(friend_map):
    """Given a map whose values are numbers, return a list of the keys.
    The keys are sorted by the number they map to, from greatest to least.
    When two keys map to the same number, the keys are sorted by their
    natural sort order, from least to greatest.
    """
    return [v[0] for v in sorted(friend_map.items(), key=lambda kv: (-kv[1], kv[0]))]


def recommend_by_number_of_common_friends(graph, user):
    """Return a list of friend recommendations for the given user.
    The friend recommendation list consists of names of people in the graph
    who are not yet a friend of the given user.
    The order of the list is determined by the number of common friends.
    """
    return number_map_to_sorted_list(number_of_common_friends_ratio_map(graph, user))


def influence_map(graph, user):
    """Returns a map from each user U to the friend influence, with respect to the given user.
    The map only contains users who have at least one friend in common with U,
    and are neither U nor one of U's friends.
    See the assignment for the definition of friend influence.
    """
    user_friends_of_friends = friends_of_friends(graph, user)
    friend_influence_map = {}

    for friend in user_friends_of_friends:
        user_common_friends = common_friends(graph, user, friend)
        if len(user_common_friends) >= 1:
            friend_influence_map[friend] = sum(
                [1 / len(friends(graph, val)) for val in user_common_friends]
            )

    return friend_influence_map


def recommend_by_influence(graph, user):
    """Return a list of friend recommendations for the given user.
    The friend recommendation list consists of names of people in the graph
    who are not yet a friend of the given user.
    The order of the list is determined by the influence measurement.
    """
    return number_map_to_sorted_list(influence_map(graph, user))

#####

def interests(interest_graph, user):
    """Returns a set of the interests of the given user, in the given interest graph"""
    return set(interest_graph.neighbors(user))
    


def number_of_common_interest_map(graph, interest_graph, user):
    """
    Returns a map for each friend of friend of the User U
    based on the common interests they share, the friend will
    recieve a value between 1 & 4.
    1 if they share no interest 4 if they share all interests.
    """
    
    common_interest_map = {}
    user_friends = friends_of_friends(graph, user)
    
    user_interest = interests(interest_graph, user)
    
    for friend in user_friends:
        length = len(common_friends(graph, user, friend))
        if length >= 1:
            common_interest_map[friend] = 1+ len(user_interest.intersection(interests(interest_graph, friend)))
            
    return common_interest_map
        
    
def recommend_by_common_friends_interest(graph, interest_graph, user):
    """Return a list of friend recommendations for the given user.
    The friend recommendation list consists of names of people in the graph
    who are not yet a friend of the given user.
    The order of the list is determined by the number of common interest they share.
    """
    return number_map_to_sorted_list(number_of_common_interest_map(graph, interest_graph, user))



####

def user_posts(post_graph, user):
    """Returns a set of the posts of the given user, in the given post graph"""
    return set(post_graph.neighbors(user))


def recommend_posts_by_friend_relation(graph, post_graph, user):
    user_friend = friends(graph, user)
    user_foaf = friends_of_friends(graph, user)
    
    friend_score_map = {}
    
    for friend in user_friend:
        friend_score_map 
        
    #Pas fini
    return
    
    
    