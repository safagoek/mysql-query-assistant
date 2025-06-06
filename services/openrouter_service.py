from openai import OpenAI
from config import Config
import os

class OpenRouterService:
    def __init__(self):
        # API key kontrolü
        api_key = Config.OPENROUTER_API_KEY
        if not api_key or api_key == "your_openrouter_api_key_here":
            raise ValueError("OpenRouter API key bulunamadı! Lütfen .env dosyasında OPENROUTER_API_KEY değerini ayarlayın.")
        
        try:
            self.client = OpenAI(
                base_url=Config.OPENROUTER_BASE_URL,
                api_key=api_key,
            )
        except Exception as e:
            print(f"OpenAI client oluşturma hatası: {e}")
            raise
    
    def generate_sql_query(self, user_prompt, schema_info):
        """Kullanıcı isteğine göre SQL sorgusu oluştur"""
        
        # Şema bilgilerini metin haline getir
        schema_text = self._format_schema_for_prompt(schema_info)
        
        system_prompt = f"""
Sen bir MySQL uzmanısın. Aşağıdaki veritabanı şeması bilgilerine göre kullanıcının isteğini karşılayan SQL sorgusu yazman gerekiyor.

VERİTABANI ŞEMASI:
{schema_text}

KURALLAR:
1. Sadece SELECT sorguları yaz (güvenlik için)
2. Sorgu syntax'ı MySQL'e uygun olmalı
3. Tablo ve sütun isimlerini şemada verilen isimlerle tam olarak eşleştir
4. Mümkün olduğunca optimize edilmiş sorgu yaz
5. LIMIT kullanarak sonuç sayısını makul tut (örnek: LIMIT 50)
6. Sadece SQL kodunu döndür, açıklama yapma
7. SQL kodunu ``` işaretleri olmadan döndür
        """
        
        try:
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "http://localhost:5000",
                    "X-Title": "MySQL Query Assistant",
                },
                model=Config.OPENROUTER_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            sql_query = completion.choices[0].message.content.strip()
            
            # SQL kodunu temizle (markdown işaretlerini kaldır)
            sql_query = self._clean_sql_response(sql_query)
            
            return True, sql_query
            
        except Exception as e:
            return False, f"AI sorgu oluşturma hatası: {str(e)}"
    
    def _clean_sql_response(self, sql_response):
        """AI yanıtından SQL kodunu temizle"""
        # Markdown code block işaretlerini kaldır
        if sql_response.startswith('```'):
            lines = sql_response.split('\n')
            sql_response = '\n'.join(lines[1:-1])
        
        # sql veya SQL keyword'ünü kaldır
        if sql_response.lower().startswith('sql\n'):
            sql_response = sql_response[4:]
        
        return sql_response.strip()
    
    def _format_schema_for_prompt(self, schema_info):
        """Şema bilgilerini AI için uygun formata çevir"""
        schema_text = f"Veritabanı: {schema_info['database']}\n\n"
        
        for table_name, table_info in schema_info['tables'].items():
            schema_text += f"Tablo: {table_name}\n"
            schema_text += "Sütunlar:\n"
            
            for column in table_info['columns']:
                pk_indicator = " (PRIMARY KEY)" if column['name'] in table_info['primary_keys'] else ""
                null_indicator = " (NULL)" if column['null'] == 'YES' else " (NOT NULL)"
                schema_text += f"  - {column['name']}: {column['type']}{pk_indicator}{null_indicator}\n"
            
            schema_text += "\n"
        
        return schema_text