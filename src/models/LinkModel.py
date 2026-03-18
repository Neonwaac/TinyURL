from src.database.mysql_connection import get_mysql_connection

class LinkModel:
    @staticmethod
    def create_link(codigo, url_original):
        connection = get_mysql_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO links (codigo, url_original) VALUES (%s, %s)"
                cursor.execute(sql, (codigo, url_original))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error creating link: {e}")
            return False
        finally:
            connection.close()

    @staticmethod
    def get_link_by_code(codigo):
        connection = get_mysql_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM links WHERE codigo = %s AND activo = TRUE"
                cursor.execute(sql, (codigo,))
                result = cursor.fetchone()
            return result
        except Exception as e:
            print(f"Error getting link: {e}")
            return None
        finally:
            connection.close()

    @staticmethod
    def get_link_by_url(url_original):
        connection = get_mysql_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM links WHERE url_original = %s LIMIT 1"
                cursor.execute(sql, (url_original,))
                result = cursor.fetchone()
            return result
        except Exception as e:
            print(f"Error getting link by URL: {e}")
            return None
        finally:
            connection.close()

    @staticmethod
    def increment_clicks(codigo):
        connection = get_mysql_connection()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE links SET clicks = clicks + 1 WHERE codigo = %s"
                cursor.execute(sql, (codigo,))
            connection.commit()
        except Exception as e:
            print(f"Error incrementing clicks: {e}")
        finally:
            connection.close()
            
    @staticmethod
    def get_all_links():
        connection = get_mysql_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM links ORDER BY fecha_creacion DESC"
                cursor.execute(sql)
                result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error getting all links: {e}")
            return []
        finally:
            connection.close()
