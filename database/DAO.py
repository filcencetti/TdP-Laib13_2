from database.DB_connect import DBConnect
from model.driver import Driver


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def getAllSeasons():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = """
                select s.year
                from seasons s
                """
        cursor.execute(query)

        for row in cursor:
            result.append(row[0])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllPilots(season):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select d.driverId, d.driverRef, d.number, d.code, d.forename, d.surname, d.dob, d.nationality, d.url
                from drivers d, results re, races ra
                where d.driverId = re.driverId 
                and re.raceId = ra.raceId
                and ra.year = %s
                and re.position is not Null
                """
        cursor.execute(query,(season,))

        for row in cursor:
            result.append(Driver(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(season):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = """
                select re1.driverId, re2.driverId, count(distinct re1.raceId)
                from results re1, results re2, races ra1, races ra2
                where ra1.raceId = re1.raceId
                and ra2.raceId = re2.raceId
                and re1.raceId = re2.raceId
                and re1.`position` < re2.`position`
                and ra2.`year` = ra1.`year`
                and ra1.year = %s
                group by re1.driverId, re2.driverId
                """
        cursor.execute(query, (season,))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result