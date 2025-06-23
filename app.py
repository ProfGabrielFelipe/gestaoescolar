import streamlit as st
import pandas as pd
from io import BytesIO

# Função para salvar dados em um arquivo XLSX
def salvar_dados_completos(alunos):
    dados = []
    for aluno in alunos:
        for disciplina, notas in aluno["Notas"].items():
            dados.append({
                "Nome": aluno["Nome"],
                "RA": aluno["RA"],
                "Turma": aluno["Turma"],
                "Disciplina": disciplina,
                "Notas": ", ".join(map(str, notas)),
                "Média": sum(notas) / len(notas) if notas else 0,
                "Parecer Descritivo": aluno.get("Parecer Descritivo", ""),
                "Status": aluno.get("Status", ""),
                "Bimestre": aluno.get("Bimestre", ""),
            })
    df = pd.DataFrame(dados)
    output = BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)
    return output

# Configuração inicial do Streamlit
st.set_page_config(page_title="Gestão Escolar", layout="wide")

# Título principal do aplicativo
st.title("Sistema de Gestão Escolar 📚")

# Menu de navegação
menu = st.sidebar.radio("Navegação", ["Cadastro de Alunos", "Médias por Disciplina", "Conselho de Classe", "Importar Turmas"])

# Lista inicial de alunos (simulação de banco de dados)
if "alunos" not in st.session_state:
    st.session_state["alunos"] = []

# Disciplinas por turma
disciplinas = {
    # Ensino Fundamental II
    "6º A": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Tecnologia", "Educação Financeira", "Redação e Leitura"],
    "6º B": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Tecnologia", "Educação Financeira", "Redação e Leitura"],
    "6º C": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Tecnologia", "Educação Financeira", "Redação e Leitura"],
    "7º A": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Tecnologia", "Educação Financeira", "Redação e Leitura"],
    "7º B": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Tecnologia", "Educação Financeira", "Redação e Leitura"],
    "8º A": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Tecnologia", "Educação Financeira", "Redação e Leitura"],
    "8º B": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Tecnologia", "Educação Financeira", "Redação e Leitura"],
    "9º A": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Orientação de Estudos de Matemática", "Orientação de Estudos de Português", "Redação e Leitura"],
    "9º B": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Orientação de Estudos de Matemática", "Orientação de Estudos de Português", "Redação e Leitura"],
    "9º C": ["Português", "Inglês", "Arte", "Educação Física", "Matemática", "Ciências", "Geografia", "História", "Projeto de Vida", "Orientação de Estudos de Matemática", "Orientação de Estudos de Português", "Redação e Leitura"],
    # Ensino Médio
    "1ª Série A": ["Português", "Redação e Leitura", "Inglês", "Artes", "Educação Física", "Matemática", "Educação Financeira", "Biologia", "Física", "Química", "Filosofia", "Geografia", "História"],
    "1ª Série B": ["Português", "Redação e Leitura", "Inglês", "Artes", "Educação Física", "Matemática", "Educação Financeira", "Biologia", "Física", "Química", "Filosofia", "Geografia", "História"],
    "1ª Série C": ["Português", "Redação e Leitura", "Inglês", "Artes", "Educação Física", "Matemática", "Educação Financeira", "Biologia", "Física", "Química", "Filosofia", "Geografia", "História"],
    "1ª Série D": ["Português", "Redação e Leitura", "Inglês", "Artes", "Educação Física", "Matemática", "Educação Financeira", "Biologia", "Física", "Química", "Filosofia", "Geografia", "História"],
    "2ª Série A": ["Português", "Redação e Leitura", "Inglês", "Educação Financeira", "Empreendedorismo", "Programação", "Educação Física", "Matemática", "Biologia", "Física", "Química", "Geografia", "História", "Sociologia"],
    "2ª Série B": ["Liderança", "Oratória", "Sociologia", "História", "Geografia", "Química", "Física", "Biologia", "Educação Financeira", "Matemática", "Educação Física", "Inglês", "Redação e Leitura", "Português"],
    "2ª Série C": ["Liderança", "Oratória", "Sociologia", "História", "Geografia", "Química", "Física", "Biologia", "Educação Financeira", "Matemática", "Educação Física", "Inglês", "Redação e Leitura", "Português"],
    "3ª Série A": ["Empreendedorismo", "Programação", "Biotecnologia", "Química Aplicada", "História", "Física", "Matemática", "Educação Física", "Inglês", "Redação e Leitura", "Português", "Orientação de Estudos Matemática", "Orientação de Estudos Português"],
    "3ª Série B": ["Oratória", "Geopolítica", "Filosofia e Sociedade Moderna", "Arte e Mídias Digitais", "História", "Física", "Matemática", "Educação Física", "Inglês", "Redação e Leitura", "Português", "Orientação de Estudos Matemática", "Orientação de Estudos Português"],
    "3ª Série C": ["Oratória", "Geopolítica", "Filosofia e Sociedade Moderna", "Arte e Mídias Digitais", "História", "Física", "Matemática", "Educação Física", "Inglês", "Redação e Leitura", "Português", "Orientação de Estudos Matemática", "Orientação de Estudos Português"],
}

# Página de Importação de Turmas
if menu == "Importar Turmas":
    st.header("Importar Turmas via Planilha XLSX")

    # Instruções para o usuário
    st.markdown("""
    **Instruções para importar turmas:**
    - A planilha deve estar no formato `.xlsx`.
    - As colunas obrigatórias são: **Nome**, **RA**, **Data de Nascimento**, **Turma**, **Situação**, **Comentários**.
    - Certifique-se de que os dados estejam corretos antes de importar.
    """)

    # Upload da planilha
    arquivo = st.file_uploader("Envie a planilha XLSX", type=["xlsx"])

    if arquivo:
        try:
            # Lê a planilha enviada
            df_importado = pd.read_excel(arquivo)

            # Valida se as colunas obrigatórias estão presentes
            colunas_obrigatorias = ["Nome", "RA", "Data de Nascimento", "Turma", "Situação", "Comentários"]
            if all(coluna in df_importado.columns for coluna in colunas_obrigatorias):
                # Adiciona os alunos importados à lista existente
                novos_alunos = df_importado.to_dict(orient="records")
                for aluno in novos_alunos:
                    turma = aluno["Turma"]
                    if turma in disciplinas:
                        aluno["Notas"] = {disciplina: [] for disciplina in disciplinas[turma]}
                        aluno["Parecer Descritivo"] = ""
                        aluno["Status"] = ""
                        aluno["Bimestre"] = ""
                        st.session_state["alunos"].append(aluno)
                st.success(f"{len(novos_alunos)} alunos importados com sucesso!")
            else:
                st.error("A planilha enviada não contém todas as colunas obrigatórias.")
        except Exception as e:
            st.error(f"Erro ao processar a planilha: {e}")

    # Exibe a lista atualizada de alunos
    if st.session_state["alunos"]:
        st.subheader("Lista Atualizada de Alunos")
        df_alunos = pd.DataFrame(st.session_state["alunos"])
        st.dataframe(df_alunos)

# Outras páginas continuam aqui...