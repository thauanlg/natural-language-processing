# Simplificação de Obras do Machado de Assis utilizando Processamento de Linguagem Natural

Este trabalho realiza a simplificação de 5 obras do Machado de Assis. Para isso utilizamos vários córpus existentes para o português brasileiro, cujo quais eram responsáveis por auxiliar na lematização, na análise lexica, na análise sintática, dentre outras. Foi densenvolvido uma interface web para se apresentar o resultado da simplificação dos textos. Para detalhes sobre o trabalho, leia o arquivo _Simplificação de Obras de Machado de Assis com PLN.pdf_ que contém uma descrição completa.

### Requisitos:
 Antes de executar o programa que realiza a simplificação, é necessário instalar no python os pacotes nltk e o córpus machado do nltk.corpus. Se for necessário outro pacote, ocorrerá um erro na execução informando o pacote que está faltando, sendo necessário a sua instalação. Além disso, devido ao tamanho dos córpus utilizados por nós resolvemos armazená-los no formato zip. O arquivo _dados.zip_ contém a pasta com todos as bases utilizados para o nosso trabalho; é necessário somente descompactar.

### Execução:
Para executar a simplificação, entre na pasta "src" e execute o comando:

    python simplifica.py

Será impresso a sequência do pipeline de execução da simplificação.

### Saída:
O resultado da simplificação será criado na pasta "saida", onde contém os textos simplificados. A simplificação  está representado na forma {"palavra_dificil":["simplificação1","simplificação2","simplificação3"]}.

### Resultados nos livros:
Para exibição para o usuários final foram criadas página HTML para os livros. Para navegar por estas páginas basta entrar na pasta web e abrir a página index.html. Então escolhe-se um livro para visualizar. Abrir um novo livro depois é possível voltando para a tela inicial. A conexão com Internet é necessária porque há bibliotecas JavaScript carregadas dinamicamente. A execução acima somente irá gerar o texto simplificado no formato ".txt", não gerando as páginas html.
