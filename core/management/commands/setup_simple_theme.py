"""
Comando para configurar tema bonito da interface admin (versão simplificada)
"""
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Configura tema bonito para a interface administrativa'

    def handle(self, *args, **options):
        try:
            from admin_interface.models import Theme
            
            self.stdout.write('🎨 Configurando tema moderno para o admin...')
            
            # Deletar temas existentes
            Theme.objects.all().delete()
            
            # Criar tema básico e funcional
            theme = Theme.objects.create(
                name='Pulse - Interface Moderna',
                active=True,
                
                # Configurações básicas
                title='🏥 Sistema Pulse - Gestão de Agendamentos',
                title_visible=True,
                title_color='#FFFFFF',
                
                # Cores do cabeçalho
                css_header_background_color='#2196F3',  # Azul moderno
                css_header_text_color='#FFFFFF',
                css_header_link_color='#E3F2FD',
                css_header_link_hover_color='#FFFFFF',
                
                # Cores dos módulos
                css_module_background_color='#FFFFFF',
                css_module_text_color='#333333',
                css_module_link_color='#2196F3',
                css_module_link_hover_color='#1976D2',
                css_module_rounded_corners=True,
                
                # Links genéricos
                css_generic_link_color='#2196F3',
                css_generic_link_hover_color='#1976D2',
                css_generic_link_active_color='#0D47A1',
                
                # Botões
                css_save_button_background_color='#4CAF50',
                css_save_button_background_hover_color='#45A049',
                css_save_button_text_color='#FFFFFF',
                
                css_delete_button_background_color='#F44336',
                css_delete_button_background_hover_color='#D32F2F',
                css_delete_button_text_color='#FFFFFF',
                
                # Recursos avançados
                related_modal_active=True,
                related_modal_background_color='#000000',
                related_modal_background_opacity=50,
                related_modal_rounded_corners=True,
                
                # Layout
                list_filter_dropdown=True,
                recent_actions_visible=True,
                foldable_apps=True,
                
                # Logo
                logo_visible=True,
                logo_color='#FFFFFF',
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Tema "{theme.name}" configurado com sucesso!')
            )
            self.stdout.write('🎨 Interface administrativa modernizada!')
            self.stdout.write('🔄 Recarregue a página do admin para ver as mudanças.')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao configurar tema: {e}')
            )
            self.stdout.write('ℹ️ Tentando configuração manual...')
            
            # Configuração manual via banco
            from django.db import connection
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT OR REPLACE INTO admin_interface_theme (
                            name, active, title, title_visible, title_color,
                            css_header_background_color, css_header_text_color,
                            css_module_background_color, css_module_text_color,
                            css_save_button_background_color, css_save_button_text_color,
                            logo_visible, recent_actions_visible
                        ) VALUES (
                            'Pulse Moderno', 1, '🏥 Sistema Pulse', 1, '#FFFFFF',
                            '#2196F3', '#FFFFFF',
                            '#FFFFFF', '#333333',
                            '#4CAF50', '#FFFFFF',
                            1, 1
                        )
                    """)
                self.stdout.write(
                    self.style.SUCCESS('✅ Tema configurado via SQL!')
                )
            except Exception as sql_error:
                self.stdout.write(
                    self.style.ERROR(f'❌ Erro SQL: {sql_error}')
                )