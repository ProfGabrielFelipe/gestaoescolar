import os
import streamlit as st
import pandas as pd
import datetime
import time

# Diretórios para armazenar os arquivos localmente
PASTA_FOTOS = "fotos"
PASTA_UPLOADS = "uploads"

# Criar as pastas, se não existirem
os.makedirs(PASTA_FOTOS, exist_ok=True)
os.makedirs(PASTA_UPLOADS, exist_ok=True)

# Função para salvar arquivos localmente com nome único
def salvar_arquivo_com_nome_unico(diretorio, arquivo):
    extensao = arquivo.name.split(".")[-1]  # Obtém a extensão do arquivo
    nome_unico = f"{int(time.time())}.{extensao}"  # Gera um nome único baseado no timestamp
    caminho_arquivo = os.path.join(diretorio, nome_unico)
    with open(caminho_arquivo, "wb") as f:
        f.write(arquivo.read())
    return caminho_arquivo, nome_unico

# Função para salvar os dados dos alunos em um arquivo XLSX
def salvar_alunos_xlsx(alunos):
    df = pd.DataFrame(alunos)
    df.to_excel("alunos.xlsx", index=False, engine="openpyxl")

# Carregar os dados dos alunos ao iniciar o sistema
if os.path.exists("alunos.xlsx"):
    alunos = pd.read_excel("alunos.xlsx", engine="openpyxl").to_dict(orient="records")
else:
    alunos = []

# Disciplinas por turma
disciplinas_por_turma = {
    # Ensino Fundamental II
    "6º A": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Tecnologia", "Educação Financeira", "Redação e Leitura"],
    "6º B": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Tecnologia", "Educação Financeira", "Redação e Leitura"],
    "6º C": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Tecnologia", "Educação Financeira", "Redação e Leitura"],
    "7º A": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Tecnologia", "Educação Financeira", "Redação e Leitura"],
    "7º B": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Tecnologia", "Educação Financeira", "Redação e Leitura"],
    "8º A": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Tecnologia", "Educação Financeira", "Redação e Leitura"],
    "8º B": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Tecnologia", "Educação Financeira", "Redação e Leitura"],
    "9º A": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Orientação de Estudos Matemática", "Orientação de Estudos Português", "Redação e Leitura"],
    "9º B": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Orientação de Estudos Matemática", "Orientação de Estudos Português", "Redação e Leitura"],
    "9º C": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Orientação de Estudos Matemática", "Orientação de Estudos Português", "Redação e Leitura"],
    # Ensino Médio
    "1ª Série A": ["Português", "Redação e Leitura", "Inglês", "Artes", "Educação Física", "Matemática", "Educação Financeira", "Biologia", "Física", "Química", "Filosofia", "Geografia", "História"],
    "1ª Série B": ["Português", "Redação e Leitura", "Inglês", "Artes", "Educação Física", "Matemática", "Educação Financeira", "Biologia", "Física", "Química", "Filosofia", "Geografia", "História"],
    "1ª Série C": ["Português", "Redação e Leitura", "Inglês", "Artes", "Educação Física", "Matemática", "Educação Financeira", "Biologia", "Física", "Química", "Filosofia", "Geografia", "História"],
    "1ª Série D": ["Português", "Redação e Leitura", "Inglês", "Artes", "Educação Física", "Matemática", "Educação Financeira", "Biologia", "Física", "Química", "Filosofia", "Geografia", "História"],
    "2ª Série A": ["Português", "Redação e Leitura", "Inglês", "Educação Financeira", "Empreendedorismo", "Programação", "Educação Física", "Matemática", "Biologia", "Física", "Química", "Geografia", "História", "Sociologia"],
    "2ª Série B": ["Português", "Redação e Leitura", "Inglês", "Educação Financeira", "Empreendedorismo", "Programação", "Educação Física", "Matemática", "Biologia", "Física", "Química", "Geografia", "História", "Sociologia"],
    "2ª Série C": ["Português", "Redação e Leitura", "Inglês", "Educação Financeira", "Empreendedorismo", "Programação", "Educação Física", "Matemática", "Biologia", "Física", "Química", "Geografia", "História", "Sociologia"],
    "3ª Série A": ["Empreendedorismo", "Programação", "Biotecnologia", "Química Aplicada", "História", "Física", "Matemática", "Educação Física", "Inglês", "Redação e Leitura", "Português", "Orientação de Estudos Matemática", "Orientação de Estudos Português"],
    "3ª Série B": ["Empreendedorismo", "Programação", "Biotecnologia", "Química Aplicada", "História", "Física", "Matemática", "Educação Física", "Inglês", "Redação e Leitura", "Português", "Orientação de Estudos Matemática", "Orientação de Estudos Português"],
    "3ª Série C": ["Empreendedorismo", "Programação", "Biotecnologia", "Química Aplicada", "História", "Física", "Matemática", "Educação Física", "Inglês", "Redação e Leitura", "Português", "Orientação de Estudos Matemática", "Orientação de Estudos Português"]
}

# Configuração do layout do Streamlit
st.set_page_config(page_title="Gestão Escolar", layout="wide")
st.title("📚 Gestão Escolar - Sistema de Cadastro")

# Menu de navegação
menu = st.sidebar.radio("Navegação", ["Cadastro de Alunos", "Conselho de Classe", "Importar/Exportar Dados"])

# Página: Cadastro de Alunos
if menu == "Cadastro de Alunos":
    st.header("📋 Cadastro de Alunos")
    st.markdown("Preencha os dados abaixo para cadastrar um novo aluno no sistema.")
    st.divider()
    with st.form("form_cadastro"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome do aluno")
            ra = st.text_input("RA")
            data_nasc = st.date_input("Data de nascimento", min_value=datetime.date(2000, 1, 1), max_value=datetime.date.today())
        with col2:
            turma = st.selectbox("Turma", list(disciplinas_por_turma.keys()))
            situacao = st.selectbox("Situação", ["Ativo", "Transferido", "Inativo"])
            comentario = st.text_area("Comentário do Conselho de Classe")
        foto = st.file_uploader("Foto do aluno", type=["jpg", "jpeg", "png"])
        cadastrar = st.form_submit_button("Cadastrar")

        if cadastrar:
            if not nome or not ra or not turma:
                st.error("⚠️ Preencha todos os campos obrigatórios!")
            elif any(aluno["ra"] == ra for aluno in alunos):
                st.error("⚠️ RA já cadastrado!")
            else:
                caminho_foto = ""
                if foto is not None:
                    caminho_foto, _ = salvar_arquivo_com_nome_unico(PASTA_FOTOS, foto)
                novo_aluno = {
                    "nome": nome,
                    "ra": ra,
                    "data_nascimento": data_nasc.strftime("%Y-%m-%d"),
                    "turma": turma,
                    "foto": caminho_foto,
                    "situacao": situacao,
                    "comentario": comentario,
                    "frequencia": 100,
                    "medias": {disciplina: 0 for disciplina in disciplinas_por_turma[turma]},
                }
                alunos.append(novo_aluno)
                salvar_alunos_xlsx(alunos)
                st.success(f"✅ Aluno {nome} cadastrado com sucesso!")