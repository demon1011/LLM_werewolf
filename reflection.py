from utils.reflection_process import reflector
from memory_admin import memory_admin

def self_reflection(logger,char_strategies):
    reflect=reflector(logger)
    mem_admin=memory_admin('graph_werewolf.db') 
    num_list=[]
    step_list=[]
    max_retries=3
    for i in range(8):
        num_list.append(f'{i}号玩家')
    for i in range(5):
        for j in ['白天','夜晚']:
            step_list.append(f'第{i}天'+j)
    retries=0
    while retries<max_retries:
        try:
            retries+=1
            eval_info=reflect.self_evaluation()
            print(eval_info)
            assert '失败角色' in eval_info.keys()
            print('评估结果置信度检查正常')
            assert eval_info['失败角色'] in num_list
            reflection=reflect.self_reflection(eval_info['失败角色'],eval_info['失败原因'])
            print(reflection)
            assert reflection['角色职业'] in ['狼人','预言家','女巫','猎人','村民']
            print('角色职业格式检查正常。')
            assert reflection['游戏技能'] in ['白天发言','白天投票','查验身份','解药决策','毒药决策','猎枪决策','狼人杀人']
            print('游戏技能格式检查正常。')
            assert any(x in reflection['游戏环节'] for x in step_list)
            print('游戏环节格式检查正常。')
            assert '号玩家'  not in reflection['游戏建议']
            print('游戏建议通用性检查正常。')
            num_key=eval_info['失败角色'][0]
            related_strategy=[]
            for key in char_strategies.keys():
                if str(key)==num_key:
                    src_strategy=char_strategies[key]
                else:
                    related_strategy.append(char_strategies[key])
            related_strategy=list(set(related_strategy))
            res=mem_admin.update_advice(src_strategy,related_strategy,reflection)
            break
        except Exception as e:
            print(e)
    if retries==max_retries:
        return 1
    else:
        return res