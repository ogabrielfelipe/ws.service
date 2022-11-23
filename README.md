# WS-Service

O objetivo do sistema é para realizar o controllhe de HelpDesks, onde o administrador poderia cadastrar a competência (mês vigente) e com isso os usuários poderiam realizar o cadastro de solicitantes, os sistemas que prestam suporte e os módulos, na virada do mês o administrador fecharia a competência e não poderia ser realizado mais nenhuma cadastro na competência anterior e o mesmo poderia exportar os atendimentos dos usuários.

O Sistema foi desenvolvimento em forma de API, utilizando o framework Flask e banco de dados Postgresql através do Supabase. O projeto utiliza o JWT para realizar as autenticações, utiliza o SQLAlchemy e o Marshmallow para executar comandos SQL e realizar as persistências das requisições. Principais funcionalidades do sistema é: Gerenciamentos de Sistemas; Gerenciamentos de Módulos; Gerenciamento de Clientes; Gerenciamento de Setores; Gerenciamento de Competências; Gerenciamento de Atendimentos e Gerenciamento de Usuários.
