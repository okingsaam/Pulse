"""
Comando para configurar tema bonito da interface admin
"""
from django.core.management.base import BaseCommand
from admin_interface.models import Theme

class Command(BaseCommand):
    help = 'Configura tema bonito para a interface administrativa'

    def handle(self, *args, **options):
        self.stdout.write('🎨 Configurando tema moderno para o admin...')
        
        # Deletar temas existentes
        Theme.objects.all().delete()
        
        # Criar tema moderno e profissional
        theme = Theme.objects.create(
            name='Pulse - Tema Moderno',
            active=True,
            
            # Cores principais
            primary_color='#2196F3',      # Azul moderno
            secondary_color='#FFC107',    # Amarelo/dourado
            accent_color='#4CAF50',       # Verde para sucesso
            
            # Título e logo
            title='Sistema Pulse - Agendamentos',
            title_color='#FFFFFF',
            title_visible=True,
            
            # Favicon e logo
            favicon='/static/img/favicon.ico',
            logo_visible=True,
            logo_color='#FFFFFF',
            logo_max_height=50,
            logo_max_width=200,
            
            # Tema geral
            css_header_background_color='#1976D2',    # Azul mais escuro para header
            css_header_text_color='#FFFFFF',
            css_header_link_color='#E3F2FD',
            css_header_link_hover_color='#FFFFFF',
            
            # Módulos/aplicações
            css_module_background_color='#FFFFFF',
            css_module_text_color='#333333',
            css_module_link_color='#1976D2',
            css_module_link_hover_color='#0D47A1',
            css_module_rounded_corners=True,
            
            # Sidebar
            css_generic_link_color='#1976D2',
            css_generic_link_hover_color='#0D47A1',
            css_generic_link_active_color='#2196F3',
            
            # Botões de save
            css_save_button_background_color='#4CAF50',
            css_save_button_background_hover_color='#45A049',
            css_save_button_text_color='#FFFFFF',
            
            # Botões de delete
            css_delete_button_background_color='#F44336',
            css_delete_button_background_hover_color='#D32F2F',
            css_delete_button_text_color='#FFFFFF',
            
            # Configurações de layout
            related_modal_active=True,
            related_modal_background_color='#000000',
            related_modal_background_opacity=50,
            related_modal_rounded_corners=True,
            related_modal_close_button_visible=True,
            
            # Filtros e navegação
            list_filter_dropdown=True,
            list_filter_sticky=True,
            list_filter_highlight=True,
            list_filter_removal_links=True,
            
            # Formulários
            form_pagination_sticky=True,
            form_submit_sticky=True,
            show_fieldsets_as_tabs=True,
            show_inlines_as_tabs=True,
            
            # Outros recursos
            recent_actions_visible=True,
            environment_name='Desenvolvimento',
            environment_color='#4CAF50',
            
            # Apps dobráveis
            foldable_apps=True,
            
            # Inlines
            collapsible_stacked_inlines=True,
            collapsible_stacked_inlines_collapsed=False,
            collapsible_tabular_inlines=True,
            collapsible_tabular_inlines_collapsed=False,
            
            # Escolhedor de idioma
            language_chooser_active=False,
            language_chooser_display='both',
            language_chooser_control='default-select',
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Tema "{theme.name}" configurado com sucesso!')
        )
        self.stdout.write('🎨 Interface administrativa modernizada!')
        self.stdout.write('🔄 Recarregue a página do admin para ver as mudanças.')
        
        # Informações do tema
        self.stdout.write('\n📋 Características do tema:')
        self.stdout.write(f'  • Cor principal: {theme.primary_color}')
        self.stdout.write(f'  • Cor secundária: {theme.secondary_color}')
        self.stdout.write(f'  • Título: {theme.title}')
        self.stdout.write(f'  • Ambiente: {theme.environment_name}')
        self.stdout.write('  • Layout responsivo e moderno')
        self.stdout.write('  • Filtros e formulários otimizados')
        self.stdout.write('  • Modais e popups melhorados')