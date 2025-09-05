import pygraphs as pg

class memory_admin():
    def __init__(self,graph_name):
        self.graph_name=graph_name
        self.pg=pg.load_db(self.graph_name)
    def delete_mem(self,mem,mem_type='vertex'):
        #删除一个已有的memory
        assert mem_type in ['vertex','edge']
        if mem_type=='vertex':
            if type(mem)==list:
                self.pg.del_vertexes(mem)
            else:
                self.pg.del_vertexe([mem])
        if mem_type=='edge':
            if type(mem)==list:
                self.pg.del_edges(mem)
            else:
                self.pg.del_edge([mem])
    def find_vertex(self,filter_type='type',type_name=None,src_filter=None,dst_filter=None,relation_type=None,filter_dict=None):
        assert filter_type in ['type','src','dst']
        if filter_type=='type':
            query_elements = self.pg.query(condition_vertex=lambda x: ('Type' in x) and x['Type'] == type_name)
        else:
            query_elements=[]
            if src_filter:
                query_edges=src_filter.dst
                for edge in query_edges:
                    if relation_type:
                        if edge.val['Type']==relation_type:
                            query_elements.append(edge.dst)
                    else:
                        query_elements.append(edge.dst)      
            if dst_filter:
                query_edges=dst_filter.src
                for edge in query_edges:
                    if relation_type:
                        if edge.val['Type']==relation_type:
                            query_elements.append(edge.src)
                    else:
                        query_elements.append(edge.src)   
        if filter_dict:
            res_list=list(query_elements)
            for fil_key in filter_dict.keys():
                for element in res_list:
                    if filter_dict[fil_key] not in element.val[fil_key]:
                        res_list.remove(element)
            if len(res_list)==1:
                res=res_list[0]
                for fil_key in filter_dict.keys():
                    if filter_dict[fil_key] not in res.val[fil_key]:
                        return '无'
                return res_list
            return res_list
        return list(query_elements)
    def consult_strategy(self,character):
        #搜索一个对应的策略
        return self.pg.query(condition_vertex=lambda x: x['Type'] == 'Strategy' and x['character'] == character)
    def consult_advice(self,src_strategy,search_dict):
        #搜索一个对应的行为建议
        ##抛开strategy限制
        res=self.find_vertex(filter_type='type',type_name='advice',filter_dict=search_dict)
        #################
#        res=self.find_vertex(filter_type='src',src_filter=src_strategy,relation_type='HasAdvice',filter_dict=search_dict)
        return res
    def consult_team_strategy(self):
        #搜索一个对应的团队策略
        pass
    def add_advice(self,src_strategy,related_strategies,content):
        strategy_name=src_strategy.primary_key
        related_names=[relates.primary_key for relates in related_strategies]
        related_names.sort()
        primary_key=strategy_name+'-related-'+'_'.join(related_names)+'-advice-'+content['角色职业']+'_'+content['游戏环节']+'_'+content['游戏技能'] 
        content['primary_key']=primary_key
        content['Type']='advice'
        self.pg.add_vertexes_from_list(vertexes_list=[[primary_key,content]])
        ####增加edge############
        edge_list=[]
        edge_list.append([strategy_name,{'Type':'HasAdvice'},primary_key])
        for rlt_advice in related_names:
            edge_list.append([rlt_advice,{'Type':'RalatedStrategy'},primary_key])
        self.pg.add_edges_from_list(edges_list=edge_list)
        #################
        return 0
    def merge_advice(self,target_vertex,content):
        exist_content=target_vertex.val
        new_content=dict()
        print("merging advice, possible conflict between advices:")
        print("existed advice:")
        print(exist_content)
        print("advice to be added:")
        print(content)
        new_content['primary_key']=exist_content['primary_key']
        new_content['角色职业']=exist_content['角色职业']
        new_content['游戏环节']=exist_content['游戏环节']
        new_content['游戏技能']=exist_content['游戏技能']
        new_content['游戏局面']=exist_content['游戏局面']+'###'+content['游戏局面']
        new_content['游戏建议']=exist_content['游戏建议']+'###'+content['游戏建议']
        self.pg.set_val(target_vertex,new_content)
        return 0
    def update_advice(self,src_strategy,related_strategies,content):
        strategy_name=src_strategy.primary_key
        related_names=[relates.primary_key for relates in related_strategies]
        related_names.sort()
        primary_key=strategy_name+'-related-'+'_'.join(related_names)+'-advice-'+content['角色职业']+'_'+content['游戏环节']+'_'+content['游戏技能']
        print(primary_key)
        exist_vertex=self.pg.query(condition_vertex=lambda x: ('primary_key' in x) and x['primary_key'] == primary_key)
        if len(exist_vertex)==0:
            print('adding new advice!')
            res=self.add_advice(src_strategy,related_strategies,content)
        else:
            print('merging advice!')
            target_vertex=list(exist_vertex)[0]
            content['primary_key']=primary_key
            res=self.merge_advice(target_vertex=target_vertex,content=content)
        pg.save_db(self.pg,self.graph_name)
        return res
    def delete_advice(self,primary_key):
        exist_vertex=self.pg.query(condition_vertex=lambda x: ('primary_key' in x) and x['primary_key'] == primary_key)
        if len(exist_vertex)==0:
            print('vertex not exist!')
            return 1
        else:
            vertex=list(exist_vertex)[0]
            sub_advices=vertex.val['游戏建议'].split('###')
            if len(sub_advices)>1:
                advice_content=vertex.val
                advice_content['游戏局面']='###'.join(advice_content['游戏局面'].split('###')[:-1])
                advice_content['游戏建议']='###'.join(advice_content['游戏建议'].split('###')[:-1])
                self.pg.set_val(vertex,advice_content)
                pg.save_db(self.pg,self.graph_name)
                return 0
            else:
                self.pg.del_edges(edges_to_del=list(vertex.src))
                self.pg.del_edges(edges_to_del=list(vertex.dst))
                self.pg.del_vertex(vertex_to_del=vertex)
                pg.save_db(self.pg,self.graph_name)
                return 0
