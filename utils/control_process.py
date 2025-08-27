import random
from collections import Counter

import os
import sys
project_root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,project_root)
from memory_admin import memory_admin
from base_llm import base_llm
from utils.extraction_process import kill_vote_extr,day_vote_extr,seer_val_extr,witch_poison_extr,witch_antidote_extr,hunter_vegence_extr



def choose_advice(round_count,step,skill,char,strategy):
    translator={'werewolf':'狼人',
            'seer':'预言家',
            'witch':'女巫',
            'villager':'村民',
            'hunter':'猎人'}
    if char in translator.keys():
        character=translator[char]
    else:
        character=char
    consulter=memory_admin('graph_werewolf.db')
    filter_dict={}
    filter_dict['角色职业']=character
    filter_dict['游戏技能']=skill
    filter_dict['游戏环节']=f'第{round_count}天'+step
    advices=consulter.consult_advice(strategy,filter_dict)
    if advices=='无' or len(advices)==0:
        return '无'
    else:
        i=len(advices)
        res_index=random.randint(0,i-1)
        return advices[res_index].val['游戏建议']
def night_werewolf_kill(werewolves,round_count):
    input_2_json_llm=base_llm("你是一个从对话内容提取json字符串的小助手，可以根据提示从对话中精准提取信息，并以规定的json格式返回")
    print("夜晚狼人开始行动：")
    for werewolf in werewolves:
        advice=choose_advice(round_count,'夜晚','狼人杀人','狼人',werewolf.strategy_vertex)
        res=werewolf.kill_speech(advice=advice)
        print(f"狼人{werewolf.num}号发言:"+res)
    votes=[]
    for werewolf in werewolves:
        res = werewolf.kill_vote()
        vote_res=kill_vote_extr(input_2_json_llm,res)
        votes.append(vote_res)
    print("vote result:")
    print(votes)
    print(Counter(votes).most_common(1)[0][0])
    return Counter(votes).most_common(1)[0][0]
def night_witch(witch,killed_num,round_count):
    input_2_json_llm=base_llm("你是一个从对话内容提取json字符串的小助手，可以根据提示从对话中精准提取信息，并以规定的json格式返回")
    print("女巫开始行动：")
    killed_rescue= -1
    poison_kill=-1
    if witch.antidote==1 and killed_num>-1:
        advice=choose_advice(round_count,'夜晚','解药决策','女巫',witch.strategy_vertex)
        res=witch.use_antidote(killed_num,advice=advice)
        antidote_res=witch_antidote_extr(input_2_json_llm,res)
        if antidote_res == '是':
            witch.antidote=0
            killed_rescue = killed_num
    if witch.poison==1:
        advice=choose_advice(round_count,'夜晚','毒药决策','女巫',witch.strategy_vertex)
        res=witch.use_poison(advice=advice)
        poison_res=witch_poison_extr(input_2_json_llm,res)
        if poison_res != -1:
            witch.poison=0
            poison_kill=poison_res
    return killed_rescue,poison_kill         
def night_seer(seer,num,char_dist,game_logger,round_count):
    input_2_json_llm=base_llm("你是一个从对话内容提取json字符串的小助手，可以根据提示从对话中精准提取信息，并以规定的json格式返回")
    print("预言家开始行动：")
    advice=choose_advice(round_count,'夜晚','查验身份','预言家',seer.strategy_vertex)
    res=seer.char_val(advice=advice)
    val_res=seer_val_extr(input_2_json_llm,res)   
    if val_res==-1:
        content="预言家今夜选择不验证任何人的身份"
        print(content)
        game_logger.add_log('预言家验证身份',num,'seer',content)
    else:
        if char_dist[val_res] == 'werewolf':
            content=f"{val_res}号玩家身份被验证是狼人，属于狼人阵营"
            print(content)
        else:
            content=f"{val_res}号玩家身份被验证属于人类阵营"
            print(content)
        game_logger.add_log('预言家验证身份',num,'seer',content)
def hunter_vengence(hunter,alive_list,round_count,step):
    input_2_json_llm=base_llm("你是一个从对话内容提取json字符串的小助手，可以根据提示从对话中精准提取信息，并以规定的json格式返回")
    vengence_kill=-1
    print("猎人即将死亡，开始复仇决策：")
    advice=choose_advice(round_count,step,'猎枪决策','猎人',hunter.strategy_vertex)
    res=hunter.vengence(alive_list=alive_list,advice=advice)
    print(res)
    vengence_res=hunter_vegence_extr(input_2_json_llm,res)
    if vengence_res!= -1:
        vengence_kill=vengence_res
    return vengence_kill
def day_kill(alive_list,char_instances,game_logger,round_count):
    input_2_json_llm=base_llm("你是一个从对话内容提取json字符串的小助手，可以根据提示从对话中精准提取信息，并以规定的json格式返回")
    print("白天讨论开始：")
    alive_list.sort()
    for i in alive_list:
        advice=choose_advice(round_count,'白天','白天发言',char_instances[i].speaker,char_instances[i].strategy_vertex)
        res=char_instances[i].speech(advice=advice)
        print(f"{i}:{res}")
    votes=[]
    vote_gesture=dict()
    for i in alive_list:
        advice=choose_advice(round_count,'白天','白天投票',char_instances[i].speaker,char_instances[i].strategy_vertex)
        res=char_instances[i].day_vote()
        vote_res=day_vote_extr(input_2_json_llm,res)
        vote_gesture[i]=vote_res
        votes.append(vote_res)
    for j in vote_gesture.keys():
        log_info=f'{j}号玩家投票:{vote_gesture[j]}号玩家'
        game_logger.add_log('观察日志',-1,'moderater',log_info)
    return Counter(votes).most_common(1)[0][0]
def kill_result(alive_list,kill_list):
    for i in kill_list:
        if i in alive_list:
            alive_list.remove(i)
        else:
            print(f"{i}号玩家已经死亡，不能再次消灭！")
    return alive_list