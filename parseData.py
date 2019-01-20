from copy import deepcopy

def msg_parse(incm_msg, bus_obj):
    incm_msg = incm_msg.lower()
    msg = incm_msg.split()
    func_dict = {'rte': rte_parse, 'stp': stp_parse, 'arvl': arvl_parse, 'rucs': rucs_parse}
    if len(msg) > 1:
        msg.pop(0)
    else:
        return 'incomplete command: \ncommand contained \'' + msg[0] + '\''
    
    try:
        return func_dict[msg[0]](msg, bus_obj)
    except:
        return 'problem with command \ncommand contained \'' + msg[1] + '\''


def rte_parse(msg, *args):
    return msg


def stp_parse(msg, bus_obj):
    rte_data = bus_obj.rte
    rte_values = list(rte_data.values())
    return [msg[0], string_match(rte_values, msg[1])]


def arvl_parse(msg, bus_obj):
    rte_data = bus_obj.rte
    rte_values = list(rte_data.values())
    bus_line = string_match(rte_values, msg[1])
    if isinstance(bus_line, list):
        return [msg[0], bus_line]
    stp_data = bus_obj.stp
    stops_for_route = list(stp_data[bus_line].keys())
    selected_stop = string_match(stops_for_route, msg[2])
    if isinstance(selected_stop, list):
        return [msg[0], bus_line, selected_stop]
    rqst_bus_stps = deepcopy(stp_data[bus_line])                         #copy necessary dictionary over to set keys to lower case
    rqst_bus_stps = {k.lower(): v for k, v in rqst_bus_stps.items()}        #set keys to lower case in dictionary
    return [msg[0], bus_line, rqst_bus_stps[selected_stop]]


def rucs_parse(msg, *args):
    return msg


def error_parse(err_msg, bus_obj):
    if err_msg[0] in bus_obj.rte.keys():
        return sterror_parse(err_msg[1], bus_obj.stp)
    else:
        return starvl_parse(err_msg)


def starvl_parse(err_msg):
    rtrn_msg = 'you might be referring to stop \n'
    for counter, stop in enumerate(err_msg):
        rtrn_msg += stop + '\n'
    return rtrn_msg


def sterror_parse(err_msg, bus_stps):
    rtrn_msg = 'you might be referring to bus '
    for counter, stops in enumerate(err_msg):
        rtrn_msg += err_msg[counter] + ' with stops \n'
        for key, value in bus_stps[err_msg[counter]].items():
            rtrn_msg += key + '\n'
        if counter < len(err_msg) - 1:
            rtrn_msg += 'or bus '
    return rtrn_msg


# match_to = all stops, match_from = user message
def string_match(match_to, match_from):
    correct_match = []
    match_from = match_from.lower()
    match_to_list = [word.lower() for word in match_to]
    match_to_list = [word for word in match_to_list if match_from in word]
    for counter, word in enumerate(match_to_list):
        if match_from == word:
            correct_match.append(word)
    if len(correct_match) > 0:
        match_to_list = [word for word in match_to_list if word in correct_match]
    if len(match_to_list) > 1:
        return match_to_list
    return match_to_list[0]
