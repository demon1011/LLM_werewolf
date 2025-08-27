import sqlite3
import pandas as pd
from datetime import datetime

class admin_logger():
    def __init__(self,db_name):
        self.db_name=db_name
    def find_all_games(self):
        self.conn=sqlite3.connect(self.db_name)
        sql="SELECT name FROM sqlite_master WHERE type='table'AND name NOT LIKE 'sqlite_%';"
        games = pd.read_sql_query(sql, self.conn)
        self.conn.commit()
        self.conn.close()
        return games
    def drop_game(self,table_name):
        self.conn=sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        drop_query = f"DROP TABLE IF EXISTS {table_name};"
        self.cursor.execute(drop_query)
        self.cursor.close()
        self.conn.close()
    def get_row_count(self, table_name):
        """
        查询指定表中的行数。
        
        :param table_name: 要查询的表的名称
        :return: 表中的行数
        """
        self.conn=sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        query = f"SELECT COUNT(*) FROM `{table_name}`;"
        try:
            self.cursor.execute(query)
            row_count = self.cursor.fetchone()[0]
            self.cursor.close()
            self.conn.close()
            return row_count
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
    def check_logs(self,table_name):
        self.conn=sqlite3.connect(self.db_name)
        df = pd.read_sql_query(f"SELECT * FROM '{table_name}' ", self.conn)
        night=1
        day=0
        history_log="【游戏记录】:\n"+f"第 %d 夜:\n"%night
        for index, row in df.iterrows():
            if row['speaker']=='moderater':
                if row['content']=='夜晚结束' and index < len(df)-1:
                    day+=1
                    history_log+=f"第 %d 天:\n"%day
                elif row['content']=='白天结束' and index <len(df)-1:
                    night+=1
                    history_log+=f"第 %d 夜:\n"%night
                elif index == len(df)-1:
                    pass
                else:
                    formatted_log = f"发生事件: {row['content']}"
                    history_log+=formatted_log +"\n"
            else:
                formatted_log = f"{row['player']}号玩家执行 {row['type']}: {row['content']}"
                history_log+=formatted_log +"\n"
        self.conn.close()
        return history_log

class game_logger(admin_logger):
    def __init__(self,db_name):
        self.db_name=db_name
        self.table_name="game_"+datetime.now().strftime("%Y%m%d%H%M%S")
        self.conn=sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        create_table_sql = f'''CREATE TABLE IF NOT EXISTS {self.table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        player INT NOT NULL,
        speaker TEXT NOT NULL,
        content TEXT NOT NULL
            )
        '''
        self.cursor.execute(create_table_sql)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
    def add_log(self,log_type,num,speaker,content):
        self.conn=sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        insert_sql = f"INSERT INTO '{self.table_name}' (type,player, speaker,content) VALUES (?, ?, ?,?)"
        self.cursor.execute(insert_sql, (log_type,num, speaker,content))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        return 0
    def optimize_recent_log(self,content):
        self.conn=sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        query_latest_id=f"SELECT MAX(id) FROM '{self.table_name}'"
        self.cursor.execute(query_latest_id)
        latest_id=self.cursor.fetchone()[0]
        update_query=f"UPDATE '{self.table_name}' SET content = '{content}' WHERE id = {latest_id}"
        self.cursor.execute(update_query)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        return 0
    def get_cur_log(self,speaker):
        self.conn=sqlite3.connect(self.db_name)
        translator={'werewolf':'狼人',
                    'seer':'预言家',
                    'witch':'女巫',
                    'villager':'村民',
                    'hunter':'猎人',
                    'moderater':'裁判'}
        if speaker=="werewolf":
            allowed_speaker={'werewolf':['夜晚狼人杀人发言','白天发言'],
                            'seer':['白天发言'],
                            'witch':['白天发言'],
                            'villager':['白天发言'],
                            'hunter':['白天发言'],
                            'moderater':['观察日志']}
            df = pd.read_sql_query(f"SELECT * FROM '{self.table_name}' ", self.conn)
            night=0
            day=1
            history_log="【游戏记录】:\n<<<"+f"第 %d 夜:\n"%night
            for index, row in df.iterrows():
                if row['type'] in allowed_speaker[row['speaker']]:
                    if row['speaker']=='moderater':
                        formatted_log = f"发生事件: {row['content']}"
                        history_log+=formatted_log +"\n"
                    else:
                        formatted_log = f"{row['player']}号玩家执行 {row['type']}: {row['content']}"
                        history_log=history_log+formatted_log +"\n"
            history_log+='>>>'
            self.conn.close()
            return history_log
        elif speaker=="seer":
            allowed_speaker={'werewolf':['白天发言'],
                            'seer':['预言家验证身份','白天发言'],
                            'witch':['白天发言'],
                            'villager':['白天发言'],
                            'hunter':['白天发言'],
                            'moderater':['观察日志']}
            df = pd.read_sql_query(f"SELECT * FROM '{self.table_name}' ", self.conn)
            night=1
            day=1
            history_log="【游戏记录】:\n<<<"+f"第 %d 夜:\n"%night
            for index, row in df.iterrows():
                if row['type'] in allowed_speaker[row['speaker']]:
                    if row['speaker']=='moderater':
                        formatted_log = f"发生事件: {row['content']}"
                        history_log+=formatted_log +"\n"
                    else:
                        formatted_log = f"{row['player']}号玩家执行 {row['type']}: {row['content']}"
                        history_log=history_log+formatted_log +"\n"
            history_log+='>>>'
            self.conn.close()
            return history_log
        elif speaker=="witch":
            allowed_speaker={'werewolf':['白天发言'],
                            'seer':['白天发言'],
                            'witch':['解药决策','毒药决策','白天发言'],
                            'villager':['白天发言'],
                            'hunter':['白天发言'],
                            'moderater':['观察日志']}
            df = pd.read_sql_query(f"SELECT * FROM '{self.table_name}' ", self.conn)
            night=1
            day=1
            history_log="【游戏记录】:\n<<<"+f"第 %d 夜:\n"%night
            for index, row in df.iterrows():
                if row['type'] in allowed_speaker[row['speaker']]:
                    if row['speaker']=='moderater':
                        formatted_log = f"发生事件: {row['content']}"
                        history_log=history_log+formatted_log +"\n"
                    else:
                        formatted_log = f"{row['player']}号玩家执行 {row['type']}: {row['content']}"
                        history_log=history_log+formatted_log +"\n"
            history_log+='>>>'
            self.conn.close()
            return history_log
        else:
            allowed_speaker={'werewolf':['白天发言'],
                            'seer':['白天发言'],
                            'witch':['白天发言'],
                            'villager':['白天发言'],
                            'hunter':['白天发言'],
                            'moderater':['观察日志']}
            df = pd.read_sql_query(f"SELECT * FROM '{self.table_name}' ", self.conn)
            night=1
            day=1
            history_log="【游戏记录】:\n<<<"+f"第 %d 夜:\n"%night
            for index, row in df.iterrows():
                if row['type'] in allowed_speaker[row['speaker']]:
                    if row['speaker']=='moderater':
                        formatted_log = f"发生事件: {row['content']}"
                        history_log+=formatted_log +"\n"
                    else:
                        formatted_log = f"{row['player']}号玩家执行 {row['type']}: {row['content']}"
                        history_log=history_log+formatted_log +"\n"
            history_log+='>>>'
            self.conn.close()
            return history_log
        def close_connection(self):
            self.cursor.close()
            self.conn.close()
            return 0