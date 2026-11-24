# Executa cada consulta de 03_consultas.sql no MySQL de teste, com a data do seminário,
# e salva enunciado, SQL e resultado em resultados.json (usado para montar o documento).
import re, json, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
MYSQL = r'C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe'
texto = open('entrega/03_consultas.sql', encoding='utf-8').read()
blocos = re.findall(r'/\* -+\n(.*?)-+ \*/\n(.*?)(?=\n/\* -+|\Z)', texto, re.S)
saida = []
for cab, sql in blocos:
    cab = '\n'.join(l.strip() for l in cab.strip().splitlines())
    num = re.match(r'(Q\d+)\.', cab).group(1)
    enunciado = re.sub(r'\s+', ' ', re.search(r'Q\d+\.\s*(.*?)\nComandos:', cab, re.S).group(1)).strip()
    comandos = re.sub(r'\s+', ' ', cab.split('Comandos:', 1)[1]).strip()
    sql = sql.strip()
    p = subprocess.run([MYSQL, '-h127.0.0.1', '-P3399', '-uroot', '--default-character-set=utf8mb4', '-B', 'crie_demandas',
                        '-e', "SET TIMESTAMP = UNIX_TIMESTAMP('2026-11-30 19:00:00'); " + sql],
                       capture_output=True, text=True, encoding='utf-8')
    if p.returncode != 0:
        print(num, 'ERRO', p.stderr); sys.exit(1)
    linhas = [l.split('\t') for l in p.stdout.rstrip('\n').split('\n')] if p.stdout.strip() else [[]]
    saida.append({'num': num, 'enunciado': enunciado, 'comandos': comandos, 'sql': sql, 'colunas': linhas[0], 'linhas': linhas[1:]})
    print(f'{num}: {len(linhas)-1} linhas | {enunciado[:70]}')
json.dump(saida, open('ferramentas/resultados.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
