def char_alive_check(aliv_list,char_dist):
    char_aliv=[]
    for i in aliv_list:
        char_aliv.append(char_dist[i])
    return set(char_aliv)
def endcheck(aliv_list,char_dist,logger):
    translator={'werewolf':'狼人',
                    'seer':'预言家',
                    'witch':'女巫',
                    'villager':'村民',
                    'hunter':'猎人',
                    'moderater':'裁判'}
    char_aliv=char_alive_check(aliv_list,char_dist)
    if "villager" not in char_aliv:
        logger.add_log('观察日志',-1,'moderater','游戏结束,普通村民全被消灭，狼人阵营胜利')
        log_info="本局游戏玩家角色:"
        for i in char_dist.keys():
            log_info+= str(i)+"号玩家-"+translator[char_dist[i]]+'、'
            log_inf=log_info[:-1]+'。'
        logger.add_log('观察日志',-1,'moderater',log_info)
        log_info="剩余存活玩家:"
        for i in aliv_list:
            log_info+= str(i)+"号玩家("+translator[char_dist[i]]+')、'
            log_inf=log_info[:-1]+'。'
        logger.add_log('观察日志',-1,'moderater',log_info)
        return 1
    elif char_aliv=={"werewolf","villager"}:
        logger.add_log('观察日志',-1,'moderater','游戏结束,神职人员全被消灭，狼人阵营胜利')
        log_info="本局游戏玩家角色:"
        for i in char_dist.keys():
            log_info+= str(i)+"号玩家-"+translator[char_dist[i]]+'、'
            log_inf=log_info[:-1]+'。'
        logger.add_log('观察日志',-1,'moderater',log_info)
        log_info="剩余存活玩家:"
        for i in aliv_list:
            log_info+= str(i)+"号玩家("+translator[char_dist[i]]+')、'
            log_inf=log_info[:-1]+'。'
        logger.add_log('观察日志',-1,'moderater',log_info)
        return 1
    elif "werewolf" not in char_aliv:
        logger.add_log('观察日志',-1,'moderater','游戏结束,狼人全被消灭，人类阵营胜利')
        log_info="本局游戏玩家角色:"
        for i in char_dist.keys():
            log_info+= str(i)+"号玩家-"+translator[char_dist[i]]+'、'
            log_inf=log_info[:-1]+'。'
        logger.add_log('观察日志',-1,'moderater',log_info)
        log_info="剩余存活玩家:"
        for i in aliv_list:
            log_info+= str(i)+"号玩家("+translator[char_dist[i]]+')、'
            log_inf=log_info[:-1]+'。'
        logger.add_log('观察日志',-1,'moderater',log_info)
        return 2
    else:
        return 0    