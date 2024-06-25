from database.DB_connect import DBConnect
from model.team import Team


class DAO():
    @staticmethod
    def getYear():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct t.`year` as year
                        from teams t 
                        where t.`year` >= 1980  """
            cursor.execute(query, )
            for row in cursor:
                result.append(row["year"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getTeam(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct t.teamCode as code,  t.name as name 
                        from teams t 
                        where t.`year` = %s  """
            cursor.execute(query, (year,) )
            for row in cursor:
                result.append(Team(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getSalario(year, code1):
        cnx = DBConnect.get_connection()
        result = 0
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT sum(s.salary) as peso
                        FROM (select t2.ID as id
                        from teams t2
                        where t2.teamCode = %s) as tmp, salaries s , teams t , appearances a 
                        WHERE s.`year` = t.`year` and t.`year` = a.`year` 
                        and a.`year` = %s
                        and t.teamCode = %s
                        and tmp.ID = a.teamID 
                        and s.playerID = a.playerID"""
            cursor.execute(query, (code1, year, code1))
            for row in cursor:
                result = row["peso"]
            cursor.close()
            cnx.close()
        return result
