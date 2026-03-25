import pandas as pd
from datetime import datetime

def tratar_base_rh(uploaded_file):
    # 1. Lê o arquivo original (que vem com 2018-01-31)
    df = pd.read_csv(uploaded_file, sep=None, engine='python')
    
    # 2. Identifica quais são as colunas de data (mesmo que mudem de nome)
    col_nasc_orig = next((c for c in df.columns if 'nascimento' in c.lower() or 'nasc' in c.lower()), None)
    col_adm_orig = next((c for c in df.columns if 'admissão' in c.lower() or 'adm' in c.lower()), None)
    col_email_orig = next((c for c in df.columns if 'Email' in c.lower() or 'email' in c.lower()), None)

    # 3. CONVERSÃO CRUCIAL: Transforma o texto '2018-01-31' em data real do Python
    if col_nasc_orig:
        df[col_nasc_orig] = pd.to_datetime(df[col_nasc_orig], errors='coerce')
        # Cria as colunas separadas como no seu arquivo processado
        df['Dia_Nascimento'] = df[col_nasc_orig].dt.day
        df['Mes_Nascimento'] = df[col_nasc_orig].dt.month
        df['Ano_Nascimento'] = df[col_nasc_orig].dt.year
        
    if col_adm_orig:
        df[col_adm_orig] = pd.to_datetime(df[col_adm_orig], errors='coerce')
        # Cria as colunas separadas
        df['Dia_Admissao'] = df[col_adm_orig].dt.day
        df['Mes_Admissao'] = df[col_adm_orig].dt.month
        df['Ano_Admissao'] = df[col_adm_orig].dt.year

    # 4. Cálculos Automáticos (Idade e Tempo de Casa)
    hoje = datetime.now()
    if col_nasc_orig:
        df['Idade_Anos'] = df[col_nasc_orig].apply(lambda x: hoje.year - x.year - ((hoje.month, hoje.day) < (x.month, x.day)) if pd.notnull(x) else 0)
    
    if col_adm_orig:
        df['Tempo_Empresa_Anos'] = df[col_adm_orig].apply(lambda x: hoje.year - x.year - ((hoje.month, hoje.day) < (x.month, x.day)) if pd.notnull(x) else 0)

    # 5. Tratamento e Validação de E-mail
    if col_email_orig:
        # 1. Limpa os dados: remove espaços antes e depois e transforma em texto
        df['Email'] = df[col_email_orig].fillna('').astype(str).str.strip()
        
        # 2. Define a regra matemática (Regex) de um e-mail válido genérico
        # Aceita qualquer formato padrão: nome@provedor.com, nome.sobrenome@provedor.com.br, etc.
        padrao_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        # 3. Testa a coluna inteira contra essa regra (retorna Verdadeiro ou Falso)
        emails_validos = df['Email'].str.match(padrao_email)
        
        # 4. Substitui os que NÃO (~) são válidos por 'não informado'
        df.loc[~emails_validos, 'Email'] = 'não informado'
    else:
        # Caso a coluna nem exista no arquivo
        df['Email'] = "não informado"
    
    return df