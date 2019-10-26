from typing import List, Tuple


def table_fb(old, cur):
    """

    :type old: Table
    :type cur: Table
    :rtype: List
    """
    result: List[Tuple] = []
    for service in old.service_names:
        zero_attacks = True
        for team in old.team_names:
            if old.teams[team][service]['fatt'] != 0:
                zero_attacks = False
                break
        if not zero_attacks:
            continue
        for team in cur.team_names:
            if cur.teams[team][service]['fatt'] != 0:
                result.append((service, team))
    return result


def team_bloud(old, cur, team):
    """

    :type old: Table
    :type cur: Table
    :type team: str
    :rtype: List[str]
    """
    result: List[str] = []
    for service in old.service_names:
        if cur.teams[team][service]['fatt'] - old.teams[team][service]['fatt'] > 0:
            result.append(service)
    return result


def team_owned(old, cur, team):
    """

    :type old: Table
    :type cur: Table
    :type team: str
    :rtype: List[str]
    """
    result: List[str] = []
    for service in old.service_names:
        if cur.teams[team][service]['fdef'] - old.teams[team][service]['fdef'] < 0:
            result.append(service)
    return result


def team_change_status(old, cur, team):
    """

    :type old: Table
    :type cur: Table
    :type team: str
    :rtype: List[Tuple]
    """
    result: List[Tuple] = []
    for service in cur.service_names:
        old_status = old.teams[team][service]['status']
        cur_status = cur.teams[team][service]['status']
        if old_status != cur_status:
            result.append((service, cur_status))
    return result
