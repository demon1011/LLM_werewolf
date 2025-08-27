from game_init import game_init
from day import day
from night import night
from reflection import self_reflection

def game_start():
    alive_list,char_dist,char_instances,logger,char_strategies=game_init()
    game_result=0
    round_counter=0
    while round_counter<5:
        game_res,alive_list=night(logger,alive_list,char_dist,char_instances,round_counter)
        game_result=game_res
        if game_result>0:
            print(alive_list)
            print(char_dist)
            break
        else:  
            round_counter+=1
            game_res,alive_list=day(logger,alive_list,char_dist,char_instances,round_counter)
            game_result=game_res
            if game_result>0:
                print(alive_list)
                print(char_dist)
                break
    reflect_res=self_reflection(logger,char_strategies)
    print(game_result)
    print(alive_list)
    print(char_dist)
    print(f'reflection_result:{reflect_res}')
    return game_result

if __name__=="__main__":
    res_list=[]
    for i in range(10):
        a=game_start()
        res_list.append(a)
    print(res_list)