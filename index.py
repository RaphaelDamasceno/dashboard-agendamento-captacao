# --- ESQUERDA: HERO CARD ---
    with col_left:
        latest = df.iloc[0]
        id_esteira = str(latest.get('id_esteira', '0'))
        is_captacao = id_esteira == '10'
        
        badge_text = "CAPTAÇÃO" if is_captacao else "AGENDAMENTO"
        badge_style = "color:var(--success-text); background:var(--success-bg); border-color:var(--success-border);" if is_captacao else "color:var(--info-text); background:var(--info-bg); border-color:var(--info-border);"
        
        # Tratamento seguro das variáveis
        nome_resp = latest.get('responsavel', 'Indefinido')
        iniciais = "".join([n[0] for n in nome_resp.split()[:2]]).upper()
        
        # CORREÇÃO 1: Removido o escape extra aqui, pois o sanitize_df já fez isso.
        # Se você aplicar escape de novo, "João" viraria "Jo&amp;atilde;o" na tela.
        nome_cartao = latest.get('nome_cartao', '---') 
        
        tempo = pd.to_datetime(latest['data_conclusao']).strftime("%H:%M")

        # CORREÇÃO 2: HTML compactado sem indentações profundas e linhas vazias
        # Isso impede que o Streamlit ache que é um bloco de código.
        html_content = f"""
        <div class="lovable-card hero-card">
            <div class="hero-label">
                <span class="icon-sm">{ICONS['flame']}</span> ÚLTIMA CONVERSÃO
            </div>
            <div class="hero-value">
                {nome_cartao}
            </div>
            <div class="badge-pill" style="{badge_style} margin-bottom: 2rem;">
                {badge_text} REALIZADO
            </div>
            <div style="width: 50%; height: 1px; background: var(--border); margin-bottom: 2rem;"></div>
            <div style="display:flex; flex-direction:column; align-items:center;">
                <div class="hero-avatar">{iniciais}</div>
                <div style="font-size:1.2rem; font-weight:700; color:var(--text-main); margin-bottom:4px;">
                    {nome_resp}
                </div>
                <div style="font-size:0.9rem; color:var(--text-muted); display:flex; align-items:center; gap:6px;">
                    {ICONS['clock']} Hoje às {tempo}
                </div>
            </div>
        </div>
        """
        
        st.markdown(clean_html(html_content), unsafe_allow_html=True)
