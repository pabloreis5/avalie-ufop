# **CSI606-2025-01 - Proposta de Trabalho Final**

## *Discente: Pablo Reis*

---

### Resumo

Este trabalho propõe o desenvolvimento de um Sistema de Avaliação de Disciplinas que permite aos alunos avaliarem de forma anônima as disciplinas cursadas e seus respectivos professores. O sistema visa criar um canal seguro e transparente de feedback acadêmico, possibilitando que os estudantes expressem suas opiniões sem receio de exposição, enquanto oferece aos docentes e coordenadores acesso a dados consolidados para aprimoramento contínuo do processo de ensino. A aplicação garantirá o anonimato completo das respostas, utilizará um banco de dados relacional para armazenamento seguro das informações e disponibilizará painéis administrativos com relatórios e estatísticas visuais sobre a satisfação dos alunos.

---

### 1. Tema

O trabalho final tem como tema o desenvolvimento de um **Sistema Web de Avaliação Anônima de Disciplinas e Professores**, com foco na coleta estruturada de feedback acadêmico e na geração de relatórios estatísticos para apoio à gestão pedagógica institucional.

---

### 2. Escopo

Este projeto terá as seguintes funcionalidades:

#### 2.1 Módulo de Cadastro e Gestão
- Cadastro de disciplinas com informações básicas (código, nome, carga horária, ementa)
- Cadastro de professores (nome, departamento, titulação)
- Cadastro de turmas vinculando disciplina, professor, semestre e código único de acesso
- Gerenciamento completo (CRUD) de todas as entidades do sistema

#### 2.2 Módulo de Avaliação pelos Alunos
- Acesso anônimo às avaliações através de código único da turma
- Formulário de avaliação com:
  - Perguntas objetivas utilizando escala de 1 a 5 (sobre conteúdo, didática, materiais, atendimento, infraestrutura)
  - Campo opcional para comentários e sugestões em texto livre
- Garantia de anonimato total (sistema não armazena identificação do avaliador)
- Interface intuitiva e responsiva para preenchimento

#### 2.3 Módulo Administrativo
- Painel de controle para coordenadores e gestores acadêmicos
- Visualização de relatórios consolidados por:
  - Disciplina
  - Professor
  - Semestre letivo
  - Departamento
- Exibição de médias gerais e por critério de avaliação
- Gráficos estatísticos de satisfação (barras, pizza, linhas de tendência)
- Listagem de comentários textuais agregados por turma

#### 2.4 Funcionalidades Técnicas
- Armazenamento seguro em banco de dados relacional (PostgreSQL ou SQLite)
- Interface web responsiva compatível com dispositivos móveis
- Validação de dados no front-end e back-end
- Geração dinâmica de relatórios e gráficos

---

### 3. Restrições

Neste trabalho **não serão considerados**:

- Sistema de autenticação institucional integrada (login via LDAP, AD ou SSO)
- Controle de períodos ou janelas temporais para abertura/fechamento de avaliações
- Notificações automáticas por e-mail ou SMS aos alunos
- Sistema de permissões granulares com múltiplos níveis de acesso
- Exportação de relatórios em PDF ou outros formatos para download
- Análise avançada de sentimento utilizando processamento de linguagem natural (NLP)
- Módulo de comparação entre departamentos ou cursos distintos
- Histórico de evolução temporal das avaliações ao longo de múltiplos semestres
- Integração com sistemas acadêmicos externos (SIA, SIGA, etc.)
- Funcionalidade de resposta ou contestação por parte dos professores avaliados

---

### 4. Protótipo

Protótipos de baixa fidelidade para as principais páginas do sistema foram elaborados, incluindo:

- **Página inicial**: Entrada do código da turma para acesso anônimo
- **Formulário de avaliação**: Interface de preenchimento das questões objetivas e comentários
- **Dashboard administrativo**: Painel com gráficos e estatísticas consolidadas
- **Página de relatórios**: Visualização detalhada por disciplina/professor

Os protótipos podem ser encontrados no diretório `/prototipos` deste repositório.

**Ferramentas utilizadas**: Figma / Canva / Desenhos à mão digitalizados

---

### 5. Referências

SOMMERVILLE, Ian. **Engenharia de Software**. 10. ed. São Paulo: Pearson Education do Brasil, 2018.

PRESSMAN, Roger S.; MAXIM, Bruce R. **Engenharia de Software: Uma Abordagem Profissional**. 8. ed. Porto Alegre: AMGH, 2016.

SILBERSCHATZ, Abraham; KORTH, Henry F.; SUDARSHAN, S. **Sistema de Banco de Dados**. 6. ed. Rio de Janeiro: Elsevier, 2012.

FLASK. **Flask Documentation**. Disponível em: https://flask.palletsprojects.com/. Acesso em: 18 nov. 2025.

REACT. **React Documentation**. Disponível em: https://react.dev/. Acesso em: 18 nov. 2025.

POSTGRESQL. **PostgreSQL: The World's Most Advanced Open Source Relational Database**. Disponível em: https://www.postgresql.org/. Acesso em: 18 nov. 2025.

---

## Estrutura do Repositório

```
/
├── README.md                 # Este arquivo
├── /prototipos              # Protótipos de interface
├── /docs                    # Documentação adicional
├── /src                     # Código-fonte da aplicação
│   ├── /backend            # Código do servidor
│   ├── /frontend           # Código da interface
│   └── /database           # Scripts SQL e migrações
└── /tests                   # Testes automatizados
```

---

## Tecnologias Previstas

- **Back-end**: Python com Flask ou FastAPI
- **Banco de Dados**: PostgreSQL (produção) / SQLite (desenvolvimento)
- **Front-end**: React ou HTML/CSS/JavaScript
- **Gráficos**: Chart.js ou Recharts
- **Versionamento**: Git e GitHub

---

**Observação**: Este documento será atualizado conforme o desenvolvimento do projeto avança.