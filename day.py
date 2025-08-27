from utils.check_process import char_alive_check,endcheck
from utils.control_process import day_kill,hunter_vengence

def day(game_logger,alive_list,char_dist,char_instances,round_count):
    #初始化
    game_logger.add_log('观察日志',-1,'moderater',f'第{round_count}天白天开始')
    alive_char=char_alive_check(alive_list,char_dist)
    #发言
    day_killed=day_kill(alive_list,char_instances,game_logger,round_count)
    #结算
    kill_list=[]
    if day_killed>-1:
        kill_list.append(day_killed)
        if char_dist[day_killed] == 'hunter':
            hunter= char_instances[day_killed]
            vengence_res=hunter_vengence(hunter,alive_list,round_count,'白天')
            if vengence_res>-1:
                kill_list.append(vengence_res)
                log_info=f'猎人开枪带走了{vengence_res}号玩家'
                game_logger.add_log('观察日志',-1,'moderater',log_info)
    for i in kill_list:
        if i in alive_list:
            alive_list.remove(i)
    print("白天死亡玩家：")
    print(kill_list)
    if len(kill_list)>0:
        log_info=f"第{round_count}天白天死亡玩家:"
        for i in kill_list:
            log_info+= str(i)+"号玩家、"
        log_inf=log_info[:-1]+'。'
        game_logger.add_log('观察日志',-1,'moderater',log_info)
    else:
        game_logger.add_log('观察日志',-1,'moderater',f'第{round_count}天白天无人死亡')
    print("剩余玩家：")
    print(alive_list)
    log_info=f"第{round_count}天白天，剩余存活玩家:"
    for i in alive_list:
        log_info+= str(i)+"号玩家、"
    log_info=log_info[:-1]+'。'
    game_logger.add_log('观察日志',-1,'moderater',log_info)
    game_res= endcheck(alive_list,char_dist,game_logger)
    game_logger.add_log('观察日志',-1,'moderater',f'第{round_count}个白天结束')
    return game_res,alive_list