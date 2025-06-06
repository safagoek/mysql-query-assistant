let currentQuery = '';

// Sayfa yüklendiğinde veritabanlarını yükle
document.addEventListener('DOMContentLoaded', function() {
    loadDatabases();
});

// Veritabanlarını yükle
function loadDatabases() {
    fetch('/get-databases')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('databaseSelect');
            select.innerHTML = '<option value="">Veritabanı seçin...</option>';
            
            if (data.success) {
                data.databases.forEach(db => {
                    const option = document.createElement('option');
                    option.value = db;
                    option.textContent = db;
                    select.appendChild(option);
                });
            } else {
                showAlert('danger', 'Veritabanları yüklenemedi: ' + data.message);
            }
        })
        .catch(error => {
            showAlert('danger', 'Bağlantı hatası: ' + error.message);
        });
}

// Veritabanına bağlan
function connectDatabase() {
    const databaseName = document.getElementById('databaseSelect').value;
    
    if (!databaseName) {
        showAlert('warning', 'Lütfen bir veritabanı seçin');
        return;
    }

    fetch('/connect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            database_name: databaseName
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('success', 'Veritabanına başarıyla bağlanıldı');
            displaySchema(data.schema);
            document.getElementById('generateBtn').disabled = false;
        } else {
            showAlert('danger', data.message);
        }
    })
    .catch(error => {
        showAlert('danger', 'Bağlantı hatası: ' + error.message);
    });
}

// Şema bilgilerini göster
function displaySchema(schema) {
    const schemaCard = document.getElementById('schemaCard');
    const schemaInfo = document.getElementById('schemaInfo');
    
    let html = `<h6>Veritabanı: ${schema.database}</h6>`;
    html += '<div class="accordion" id="tablesAccordion">';
    
    let index = 0;
    for (const [tableName, tableInfo] of Object.entries(schema.tables)) {
        html += `
            <div class="accordion-item">
                <h2 class="accordion-header" id="heading${index}">
                    <button class="accordion-button collapsed" type="button" 
                            data-bs-toggle="collapse" data-bs-target="#collapse${index}">
                        ${tableName}
                    </button>
                </h2>
                <div id="collapse${index}" class="accordion-collapse collapse" 
                     data-bs-parent="#tablesAccordion">
                    <div class="accordion-body">
                        <small>
        `;
        
        tableInfo.columns.forEach(column => {
            const isPK = tableInfo.primary_keys.includes(column.name);
            html += `<div class="d-flex justify-content-between">
                <span${isPK ? ' class="fw-bold text-primary"' : ''}>${column.name}</span>
                <span class="text-muted">${column.type}</span>
            </div>`;
        });
        
        html += '</small></div></div></div>';
        index++;
    }
    
    html += '</div>';
    schemaInfo.innerHTML = html;
    schemaCard.style.display = 'block';
}

// AI ile sorgu oluştur
function generateQuery() {
    const prompt = document.getElementById('promptInput').value.trim();
    
    if (!prompt) {
        showAlert('warning', 'Lütfen ne yapmak istediğinizi yazın');
        return;
    }

    // Loading göster
    const generateBtn = document.getElementById('generateBtn');
    const originalText = generateBtn.innerHTML;
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Oluşturuluyor...';
    generateBtn.disabled = true;

    fetch('/generate-query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            prompt: prompt
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentQuery = data.raw_query;
            document.getElementById('generatedQuery').textContent = data.query;
            
            // Syntax highlighting
            Prism.highlightElement(document.getElementById('generatedQuery'));
            
            document.getElementById('queryCard').style.display = 'block';
            showAlert('success', 'Sorgu başarıyla oluşturuldu');
        } else {
            showAlert('danger', 'Sorgu oluşturulamadı: ' + data.message);
        }
    })
    .catch(error => {
        showAlert('danger', 'Hata: ' + error.message);
    })
    .finally(() => {
        generateBtn.innerHTML = originalText;
        generateBtn.disabled = false;
    });
}

// Sorguyu çalıştır
function executeQuery() {
    if (!currentQuery) {
        showAlert('warning', 'Çalıştırılacak sorgu bulunamadı');
        return;
    }

    fetch('/execute-query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            query: currentQuery
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayResults(data.results, data.row_count, data.column_count);
            showAlert('success', `Sorgu başarıyla çalıştırıldı. ${data.row_count} satır döndü.`);
        } else {
            showAlert('danger', 'Sorgu hatası: ' + data.message);
        }
    })
    .catch(error => {
        showAlert('danger', 'Hata: ' + error.message);
    });
}

// Sonuçları göster
function displayResults(results, rowCount, columnCount) {
    const resultsDiv = document.getElementById('queryResults');
    
    if (!results || results.length === 0) {
        resultsDiv.innerHTML = '<p class="text-muted">Sonuç bulunamadı</p>';
    } else {
        // Tablo oluştur
        let html = '<div class="table-responsive"><table class="table table-striped table-sm">';
        
        // Başlık satırı
        html += '<thead class="table-dark"><tr>';
        const columns = Object.keys(results[0]);
        columns.forEach(column => {
            html += `<th>${column}</th>`;
        });
        html += '</tr></thead>';
        
        // Veri satırları
        html += '<tbody>';
        results.forEach(row => {
            html += '<tr>';
            columns.forEach(column => {
                const value = row[column];
                html += `<td>${value !== null ? value : '<span class="text-muted">NULL</span>'}</td>`;
            });
            html += '</tr>';
        });
        html += '</tbody></table></div>';
        
        resultsDiv.innerHTML = html;
    }
    
    document.getElementById('resultsCard').style.display = 'block';
}

// Sorguyu kopyala
function copyQuery() {
    const queryText = document.getElementById('generatedQuery').textContent;
    
    navigator.clipboard.writeText(queryText).then(() => {
        showAlert('info', 'Sorgu kopyalandı');
    }).catch(err => {
        console.error('Kopyalama hatası: ', err);
    });
}

// Alert göster
function showAlert(type, message) {
    const statusDiv = document.getElementById('connectionStatus');
    statusDiv.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
}