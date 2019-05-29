# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#cd /Users/ltl/Desktop/2018-Spring/490/Project2/data

from pandas import Series, DataFrame
import pandas as pd

####################################################################
# Data Loading. 
    # load relevant .dat files into different dataframe.
    # use groupby and relevant function like value_counts etc. to get several Series that will be used for answering questions.
        # apn : total play number of an artist with aid(artistID) as index
        # aln : total listener number of an artist with aid(artistID) as index
        # upn : total play number of an user with uid(userID) as index
        # ufn : total friend number of an user with uid(userID) as index
        # atn : total tag number of an artist with aid(artistID) as index
####################################################################

artists_df = pd.read_table('artists.dat', encoding="utf-8", sep="\t", index_col='id')
user_artists_df = pd.read_table('user_artists.dat', encoding="utf-8", sep="\t")
user_artists_df.columns = ['uid','aid','play_num']
user_friends_df = pd.read_table('user_friends.dat', encoding="utf-8", sep="\t")
user_friends_df.columns = ['uid','fid']
tag_info_df = pd.read_table('user_taggedartists.dat', encoding="utf-8", sep="\t")
tag_info_df.columns = ['uid', 'aid', 'tid', 'day', 'month', 'year']


apn = user_artists_df.groupby('aid').sum()['play_num']
aln = user_artists_df['aid'].value_counts()
upn = user_artists_df.groupby('uid').sum()['play_num']
ufn = user_friends_df['uid'].value_counts()
atn = tag_info_df['tid'].groupby(tag_info_df.aid).count()


####################################################################
# Q1. Who are the top artists? 
    # sort Series "apn" in a descending order and print the top 10.
####################################################################

print('\n'+'!'*40 +'\n')
print('1. Who are the top artists?\n')
#top10 artists' play number
apn_top10 = apn.sort_values(ascending=False).head(10)
for aid in apn_top10.index:
    print("\t"+str(artists_df.name[aid])+"("+str(aid)+")\t"+str(apn_top10[aid]))


####################################################################
# Q2. What artists have the most listeners?
    # sort Series "aln" in a descending order and print the top 10.
####################################################################
    
print('\n'+'!'*40 +'\n')
print('2. What artists have the most listeners?\n')
#top10 artists' user number
aln_top10 = aln.head(10)
for aid in aln_top10.index:
    print('\t'+str(artists_df.name[aid])+"("+str(aid)+")\t"+str(aln_top10[aid]))


####################################################################
# Q3. Who are the top users?
    #  sort Series "upn" in a descending order and print the top 10.
####################################################################
    
print('\n'+'!'*40 +'\n')
print('3. Who are the top users?\n')
#top10 users' play number
upn_top10 = upn.sort_values(ascending=False).head(10)
for uid in upn_top10.index:
    print("\t" + str(uid) +'\t'+ str(upn_top10[uid]))


####################################################################
# Q4. What artists have the highest average number of plays per listener?
    # convert Series "aln" and "apn" into DataFrame Type
    # merge "aln_df" and "apn_df" as a new "ainfo_df"
        # ainfo_df use aid as index
        # columns "play_num" and "user_num"
    # add a new column "user_avg_play" by "play_num" divided by "user_num"
    # sort ainfo_df by "user_avg_play" and get the top 10 to print out
####################################################################
    
print('\n'+'!'*40 +'\n')
print('4. What artists have the highest average number of plays per listener?\n')

aln_df = DataFrame(aln.values, index=aln.index)
aln_df.columns = ['user_num']
apn_df = DataFrame(apn.values, index=apn.index)
apn_df.columns = ['play_num']

# ainfo_df : a dataframe that contains information of an artist including columns: play_num, user_num
ainfo_df = aln_df.join(apn_df)
ainfo_df['user_avg_play'] = ainfo_df['play_num']/ainfo_df['user_num']
a_avg_top10 = ainfo_df.sort_values(by='user_avg_play', ascending=False).head(10)

for aid in a_avg_top10.index:
    print('\t' + str(artists_df.name[aid]) +" ("+str(aid)+")")
    print('\tTotal number of plays: '+str(a_avg_top10.play_num[aid]))
    print('\tTotal number of listeners: '+str(a_avg_top10.user_num[aid]))
    print('\tAverage number of plays per listener: '+str(int(round(a_avg_top10.user_avg_play[aid])))+'\n')


####################################################################
# Q5. What artists with at least 50 listeners have the highest average number of plays per listener?
    # very similar to Q4.
    # the only difference is use ainfo_df.user_num>50 to get artists with at least 50 listeners before sort and print.
####################################################################
    
print('\n'+'!'*40 +'\n')
print('5. What artists with at least 50 listeners have the highest average number of plays per listener?\n')
#a50_avg = 
a50_avg_top10 = ainfo_df[ainfo_df.user_num>50].sort_values(by='user_avg_play', ascending=False).head(10)
for aid in a50_avg_top10.index:
    print('\t' + str(artists_df.name[aid]) +" ("+str(aid)+")")
    print('\tTotal number of plays: '+str(a50_avg_top10.play_num[aid]))
    print('\tTotal number of listeners: '+str(a50_avg_top10.user_num[aid]))
    print('\tAverage number of plays per listener: '+str(int(round(a50_avg_top10.user_avg_play[aid])))+'\n')


####################################################################
# Q6. Do users with five or more friends listen to more songs?
    # convert Series ufn into a DataFrame ufn_df
    # using "ufn_df.friend_num" to classify users has >=5 friends or <5 friends.
        # ufn5_yes
        # ufn5_no
    # using for loop to calculate the total number of plays of two group of users
        # ufn5_yes_plays
        # ufn5_no_plays
    # calculate average number of plays per user of two groups:
        # avg5_yes = ufn5_yes_plays/len(ufn5_yes)
        # avg5_no = ufn5_no_plays/len(ufn5_no)
    # compare "avg5_yes" and "avg5_no" and print out conclusion.
####################################################################
    
print('\n'+'!'*40 +'\n')
print('6. Do users with five or more friends listen to more songs?\n')

ufn_df = DataFrame(ufn.values, index=ufn.index)
ufn_df.columns = ['friend_num']
ufn5_yes = ufn_df[ufn_df.friend_num>=5]
ufn5_no = ufn_df[ufn_df.friend_num<5]

# calculate the total number of two group of users
ufn5_yes_plays = 0
ufn5_no_plays = 0
for uid in ufn5_yes.index:
    ufn5_yes_plays += upn[uid]
for uid in ufn5_no.index:
    ufn5_no_plays += upn[uid]
avg5_yes = int(round(ufn5_yes_plays/len(ufn5_yes)))
avg5_no = int(round(ufn5_no_plays/len(ufn5_no)))


print('\tAverage number of song plays for users who have 5 friends or more:\t' + str(avg5_yes))
print('\tAverage number of song plays for users who have less than 5 friends:\t' + str(avg5_no))
if avg5_yes <= avg5_no:
    print('\tIt is false that users with five or more friends listen to more songs.')
else:
    print('\tIt is ture that users with five or more friends listen to more songs.')


####################################################################
# Q7. How similar are two artists?
    # store all users ids of each artist into independent set
    # using "set1 & set2" to get the intersection of two uid sets
    # using "set1 & set2" to get all nonredundant uid in two sets
    # calulate Jaccard and print out
####################################################################
    
print('\n'+'!'*40 +'\n')
print('7. How similar are two artists? \n (decimals are the Jaccard similarity between 2 artists)\n')

def artist_sim(aid1, aid2):
    uid1 = set(user_artists_df[user_artists_df.aid==aid1].uid.values)
    uid2 = set(user_artists_df[user_artists_df.aid==aid2].uid.values)
    sim = len(uid1 & uid2) / len(uid1 | uid2)
    print('\t' + str(artists_df.name[aid1])+'    '+str(artists_df.name[aid2])+'    '+str(sim))

artist_sim(735,562)
artist_sim(735,89)
artist_sim(735,289)
artist_sim(89,289)
artist_sim(89,67)
artist_sim(67,735)


####################################################################
# Q8. Analysis of top tagged artists:
    # atn_top10: a Series of top 10 artists with most overall tag numbers. index: aid
    # atn_permonth: a Series represents the total tag number of an artist in a specific year and month.
        # multiple index: year, month, aid from level 0 to level 2.
        # value: total tag number.
    # ym: a Series aim to get "year, month" in order.
        # Here, values are not important because I just want index of ym -- year, month.
    # month is a list of Month name used to translate month number to required sting to print.
    # top10_rank_dic is a dictionary:
        # key: (year, month) tuple
        # value: a list of artist ids of artists who are in the top10 list of this (year, month)
    # in10 is a function aims to:
        # input: (aid, the dictionary top10_rank_dic)
        # output: (times, ymIn10)
            # times: the number of months artist with aid was in the top 10 in terms of number of tags
                # type: int
                # if aid in dic[key], times will add 1.
            # ymIn10 is the list of (year, month) tuples.
                # type: list
                # (year, month) were the time artist with aid entered the top 10 in terms of number of tags
    # during printing:
        # res: (times, ymIn10)
        # res[0]: times
        # res[1]: ymIn10
        # res[1][0]: first time (year, month) artist with aid entered the top 10
        # res[1][0][0]: year
        # res[1][0][1]: month - number
        # month[res[1][0][1]-1]: month - name string
####################################################################

print('\n'+'!'*40 +'\n')
print('8. Analysis of top tagged artists:\n')

atn_top10 = atn.sort_values(ascending = False).head(10)  
atn_permonth = tag_info_df['tid'].groupby([tag_info_df.year, tag_info_df.month, tag_info_df.aid]).count()
ym = tag_info_df['tid'].groupby([tag_info_df.year, tag_info_df.month]).count()
month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

top10_rank_dic = {}
for i in range(len(ym)):
    top10_rank_dic[ym.index[i]] = list(atn_permonth[ym.index[i][0]][ym.index[i][1]].sort_values(ascending =False).head(10).index)

def in10(aid, dic):
    times = 0
    ymIn10 = []
    for key in dic.keys():
        if aid in dic[key]:
            times += 1
            ymIn10.append(key)
    return times, ymIn10

for aid in atn_top10.index:
    res = in10(aid, top10_rank_dic)
    print('\t'+str(artists_df.name[aid])+"("+str(aid)+")\tnum tags = "+ str(atn_top10[aid]))
    print('\t\tFirst month in top10 = ' + month[res[1][0][1]-1] +' ' + str(res[1][0][0]))
    print('\t\tMonths in top10 ='+ str(res[0])+'\n')
    



        





