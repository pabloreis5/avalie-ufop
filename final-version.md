# **CSI606-2024-02 - Remoto - Trabalho Final - Resultados**

## *Discente: Pablo Reis*

---

### Resumo

O presente trabalho consiste no desenvolvimento de um **Sistema Web de Avaliação de Disciplinas** da UFOP, denominado **Avalie UFOP**. O sistema foi implementado como uma aplicação web que permite aos estudantes avaliar, de forma totalmente anônima, as disciplinas cursadas e os professores que as ministraram. A plataforma oferece um canal estruturado de feedback acadêmico, possibilitando a atribuição de notas em escala de 0 a 5 e a inclusão de comentários opcionais. Os dados coletados são armazenados em banco de dados relacional SQLite e utilizados para o cálculo automático de médias e geração de rankings ordenados das disciplinas, fornecendo subsídios para análise da satisfação discente. A aplicação foi desenvolvida utilizando Flask como framework backend, com interface responsiva em HTML/CSS e interatividade implementada em JavaScript.

---

### 1. Funcionalidades implementadas

As seguintes funcionalidades previstas na proposta foram implementadas com sucesso:

- **Estrutura acadêmica completa**: Sistema de cadastro de cursos (Engenharia Elétrica, Engenharia de Computação, Engenharia de Produção e Sistemas de Informação), com a implementação completa das 40 disciplinas do curso de Sistemas de Informação, incluindo códigos e nomes oficiais. O cadastro de professores foi implementado para permitir a avaliação docente.

- **Módulo de avaliação anônima**: Interface intuitiva e responsiva que permite aos alunos selecionar o curso, disciplina filtrada dinamicamente por curso, professor, atribuir nota de 0 a 5 estrelas e incluir comentário textual opcional. A funcionalidade de anonimato foi garantida pela ausência completa de campos de identificação ou mecanismos de rastreamento do usuário.

- **Validação de dados**: Implementação de validação tanto no frontend (JavaScript) quanto no backend (Python/Flask), garantindo que todos os campos obrigatórios sejam preenchidos e que as notas estejam dentro do intervalo válido (0-5).

- **Módulo de visualização de resultados**: Sistema completo de ranking que apresenta as disciplinas ordenadas por média de avaliação (maior para menor) e, em caso de empate, por número de avaliações. O ranking exibe informações agregadas como nome da disciplina, curso (abreviado), professor, média calculada com duas casas decimais e total de avaliações recebidas.

- **Persistência de dados**: Banco de dados relacional SQLite com estrutura normalizada contendo tabelas para cursos, disciplinas, professores e avaliações. Sistema de seed automático para popular dados iniciais na primeira execução.

- **Interface de navegação**: Sistema de navegação coeso com três páginas principais (Home, Avaliar e Ranking), implementado com header fixo e design responsivo que se adapta a diferentes dispositivos.

- **Sistema de busca**: Funcionalidade de busca em tempo real no ranking, permitindo aos usuários filtrar disciplinas por nome diretamente na interface.

---

### 2. Funcionalidades previstas e não implementadas

Todas as funcionalidades previstas na proposta inicial foram implementadas. Não houve funcionalidades planejadas que ficaram pendentes de implementação.

---

### 3. Outras funcionalidades implementadas

Além das funcionalidades previstas, foram implementados os seguintes recursos adicionais:

- **Interface visual aprimorada**: Design moderno e responsivo com paleta de cores consistente, uso de ícones emoji para melhor usabilidade, efeitos de hover e animações sutis para melhorar a experiência do usuário.

- **Sistema de busca dinâmica**: Implementação de campo de busca no ranking com filtragem em tempo real utilizando JavaScript, permitindo localização rápida de disciplinas específicas.

- **Indicadores visuais de qualidade**: Sistema de badges coloridos no ranking que categoriza visualmente as médias das disciplinas (excelente ≥ 4, bom ≥ 3, regular < 3), facilitando a identificação rápida das melhores avaliações.

- **Destaque das top 3 posições**: Diferenciação visual das três primeiras posições do ranking com cores específicas (ouro, prata e bronze), criando hierarquia visual clara.

- **Contador de avaliações**: Exibição do total de avaliações recebidas por cada disciplina no ranking, fornecendo contexto sobre a confiabilidade das médias apresentadas.

- **Mensagens de estado**: Implementação de feedback visual quando não há resultados na busca do ranking e apresentação do total de disciplinas avaliadas.

- **Meta tags SEO**: Inclusão de tags de descrição e viewport para melhor indexação e visualização em dispositivos móveis.

---

### 4. Principais desafios e dificuldades

Durante o desenvolvimento do projeto, os seguintes desafios foram enfrentados e superados:

- **Filtragem dinâmica de disciplinas**: A implementação da filtragem de disciplinas por curso selecionado exigiu comunicação eficiente entre frontend e backend. A solução adotada foi passar todos os dados de disciplinas para o template e implementar a lógica de filtragem via JavaScript, utilizando o atributo `data-curso-id` nas opções do select, permitindo filtragem instantânea sem requisições adicionais ao servidor.

- **Garantia de anonimato**: Assegurar o anonimato total das avaliações foi uma preocupação central. A solução implementada consistiu em não coletar nenhum dado identificador do usuário, nem mesmo endereço IP ou timestamps que pudessem ser correlacionados, mantendo apenas os dados essenciais da avaliação (curso, disciplina, professor, nota e comentário opcional).

- **Validação robusta de dados**: Implementar validação tanto no frontend quanto no backend para prevenir envios inválidos. Foram criadas validações de presença de campos obrigatórios, verificação de tipos de dados e checagem de intervalos numéricos válidos para as notas.

- **Estrutura do banco de dados**: Definir uma estrutura de banco de dados normalizada e eficiente que permitisse consultas agregadas de forma performática. A solução adotou tabelas relacionadas com chaves estrangeiras adequadas e consultas SQL otimizadas com joins e agregações para o cálculo de médias e contagens.

- **Design responsivo**: Criar uma interface que funcionasse adequadamente em diferentes tamanhos de tela. Utilizou-se CSS flexbox e media queries para adaptar o layout, garantindo boa usabilidade tanto em dispositivos móveis quanto em desktops.

---

### 5. Instruções para instalação e execução

#### 5.1 Pré-requisitos

- Python 3.8 ou superior instalado
- Pip (gerenciador de pacotes Python)
- Navegador web moderno

#### 5.2 Instalação

**1. Clone ou baixe o repositório do projeto:**
```bash
cd avalie-ufop
```

**2. Crie um ambiente virtual Python (recomendado):**
```bash
python -m venv venv
```

**3. Ative o ambiente virtual:**

- No Windows:
```powershell
.\venv\Scripts\Activate.ps1
```

- No Linux/Mac:
```bash
source venv/bin/activate
```

**4. Instale as dependências do projeto:**
```bash
pip install -r requirements.txt
```

#### 5.3 Configuração

Não há configurações adicionais necessárias. O banco de dados SQLite (`app.db`) será criado automaticamente na primeira execução, e os dados iniciais (cursos, disciplinas de Sistemas de Informação e professores de exemplo) serão populados automaticamente através do sistema de seed implementado.

#### 5.4 Execução

**1. Navegue até o diretório `src`:**
```bash
cd src
```

**2. Execute a aplicação:**
```bash
python app.py
```

**3. Acesse a aplicação no navegador:**

Abra seu navegador e acesse: `http://127.0.0.1:5000` ou `http://localhost:5000`

**4. Navegação:**

- **Página inicial**: Apresentação do sistema com acesso às funcionalidades
- **Avaliar**: Formulário de avaliação de disciplinas (acessível via menu ou botão na home)
- **Ranking**: Visualização das disciplinas ordenadas por média de avaliação

#### 5.5 Observações

- O sistema utiliza SQLite em modo de arquivo, portanto o banco de dados persiste entre execuções
- Para reiniciar o banco de dados, basta deletar o arquivo `app.db` no diretório `src`
- O modo debug está habilitado por padrão, permitindo hot-reload durante desenvolvimento
- Para ambiente de produção, recomenda-se desabilitar o modo debug e utilizar um servidor WSGI apropriado (como Gunicorn)

---

### 6. Referências

SOMMERVILLE, Ian. **Engenharia de Software**. 10. ed. São Paulo: Pearson Education do Brasil, 2018.

PRESSMAN, Roger S.; MAXIM, Bruce R. **Engenharia de Software: Uma Abordagem Profissional**. 8. ed. Porto Alegre: AMGH, 2016.

GRINBERG, Miguel. **Flask Web Development: Developing Web Applications with Python**. 2. ed. Sebastopol: O'Reilly Media, 2018.

MOZILLA DEVELOPER NETWORK. **JavaScript Documentation**. Disponível em: https://developer.mozilla.org/en-US/docs/Web/JavaScript. Acesso em: jan. 2026.

FLASK DOCUMENTATION. **Flask Documentation (3.1.x)**. Disponível em: https://flask.palletsprojects.com/. Acesso em: jan. 2026.
