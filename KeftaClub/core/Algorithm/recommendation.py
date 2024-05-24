from datetime import datetime, timedelta

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
            common_friends_map[friend] = length

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


def number_of_like_from_user_by_post(graph, post_graph, like_post, user):
    """This function takes in argument a graph that link the user with the post
    he liked. And those post are also linked with the user who posted it.
    By using the number_of_common_friends_map function, we can attribute to each
    friend the number of likes he got from the user.
    Based on that, we are going to return a map that attribute to each post
    the number of like each friend got from the user"""
    
    all_friends = friends(graph, user)
    
    liked_posts = user_posts(like_post, user)
    
    friend_likes_map = {}
    
    for friend in all_friends:
        friend_likes_map[friend] = len(liked_posts.intersection(user_posts(post_graph, friend)))
    
    like_influence_per_post = {}
    
    #initialise 0 for all the friends posts (because maybe you haven't already liked a single of your friend post)
    for friend in all_friends:
        for post in user_posts(post_graph, friend):#get each post from all friends
            like_influence_per_post[post] = 0 # initialise each post to 0
    
    #now we enter the real loop that will attribute a number of like to each post
    for friend in friend_likes_map:
        for post in user_posts(post_graph, friend):#get each post from each friend
            like_influence_per_post[post] = friend_likes_map[friend] # give to each post the score of the friend
        
    
    return like_influence_per_post


def recommend_by_number_of_like_per_user_posts(graph, post_graph, like_post, user):
    """Return a list of post recommendations for the given user based on the total number
    of likes the user gave to his friend.
    """
    return number_map_to_sorted_list(number_of_like_from_user_by_post(graph, post_graph, like_post, user))



def recommend_by_number_of_like(post_like_map):
    """Return a list of post recommendations based on the number of like of each post. 
    in other word, popularity, in other words, hold my hand, in other word, darling kiss me.
    Fill my heart with song And let me sing for ever more.
    You are all I long for, All I worship and adore.
    In other words, please be true, In other words, I love you
    """
    return number_map_to_sorted_list(post_like_map)


def number_of_common_interest_with_post(graph, interest_graph, post_graph, post_interest_graph, user):
    """Return a map where each post get assigned the number of common interest
    it has with the user
    """
    all_friends = friends(graph, user)
    
    user_interest = interests(interest_graph, user)
    
    friends_posts = set()
    
    for friend in all_friends:
        friends_posts.update(user_posts(post_graph, friend))
    
    common_interest_post_map = {}
    
    for post in friends_posts:
        common_interest_post_map[post] = len(user_interest.intersection(interests(post_interest_graph, post)))
        
        
    return common_interest_post_map
        

def recommend_by_common_interest_with_post(graph, interest_graph, post_graph, post_interest_graph, user):
    """Return a list of post recommendations based on the number of common interest
    you share with the post.
    """
    return number_map_to_sorted_list(number_of_common_interest_with_post(graph, interest_graph, post_graph, post_interest_graph, user))



def recommend_by_publication_date(nb_hours_pub_date_map):
    """Return a list of post recommendations based on the publication date.
    The most recent will be first, the oldest will be last.
    """
    return number_map_to_sorted_list(nb_hours_pub_date_map)[::-1]#to reverse order
   

def calculate_hours_since_post(posts_dates):
    """
    Takes a dictionnary with post id as key and publication date as value and
    returns a dictionnary with post id as key and number of hours since it was posted
    """
    
    current_time = datetime.now()
    hours_since_post = {}
    
    for post_id, post_date in posts_dates:
        post_datetime = datetime.strptime(post_date, "%Y-%m-%d %H:%M:%S")
        delta = current_time - post_datetime
        hours_since_post[post_id] = delta.total_seconds() // 3600  # Convert seconds to hours
    
    return hours_since_post


###### FINAL ALGORITHMS #######

def friends_recommandation_algorithm(graph, interest_graph, user):
    """Return the final list of recommanded user based on the mean result of 
    - The rif algorithm.
    - The rcf algorithm.
    - The rfi algorithm.
    The function also returns the number of common friend and the number of
    common interest shared with the recommanded users
    """
    
    rcf_map = number_of_common_friends_map(graph, user)
    rfi_map = number_of_common_interest_map(graph, interest_graph, user)
    
    rcf_result = recommend_by_number_of_common_friends(graph, user) 
    rif_result = recommend_by_influence(graph, user) 
    rfi_result = recommend_by_common_friends_interest(graph, interest_graph, user) 
    
    all_result = [rcf_result, rif_result, rfi_result]
    
    moyennes = {x: sum(i for l in all_result for i, y in enumerate(l) if y == x) / len(all_result) for x in set().union(*all_result)}
    
    return sorted(moyennes, key=moyennes.get), rcf_map, rfi_map
       
    

def posts_recommandation_algorithm(graph, interest_graph, user_post_graph, like_post_graph, post_category_graph,post_likes_count, posts_date, user):
    """Return the final list of recommanded user based on the mean result of 
    - The rlp algorithm. (recommend_by_number_of_like_per_user_posts)
    - The rnl algorithm. (recommend_by_number_of_like)
    - The rip algorithm. (recommend_by_common_interest_with_post)
    - The rpd algorithm. (recommend_by_publication_date)
    The function also returns the number of common friend and the number of
    common interest shared with the recommanded users
    """

    rlp_result = recommend_by_number_of_like_per_user_posts(graph,user_post_graph,like_post_graph, user) # nb like de toi
    rnl_result = recommend_by_number_of_like(post_likes_count) 
    rip_result = recommend_by_common_interest_with_post(graph, interest_graph, user_post_graph, post_category_graph, user) 
    
    first_step_posts = [rlp_result, rnl_result, rip_result]
    
    #Mean of the first 3 lists
    first_step_ranking = {x: sum(i for l in first_step_posts for i, y in enumerate(l) if y == x) / len(first_step_posts) for x in set().union(*first_step_posts)}
    first_ranking = sorted(first_step_ranking, key=first_step_ranking.get)
    
    #Date ranking list
    rpd_result = recommend_by_publication_date(calculate_hours_since_post(posts_date)) 
    print(rpd_result)

    
    final_step_posts = [first_ranking, rpd_result]
    
    #Final Mean of the 2 lists
    final_step_ranking = {x: sum(i for l in final_step_posts for i, y in enumerate(l) if y == x) / len(final_step_posts) for x in set().union(*final_step_posts)}
    final_ranking = sorted(final_step_ranking, key=final_step_ranking.get)

    return final_ranking
    
    
    
    
    
    
    
    