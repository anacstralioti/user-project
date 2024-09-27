<h1>Sistema em Python com Flask e SQLite</h1>

<h2>Descrição</h2>
<p>Este projeto é um sistema de autenticação de usuários desenvolvido em Python com Flask, utilizando banco de dados SQLite para armazenar informações de usuários. 
Entre suas funcionalidades estão cadastro, login e atualização de usuários.</p>

<h2>Como executar o projeto?</h2>
<ul>
    <li>Importe o projeto para o Pycharm</li>
    <li>Certifique-se que o Python esteja na versão 3.12.</li>
    <li>No terminal execute os seguintes comandos:</li>
    <ul>
      <li><pre>pip install flask</pre></li>
      <li><pre>pip install bcrypt</pre></li>
      <li><pre>python main.py</pre></li>
    </ul>
</ul>

<h2>Como usar a aplicação?</h2>

<ol>
    <li><strong>Após executar a inicialização do servidor Flask com: </strong>
        <pre>python main.py</pre>
        <p>O servidor será iniciado em <code>http://127.0.0.1:5000</code>.</p>
    </li>
    <li><strong>A partir daí, é possível acessar as rotas</strong>
        <ul>
            <li>Página inicial: <code>http://127.0.0.1:5000/</code></li>
            <li>Cadastro de usuário: <code>http://127.0.0.1:5000/cadastro</code></li>
            <li>Login de usuário: <code>http://127.0.0.1:5000/login</code></li>
            <li>Alteração de usuário: <code>http://127.0.0.1:5000/alteracao</code></li>
        </ul>
    </li>
</ol>

<h2>Funcionalidades</h2>
<ul>
    <li><strong>Cadastro de Usuário:</strong> Permite que novos usuários se cadastrem fornecendo login (e-mail), senha e nome.</li>
    <li><strong>Login de Usuário:</strong> Permite que usuários existentes façam login.</li>
    <li><strong>Alteração de Usuário:</strong> Permite que usuários atualizem suas informações (sendo "puxados" a partir do ID) e sejam bloqueados (status alterado para inativo).</li>
</ul>

<h2>Observações</h2>
<p>As senhas são armazenadas de forma segura utilizando hashing com bcrypt. O sistema assume que o e-mail fornecido no cadastro é único.</p>
