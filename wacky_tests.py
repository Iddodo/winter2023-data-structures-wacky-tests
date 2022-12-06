#!/usr/bin/env python3

import random
import math
import functools 

output = []
expected_output = []

teams = dict()
players = dict()

def add_output(input_list):
    output.append(' '.join([str(x) for x in input_list]))

def add_expected(keycode, status, more = None):
    expected_output.append(str(keycode) + ': ' + str(status) + ('' if more == None else ', ' + str(more)))

def add_expected_raw(text):
    expected_output.append(text)


# -------------------------------
def has_goalkeeper(teamId):
    if str(teamId) not in teams:
        return False
    
    for ID in teams[str(teamId)]['players']:
        if players[ID]['goalKeeper'] == 'true':
            return True

    return False

def valid_team(teamId):
    if str(teamId) not in teams:
        return False

    if len(teams[str(teamId)]['players']) < 11:
        return False

    for ID in teams[str(teamId)]['players']:
        if players[ID]['goalKeeper'] == 'true':
            return True

    return has_goalkeeper(teamId)

def player_sigma(teamId):
    sum = 0

    for ID in teams[str(teamId)]['players']:
        sum += (players[str(ID)]['goals'] - players[str(ID)]['cards'])

    return sum

def team_sigma(teamId):
    return teams[str(teamId)]['points'] + player_sigma(teamId)

def increment_player_played(teamId):
    for ID in teams[str(teamId)]['players']:
        players[str(ID)]['gamesPlayed'] += 1

def closest_player_le(targetID, player1ID, player2ID):
    target = players[str(targetID)]
    player1 = players[str(player1ID)]
    player2 = players[str(player2ID)]

    dist1_goals = abs(target['goals'] - player1['goals'])
    dist2_goals = abs(target['goals'] - player2['goals'])

    dist1_cards = abs(target['cards'] - player1['cards'])
    dist2_cards = abs(target['cards'] - player2['cards'])

    dist1_playerId = abs(target['playerId'] - player1['playerId'])
    dist2_playerId = abs(target['playerId'] - player2['playerId'])

    if dist1_goals != dist2_goals:
        return player1ID if dist1_goals < dist2_goals else player2ID

    if dist1_cards != dist2_cards:
        return player1ID if dist1_cards < dist2_cards else player2ID

    if dist1_playerId != dist2_playerId:
        return player1ID if dist1_playerId < dist2_playerId else player2ID

    return player1ID if player1['playerId'] > player2['playerId'] else player2ID

def num_valid_teams():
    counter = 0

    for ID in teams:
        if valid_team(ID):
            counter += 1
    return counter

# -------------------------------

def add_team(teamId, points):
    if teamId <= 0 or points < 0:
        add_expected('add_team', 'INVALID_INPUT')
    elif str(teamId) in teams:
        add_expected('add_team', 'FAILURE')
    else:
        teams[str(teamId)] = {'teamId': teamId, 'points': points, 'players': []}

        add_expected('add_team', 'SUCCESS')

    add_output(['add_team', teamId, points])




def remove_team(teamId):
    if teamId <= 0:
        add_expected('remove_team', 'INVALID_INPUT')
    elif str(teamId) not in teams:
        add_expected('remove_team', 'FAILURE')
    elif len(teams[str(teamId)]['players']) > 0:
        add_expected('remove_team', 'FAILURE')
    else:
        del teams[str(teamId)]
        add_expected('remove_team', 'SUCCESS')

    add_output(['remove_team', teamId])


def add_player(playerId, teamId, gamesPlayed, goals, cards, goalKeeper):

    if playerId <= 0 or teamId <= 0 or gamesPlayed < 0 or goals < 0 or cards < 0:
        add_expected('add_player', 'INVALID_INPUT')
    elif gamesPlayed == 0 and (goals > 0 or cards > 0):
        add_expected('add_player', 'INVALID_INPUT')
    elif str(teamId) not in teams:
        add_expected('add_player', 'FAILURE')
    elif str(playerId) in players:
        add_expected('add_player', 'FAILURE')
    else:
        players[str(playerId)] = {
            'playerId': playerId,
            'teamId': teamId,
            'gamesPlayed': gamesPlayed,
            'goals': goals,
            'cards': cards,
            'goalKeeper': goalKeeper
        }
        teams[str(teamId)]['players'].append(str(playerId))

        add_expected('add_player', 'SUCCESS')

    add_output(['add_player', playerId, teamId, gamesPlayed, goals, cards, goalKeeper])


def remove_player(playerId):
    if playerId <= 0:
        add_expected('remove_player', 'INVALID_INPUT')
    elif str(playerId) not in players:
        add_expected('remove_player', 'FAILURE')
    else:
        teamId = players[str(playerId)]['teamId']
        teams[str(teamId)]['players'].remove(str(playerId))
        del players[str(playerId)]
        add_expected('remove_player', 'SUCCESS')

    add_output(['remove_player', playerId])

def update_player_stats(playerId, gamesPlayed, scoredGoals, cardsReceived):
    if playerId <= 0 or gamesPlayed < 0 or scoredGoals < 0 or cardsReceived < 0:
        add_expected('update_player_stats', 'INVALID_INPUT')
    elif str(playerId) not in players:
        add_expected('update_player_stats', 'FAILURE')
    else:
        player = players[str(playerId)]
        player['gamesPlayed'] += gamesPlayed
        player['goals'] += scoredGoals
        player['cards'] += cardsReceived

        add_expected('update_player_stats', 'SUCCESS')

    add_output(['update_player_stats', playerId, gamesPlayed, scoredGoals, cardsReceived])

def play_match(teamId1, teamId2):
    if teamId1 <= 0 or teamId2 <= 0 or teamId1 == teamId2:
        add_expected('play_match', 'INVALID_INPUT')

    elif str(teamId1) not in teams or str(teamId2) not in teams:
        add_expected('play_match', 'FAILURE')

    elif not (valid_team(teamId1) and valid_team(teamId2)):
        add_expected('play_match', 'FAILURE')
    else:
        team1_sigma = team_sigma(teamId1)
        team2_sigma = team_sigma(teamId2)

        if team1_sigma == team2_sigma:
            teams[str(teamId1)]['points'] += 1
            teams[str(teamId2)]['points'] += 1
        else:
            winner = teamId1 if team1_sigma > team2_sigma else teamId2
            teams[str(winner)]['points'] += 3

        increment_player_played(teamId1)
        increment_player_played(teamId2)

        add_expected('play_match', 'SUCCESS')

    add_output(['play_match', teamId1, teamId2])

def get_num_played_games(playerId):
    if playerId <= 0:
        add_expected('get_num_played_games', 'INVALID_INPUT')

    elif str(playerId) not in players:
        add_expected('get_num_played_games', 'FAILURE')

    else:
        add_expected('get_num_played_games', 'SUCCESS', str(players[str(playerId)]['gamesPlayed']))

    add_output(['get_num_played_games', playerId])

def get_team_points(teamId):
    if teamId <= 0:
        add_expected('get_team_points', 'INVALID_INPUT')
    elif str(teamId) not in teams:
        add_expected('get_team_points', 'FAILURE')
    else:
        add_expected('get_team_points', 'SUCCESS', teams[str(teamId)]['points'])

    add_output(['get_team_points', teamId])

def unite_teams(teamId1, teamId2, newTeamId):
    if newTeamId <= 0 or teamId1 <= 0 or teamId2 <= 0 or teamId1 == teamId2:
        add_expected('unite_teams', 'INVALID_INPUT')

    elif (str(teamId1) not in teams or str(teamId2) not in teams):
        add_expected('unite_teams', 'FAILURE')

    elif (not (newTeamId == teamId1 or newTeamId == teamId2)) and str(newTeamId) in teams:
        add_expected('unite_teams', 'FAILURE')

    else:
        team1 = teams[str(teamId1)]
        team2 = teams[str(teamId2)]

        new_team = {
            'teamId': newTeamId,
            'points': team1['points'] + team2['points'],
            'players': team1['players'] + team2['players']
        }

        for ID in new_team['players']:
            players[ID]['teamId'] = newTeamId


        del teams[str(teamId1)]
        del teams[str(teamId2)]

        teams[str(newTeamId)] = new_team

        add_expected('unite_teams', 'SUCCESS')

    add_output(['unite_teams', teamId1, teamId2, newTeamId])

def get_top_scorer(teamId):
    if teamId == 0:
        add_expected('get_top_scorer', 'INVALID_INPUT')

    elif teamId > 0:
        if str(teamId) not in teams or (len(teams[str(teamId)]['players']) == 0):
            add_expected('get_top_scorer', 'FAILURE')
        else:
            max_score = -1
            max_player = None

            for ID in teams[str(teamId)]['players']:
                player = players[ID]
                if player['goals'] > max_score:
                    max_score = player['goals']
                    max_player = player
                elif player['goals'] == max_score:
                    if player['cards'] < max_player['cards']:
                        max_player = player
                    elif player['cards'] == max_player['cards']:
                        max_player = player if player['playerId'] > max_player['playerId'] else max_player

            add_expected('get_top_scorer', 'SUCCESS', max_player['playerId'])

    elif teamId < 0:
        if (len(players) == 0):
            add_expected('get_top_scorer', 'FAILURE')
        else:
            max_score = -1
            max_player = None

            for ID in players:

                player = players[ID]

                if player['goals'] > max_score:
                    max_score = player['goals']
                    max_player = player
                elif player['goals'] == max_score:
                    if player['cards'] < max_player['cards']:
                        max_player = player
                    elif player['cards'] == max_player['cards']:
                        max_player = player if player['playerId'] > max_player['playerId'] else max_player

            add_expected('get_top_scorer', 'SUCCESS', max_player['playerId'])

    add_output(['get_top_scorer', teamId])

def get_all_players_count(teamId):
    if teamId == 0:
        add_expected('get_all_players_count', 'INVALID_INPUT')

    elif teamId > 0:
        if str(teamId) not in teams:
            add_expected('get_all_players_count', 'FAILURE')
        else:
            add_expected('get_all_players_count', 'SUCCESS',
                         str(len(teams[str(teamId)]['players'])))
    elif teamId < 0:
            add_expected('get_all_players_count', 'SUCCESS',
                         str(len(players)))

    add_output(['get_all_players_count', teamId])

def player_goals_ID_le(ID1, ID2):
    player1 = players[str(ID1)]
    player2 = players[str(ID2)]
 
    if player1['goals'] != player2['goals']:
        return -1 if player1['goals'] < player2['goals'] else 1
 
    if player1['cards'] != player2['cards']:
        return -1 if player1['cards'] > player2['cards'] else 1
 
    return -1 if ID1 < ID2 else 1

def get_all_players(teamId):
    if teamId == 0:
        add_expected('get_all_players', 'INVALID_INPUT')

    elif teamId > 0:
        if str(teamId) not in teams:
            add_expected('get_all_players', 'INVALID_INPUT') # in order to be compatible to the main which creates the output buffer as nullptr in this case
        elif len(teams[str(teamId)]['players']) == 0:
            add_expected('get_all_players', 'INVALID_INPUT') # in order to be compatible to the main which creates the output buffer as nullptr in this case
        else:
            res_array = teams[str(teamId)]['players']

            sorted_players = sorted(res_array, key=functools.cmp_to_key(player_goals_ID_le))

            add_expected_raw('get_all_players: SUCCESS' + '\n' + '\n'.join(sorted_players))

    elif teamId < 0:
        if len(players) == 0:
            add_expected('get_all_players', 'INVALID_INPUT') # in order to be compatible to the main which creates the output buffer as nullptr in this case
        else:
            res_array = [str(players[player]['playerId']) for player
                              in players]

            sorted_players = sorted(res_array, key=functools.cmp_to_key(player_goals_ID_le))

            add_expected_raw('get_all_players: SUCCESS' + '\n' + '\n'.join(sorted_players))


    add_output(['get_all_players', teamId])

def get_closest_player(playerId, teamId):
    add_output(['get_closest_player', playerId, teamId])

    if playerId <= 0 or teamId <= 0:
        add_expected('get_closest_player', 'INVALID_INPUT')

    elif str(teamId) not in teams or str(playerId) not in teams[str(teamId)]['players']:
        add_expected('get_closest_player', 'FAILURE')

    elif len(players) == 1:
        add_expected('get_closest_player', 'FAILURE')

    else:
        closest = None

        in_order_players =  sorted(list(players.keys()), key=functools.cmp_to_key(player_goals_ID_le))

        target_index = in_order_players.index(str(playerId))

        if target_index == 0:
            closest = in_order_players[1]

        elif target_index == len(in_order_players) - 1:
            closest = in_order_players[-2]

        else:
            closest = closest_player_le(in_order_players[target_index], in_order_players[target_index - 1], in_order_players[target_index + 1])

        add_expected('get_closest_player', 'SUCCESS', players[closest]['playerId'])


def knockout_winner(minTeamId, maxTeamId):
    add_output(['knockout_winner', minTeamId, maxTeamId])

    if minTeamId < 0 or maxTeamId < 0 or maxTeamId < minTeamId:
        add_expected('knockout_winner', 'INVALID_INPUT')

    elif num_valid_teams() <= 0:
        add_expected('knockout_winner', 'FAILURE')

    else:
        playing_teams = []
        sorted_teams = [int(x) for x in list(teams.keys())]
        sorted_teams.sort()

        for ID in sorted_teams:
            if (not valid_team(ID)):
                continue

            if (not (ID >= minTeamId and ID <= maxTeamId)):
                continue

            playing_teams.append(teams[str(ID)].copy())
            playing_teams[-1]['sigma'] = team_sigma(ID)

        if not playing_teams:
            add_expected('knockout_winner', 'FAILURE')
            return

        while len(playing_teams) >= 2:
            round_winners = []

            for t in list(zip(playing_teams[::2], playing_teams[1::2])):
                team1, team2 = t

                winner = None
                if team1['sigma'] != team2['sigma']:
                    winner = team1 if team1['sigma'] > team2['sigma'] else team2
                else:
                    winner = team1 if team1['teamId'] > team2['teamId'] else team2

                loser = team1 if winner == team2 else team2

                winner['sigma'] += 3 + loser['sigma']

                round_winners.append(winner)

            if (len(playing_teams) % 2 == 1):
                round_winners.append(playing_teams[-1])

            playing_teams = round_winners

        add_expected('knockout_winner', 'SUCCESS', playing_teams[0]['teamId'])

#-----------------------------------------------------


turn_off_validity_checks = True

num_teams = 20
num_players = 200
max_start_points = 69
num_teams_invalid_points = 20

magic_number = 12345
small_magic = 5

bool_opts = ['true'] * 5 + ['false']


actual_team_ids = list(range(1, num_teams + 1))
actual_player_ids = list(range(1, num_players + 1))

def random_team_ID():
    return random.choice(actual_team_ids)

def random_int_list_extended(l, num_original = None):
    if turn_off_validity_checks:
        return random.choice(l)

    if num_original == None:
        num_original = len(l)

    num_margins = int(len(l) / 5)
    ext = [(-1) * x for x in l][:num_margins]
    ext += [max(l) + x for x in l][:num_margins]
    ext += [0]
    ext += l[:num_original]

    return random.choice(ext)

def random_team_ID_extended(num_original = len(actual_team_ids)):
    if turn_off_validity_checks:
        return random.choice(actual_team_ids)

    return random_int_list_extended(actual_team_ids + [x for x in list(range(1, num_teams + 1)) if x not in actual_team_ids], num_original)


def random_player_ID_extended():
    if turn_off_validity_checks:
        return random.choice(actual_player_ids)

    return random_int_list_extended(actual_player_ids + [x for x in list(range(1, num_players + 1)) if x not in actual_player_ids])

def random_positive_number():
    return random.randint(1, magic_number)

def random_almost_positive():
    if turn_off_validity_checks:
        return random_positive_number()
    return random.randint(-10, magic_number)

def random_bool():
    return random.choice(bool_opts)

random_commands = [
    'add_team',
    'remove_team',
    'add_player',
    'remove_player',
    'update_player_stats',
    'play_match',
    'get_num_played_games',
    'get_team_points',
    'unite_teams',
    'get_top_scorer',
    'get_all_players_count',
    'get_all_players',
    'get_closest_player',
    'knockout_winner',
]

def random_command():
    return random.choice(random_commands)

def execute_random_command(command):
    if command == 'add_team':
        team_id = random_team_ID_extended()
        points = random_almost_positive()
        add_team(team_id, points)

        if ("SUCCESS" in expected_output[-1]):
            actual_team_ids.append(team_id)
        return

    if command == 'remove_team':
        team_id = random_team_ID_extended()
        remove_team(team_id)

        if ("SUCCESS" in expected_output[-1]):
            actual_team_ids.remove(team_id)
        return

    if command == 'add_player':
        player_id = random_player_ID_extended()
        team_id = random_team_ID()
        gamesPlayed = random_almost_positive()
        goals = random_almost_positive()
        cards = random_almost_positive()

        add_player(player_id, team_id, gamesPlayed, goals, cards, random_bool())

        if ("SUCCESS" in expected_output[-1]):
            actual_player_ids.append(player_id)
        return

    if command == 'remove_player':
        player_id = random_player_ID_extended()
        remove_player(player_id)
        if ("SUCCESS" in expected_output[-1]):
            actual_player_ids.remove(player_id)
        return

    if command == 'update_player_stats':
        player_id = random_player_ID_extended()
        gamesPlayed = random_almost_positive()
        goals = random_almost_positive()
        cards = random_almost_positive()
        update_player_stats(player_id, gamesPlayed, goals, cards)
        return

    if command == 'play_match':
        team_id1 = random_team_ID_extended()
        team_id2 = random_team_ID_extended()
        play_match(team_id1, team_id2)
        return

    if command == 'get_num_played_games':
        player_id = random_player_ID_extended()
        get_num_played_games(player_id)
        return

    if command == 'get_team_points':
        team_id = random_team_ID_extended()
        get_team_points(team_id)
        return

    if command == 'unite_teams':
        team_id1 = random_team_ID_extended()
        team_id2 = random_team_ID_extended()
        team_id_new = random_team_ID_extended(int(math.sqrt(len(actual_team_ids))))
        unite_teams(team_id1, team_id2, team_id_new)

        if ("SUCCESS" in expected_output[-1]):
            actual_team_ids.remove(team_id1)
            actual_team_ids.remove(team_id2)
            actual_team_ids.append(team_id_new)
        return

    if command == 'get_top_scorer':
        team_id = random_team_ID_extended()
        get_top_scorer(team_id)
        return

    if command == 'get_all_players_count':
        team_id = random_team_ID_extended()
        get_all_players_count(team_id)
        return

    if command == 'get_all_players':
        team_id = random_team_ID_extended()
        get_all_players(team_id)
        return

    if command == 'get_closest_player':
        player_id = random_player_ID_extended()
        team_id = random_team_ID_extended()

        if turn_off_validity_checks:
            team_id = players[str(player_id)]['teamId']
        get_closest_player(player_id, team_id)
        return

    if command == 'knockout_winner':
        if turn_off_validity_checks:
            min_team_id = random_team_ID_extended()
            max_team_id = random.choice(actual_team_ids[actual_team_ids.index(min_team_id):])
            knockout_winner(min_team_id, max_team_id)
            knockout_winner(min_team_id - small_magic, max_team_id + small_magic)
            knockout_winner(min_team_id - small_magic, max_team_id - small_magic)
            knockout_winner(min_team_id + small_magic, max_team_id + small_magic)
            knockout_winner(min_team_id + small_magic, max_team_id - small_magic)
            return

        min_team_id = random_team_ID_extended()
        max_team_id = random_team_ID_extended()

        knockout_winner(min_team_id, max_team_id)


for ID in actual_team_ids:
    add_team(ID, random_positive_number())


for ID in range(1, num_players + 1):
    add_player(ID, random_team_ID(), random_positive_number(), random_positive_number(), random_positive_number(), random_bool())


num_commands = 1000

for i in range(0, num_commands):
    execute_random_command(random_command())


for ID in actual_player_ids:
    remove_player(ID)

for ID in actual_team_ids:
    remove_team(ID)



# -----------------------------------------------------

test_name = 'wacky.in'
expected_name = 'wacky.out'

f_test = open(test_name, 'w')
f_expected = open(expected_name, 'w')

f_test.write('\n'.join(output))
f_expected.write('\n'.join(expected_output) + '\n')


f_test.close()
f_expected.close()
