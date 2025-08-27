from utils.check_process import char_alive_check,endcheck
from utils.control_process import night_werewolf_kill,night_witch,night_seer,hunter_vengence


def night(game_logger,alive_list,char_dist,char_instances,round_count):
    #初始化,确认角色分布
    game_logger.add_log('观察日志',-1,'moderater',f'第{round_count}天夜晚开始')
    alive_char=char_alive_check(alive_list,char_dist)
    kill_list=[]
    rescue_list=[]
    #狼人杀人
    werewolves=[]
    for i in alive_list:
        if char_dist[i] == "werewolf":
            werewolves.append(char_instances[i])
    werewolf_killed=night_werewolf_kill(werewolves,round_count)
    if werewolf_killed>-1:
        kill_list.append(werewolf_killed)
    #女巫救人/毒人
    if 'witch' in alive_char:
        for i in char_dist.keys():
            if char_dist[i] == 'witch':
                witch=char_instances[i]
        rescue,poison=night_witch(witch,werewolf_killed,round_count)
        if poison>-1:
            kill_list.append(poison)
        if rescue>-1:
            rescue_list.append(rescue)
    #预言家验人
    if 'seer' in alive_char:
        for i in char_dist.keys():
            if char_dist[i] == 'seer':
                seer=char_instances[i]
                num_seer=i
        night_seer(seer,num_seer,char_dist,game_logger,round_count)
    #夜晚结算
    for i in rescue_list:
        if i in kill_list:
            kill_list.remove(i)
    for j in kill_list:
        if char_dist[j] == 'hunter':
            hunter= char_instances[j]
            vengence_res=hunter_vengence(hunter,alive_list,round_count=round_count,step='夜晚')
            if vengence_res>-1:
                kill_list.append(vengence_res)
                log_info=f'猎人开枪带走了{vengence_res}号玩家'
                game_logger.add_log('观察日志',-1,'moderater',log_info)
    for k in kill_list:
        if k in alive_list:
            alive_list.remove(k)
    print("夜晚死亡玩家：")
    print(kill_list)
    if len(kill_list)>0:
        log_info=f"第{round_count}天夜晚死亡玩家:"
        for i in kill_list:
            log_info+= str(i)+"号玩家、"
        log_inf=log_info[:-1]+'。'
        game_logger.add_log('观察日志',-1,'moderater',log_info)
    else:
        game_logger.add_log('观察日志',-1,'moderater',f'第{round_count}天夜晚无人死亡')
    print("剩余玩家：")
    print(alive_list)
    log_info=f"第{round_count}天夜晚，剩余存活玩家:"
    for i in alive_list:
        log_info+= str(i)+"号玩家、"
    log_info=log_info[:-1]+'。'
    game_logger.add_log('观察日志',-1,'moderater',log_info)
    game_res= endcheck(alive_list,char_dist,game_logger)
    game_logger.add_log('观察日志',-1,'moderater',f'第{round_count}天夜晚结束')
    return game_res,alive_list