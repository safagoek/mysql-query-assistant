from flask import Flask, render_template, request, jsonify, session
from config import Config
from database.connection import DatabaseManager
from database.schema_analyzer import SchemaAnalyzer
import sqlparse
import traceback

app = Flask(__name__)
app.config.from_object(Config)

# Servisler - lazy loading ile
db_manager = DatabaseManager()
openrouter_service = None

def get_openrouter_service():
    """OpenRouter servisini lazy loading ile başlat"""
    global openrouter_service
    if openrouter_service is None:
        try:
            from services.openrouter_service import OpenRouterService
            openrouter_service = OpenRouterService()
        except Exception as e:
            print(f"OpenRouter servisi başlatılamadı: {e}")
            raise
    return openrouter_service

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/connect', methods=['POST'])
def connect_database():
    """Veritabanına bağlan"""
    try:
        data = request.json
        database_name = data.get('database_name')
        
        success, message = db_manager.connect(database_name)
        
        if success:
            # Şema bilgilerini al
            schema_analyzer = SchemaAnalyzer(db_manager)
            schema_success, schema_info = schema_analyzer.get_schema_info(database_name)
            
            if schema_success:
                session['schema_info'] = schema_info
                session['connected_database'] = database_name
                return jsonify({
                    'success': True,
                    'message': message,
                    'schema': schema_info
                })
            else:
                return jsonify({
                    'success': False,
                    'message': f"Bağlantı başarılı ancak şema okunamadı: {schema_info}"
                })
        else:
            return jsonify({
                'success': False,
                'message': message
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f"Bağlantı hatası: {str(e)}"
        })

@app.route('/generate-query', methods=['POST'])
def generate_query():
    """AI ile sorgu oluştur"""
    try:
        data = request.json
        user_prompt = data.get('prompt')
        
        if 'schema_info' not in session:
            return jsonify({
                'success': False,
                'message': 'Önce bir veritabanına bağlanın'
            })
        
        schema_info = session['schema_info']
        
        # OpenRouter servisini al
        try:
            service = get_openrouter_service()
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f"AI servisi başlatılamadı: {str(e)}"
            })
        
        # AI ile sorgu oluştur
        success, query = service.generate_sql_query(user_prompt, schema_info)
        
        if success:
            # SQL'i formatla
            try:
                formatted_query = sqlparse.format(query, reindent=True, keyword_case='upper')
            except:
                formatted_query = query
            
            return jsonify({
                'success': True,
                'query': formatted_query,
                'raw_query': query
            })
        else:
            return jsonify({
                'success': False,
                'message': query
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f"Sorgu oluşturma hatası: {str(e)}"
        })

@app.route('/execute-query', methods=['POST'])
def execute_query():
    """Sorguyu çalıştır"""
    try:
        data = request.json
        query = data.get('query')
        
        if not query:
            return jsonify({
                'success': False,
                'message': 'Sorgu bulunamadı'
            })
        
        # Güvenlik kontrolü - sadece SELECT sorgularına izin ver
        if not query.strip().upper().startswith('SELECT'):
            return jsonify({
                'success': False,
                'message': 'Güvenlik nedeniyle sadece SELECT sorguları çalıştırılabilir'
            })
        
        success, results, description = db_manager.execute_query(query)
        
        if success:
            return jsonify({
                'success': True,
                'results': results,
                'column_count': len(description) if description else 0,
                'row_count': len(results) if isinstance(results, list) else 0
            })
        else:
            return jsonify({
                'success': False,
                'message': results
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f"Sorgu çalıştırma hatası: {str(e)}"
        })

@app.route('/get-databases')
def get_databases():
    """Mevcut veritabanlarını listele"""
    try:
        # Önce bağlantı kur (database belirtmeden)
        success, message = db_manager.connect()
        
        if success:
            db_success, databases = db_manager.get_databases()
            if db_success:
                return jsonify({
                    'success': True,
                    'databases': databases
                })
            else:
                return jsonify({
                    'success': False,
                    'message': databases
                })
        else:
            return jsonify({
                'success': False,
                'message': message
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f"Veritabanları listelenemedi: {str(e)}"
        })

@app.route('/test-openrouter')
def test_openrouter():
    """OpenRouter bağlantısını test et"""
    try:
        service = get_openrouter_service()
        return jsonify({
            'success': True,
            'message': 'OpenRouter servisi başarıyla başlatıldı'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'OpenRouter servisi hatası: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)