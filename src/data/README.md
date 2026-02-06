# Dados do Sistema Avalie-UFOP

Esta pasta contém os dados que serão importados para o banco de dados através do script `seed_database.py`.

## Estrutura de Arquivos

### cursos.csv
Lista de todos os cursos disponíveis no sistema.

**Formato:**
```csv
nome
Nome do Curso
```

### professores.csv
Lista de professores que podem ser avaliados.

**Formato:**
```csv
nome
Nome do Professor
```

### disciplinas_*.csv
Arquivos contendo as disciplinas de cada curso. Você pode criar quantos arquivos quiser seguindo o padrão `disciplinas_*.csv`.

**Formato:**
```csv
codigo,nome,curso
CODIGO,Nome da Disciplina,Nome do Curso
```

**Importante:** O valor da coluna `curso` deve corresponder exatamente a um nome no arquivo `cursos.csv`.

## Como Adicionar um Novo Curso

### 1. Adicione o curso em cursos.csv
```csv
nome
Engenharia Mecânica
```

### 2. Crie um arquivo de disciplinas
Crie um arquivo `disciplinas_engenharia_mecanica.csv`:

```csv
codigo,nome,curso
MEC101,Introdução à Engenharia Mecânica,Engenharia Mecânica
MEC102,Desenho Técnico,Engenharia Mecânica
CEA050,Cálculo Diferencial e Integral I,Engenharia Mecânica
```

### 3. Execute o script de seed
```bash
cd src
python seed_database.py
```

O script vai:
- ✓ Criar as tabelas (se não existirem)
- ✓ Importar os novos cursos
- ✓ Importar as disciplinas
- ✓ Evitar duplicação de dados

## Vantagens desta Abordagem

✅ **Escalável**: Adicione quantos cursos quiser sem modificar código     
✅ **Organizado**: Dados separados por arquivo facilitam manutenção
✅ **Versionável**: Arquivos CSV podem ser versionados no Git
✅ **Fácil edição**: Qualquer pessoa pode editar CSVs (Excel, LibreOffice, etc.)
✅ **Reutilizável**: Scripts podem ser executados múltiplas vezes sem duplicar dados
