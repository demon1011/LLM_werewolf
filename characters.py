from base_llm import base_llm


class werewolf():
    def __init__(self,char_info,num,logger,strategy):
        self.char_info=char_info
        self.llm=base_llm(self.char_info)
        self.num=num
        self.speaker='werewolf'
        self.logger=logger
        self.strategy=strategy.val['Description']
        self.strategy_vertex=strategy
    def get_cur_state(self):
        return self.logger.get_cur_log(self.speaker)
    def kill_speech(self,advice='无'):     #杀人发言
        cur_state=self.get_cur_state()
        prompt=self.char_info+cur_state+'''现在是夜晚时间，请你根据【游戏记录】中的信息，结合【游戏策略】，请仔细思考应该消灭几号玩家，并在和其他狼人的讨论中发言。
        请根据你们的胜利条件，在发言中一步一步推导得出结论，选择消灭哪个玩家胜算最大，然后把发言内容写到【发言内容】中,发言内容请简洁，必须控制在150字内,注意你的【发言内容】会被他人看到，所以请不要把策略、行动建议或其他思考内容写到里面。'''+'【游戏策略】:'+self.strategy+'\n'+'【建议】:'+advice+'\n【发言内容】:'
        result=self.llm.call_with_messages(prompt)
        res=result
        self.logger.add_log('夜晚狼人杀人发言',self.num,self.speaker,res)
        return res
    def kill_vote(self,advice='无'):     #杀人投票
        cur_state=self.get_cur_state()
        prompt=self.char_info+cur_state+'''现在是夜晚时间，请你根据【游戏记录】中的信息，结合【游戏策略】，作为一个狼人玩家，请仔细思考决定投票消灭几号玩家,并给出投票结果的玩家编号,记住你只能消灭1位玩家。
        请根据大家的发言和建议，综合考虑后把投票结果写到【投票结果】中。'''+'【游戏策略】:'+self.strategy+'\n'+'【建议】:'+advice+'\n【投票结果】:'
        result=self.llm.call_with_messages(prompt)
        res=result
        self.logger.add_log('夜晚狼人杀人投票',self.num,self.speaker,res)
        return res
    def speech(self,advice='无'):    #白天发言
        cur_state=self.get_cur_state()
        prompt=self.char_info+cur_state+'''当前是白天讨论时间，大家会按照0~7的玩家编号依次发言，现在轮到你发言，请你从你所在阵营的胜利条件出发，根据【游戏记录】中的信息，一步一步推导如何发言才能帮助狼人阵营获胜，并整理出你的发言思路，写到【发言思路】中。
        注意你的【发言思路】中一定不要使用狼人在晚上杀人的讨论和投票结果相关信息，否则可能被人发现你们狼人团队！
        '''+'\n【发言思路】:'
        thought=self.llm.call_with_messages(prompt)
        prompt=self.char_info+cur_state+'''现在是白天时间轮到你发言，请你根据本局游戏你的【游戏策略】和【建议】，适当修改、删减或补充【发言思路】作为本轮你的发言内容，并写到【发言内容】中。注意你的发言内容会被所有人听到，所以请不要把策略、行动建议或其他思考内容或评价等可能暴露你真实想法的内容写到【发言内容】里。
        '''+'【发言思路】:'+thought+'\n'+'【建议】:'+'【游戏策略】:'+self.strategy+'\n'+advice+'\n【发言内容】:'
        res=self.llm.call_with_messages(prompt)
        self.logger.add_log('白天发言',self.num,self.speaker,res)
        return res
    def day_vote(self,advice='不要投票选择自己阵营的狼人玩家消灭。'):    #白天投票
        cur_state=self.get_cur_state()
        prompt=self.char_info+cur_state+'''现在是白天投票时间，请你从你的角色和胜利条件出发，根据【游戏记录】中今天的对话和历史信息，结合【游戏策略】，仔细思考投票决定消灭几号玩家才能获胜,记住你只能消灭1位玩家。
        请一步一步思考如何投票才能让狼人阵营胜算最大，然后把投票结果写到【投票结果】中。'''+'【游戏策略】:'+self.strategy+'\n'+'【建议】:'+advice+'\n【投票结果】:'
        result=self.llm.call_with_messages(prompt)
        res=result
        self.logger.add_log('白天投票',self.num,self.speaker,res)
        return res
    
class seer():
    def __init__(self,char_info,num,logger,strategy):
        self.char_info=char_info
        self.llm=base_llm(self.char_info)
        self.num=num
        self.speaker='seer'
        self.logger=logger
        self.strategy=strategy.val['Description']
        self.strategy_vertex=strategy
    def get_cur_state(self):
        return self.logger.get_cur_log(self.speaker)
    def get_cur_state_talk(self):
        logs=self.logger.get_cur_log(self.speaker)
        log_list=logs.split('白天开始')
        talks='\n<<<'+log_list[-1]
        history='白天开始'.join(log_list[:-1])+'白天开始>>>'
        return history,talks
    def char_val(self,advice='无'):     #验身份
        cur_state=self.get_cur_state()
        prompt=self.char_info+cur_state+'''现在是夜晚时间，你可以选择1个玩家获得其真实身份信息，请你根据【游戏记录】中的信息，结合【游戏策略】，请仔细思考验证哪个嫌疑最大的玩家，并给出玩家编号,记住你只能验证一位玩家的身份。
        请仔细思考中，然后把验身份的对象玩家编号写到【玩家编号】中。'''+'【游戏策略】:'+self.strategy+'\n'+'【建议】:'+advice+'\n【玩家编号】:'
        result=self.llm.call_with_messages(prompt)
        res=result
        self.logger.add_log('预言家验证身份',self.num,self.speaker,res)
        return res
    def speech(self,advice='无'):    #白天发言
        logs,talk=self.get_cur_state_talk()
        prompt==self.char_info+logs+'''\n当前是白天讨论时间，大家会按照0~7的玩家编号依次发言，然后共同投票选择消灭一位玩家，人类玩家需要合作找到狼人玩家投票消灭他们，而狼人玩家则可能通过谎言误导人类玩家投票选择消灭人类阵营的队友。请根据你的【游戏记录】中的历史信息和本轮【投票发言】中的内容仔细思考，一步一步推理如何发言才能帮助人类阵营找到狼人，并整理出你的发言思路，写到【发言思路】中。
        '''+'\n\n【投票发言】:'+talk+'\n\n【发言思路】:'
        thought=self.llm.call_with_messages(prompt)
        prompt=self.char_info+logs+'''现在是白天时间轮到你发言，请你根据本局游戏你的【游戏策略】和【建议】，利用【游戏记录】中的信息对【发言思路】中的内容修改、删减或补充，发表你的发言内容，并写到【发言内容】中。注意你的发言内容会被所有人听到，所以请不要把策略、行动建议或其他思考内容或评价等可能暴露你真实想法的内容写到【发言内容】里。
        '''+'【发言思路】:'+thought+'\n'+'【游戏策略】:'+self.strategy+'\n'+'【建议】:'+advice+'\n【发言内容】:'
        res=self.llm.call_with_messages(prompt)
        self.logger.add_log('白天发言',self.num,self.speaker,res)
        return res
    def day_vote(self,advice='无'):    #白天投票
        logs,talk=self.get_cur_state_talk()
        prompt=self.char_info+logs+'''现在是白天投票时间，大家会选择投票消灭一位最可能是狼人的玩家，请你从你的角色和胜利条件出发，根据【游戏记录】的历史信息和【投票发言】中今天的发言记录，结合【游戏策略】，仔细思考，一步一步推导得出几号玩家最有可能是狼人并消灭他,记住你只能消灭1位玩家。然后把投票结果写到【投票结果】中。
        注意根据游戏机制，你在【游戏记录】中获得的信息是100%真实的，而在【投票发言】中可能会有人说谎，因此其中的信息可能有人在误导你！
        '''+'\n\n【投票发言】:'+talk+'\n\n【建议】:'+advice+'\n\n【投票结果】:'
        result=self.llm.call_with_messages(prompt)
        res=result
        self.logger.add_log('白天投票',self.num,self.speaker,res)
        return res

class witch():
    def __init__(self,char_info,num,logger,strategy):
        self.char_info=char_info
        self.llm=base_llm(self.char_info)
        self.num=num
        self.speaker='witch'
        self.logger=logger
        self.poison=1
        self.antidote=1
        self.strategy=strategy.val['Description']
        self.strategy_vertex=strategy
    def get_cur_state(self):
        return self.logger.get_cur_log(self.speaker)
    def get_cur_state_talk(self):
        logs=self.logger.get_cur_log(self.speaker)
        log_list=logs.split('白天开始')
        talks='\n<<<'+log_list[-1]
        history='白天开始'.join(log_list[:-1])+'白天开始>>>'
        return history,talks
    def use_poison(self,advice='无'):     #毒药
        cur_state=self.get_cur_state()
        prompt=self.char_info+cur_state+'''现在是夜晚时间，请你根据【游戏记录】中的信息，确定当前剩余存活的玩家有哪几位，然后结合【游戏策略】，仔细思考是否使用女巫的毒药消灭其中1位目前存活的玩家,记住你只能消灭1位玩家。
        请仔细思考，然后把你的决定写到【毒药决策】中。'''+'【游戏策略】:'+self.strategy+'\n'+'【建议】:'+advice+'\n【毒药决策】:'
        result=self.llm.call_with_messages(prompt)
        res=result
        self.logger.add_log('毒药决策',self.num,self.speaker,res)
        return res
    def use_antidote(self,killed_player,advice="1.如果被消灭的玩家是你自己，一定要使用解药；2.如果你确定被消灭的玩家是预言家，可以考虑使用解药；3.根据胜利条件和当前剩余玩家的角色判断即将输掉比赛，请使用解药解救该玩家。"):     #解药
        cur_state=self.get_cur_state()
        prompt=self.char_info+'【游戏策略】:'+self.strategy+'\n'+cur_state+'''现在是夜晚时间,%d号玩家被狼人消灭,请你根据【游戏记录】中的历史信息，结合【游戏策略】，请仔细思考，并是否使用解药复活该玩家。
        请仔细思考，然后把你的决定写到【解药决策】中。'''%(killed_player)+'【建议】:'+advice+'\n【解药决策】:'
        result=self.llm.call_with_messages(prompt)
        res=result
        self.logger.add_log('解药决策',self.num,self.speaker,res)
        return res
    def speech(self,advice='无'):    #发言
        logs,talk=self.get_cur_state_talk()
        prompt=self.char_info+logs+'''\n当前是白天讨论时间，大家会按照0~7的玩家编号依次发言，然后共同投票选择消灭一位玩家，人类玩家需要合作找到狼人玩家投票消灭他们，而狼人玩家则可能通过谎言误导人类玩家投票选择消灭人类阵营的队友。请根据你的【游戏记录】中的历史信息和本轮【投票发言】中的内容仔细思考，一步一步推理如何发言才能帮助人类阵营找到狼人，并整理出你的发言思路，写到【发言思路】中。
        '''+'\n\n【投票发言】:'+talk+'\n\n【发言思路】:'
        thought=self.llm.call_with_messages(prompt)
        prompt=self.char_info+logs+'''现在是白天时间轮到你发言，请你根据本局游戏你的【游戏策略】和【建议】，利用【游戏记录】中的信息对【发言思路】中的内容修改、删减或补充，发表你的发言内容，并写到【发言内容】中。注意你的发言内容会被所有人听到，所以请不要把策略、行动建议或其他思考内容或评价等可能暴露你真实想法的内容写到【发言内容】里。
        '''+'【发言思路】:'+thought+'\n'+'【游戏策略】:'+self.strategy+'\n'+'【建议】:'+advice+'\n【发言内容】:'
        res=self.llm.call_with_messages(prompt)
        self.logger.add_log('白天发言',self.num,self.speaker,res)
        return res
    def day_vote(self,advice='无'):    #白天投票
        logs,talk=self.get_cur_state_talk()
        prompt=self.char_info+logs+'''现在是白天投票时间，大家会选择投票消灭一位最可能是狼人的玩家，请你从你的角色和胜利条件出发，根据【游戏记录】的历史信息和【投票发言】中今天的发言记录，结合【游戏策略】，仔细思考，一步一步推导得出几号玩家最有可能是狼人并消灭他,记住你只能消灭1位玩家。然后把投票结果写到【投票结果】中。
        注意根据游戏机制，你在【游戏记录】中获得的信息是100%真实的，而在【投票发言】中可能会有人说谎，因此其中的信息可能有人在误导你！
        '''+'\n\n【投票发言】:'+talk+'\n\n【建议】:'+advice+'\n\n【投票结果】:'
        result=self.llm.call_with_messages(prompt)
        res=result
        self.logger.add_log('白天投票',self.num,self.speaker,res)
        return res

class villager():
    def __init__(self,char_info,num,logger,strategy):
        self.char_info=char_info
        self.llm=base_llm(self.char_info)
        self.num=num
        self.speaker='villager'
        self.logger=logger
        self.strategy=strategy.val['Description']
        self.strategy_vertex=strategy
    def get_cur_state(self):
        return self.logger.get_cur_log(self.speaker)
    def get_cur_state_talk(self):
        logs=self.logger.get_cur_log(self.speaker)
        log_list=logs.split('白天开始')
        talks='\n<<<'+log_list[-1]
        history='白天开始'.join(log_list[:-1])+'白天开始>>>'
        return history,talks
    def speech(self,advice='无'):    #发言
        logs,talk=self.get_cur_state_talk()
        prompt=self.char_info+logs+'''\n当前是白天讨论时间，大家会按照0~7的玩家编号依次发言，然后共同投票选择消灭一位玩家，人类玩家需要合作找到狼人玩家投票消灭他们，而狼人玩家则可能通过谎言误导人类玩家投票选择消灭人类阵营的队友。请根据你的【游戏记录】中的历史信息和本轮【投票发言】中的内容仔细思考，一步一步推理如何发言才能帮助人类阵营找到狼人，并整理出你的发言思路，写到【发言思路】中。
        '''+'\n\n【投票发言】:'+talk+'\n\n【发言思路】:'
        thought=self.llm.call_with_messages(prompt)
        prompt=self.char_info+logs+'''现在是白天时间轮到你发言，请你根据本局游戏你的【游戏策略】和【建议】，利用【游戏记录】中的信息对【发言思路】中的内容修改、删减或补充，发表你的发言内容，并写到【发言内容】中。注意你的发言内容会被所有人听到，所以请不要把策略、行动建议或其他思考内容或评价等可能暴露你真实想法的内容写到【发言内容】里。
        '''+'【发言思路】:'+thought+'\n'+'【游戏策略】:'+self.strategy+'\n'+'【建议】:'+advice+'\n【发言内容】:'
        res=self.llm.call_with_messages(prompt)
        self.logger.add_log('白天发言',self.num,self.speaker,res)
        return res
    def day_vote(self,advice='无'):    #白天投票
        logs,talk=self.get_cur_state_talk()
        prompt=self.char_info+logs+'''现在是白天投票时间，大家会选择投票消灭一位最可能是狼人的玩家，请你从你的角色和胜利条件出发，根据【游戏记录】的历史信息和【投票发言】中今天的发言记录，结合【游戏策略】，仔细思考，一步一步推导得出几号玩家最有可能是狼人并消灭他,记住你只能消灭1位玩家。然后把投票结果写到【投票结果】中。
        注意根据游戏机制，你在【游戏记录】中获得的信息是100%真实的，而在【投票发言】中可能会有人说谎，因此其中的信息可能有人在误导你！
        '''+'\n\n【投票发言】:'+talk+'\n\n【建议】:'+advice+'\n\n【投票结果】:'
        result=self.llm.call_with_messages(prompt)
        res=result
        self.logger.add_log('白天投票',self.num,self.speaker,res)
        return res
    
class hunter():
    def __init__(self,char_info,num,logger,strategy):
        self.char_info=char_info
        self.llm=base_llm(self.char_info)
        self.num=num
        self.speaker='hunter'
        self.logger=logger
        self.strategy=strategy.val['Description']
        self.strategy_vertex=strategy
    def get_cur_state(self):
        return self.logger.get_cur_log(self.speaker)
    def get_cur_state_talk(self):
        logs=self.logger.get_cur_log(self.speaker)
        log_list=logs.split('白天开始')
        talks='\n<<<'+log_list[-1]
        history='白天开始'.join(log_list[:-1])+'白天开始>>>'
        return history,talks
    def vengence(self,alive_list,advice='无'):     #复仇子弹
        cur_state=self.get_cur_state()
        alive_info="当前存活玩家:"
        for i in alive_list:
            alive_info+= str(i)+"号玩家、"
        alive_info=alive_info[:-1]+'。'
        prompt=self.char_info+'''现在你即将被消灭，请你从你的角色和胜利条件出发，根据【游戏记录】中的信息，结合【游戏策略】，请仔细思考是否使用猎人的猎枪复仇消灭一名玩家，以及消灭几号玩家,记住你只能消灭1位玩家。
        请仔细思考，然后把你的决定写到【猎枪决策】中。'''+'【游戏策略】:'+self.strategy+'\n'+cur_state+'【建议】:'+advice+'\n'+alive_info+'\n【猎枪决策】:'
        result=self.llm.call_with_messages(prompt)
        res=result
        self.logger.add_log('猎枪决策',self.num,self.speaker,res)
        return res
    def speech(self,advice='无'):    #发言
        logs,talk=self.get_cur_state_talk()
        prompt=self.char_info+logs+'''\n当前是白天讨论时间，大家会按照0~7的玩家编号依次发言，然后共同投票选择消灭一位玩家，人类玩家需要合作找到狼人玩家投票消灭他们，而狼人玩家则可能通过谎言误导人类玩家投票选择消灭人类阵营的队友。请根据你的【游戏记录】中的历史信息和本轮【投票发言】中的内容仔细思考，一步一步推理如何发言才能帮助人类阵营找到狼人，并整理出你的发言思路，写到【发言思路】中。
        '''+'\n\n【投票发言】:'+talk+'\n\n【发言思路】:'
        thought=self.llm.call_with_messages(prompt)
        prompt=self.char_info+logs+'''现在是白天时间轮到你发言，请你根据本局游戏你的【游戏策略】和【建议】，利用【游戏记录】中的信息对【发言思路】中的内容修改、删减或补充，发表你的发言内容，并写到【发言内容】中。注意你的发言内容会被所有人听到，所以请不要把策略、行动建议或其他思考内容或评价等可能暴露你真实想法的内容写到【发言内容】里。
        '''+'【发言思路】:'+thought+'\n'+'【游戏策略】:'+self.strategy+'\n'+'【建议】:'+advice+'\n【发言内容】:'
        res=self.llm.call_with_messages(prompt)
        self.logger.add_log('白天发言',self.num,self.speaker,res)
        return res
    def day_vote(self,advice='无'):    #白天投票
        logs,talk=self.get_cur_state_talk()
        prompt=self.char_info+logs+'''现在是白天投票时间，大家会选择投票消灭一位最可能是狼人的玩家，请你从你的角色和胜利条件出发，根据【游戏记录】的历史信息和【投票发言】中今天的发言记录，结合【游戏策略】，仔细思考，一步一步推导得出几号玩家最有可能是狼人并消灭他,记住你只能消灭1位玩家。然后把投票结果写到【投票结果】中。
        注意根据游戏机制，你在【游戏记录】中获得的信息是100%真实的，而在【投票发言】中可能会有人说谎，因此其中的信息可能有人在误导你！
        '''+'\n\n【投票发言】:'+talk+'\n\n【建议】:'+advice+'\n\n【投票结果】:'
        result=self.llm.call_with_messages(prompt)
        res=result
        self.logger.add_log('白天投票',self.num,self.speaker,res)
        return res
    
