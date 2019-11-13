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
            if old.cells[team][service]['fatt'] != 0:
                zero_attacks = False
                break
        if not zero_attacks:
            continue
        for team in cur.team_names:
            if cur.cells[team][service]['fatt'] != 0:
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
        if cur.cells[team][service]['fatt'] - old.cells[team][service]['fatt'] > 0:
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
        if cur.cells[team][service]['fdef'] - old.cells[team][service]['fdef'] < 0:
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
        cur_status = cur.cells[team][service]['status']
        if cur_status != "up":
            result.append((service, cur_status))
    return result
