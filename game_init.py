import random
from logger import game_logger
from characters import werewolf,seer,witch,hunter,villager
from system_prompt import game_intro
from memory_admin import memory_admin

def choose_strategy(char):
    consulter=memory_admin('graph_werewolf.db')
    strategies=consulter.consult_strategy(char)
    chosen_strategy=random.choice(list(strategies))
    return chosen_strategy

def char_info_initialize(char_dist):
    char_info_dic={}
    for i in char_dist.keys():
        if char_dist[i]=='villager':
            info=game_intro+"你是%d号玩家，你的身份是村民。\n"%(i)
            char_info_dic[i]=info
        elif char_dist[i]=='seer':
            info=game_intro+"你是%d号玩家，你的身份是预言家。\n"%(i)
            char_info_dic[i]=info
        elif char_dist[i]=='witch':
            info=game_intro+"你是%d号玩家，你的身份是女巫。\n"%(i)
            char_info_dic[i]=info
        elif char_dist[i]=='hunter':
            info=game_intro+"你是%d号玩家，你的身份是猎人。\n"%(i)
            char_info_dic[i]=info
        elif char_dist[i]=='werewolf':
            werewolf_list=[key for key,value in char_dist.items() if value=='werewolf']
            werewolf_list.remove(i)
            info=game_intro+"你是%d号玩家，你的身份是狼人，你的狼人队友包括"%(i)
            for j in werewolf_list:
                info+="%d号玩家、"%(j)
            info=info[:-1]+"。\n"
            char_info_dic[i]=info
    return char_info_dic

def game_init():
    logger=game_logger('werewolf.db')
    char_quota={"seer":1,"witch":1,"hunter":1,"villager":2,"werewolf":3}
    numbers=list(range(8))
    aliv_list=list(range(8))
    random.shuffle(numbers)
    char_dist={}
    char_dist[numbers[0]]="seer"
    char_dist[numbers[1]]="witch"
    char_dist[numbers[2]]="hunter"
    char_dist[numbers[3]]="villager"
    char_dist[numbers[4]]="villager"
    char_dist[numbers[5]]="werewolf"
    char_dist[numbers[6]]="werewolf"
    char_dist[numbers[7]]="werewolf"
    char_info=char_info_initialize(char_dist=char_dist)
    char_instances={}
    char_strategies={}
    for i in char_dist.keys():
        strategy=choose_strategy(char_dist[i])
        char_strategies[i]=strategy
        if char_dist[i]=="werewolf":
            char_instances[i]=werewolf(char_info[i],i,logger,strategy)
        elif char_dist[i]=="seer":
            char_instances[i]=seer(char_info[i],i,logger,strategy)
        elif char_dist[i]=="witch":
            char_instances[i]=witch(char_info[i],i,logger,strategy)
        elif char_dist[i]=="villager":
            char_instances[i]=villager(char_info[i],i,logger,strategy)
        elif char_dist[i]=="hunter":
            char_instances[i]=hunter(char_info[i],i,logger,strategy)
    log_info="游戏开始，当前存活玩家:"
    for i in aliv_list:
        log_info+= str(i)+"号玩家、"
    log_info=log_info[:-1]+'。'
    logger.add_log('观察日志',-1,'moderater',log_info)
    return aliv_list,char_dist,char_instances,logger,char_strategies