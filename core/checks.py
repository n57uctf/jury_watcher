from typing import List, Tuple, AnyStr


def table_fb(old, cur):
    """

    :type old: Table
    :type cur: Table
    :rtype: List
    """
    result: List[Tuple] = []
    for i, service in enumerate(old.service_names):
        zero_attacks = True
        for team in old.teams:
            if team.services[i].fatt != 0:
                zero_attacks = False
                break
        if not zero_attacks:
            continue
        for team in cur.teams:
            if team.services[i].fatt != 0:
                result.append((service, team.name))
    return result


def team_bloud(old, cur, team):
    """

    :type old: Table
    :type cur: Table
    :type team: basestring
    :rtype: List[AnyStr]
    """
    result: List[AnyStr] = []
    for i, service in enumerate(old.service_names):
        if cur[team].services[i].fatt - old[team].services[i].fatt > 0:
            result.append(service)
    return result


def team_owned(old, cur, team):
    """

    :type old: Table
    :type cur: Table
    :type team: basestring
    :rtype: List[AnyStr]
    """
    result: List[AnyStr] = []
    for i, service in enumerate(old.service_names):
        if cur[team].services[i].fdef - old[team].services[i].fdef < 0:
            result.append(service)
    return result


def team_change_status(old, cur, team):
    """

    :type old: Table
    :type cur: Table
    :rtype: List[Tuple]
    """
    result: List[Tuple] = []
    for i, service in enumerate(cur.service_names):
        old_status = old[team].services[i].status
        cur_status = cur[team].services[i].status
        if old_status != cur_status:
            result.append((service, cur_status))
    return result
