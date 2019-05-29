import codecs
from operator import itemgetter

file1 = codecs.open("artists.dat", encoding="utf-8")
file1.readline()  # skip the first line
aid2name = {}  # a new dictionary to store artistID and name
aid_list = []

for line in file1:  # process each line in the artist file
    line = line.strip()
    fields1 = line.split('\t')
    aid = int(fields1[0])
    name = fields1[1]
    aid2name[aid] = name  # aid as key and name as value
    aid_list.append(aid)


file2 = codecs.open("user_artists.dat", encoding="utf-8")
file2.readline()  # skip the first line

uid2numplays = {}  # a new dictionary to store userID and total numplays by each user
aid2numplays = {}  # a new dictionary to store artistID and total numplays of the artist

u_numplays = {}  # a new dictionary to store userID and lists of numplays by each user
a_numplays = {}  # a new dictionary to store artistID and lists of numplays by each user

aid2listeners = {}  # a new dictionary to store artistID and num of listeners
a_listeners = {}  # a new dictionary to store artistID and listenerID

average_num_plays = {}  # a new dictionary to store artistID and average number of plays per listener for each artist
average_num_plays_50 = {}  # a new dictionary to store artistID of those who have at least 50 listeners and average
    # number of plays per listener for each artist

for line in file2:  # process each line in the user file
    line = line.strip()
    fields2 = line.split('\t')
    uid = int(fields2[0])
    aid = int(fields2[1])
    numplays = int(fields2[2])

    u_numplays.setdefault(uid, []).append(numplays)  # uid as key and list of numplays as value
    a_numplays.setdefault(aid, []).append(numplays)  # aid as key and list of numplays as value
    a_listeners.setdefault(aid, []).append(uid)  # aid as key and list of uid as value


file3 = codecs.open("user_friends.dat", encoding="utf-8")
file3.readline()  # skip the first line

u_friends = {}  # a new dictionary to store userID and lists of friendID of this user
u_f_num = {}  # a new dictionary to store userID and the number of friends of this user

for line in file3:  # process each line in the friends file
    line = line.strip()
    fields3 = line.split('\t')
    uid = int(fields3[0])
    fid = int(fields3[1])  # get the friendID

    u_friends.setdefault(uid, []).append(fid)  # uid as key and list of friendID as value

for key in u_numplays:
    v_list = list(u_numplays.get(key))  # turn the value tuple into a list
    total_num = 0
    for num in v_list:
        total_num = total_num + num  # add up the total numplays of each user
    uid2numplays.setdefault(key, total_num)  # uid as key and total numplays of each user as value

sorted_u = sorted(uid2numplays.items(), key = itemgetter(1), reverse = True)  # create a sorted version of uid2numplays,
    # in descending order

for key2 in a_numplays:
    v_list2 = list(a_numplays.get(key2))  # turn the value tuple into a list
    total_num2 = 0
    for num2 in v_list2:
        total_num2 = total_num2 + num2  # add up the total numplays of each artist
    aid2numplays.setdefault(key2, total_num2)  # aid as key and total numplays of each artist as value

sorted_a = sorted(aid2numplays.items(), key = itemgetter(1), reverse = True)  # create a sorted version of aid2numplays,
    # in descending order

for key3 in a_listeners:
    listener_num = len(a_listeners.get(key3))  # the length of each value list equals the total num of listeners of
        # each artist
    aid2listeners.setdefault(key3, listener_num)

sorted_l = sorted(aid2listeners.items(), key = itemgetter(1), reverse = True)  # create a sorted version of
    # aid2listeners, in descending order

for key4 in aid2numplays:
    average_num = aid2numplays.get(key4) / aid2listeners.get(key4)  # the average num equals to num of total plays
    # divided by num of listeners
    average_num_plays.setdefault(key4, average_num)
    if aid2listeners.get(key4) >= 50:  # if the artist have at least 50 listeners, then add it to the
        # average_num_play_50 dictionary
        average_num_plays_50.setdefault(key4, average_num)

sorted_n = sorted(average_num_plays.items(), key = itemgetter(1), reverse = True)  # create a sorted version of
    # average_num_play, in descending order

sorted_n_50 = sorted(average_num_plays_50.items(), key = itemgetter(1), reverse = True)  # create a sorted version of
    # average_num_play_50, in descending order


total_num3 = 0  # the total number of song plays by users who have five or more friends
total_num4 = 0  # the total number of song plays by users who have less than five friends
u_5plus_averageplay = 0  # the average number of song plays by users who have >=5 friends
u_5less_averageplay = 0  # the average number of song plays by users who have <5 friends
v_list3 = []  # get a list of numbers of song plays by users who have >= 5 friends
v_list4 = []  # get a list of numbers of song plays by users who have <5 friends

for key5 in u_friends:
    friend_num = len(u_friends.get(key5))  # the length of each value list equals the total num of friends of this user
    u_f_num.setdefault(key5, friend_num)

    if friend_num >= 5:
        v_list3.append(uid2numplays.get(key5))
        for num3 in v_list3:  # get a list of total number of plays by each user
            total_num3 = total_num3 + num3
        u_5plus_averageplay = total_num3 / len(v_list3)

    else:
        v_list4.append(uid2numplays.get(key5))
        for num4 in v_list4:  # get a list of total number of plays by each user
            total_num4 = total_num4 + num4
        u_5less_averageplay = total_num4 / len(v_list4)


sorted_f = sorted(u_f_num.items(), key = itemgetter(1), reverse = True)  # create a sorted version of u_f_m,
    # in descending order


def artist_sim(aid1, aid2):  # function to compare the similarity between two artists
    u_list1 = a_listeners.get(aid1)  # get the list of listeners of the first artist
    u_list2 = a_listeners.get(aid2)  # get the list of listeners of the second artist
    inter_list = []  # a new list of intersection part
    union_list = []  # a new list of union part
    for n in u_list1:
        if n in u_list2:  # if user in list1 but not in list2, append to intersection list
            inter_list.append(n)
            union_list.append(n)  # append all users in list1 and list2 to union list
        else:
            union_list.append(n)
    jaccard_index = len(inter_list) / len(union_list)  # compute the jaccard index using the length of two lists
    print("\t", aid2name.get(aid1), ",", aid2name.get(aid2), '%.2f'% jaccard_index)



# print Q1
print("\n")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("\n")
print("1. Who are the top artists?")
for i in sorted_a[:10]:
    print("\t", aid2name.get(i[0]), "(", i[0], ")", aid2numplays.get(i[0]))

# print Q2
print("\n")
print("2. What artists have the most listeners?")
for i in sorted_l[:10]:
    print("\t", aid2name.get(i[0]), "(", i[0], ")", aid2listeners.get(i[0]))

# print Q3
print("\n")
print("3. Who are the top users?")
for i in sorted_u[:10]:
    print("\t", i[0], i[1])

# print Q4
print("\n")
print("4. What artists have the highest average number of plays per listener?")
for i in sorted_n[:10]:
    print("\t", aid2name.get(i[0]), "(", i[0], ")", aid2numplays.get(i[0]), aid2listeners.get(i[0]), '%.2f'%i[1])

# print Q5
print("\n")
print("5. What artists with at least 50 listeners have the highest average number of plays per listener?")
for i in sorted_n_50[:10]:
    print("\t", aid2name.get(i[0]), "(", i[0], ")", aid2numplays.get(i[0]), aid2listeners.get(i[0]), '%.2f'%i[1])

# print Q6
print("\n")
print("6. Do users with five or more friends listen to more songs?")
print("Users with five or more friends --")
print("\t", "the total number of song they plays:")
print("\t", total_num3)

print("\t", "the average number of song they plays:")
print("\t", '%.2f'%u_5plus_averageplay)

print("Users with less than five friends --")
print("\t", "the total number of song they plays:")
print("\t", total_num4)

print("\t", "the average number of song they plays:")
print("\t", '%.2f'%u_5less_averageplay)


# print Q7
print("\n")
print("7. How similar are two artists?")
artist_sim(735,562)
artist_sim(735,89)
artist_sim(735,289)
artist_sim(89,289)
artist_sim(89,67)
artist_sim(67,735)


