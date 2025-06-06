from database.connection import DatabaseManager

class SchemaAnalyzer:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def get_schema_info(self, database_name):
        """Veritabanı şemasını analiz et"""
        schema_info = {
            'database': database_name,
            'tables': {}
        }
        
        try:
            # Tabloları al
            success, tables = self._get_tables()
            if not success:
                return False, tables
            
            # Her tablo için detayları al
            for table in tables:
                table_info = self._get_table_info(table)
                schema_info['tables'][table] = table_info
            
            return True, schema_info
            
        except Exception as e:
            return False, f"Şema analizi hatası: {str(e)}"
    
    def _get_tables(self):
        """Tabloları listele"""
        try:
            cursor = self.db_manager.connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            return True, tables
        except Exception as e:
            return False, str(e)
        finally:
            if cursor:
                cursor.close()
    
    def _get_table_info(self, table_name):
        """Tablo detaylarını al"""
        table_info = {
            'columns': [],
            'primary_keys': [],
            'foreign_keys': []
        }
        
        try:
            cursor = self.db_manager.connection.cursor(dictionary=True)
            
            # Sütun bilgilerini al
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            
            for column in columns:
                column_info = {
                    'name': column['Field'],
                    'type': column['Type'],
                    'null': column['Null'],
                    'key': column['Key'],
                    'default': column['Default'],
                    'extra': column['Extra']
                }
                table_info['columns'].append(column_info)
                
                if column['Key'] == 'PRI':
                    table_info['primary_keys'].append(column['Field'])
            
            return table_info
            
        except Exception as e:
            return {'error': str(e)}
        finally:
            if cursor:
                cursor.close()