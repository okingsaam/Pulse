"""
Comando para aplicar tema final perfeito na interface admin
"""
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Aplica o tema final perfeito para a interface administrativa'

    def handle(self, *args, **options):
        try:
            from admin_interface.models import Theme
            
            self.stdout.write('🎨 Aplicando tema final perfeito...')
            
            # Deletar temas existentes
            Theme.objects.all().delete()
            
            # Criar o tema perfeito
            theme = Theme.objects.create(
                name='Pulse - Interface Perfeita',
                active=True,
                
                # Título personalizado
                title='🏥 Sistema Pulse - Gestão Médica',
                title_visible=True,
                title_color='#FFFFFF',
                
                # Cores do cabeçalho - Azul médico profissional
                css_header_background_color='#1565C0',  # Azul médico
                css_header_text_color='#FFFFFF',
                css_header_link_color='#E3F2FD',
                css_header_link_hover_color='#FFFFFF',
                
                # Cores dos módulos - Limpo e profissional
                css_module_background_color='#FFFFFF',
                css_module_text_color='#263238',
                css_module_link_color='#1565C0',
                css_module_link_hover_color='#0D47A1',
                css_module_rounded_corners=True,
                
                # Links genéricos
                css_generic_link_color='#1565C0',
                css_generic_link_hover_color='#0D47A1',
                css_generic_link_active_color='#1976D2',
                
                # Botões de salvar - Verde médico
                css_save_button_background_color='#2E7D32',
                css_save_button_background_hover_color='#1B5E20',
                css_save_button_text_color='#FFFFFF',
                
                # Botões de deletar - Vermelho médico
                css_delete_button_background_color='#C62828',
                css_delete_button_background_hover_color='#B71C1C',
                css_delete_button_text_color='#FFFFFF',
                
                # Modal relacionado
                related_modal_active=True,
                related_modal_background_color='#000000',
                related_modal_background_opacity=60,
                related_modal_rounded_corners=True,
                related_modal_close_button_visible=True,
                
                # Filtros otimizados
                list_filter_dropdown=True,
                list_filter_sticky=True,
                list_filter_highlight=True,
                list_filter_removal_links=True,
                
                # Formulários otimizados
                form_pagination_sticky=True,
                form_submit_sticky=True,
                show_fieldsets_as_tabs=True,
                show_inlines_as_tabs=True,
                
                # Layout otimizado
                recent_actions_visible=True,
                foldable_apps=True,
                
                # Inlines colapsáveis
                collapsible_stacked_inlines=True,
                collapsible_stacked_inlines_collapsed=False,
                collapsible_tabular_inlines=True,
                collapsible_tabular_inlines_collapsed=False,
                
                # Logo
                logo_visible=True,
                logo_color='#FFFFFF',
                logo_max_height=40,
                logo_max_width=150,
                
                # Idioma
                language_chooser_active=False,
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Tema perfeito "{theme.name}" aplicado!')
            )
            
            # Agora vamos criar CSS adicional mais refinado
            self.create_enhanced_css()
            
            self.stdout.write('🎨 Interface administrativa PERFEITA configurada!')
            self.stdout.write('🔄 Recarregue o admin para ver as mudanças incríveis!')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro: {e}')
            )
    
    def create_enhanced_css(self):
        """Cria CSS adicional aprimorado"""
        css_content = """
/* CSS Final Perfeito para Admin Pulse */

/* Reset e base */
* {
    box-sizing: border-box !important;
}

/* Header aprimorado */
#header {
    background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%) !important;
    box-shadow: 0 4px 20px rgba(21, 101, 192, 0.3) !important;
    border-bottom: none !important;
}

/* Branding melhorado */
#branding h1 {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    font-weight: 700 !important;
    font-size: 26px !important;
    letter-spacing: -0.5px !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
}

/* User tools elegante */
#user-tools {
    font-size: 14px !important;
    font-weight: 500 !important;
}

#user-tools a {
    padding: 8px 12px !important;
    border-radius: 6px !important;
    transition: all 0.3s ease !important;
    margin: 0 5px !important;
}

#user-tools a:hover {
    background-color: rgba(255,255,255,0.1) !important;
}

/* Breadcrumbs médicos */
.breadcrumbs {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
    border: 1px solid #dee2e6 !important;
    border-radius: 8px !important;
    padding: 12px 20px !important;
    margin: 20px 0 !important;
    font-weight: 500 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
}

.breadcrumbs a {
    color: #1565C0 !important;
    text-decoration: none !important;
    font-weight: 600 !important;
}

.breadcrumbs a:hover {
    color: #0D47A1 !important;
    text-decoration: underline !important;
}

/* Módulos com estilo médico profissional */
.module {
    background: white !important;
    border: 1px solid #e3f2fd !important;
    border-radius: 12px !important;
    box-shadow: 0 6px 20px rgba(21, 101, 192, 0.08) !important;
    margin-bottom: 25px !important;
    overflow: hidden !important;
    transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
}

.module:hover {
    box-shadow: 0 12px 40px rgba(21, 101, 192, 0.15) !important;
    transform: translateY(-4px) !important;
}

.module h2 {
    background: linear-gradient(135deg, #1565C0 0%, #1976D2 100%) !important;
    color: white !important;
    padding: 18px 25px !important;
    margin: 0 !important;
    font-weight: 600 !important;
    font-size: 17px !important;
    letter-spacing: -0.3px !important;
    border-bottom: none !important;
    text-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
}

.module h2 a {
    color: white !important;
    text-decoration: none !important;
}

/* Links de ação médicos */
.addlink, .changelink, .viewlink {
    background: linear-gradient(135deg, #2E7D32 0%, #388E3C 100%) !important;
    color: white !important;
    padding: 10px 18px !important;
    border-radius: 8px !important;
    text-decoration: none !important;
    display: inline-block !important;
    margin: 8px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    border: none !important;
    box-shadow: 0 3px 10px rgba(46, 125, 50, 0.3) !important;
}

.addlink:hover, .changelink:hover, .viewlink:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(46, 125, 50, 0.4) !important;
    color: white !important;
}

/* Tabelas médicas elegantes */
.results {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1) !important;
    border: none !important;
    margin: 20px 0 !important;
}

.results th {
    background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%) !important;
    color: white !important;
    padding: 18px 15px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    text-align: center !important;
    letter-spacing: 0.3px !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
}

.results td {
    padding: 15px 12px !important;
    border-bottom: 1px solid #f5f5f5 !important;
    text-align: center !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}

.results tr:nth-child(even) {
    background-color: #fafafa !important;
}

.results tr:hover {
    background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%) !important;
    transition: all 0.3s ease !important;
}

/* Botões médicos profissionais */
.default, input[type="submit"], button {
    background: linear-gradient(135deg, #1565C0 0%, #1976D2 100%) !important;
    color: white !important;
    border: none !important;
    padding: 12px 24px !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    cursor: pointer !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    box-shadow: 0 4px 12px rgba(21, 101, 192, 0.3) !important;
}

.default:hover, input[type="submit"]:hover, button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(21, 101, 192, 0.4) !important;
    background: linear-gradient(135deg, #0D47A1 0%, #1565C0 100%) !important;
}

/* Mensagens médicas */
.messagelist {
    border-radius: 8px !important;
    overflow: hidden !important;
    margin-bottom: 25px !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
}

.messagelist .success {
    background: linear-gradient(135deg, #2E7D32 0%, #388E3C 100%) !important;
    color: white !important;
    padding: 18px 25px !important;
    border: none !important;
    font-weight: 600 !important;
}

.messagelist .error {
    background: linear-gradient(135deg, #C62828 0%, #D32F2F 100%) !important;
    color: white !important;
    padding: 18px 25px !important;
    border: none !important;
    font-weight: 600 !important;
}

/* Campos de formulário médicos */
input[type="text"], input[type="email"], input[type="password"], 
input[type="number"], input[type="url"], textarea, select {
    border: 2px solid #e1f5fe !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    transition: all 0.3s ease !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    background-color: #fafafa !important;
}

input[type="text"]:focus, input[type="email"]:focus, input[type="password"]:focus,
input[type="number"]:focus, input[type="url"]:focus, textarea:focus, select:focus {
    border-color: #1565C0 !important;
    outline: none !important;
    box-shadow: 0 0 0 4px rgba(21, 101, 192, 0.1) !important;
    background-color: white !important;
}

/* Sidebar médica */
#nav-sidebar {
    background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%) !important;
    border-right: 2px solid #e3f2fd !important;
    box-shadow: 2px 0 10px rgba(0,0,0,0.1) !important;
}

#nav-sidebar .current-app {
    background: linear-gradient(135deg, #1565C0 0%, #1976D2 100%) !important;
    border-radius: 8px !important;
    margin: 8px !important;
    box-shadow: 0 3px 10px rgba(21, 101, 192, 0.3) !important;
}

/* Content area médica */
#content {
    background-color: #f8f9fa !important;
    min-height: calc(100vh - 120px) !important;
    padding: 25px !important;
}

#content-main {
    background: white !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.1) !important;
    padding: 30px !important;
    margin-bottom: 25px !important;
    border: 1px solid #e3f2fd !important;
}

/* Títulos médicos */
h1, h2, h3 {
    color: #1565C0 !important;
    font-weight: 700 !important;
    font-family: 'Segoe UI', sans-serif !important;
}

/* Paginação médica */
.paginator {
    text-align: center !important;
    margin: 25px 0 !important;
}

.paginator a, .paginator .this-page {
    display: inline-block !important;
    padding: 10px 15px !important;
    margin: 0 5px !important;
    border-radius: 8px !important;
    border: 2px solid #e3f2fd !important;
    color: #1565C0 !important;
    text-decoration: none !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.paginator a:hover {
    background: linear-gradient(135deg, #1565C0 0%, #1976D2 100%) !important;
    color: white !important;
    border-color: #1565C0 !important;
    transform: translateY(-1px) !important;
}

.paginator .this-page {
    background: linear-gradient(135deg, #1565C0 0%, #1976D2 100%) !important;
    color: white !important;
    border-color: #1565C0 !important;
}

/* Indicadores médicos */
.yes, .true {
    color: #2E7D32 !important;
    font-weight: 700 !important;
}

.no, .false {
    color: #C62828 !important;
    font-weight: 700 !important;
}

/* Fieldsets médicos */
fieldset {
    border: 2px solid #e3f2fd !important;
    border-radius: 12px !important;
    padding: 25px !important;
    margin-bottom: 25px !important;
    background: #fafafa !important;
}

fieldset legend {
    background: white !important;
    padding: 8px 18px !important;
    border: 2px solid #1565C0 !important;
    border-radius: 8px !important;
    color: #1565C0 !important;
    font-weight: 700 !important;
    font-size: 16px !important;
}

/* Animações suaves */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.module, .results, #content-main {
    animation: fadeInUp 0.6s ease-out !important;
}

/* Responsividade médica */
@media (max-width: 768px) {
    .module {
        margin: 10px !important;
    }
    
    #content {
        padding: 15px !important;
    }
    
    #content-main {
        padding: 20px !important;
    }
    
    .results th, .results td {
        padding: 10px 8px !important;
        font-size: 12px !important;
    }
}
"""
        
        try:
            import os
            css_path = os.path.join('static', 'admin', 'css', 'pulse_perfect.css')
            os.makedirs(os.path.dirname(css_path), exist_ok=True)
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(css_content)
            self.stdout.write('📄 CSS perfeito criado!')
        except Exception as e:
            self.stdout.write(f'⚠️ Aviso CSS: {e}')