from collections import Counter
import re

import os
import sys
project_root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,project_root)
from base_llm import base_llm


class reflector():
    def __init__(self,logger):
        self.llm=base_llm('你是一个优秀的狼人杀玩家')
        self.logger=logger
    def get_log(self,game_name):
        return self.logger.check_logs(game_name)
    def get_game_names(self):
        return self.logger.find_all_games()
    def self_evaluation(self,sample_times=8):
        #自我评估：通过对某局游戏进行检查，反思失败方为什么会失败。
        #step1：确定游戏玩家的角色和双方的胜利条件。
        #step2：总结整个游戏过程，以及胜利方的胜利过程。
        #step3：对失败方出现错误的环节进行分析(白天投票-白天发言、毒药策略、解药策略、猎枪策略、验人策略)
        #step4：定位关键环节（角色，失误点）
        i=0
        sample_list=[]
        content_list=[]
        while i<sample_times:
            log=self.get_log(self.logger.table_name)
            prompt='''请你对**游戏记录**中的某局狼人杀游戏进行分析,结合游戏胜利规则（人类阵营胜利条件是所有狼人被消灭；狼人阵营胜利条件是2个普通村民全被消灭，或3个神职人员全被消灭。）指出失败方是哪个阵营，然后根据整个流程一步步分析推理，根据分析结论得到失败阵营中失误最大的玩家极其行为是什么。
            你可以按照以下步骤开展工作：
            1.回顾**游戏记录**的内容，整理整个游戏的过程总结，包含每个黑夜和白天发生了什么事情，最终失败方是人类阵营还是狼人阵营；
            2.根据步骤1的总结内容，定位出失败方阵营输掉游戏的最关键的1个环节，具体是哪一天的哪个环节，导致失败方阵营失去了关键人物或陷入被动的局势；
            3.根据步骤2确定出来的关键环节，根据**游戏记录**该环节中，失败方阵营里存活的玩家还剩几位，详细检查他们在关键环节的行为记录；
            4.分析步骤3中失败方阵营玩家的思考和行为进行，确定失败方哪个角色应该负有最大的责任；
            4.根据步骤2定位的关键环节和步骤3确定的失败方最大责任角色，分析该最大责任角色玩家在关键环节的具体行为，为什么会导致失败方阵营在该环节出现失误或陷入被动；
            5.将分析结果写到**分析过程**中；
            6.根据**分析过程**的内容，从失败阵营的角色中选出导致失败的最重要的环节和对应的角色玩家编号，并写入**失败角色**中,以json形式返回:
            {
                "失败角色":"玩家编号"，
                "失败原因":"原因分析"
            }；
            注意：除了狼人玩家知道狼人队友的身份以外，所有玩家在游戏中并不知道其他人的身份，所以你的分析应该考虑该玩家在信息不完整的情况下当时定的策略是否有问题，而不是简单地指出问题；
            
            **游戏记录**
            %s
            **分析过程**
            '''%(log)
            res=self.llm.call_with_messages(prompt,temp=0.5)
            print(res)
            info=re.search(r'"失败角色":\s*"([^"]*)",\s*"失败原因":\s*"([^"]*)"',res)
            eval_dict={}
            if info:
                eval_dict['失败角色']=info.group(1)
                eval_dict['失败原因']=info.group(2)
                sample_list.append(eval_dict['失败角色'])
                content_list.append(eval_dict)
            i+=1
        char_count=Counter(sample_list)
        chosen_count=char_count.most_common(1)[0][0]
        print(f"the most common time is {char_count.most_common(1)[0][1]} in {sample_times}")
        if char_count.most_common(1)[0][1]>0.6*sample_times:
            chosen_indexes=[i for i,x in enumerate(sample_list) if x==chosen_count]
            eval_dict_res=content_list[chosen_indexes[0]]
        else:
            eval_dict_res={}
        return eval_dict_res
    def self_reflection(self,char,reason):
        log=self.get_log(self.logger.table_name)
        prompt='''请你根据**失败角色**和**失败原因**中的内容，对**游戏记录**中的某局狼人杀游戏记录中该角色的玩法，一步一步仔细推理，提出具体可行的建议，以帮助提高其他玩家在以后的游戏中提高游戏水平。
        你可以按照以下步骤开展工作:
        1.根据**失败角色**和**失败原因**的内容，定位该角色出现最关键失误点应该在**游戏记录**中的哪个部分；
        2.根据失误的地方之前的**游戏记录**内容，总结该角色出现失误之前整个游戏的局面如何，包含当时剩余的存活职业有哪些，以及各职业的技能使用状况(例如猎人的猎枪，女巫的解药毒药是否已使用等)；
        3.针对**失败角色**对应的游戏职业，基于**失败原因**的经验提出通用的游戏建议，包括具体在哪一天，什么局面之下，应该如何针对最关键失误点进行优化,写到**分析过程**中；
        4.基于**分析过程**，把**经验总结**通过以下json形式给出：
        {
            "角色职业":"角色职业",
            "游戏建议":"建议内容",
            "游戏环节":"游戏建议适用的具体时间点环节(第0天夜晚/第1天白天/第1天夜晚/第2天白天/第2天夜晚/第3天白天/第3天夜晚等) "，
            "游戏技能"：“游戏技能（白天发言/白天投票/查验身份/解药决策/毒药决策/猎枪决策/狼人杀人）”，
            "游戏局面":"游戏建议适用的当下局面(包含剩余存活职业、技能使用状况，以及本轮其他角色已发言内容等)"
        }
        注意：1.你的"游戏建议"必须与"游戏局面"有严谨的逻辑联系，即"游戏建议"是因为处在对应的"游戏局面"下才有效；
             2.为了让你的建议具有通用性，"游戏建议"和"游戏局面"的描述中必须使用角色职业而不是玩家编号进行描述；
             3.为了让你的"游戏建议"更有针对性，"游戏技能"的选项中只能选择最相关的1个技能作为建议给出；
        **失败角色**
        %s
        **失败原因**
        %s
        **游戏记录**
        %s
        **分析过程**
        
        '''%(char,reason,log)
        res=self.llm.call_with_messages(prompt)
        info=re.search(r'"角色职业":\s*"([^"]*)",\s*"游戏建议":\s*"([^"]*)",\s*"游戏环节":\s*"([^"]*)",\s*"游戏技能":\s*"([^"]*)",\s*"游戏局面":\s*"([^"]*)"',res)
        reflect_dict={}
        if info:
            reflect_dict['角色职业']=info.group(1)
            reflect_dict['游戏建议']=info.group(2)
            reflect_dict['游戏环节']=info.group(3)
            reflect_dict['游戏技能']=info.group(4)
            reflect_dict['游戏局面']=info.group(5)
        return reflect_dict