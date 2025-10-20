/* ========================================== */
/*         PULSE DASHBOARD JAVASCRIPT         */
/* ========================================== */

// Dados de exemplo para os gráficos
const dashboardData = {
    appointments: {
        daily: {
            labels: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
            data: [12, 15, 8, 18, 22, 10, 5]
        },
        weekly: {
            labels: ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4'],
            data: [85, 92, 78, 95]
        },
        monthly: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
            data: [320, 285, 410, 395, 450, 380, 420, 390, 445, 520, 480, 500]
        }
    },
    revenue: {
        daily: [1200, 1500, 800, 1800, 2200, 1000, 500],
        weekly: [8500, 9200, 7800, 9500],
        monthly: [32000, 28500, 41000, 39500, 45000, 38000, 42000, 39000, 44500, 52000, 48000, 50000]
    }
};

// Configuração global do Chart.js
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.font.size = 14;
Chart.defaults.color = '#6b7280';

let appointmentsChart = null;
let revenueChart = null;

// ========================================== 
//           MODO ESCURO
// ==========================================
function initDarkMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const body = document.body;
    
    // Verificar preferência salva
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        body.classList.add('dark-mode');
        updateToggleText();
    }
    
    darkModeToggle.addEventListener('click', function() {
        body.classList.toggle('dark-mode');
        const isDark = body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDark);
        updateToggleText();
        
        // Atualizar gráficos para o tema
        updateChartsTheme(isDark);
    });
}

function updateToggleText() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const isDark = document.body.classList.contains('dark-mode');
    darkModeToggle.innerHTML = isDark ? 
        '<i class="fas fa-sun"></i><span>Modo Claro</span>' : 
        '<i class="fas fa-moon"></i><span>Modo Escuro</span>';
}

function updateChartsTheme(isDark) {
    const textColor = isDark ? '#e0e6ed' : '#6b7280';
    const gridColor = isDark ? '#374151' : '#e5e7eb';
    
    if (appointmentsChart) {
        appointmentsChart.options.scales.y.ticks.color = textColor;
        appointmentsChart.options.scales.x.ticks.color = textColor;
        appointmentsChart.options.scales.y.grid.color = gridColor;
        appointmentsChart.options.scales.x.grid.color = gridColor;
        appointmentsChart.update();
    }
    
    if (revenueChart) {
        revenueChart.options.scales.y.ticks.color = textColor;
        revenueChart.update();
    }
}

// ========================================== 
//           GRÁFICOS DINÂMICOS
// ==========================================
function initCharts() {
    createAppointmentsChart('daily');
    createRevenueChart('daily');
}

function createAppointmentsChart(period) {
    const ctx = document.getElementById('appointmentsChart').getContext('2d');
    
    if (appointmentsChart) {
        appointmentsChart.destroy();
    }
    
    const data = dashboardData.appointments[period];
    const isDark = document.body.classList.contains('dark-mode');
    
    appointmentsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Consultas Realizadas',
                data: data.data,
                borderColor: '#8e44ad',
                backgroundColor: 'rgba(142, 68, 173, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#8e44ad',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 3,
                pointRadius: 6,
                pointHoverRadius: 9,
                pointHoverBackgroundColor: '#7c3aed',
                pointHoverBorderColor: '#ffffff',
                pointHoverBorderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    align: 'start',
                    labels: {
                        color: isDark ? '#e0e6ed' : '#6b7280',
                        usePointStyle: true,
                        padding: 20,
                        font: {
                            size: 14,
                            weight: '500'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: isDark ? '#1f2937' : '#ffffff',
                    titleColor: isDark ? '#f9fafb' : '#111827',
                    bodyColor: isDark ? '#d1d5db' : '#374151',
                    borderColor: isDark ? '#374151' : '#e5e7eb',
                    borderWidth: 1,
                    cornerRadius: 8,
                    padding: 12,
                    displayColors: true,
                    callbacks: {
                        title: function(context) {
                            const periodNames = {
                                'daily': 'Dia',
                                'weekly': 'Semana',
                                'monthly': 'Mês'
                            };
                            return `${periodNames[period]}: ${context[0].label}`;
                        },
                        label: function(context) {
                            return `${context.parsed.y} consultas realizadas`;
                        },
                        afterLabel: function(context) {
                            const avg = data.data.reduce((a, b) => a + b, 0) / data.data.length;
                            const diff = context.parsed.y - avg;
                            const percentage = ((diff / avg) * 100).toFixed(1);
                            return diff > 0 ? `+${percentage}% acima da média` : `${percentage}% abaixo da média`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Número de Consultas',
                        color: isDark ? '#e0e6ed' : '#6b7280',
                        font: {
                            size: 14,
                            weight: '600'
                        }
                    },
                    ticks: {
                        color: isDark ? '#e0e6ed' : '#6b7280',
                        font: {
                            size: 12
                        }
                    },
                    grid: {
                        color: isDark ? '#374151' : '#e5e7eb',
                        lineWidth: 1
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: period === 'daily' ? 'Dias da Semana' : period === 'weekly' ? 'Semanas do Mês' : 'Meses do Ano',
                        color: isDark ? '#e0e6ed' : '#6b7280',
                        font: {
                            size: 14,
                            weight: '600'
                        }
                    },
                    ticks: {
                        color: isDark ? '#e0e6ed' : '#6b7280',
                        font: {
                            size: 12
                        }
                    },
                    grid: {
                        color: isDark ? '#374151' : '#e5e7eb',
                        lineWidth: 1
                    }
                }
            },
            animation: {
                duration: 1200,
                easing: 'easeInOutQuart'
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

function createRevenueChart(period) {
    const ctx = document.getElementById('revenueChart').getContext('2d');
    
    if (revenueChart) {
        revenueChart.destroy();
    }
    
    const data = dashboardData.revenue[period];
    const labels = dashboardData.appointments[period].labels;
    const isDark = document.body.classList.contains('dark-mode');
    
    revenueChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                label: 'Receita (R$)',
                data: data,
                backgroundColor: [
                    '#8e44ad',
                    '#7d3c98',
                    '#bb8fce',
                    '#d2b4de',
                    '#e8daef',
                    '#10b981',
                    '#f59e0b'
                ],
                borderWidth: 3,
                borderColor: isDark ? '#1f2937' : '#ffffff',
                hoverOffset: 8,
                hoverBorderWidth: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    align: 'start',
                    labels: {
                        color: isDark ? '#e0e6ed' : '#6b7280',
                        padding: 15,
                        usePointStyle: true,
                        pointStyle: 'circle',
                        font: {
                            size: 12,
                            weight: '500'
                        },
                        generateLabels: function(chart) {
                            const data = chart.data;
                            if (data.labels.length && data.datasets.length) {
                                return data.labels.map((label, i) => {
                                    const value = data.datasets[0].data[i];
                                    const formattedValue = new Intl.NumberFormat('pt-BR', {
                                        style: 'currency',
                                        currency: 'BRL'
                                    }).format(value);
                                    
                                    return {
                                        text: `${label}: ${formattedValue}`,
                                        fillStyle: data.datasets[0].backgroundColor[i],
                                        strokeStyle: data.datasets[0].backgroundColor[i],
                                        lineWidth: 0,
                                        pointStyle: 'circle',
                                        hidden: false,
                                        index: i
                                    };
                                });
                            }
                            return [];
                        }
                    }
                },
                tooltip: {
                    backgroundColor: isDark ? '#1f2937' : '#ffffff',
                    titleColor: isDark ? '#f9fafb' : '#111827',
                    bodyColor: isDark ? '#d1d5db' : '#374151',
                    borderColor: isDark ? '#374151' : '#e5e7eb',
                    borderWidth: 1,
                    cornerRadius: 8,
                    padding: 12,
                    displayColors: true,
                    callbacks: {
                        title: function(context) {
                            const periodNames = {
                                'daily': 'Dia',
                                'weekly': 'Semana', 
                                'monthly': 'Mês'
                            };
                            return `${periodNames[period]}: ${context[0].label}`;
                        },
                        label: function(context) {
                            const value = new Intl.NumberFormat('pt-BR', {
                                style: 'currency',
                                currency: 'BRL'
                            }).format(context.parsed);
                            
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed / total) * 100).toFixed(1);
                            
                            return `Receita: ${value} (${percentage}%)`;
                        }
                    }
                }
            },
            animation: {
                animateRotate: true,
                animateScale: true,
                duration: 1500,
                easing: 'easeInOutQuart'
            },
            interaction: {
                intersect: false
            }
        }
    });
}

function changeChartPeriod(period, chartType) {
    // Atualizar botões ativos
    const buttons = document.querySelectorAll(`#${chartType}Filters .filter-btn`);
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Atualizar gráfico
    if (chartType === 'appointments') {
        createAppointmentsChart(period);
    } else if (chartType === 'revenue') {
        createRevenueChart(period);
    }
}

// ========================================== 
//           NOTIFICAÇÕES
// ==========================================
function initNotifications() {
    const notifications = [
        {
            type: 'birthday',
            icon: 'fas fa-birthday-cake',
            title: 'Aniversário Hoje!',
            message: 'Maria Silva faz aniversário hoje. Que tal enviar uma mensagem?',
            badge: 'Hoje'
        },
        {
            type: 'appointment',
            icon: 'fas fa-clock',
            title: 'Consulta em 30min',
            message: 'João Santos - Consulta de rotina às 14:30',
            badge: '30min'
        },
        {
            type: 'pending',
            icon: 'fas fa-exclamation-triangle',
            title: 'Pagamento Pendente',
            message: '3 consultas com pagamento em atraso',
            badge: '3'
        },
        {
            type: 'appointment',
            icon: 'fas fa-user-plus',
            title: 'Novo Paciente',
            message: 'Ana Costa agendou primeira consulta para amanhã',
            badge: 'Novo'
        }
    ];
    
    const container = document.getElementById('notificationsContainer');
    container.innerHTML = '';
    
    notifications.forEach((notification, index) => {
        const item = document.createElement('div');
        item.className = `notification-item notification-${notification.type}`;
        item.style.animationDelay = `${index * 0.1}s`;
        item.classList.add('fade-in-left');
        
        item.innerHTML = `
            <div class="notification-icon">
                <i class="${notification.icon}"></i>
            </div>
            <div class="notification-content">
                <h4>${notification.title}</h4>
                <p>${notification.message}</p>
            </div>
            <span class="notification-badge">${notification.badge}</span>
        `;
        
        container.appendChild(item);
    });
}

// ========================================== 
//           ESTATÍSTICAS ANIMADAS
// ==========================================
function animateStats() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(stat => {
        const target = parseInt(stat.getAttribute('data-target'));
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;
        
        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            stat.textContent = Math.floor(current);
        }, 16);
    });
}

// ========================================== 
//           ATUALIZAÇÃO EM TEMPO REAL
// ==========================================
function updateRealTimeData() {
    // Simular dados atualizados
    const updates = {
        pacientesHoje: Math.floor(Math.random() * 20) + 15,
        receitaDia: Math.floor(Math.random() * 3000) + 2000,
        consultasMes: Math.floor(Math.random() * 100) + 450,
        satisfacao: Math.floor(Math.random() * 10) + 90
    };
    
    // Atualizar elementos na página
    Object.keys(updates).forEach(key => {
        const element = document.getElementById(key);
        if (element) {
            const currentValue = parseInt(element.textContent);
            const newValue = updates[key];
            
            if (currentValue !== newValue) {
                element.style.transform = 'scale(1.1)';
                element.style.color = '#8e44ad';
                
                setTimeout(() => {
                    element.textContent = newValue;
                    element.style.transform = 'scale(1)';
                    element.style.color = '';
                }, 300);
            }
        }
    });
}

// ========================================== 
//           FRASES MOTIVACIONAIS
// ==========================================
const motivationalQuotes = [
    "Cuidar é a essência da medicina. Curar, às vezes; aliviar, frequentemente; consoldar, sempre.",
    "A medicina é uma ciência de incertezas e uma arte de probabilidades.",
    "O melhor médico é aquele que conhece a inutilidade da maioria dos medicamentos.",
    "Onde quer que a arte da medicina seja amada, há também um amor pela humanidade.",
    "A prevenção é melhor que a cura. Um grama de prevenção vale mais que um quilo de cura."
];

function updateMotivationalQuote() {
    const quoteElement = document.getElementById('motivationalQuote');
    if (quoteElement) {
        const randomQuote = motivationalQuotes[Math.floor(Math.random() * motivationalQuotes.length)];
        quoteElement.style.opacity = '0';
        
        setTimeout(() => {
            quoteElement.textContent = randomQuote;
            quoteElement.style.opacity = '1';
        }, 300);
    }
}

// ========================================== 
//           INICIALIZAÇÃO
// ==========================================
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar componentes
    initDarkMode();
    initCharts();
    initNotifications();
    animateStats();
    
    // Atualizar frase motivacional a cada 30 segundos
    setInterval(updateMotivationalQuote, 30000);
    
    // Atualizar dados em tempo real a cada 10 segundos
    setInterval(updateRealTimeData, 10000);
    
    // Adicionar animações de entrada
    const elements = document.querySelectorAll('.stat-card-advanced, .chart-card, .notifications-panel');
    elements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.1}s`;
        el.classList.add('fade-in-up');
    });
    
    console.log('🩺 Dashboard Dr. Pulse inicializado com sucesso!');
});

// ========================================== 
//           FUNÇÕES AUXILIARES
// ==========================================
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    }).format(date);
}

// Exportar funções para uso global
window.changeChartPeriod = changeChartPeriod;
window.updateMotivationalQuote = updateMotivationalQuote;