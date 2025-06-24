# Unicample
  <p>Unicample é uma aplicação web baseada no jogo Geoguessr, porém, limitada a alugns institutos e locais de relevância da UNICAMP.</p>
  <p>A aplicação se dá por um Backend e um Frontend, construídos em Fast API (python) + Postgres (Banco de dados) e Angular (javascript) respectivamente, além de um docker para subir o Backend localmente e facilitar o desenvolvimento em conjunto.</p>
  
<h2>Backend</h2>
  <p>O servidor foi desenvolvido visando ao máximo concentrar toda a lógica do jogo Unicample e disponinilizar o mínimo de funções (interface) ao client. Nesse sentido o dividimos em 3 pastas principais (fora as pastas de conexão/provimento de sessão com o banco de dados e configuração do projeto) que configuram um sistema próximo de um modelo MVC (Model View Control) de design: </p>
  <li>api</li>  
  <p>&emsp;-> Local onde se econtram os diferentes endpoints da aplicação</p>
  <li>services</li>
  <p>&emsp;-> classes Single Ton em que desenvolvemos as regras de negócio do projeto, ou seja, responsáveis pela lógica utilziada nos endpoints</p>
  <li>models</li>
  <p>&emsp;-> modelos utilizados para criação das tabelas e usados pelos services</p>

  <p>Também há uma pasta na root do backend nomeada "Tests" que provê testes unitários para algumas funções principais do Unicample</p>

  <h3>Como rodar localmente:</h3>

  <h4>Subir o projeto com docker</h4>
  <ol>
      <li>Baixe o Docker</li>
      <li>No terminal do diretório do projeto, insira o comando</li>
      <pre><code class="language-bash">docker compose up --build</code></pre>
      <li>Posteriormente, pode apenas subir o projeto com:</li>
      <pre><code class="language-bash">docker compose up </code></pre>  
      <p>(obs.: o backend fastapi será hospedado na porta 8000)</p>
  </ol>

  <h4>Criar as tabelas no banco de dados</h4>
  <ol>
      <li>Enquanto o docker está com o container backend ativo, abra o diretório backend um terminal</li>
      <li>Entre no bash da image fastapi com:</li>
      <pre><code class="language-bash">docker exec -it fastpi bash</code></pre>
      <li>Agora, dentro do bash da imagem fastapi, rode os seguintes comenados em sequência:</li>
      <pre><code class="language-bash">python</code></pre>
      <pre><code class="language-bash">
      from app.db.init_db import init_db 
      init_db()
      </code></pre>
  </ol>
  <h4>Popular as tabelas (dados utilizado na criação das rodadas do jogo)</h4> 
  <ol>
      <li>Com o docker rodando o projeto, abra no navegador "localhost:8000/docs"</li>
      <li>Rode o endpoint "/admin/import-data" ou import_data</li>
  </ol>

<hr/>
<p><b>Após isso, o servidor estará pronto para ser usado e testado</b></p>
<hr/>

<h4>Testes unitários</h4>
<ol>
  <li>Com o docker rodando o projeto, entre no bash da image fastapi com:</li>
  <pre><code class="language-bash">docker exec -it fastpi bash</code></pre>
  <li>Entre no diretório tests com:</li>
  <pre><code class="language-bash">cd tests</code></pre>
  <li>Execute o comando:</li>
  <pre><code class="language-bash">pytest</code></pre>
</ol>

<h2>Frontend</h2>
<p>Projetado em angular, o cliente está dividido, em geral, nos diretórios:</p>
<li>features</li>
<p>&emsp;-> contém os componentes/páginas principais</p>
<li>services</li>
<p>&emsp;-> local de contato entre servidor e cliente</p>
<li>shared</li>
<p>&emsp;-> componentes separados que podem (e são) utilizados entre as páginas</p>

<h3>Como rodar localmente:</h3>
<ol>
  <li>Baixe a cli do angular (necessita do Node.js baixado):</li>
  <pre><code class="language-bash">npm install -g @angular/cli</code></pre>
  <li>No diretório unicample-frontend, execute:</li>
  <pre><code class="language-bash">ng serve</code></pre>
  <p>(obs.: o frontend angular será hospedado na porta 4200)</p>
</ol>
