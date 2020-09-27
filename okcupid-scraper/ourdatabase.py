import sqlite3
import os

create_database_script = """CREATE TABLE IF NOT EXISTS profile_id (
                                    id bigserial,
                                    ok_id varchar(50),
                                    accepted varchar (10)
                                );
                            
                                CREATE TABLE IF NOT EXISTS profile_info (
                                    id bigserial,
                                    ok_id varchar(50),
                                    type varchar(30),
                                    category varchar(30),
                                    title varchar(200),
                                    content varchar(7999)
                                );
                            
                                CREATE TABLE IF NOT EXISTS profile_question (
                                    id bigserial,
                                    ok_id varchar(50),
                                    question_text varchar(200),
                                    answer varchar(100),
                                    answer_position varchar(10)
                                );
                                    
                                CREATE TABLE IF NOT EXISTS questions (
                                    id bigserial,
                                    question_text varchar(200),
                                    choices varchar (200),
                                    num_choices varchar(10)
                                    );"""


class dataBase:
    """This class is used to create and/or connect to a sqlite db and store the data"""

    def __init__(self, filename):
        """We initialise here the db so that it looks cleaner in other files"""
        if os.path.isfile(filename):
            print("A database with the same name as specified exists and will be used")
        else:
            print("A new database will be created")
            sqlite3.connect(filename).cursor()

        self.__connection = sqlite3.connect(filename)
        self.__c = self.__connection.cursor()
        self.__c.executescript(create_database_script)

    def close(self):
        self.__connection.close()

    def __show_tables(self):
        """For test purposes"""
        script = """SELECT 
                    name
                    FROM 
                        sqlite_master 
                    WHERE 
                        type ='table' AND 
                        name NOT LIKE 'sqlite_%';"""
        self.__c.execute(script)
        print(self.__c.fetchall())

    def save_profile_to_db(self, dict_data, decision):
        """As named"""
        # Log the profile to the profile_db in order to find it later
        self.__c.execute("""INSERT INTO profile_id (ok_id, accepted) VALUES
                                (?,?);""", (dict_data.get('id'), decision))

        # Log the profile info to the profile_info db
        # First, basic info
        self.__c.execute("""INSERT INTO profile_info (ok_id, type, category, title, content) VALUES
                                (?, ?, ?, ?, ?);""",
                        (dict_data.get('id'), 'age', 'NULL', 'NULL', dict_data.get('age')))

        self.__c.execute("""INSERT INTO profile_info (ok_id, type, category, title, content) VALUES
                                        (?, ?, ?, ?, ?);""",
                         (dict_data.get('id'), 'location', 'NULL', 'NULL', dict_data.get('location')))

        # Then profile details
        details_types = ['basic', 'badge', 'pronoun', 'looks', 'background', 'lifestyle', 'family', 'wiw']
        for detail in details_types :
            if detail in dict_data.get('details').keys():
                print(dict_data['details'][detail])
                self.__c.execute("""INSERT INTO profile_info (ok_id, type, category, title, content) VALUES
                                                (?, ?, ?, ?, ?);""",
                                (dict_data.get('id'), 'detail', detail, 'NULL', dict_data['details'][detail]))
                self.__connection.commit()

        # Now, essays
        for essay in dict_data.get('essays'):
            self.__c.execute("""INSERT INTO profile_info (ok_id, type, category, title, content) VALUES
                                            (?, ?, ?, ?, ?);""",
                             (dict_data.get('id'), 'essay', essay.get('category').lower(), essay.get('title'), essay.\
                              get('contents')))
        self.__connection.commit()

    def save_question_type_to_db(self, question, answers):

        str_answers = '|'.join(str(elem) for elem in answers)
        self.__c.execute("""INSERT INTO questions (question_text, choices, num_choices) VALUES
                                (?,?,?);""", (question, str_answers, len(answers)))
        self.__connection.commit()






















