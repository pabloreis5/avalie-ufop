# **CSI606-2025-01 – Proposta de Trabalho Final**

## *Discente: Pablo Reis*

---

## Resumo

Este trabalho propõe o desenvolvimento de um **Sistema Web de Avaliação de Disciplinas**, cujo objetivo é permitir que alunos avaliem, de forma **anônima**, as disciplinas cursadas e os professores que as ministraram. A aplicação busca fornecer um canal simples e acessível de feedback acadêmico, possibilitando a coleta estruturada de avaliações quantitativas e comentários opcionais, sem qualquer identificação do avaliador. Os dados coletados serão armazenados em banco de dados relacional e utilizados para o cálculo de médias e geração de **rankings de melhores e piores disciplinas**, oferecendo subsídios para análise da satisfação discente e apoio à gestão pedagógica.

---

## 1. Tema

O trabalho final tem como tema o desenvolvimento de um **Sistema Web de Avaliação Anônima de Disciplinas e Professores**, com foco na coleta de feedback acadêmico por meio de formulários estruturados e na apresentação de resultados agregados, como médias e rankings de desempenho das disciplinas avaliadas.

---

## 2. Escopo

Este projeto contemplará as seguintes funcionalidades:

### 2.1 Estrutura Acadêmica

- Cadastro de cursos (ex.: Engenharia Elétrica, Engenharia de Computação, Engenharia de Produção e Sistemas de Informação)
- Cadastro de disciplinas vinculadas a um curso específico
- Cadastro de professores disponíveis para avaliação
- Organização lógica das disciplinas por curso, permitindo filtragem durante o processo de avaliação

---

### 2.2 Módulo de Avaliação pelos Alunos

- Página inicial genérica de boas-vindas com acesso ao formulário de avaliação
- Formulário de avaliação anônima contendo:
  - Seleção do curso
  - Seleção da disciplina (filtrada de acordo com o curso escolhido)
  - Seleção do professor (lista geral de docentes)
  - Atribuição de nota em escala numérica de **0 a 5**
  - Campo opcional para comentários textuais
- Garantia de anonimato total, sem armazenamento de dados que identifiquem o aluno
- Interface simples e intuitiva para preenchimento das avaliações

---

### 2.3 Módulo de Visualização de Resultados

- Armazenamento das avaliações em banco de dados relacional
- Cálculo automático das médias das notas por disciplina
- Exibição de um **ranking de disciplinas**, ordenado da melhor para a pior avaliação
- Possibilidade de visualização agregada por curso e disciplina
- Apresentação dos resultados de forma clara, por meio de tabelas e estatísticas simples

---

### 2.4 Funcionalidades Técnicas

- Persistência de dados em banco de dados relacional (SQLite ou PostgreSQL)
- Aplicação web desenvolvida em arquitetura cliente-servidor
- Validação básica de dados no envio das avaliações
- Estrutura simples, priorizando funcionalidade e clareza de implementação

---

## 3. Restrições

Neste trabalho **não serão considerados**:

- Qualquer forma de autenticação ou identificação de alunos
- Controle de período ou janela temporal para realização das avaliações
- Associação histórica de professores a disciplinas por semestre letivo
- Sistema de permissões ou perfis de usuário (administrador, professor, aluno)
- Exportação de relatórios em PDF ou outros formatos
- Dashboards interativos avançados
- Análise de sentimento ou processamento de linguagem natural nos comentários
- Comparação entre cursos distintos ou análise evolutiva ao longo do tempo
- Integração com sistemas acadêmicos institucionais
- Funcionalidade de resposta ou contestação das avaliações por professores

---

## 4. Protótipo

Protótipos foram elaborados para representar as principais telas do sistema, incluindo:

- **Página inicial**: Tela de boas-vindas com acesso ao formulário de avaliação
- **Formulário de avaliação**: Seleção de curso, disciplina, professor e preenchimento da nota e comentário
- **Página de ranking**: Exibição das disciplinas ordenadas por média de avaliação

Os protótipos encontram-se no diretório `/prototipos` deste repositório.

**Ferramentas utilizadas**: Figma e Canva

---

## 5. Referências

SOMMERVILLE, Ian. **Engenharia de Software**. 10. ed. São Paulo: Pearson Education do Brasil, 2018.

PRESSMAN, Roger S.; MAXIM, Bruce R. **Engenharia de Software: Uma Abordagem Profissional**. 8. ed. Porto Alegre: AMGH, 2016.

SILBERSCHATZ, Abraham; KORTH, Henry F.; SUDARSHAN, S. **Sistema de Banco de Dados**. 6. ed. Rio de Janeiro: Elsevier, 2012.

FLASK. **Flask Documentation**. Disponível em: https://flask.palletsprojects.com/. Acesso em: 18 nov. 2025.

---

## 6. Estrutura do Repositório

```
avalie-ufop/
│
├── src/                          # Código-fonte da aplicação
│   ├── app.py                    # Aplicação Flask principal
│   ├── app.db                    # Banco de dados SQLite (gerado automaticamente)
│   │
│   ├── static/                   # Arquivos estáticos (CSS, JS)
│   │   ├── style.css            # Estilos da aplicação
│   │   └── app.js               # JavaScript do frontend
│   │
│   ├── templates/               # Templates HTML
│   │   ├── index.html           # Página inicial
│   │   ├── avaliar.html         # Formulário de avaliação
│   │   └── ranking.html         # Ranking de disciplinas
│   │
│   └── prototipos/              # Protótipos de interface
│
├── venv/                        # Ambiente virtual Python (não versionado)
│
├── requirements.txt             # Dependências do projeto
├── readme.md                    # Documentação da proposta
├── final-version.md            # Documentação dos resultados finais
├── 02-final-version-modelo.md  # Modelo para documentação final
├── MELHORIAS.md                # Documentação das melhorias implementadas
├── CHANGELOG-VISUAL.md         # Documentação das mudanças visuais
│
└── .gitignore                  # Arquivos ignorados pelo Git
```

### Principais Arquivos

- **`src/app.py`**: Contém toda a lógica do backend, rotas Flask, operações de banco de dados e seed de dados iniciais
- **`src/static/style.css`**: Estilos modernos e responsivos da aplicação
- **`src/static/app.js`**: Lógica JavaScript para interatividade (filtros, validações, contador de caracteres)
- **`src/templates/*.html`**: Templates Jinja2 para renderização das páginas
- **`requirements.txt`**: Lista todas as dependências Python necessárias (Flask, SQLite, etc.)
- **`final-version.md`**: Documentação completa do projeto finalizado com instruções de instalação e execução
