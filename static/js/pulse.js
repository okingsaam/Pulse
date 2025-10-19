// ===========================================
// PULSE - JAVASCRIPT PERSONALIZADO
// ===========================================
// Funcionalidades de interatividade
// ===========================================

// Sistema de notificações toast
function showToast(message, type = 'info', duration = 5000) {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast fade show`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="toast-header bg-${type} text-white">
            <i class="bi bi-${getIconForType(type)} me-2"></i>
            <strong class="me-auto">Pulse</strong>
            <button type="button" class="btn-close btn-close-white" onclick="closeToast(this)"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto remove após duration
    setTimeout(() => {
        if (toast.parentNode) {
            toast.remove();
        }
    }, duration);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

function getIconForType(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-triangle',
        'warning': 'exclamation-circle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function closeToast(button) {
    const toast = button.closest('.toast');
    toast.remove();
}

// Confirmação de ações
function confirmAction(message, callback) {
    const result = confirm(message);
    if (result && callback) {
        callback();
    }
    return result;
}

// Inicialização quando DOM carrega
document.addEventListener('DOMContentLoaded', function() {
    // Adicionar animações fade-in
    const elements = document.querySelectorAll('.card, .table, .btn-group');
    elements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.1}s`;
        el.classList.add('fade-in');
    });
    
    // Adicionar confirmação para ações perigosas
    const dangerButtons = document.querySelectorAll('.btn-danger, .btn-outline-danger');
    dangerButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!this.hasAttribute('data-confirmed')) {
                e.preventDefault();
                const action = this.textContent.toLowerCase();
                if (confirmAction(`Tem certeza que deseja ${action}?`)) {
                    this.setAttribute('data-confirmed', 'true');
                    this.click();
                }
            }
        });
    });
});
document.addEventListener('DOMContentLoaded', function() {
    
    // Confirmar ações de delete
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja excluir este item?')) {
                e.preventDefault();
            }
        });
    });
    
    // Auto-hide alerts após 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
    
    // Máscaras para telefone
    const phoneInputs = document.querySelectorAll('input[type="tel"], .phone-mask');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length >= 11) {
                value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
            } else if (value.length >= 7) {
                value = value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
            } else if (value.length >= 3) {
                value = value.replace(/(\d{2})(\d{0,5})/, '($1) $2');
            }
            e.target.value = value;
        });
    });
    
    // Validação de formulários
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Tooltips do Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Atualizar hora atual em tempo real
    function updateCurrentTime() {
        const now = new Date();
        const timeString = now.toLocaleString('pt-BR');
        const timeElements = document.querySelectorAll('.current-time');
        timeElements.forEach(el => el.textContent = timeString);
    }
    
    // Atualizar a cada minuto
    updateCurrentTime();
    setInterval(updateCurrentTime, 60000);
    
});