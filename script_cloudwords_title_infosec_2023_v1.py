import sqlite3
import pandas as pd
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Função para encontrar a posição de '- https://' e remover tudo à direita
def remove_url(text):
    index = text.find('- https://')
    if index != -1:
        return text[:index].strip()
    return text

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('/home/fabio/BD_INTELLIGENCE/BD_NEWS.db')

# Consulta SQL para obter os títulos
query = "SELECT DISTINCT texto_href AS TEXTO FROM TAB_INFOSEC WHERE DateTime like '2022%'; "
df = pd.read_sql_query(query, conn)

# Verificar os nomes reais das colunas no DataFrame
print(df.columns)

# Renomear a coluna para 'TITULO' se necessário
df.columns = [col.upper() for col in df.columns]  # Ajuste para garantir consistência no caso das colunas
if 'TEXTO' in df.columns:
    df['TITULO'] = df['TEXTO'].apply(remove_url)  # Correção: use 'TITULO' em vez de 'TextoLink'
    df = df[['TITULO']]  # Manter apenas a coluna 'TITULO'
else:
    raise KeyError("A coluna 'TEXTO' não está presente no DataFrame.")

# Fechar a conexão com o banco de dados
conn.close()

# Converter os títulos para uma única string
text = " ".join(df['TITULO'])

# Tokenização e remoção de stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))  # Pode ser necessário ajustar para o idioma correto

custom_stopwords = ['b', 'https', 'an', 'with', 'is', 'not', 'since', 'were', 'have', 'more', 'some', 'any', 'us',
    'their', 'will', 'its', 'using', 'without', 'get', 'of', 'your', 'says', 'they',
    'been', 'this', 'at', 'it', 'be', 'on', 'by', 'us', 'ot', 'or', 'the', 'in', 'hacker', 'new', 'hackernews', 'hackers', 'Security','security', 'malware', 'million',
    'target', 'targeting', 'attack', 'attacks', 'targeted', 'CISA', 'CISA Update', 'CISA Release', 'Release','Cyber', 'cybersecurity'
]  # Adicione a palavra que você deseja remover

stop_words.update(custom_stopwords)

words = nltk.word_tokenize(text)
filtered_words = [word for word in words if word.lower() not in stop_words]

# Verificar se há palavras suficientes após a remoção de stopwords
if not filtered_words:
    print("Não há palavras suficientes para criar uma nuvem de palavras.")
else:
    # Unir as palavras filtradas em uma única string
    filtered_text = " ".join(filtered_words)

    # Criar uma nuvem de palavras
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(filtered_text)

    # Salvar a nuvem de palavras em um arquivo
    wordcloud.to_file("/home/fabio/pln/nuvem_de_palavras_2022_infosec.png")

    # Não exibir a nuvem de palavras interativamente
    # plt.figure(figsize=(10, 5))
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis("off")
    # plt.show()
