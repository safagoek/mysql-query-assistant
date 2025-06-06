import mysql.connector
from mysql.connector import Error
from config import Config

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.config = {
            'host': Config.MYSQL_HOST,
            'port': Config.MYSQL_PORT,
            'user': Config.MYSQL_USER,
            'password': Config.MYSQL_PASSWORD,
            'database': Config.MYSQL_DATABASE
        }
    
    def connect(self, database_name=None):
        """Veritabanına bağlan"""
        try:
            config = self.config.copy()
            if database_name:
                config['database'] = database_name
            
            self.connection = mysql.connector.connect(**config)
            if self.connection.is_connected():
                return True, "Bağlantı başarılı"
        except Error as e:
            return False, f"Bağlantı hatası: {str(e)}"
        return False, "Bilinmeyen hata"
    
    def execute_query(self, query):
        """Sorgu çalıştır"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                return True, results, cursor.description
            else:
                self.connection.commit()
                return True, f"Sorgu başarıyla çalıştırıldı. Etkilenen satır: {cursor.rowcount}", None
                
        except Error as e:
            return False, f"Sorgu hatası: {str(e)}", None
        finally:
            if cursor:
                cursor.close()
    
    def get_databases(self):
        """Mevcut veritabanlarını listele"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            return True, databases
        except Error as e:
            return False, f"Veritabanları listelenemedi: {str(e)}"
        finally:
            if cursor:
                cursor.close()
    
    def close(self):
        """Bağlantıyı kapat"""
        if self.connection and self.connection.is_connected():
            self.connection.close()