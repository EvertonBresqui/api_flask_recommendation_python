# Manual de intalação e configuração

## Processo de instalação de softwares:

### Instalar python 3.8.5

### Instalar libs requeridas python 3:

> pip3 install flask

> pip3 install Flask-PyMongo

> pip3 install pyjwt

### Instalar MongoDB v4.4.10

## Processo de configuração de softwares:

### Configurações IDE vscode para debug:

Dentro do Visual Studio Code pressione as seguinte teclas Ctrl+Shift+P e
selecione o interpretador onde foi instalado o flask;
Depois na área de debug do Visual Studio Code clique no link create a launch.json file e informe o nome main.py no qual é o arquivo de inicialização do flask.

### Configurações MongoDB:

#### Entre no terminal e entre no interpretador do mongo e digite os comandos abaixo:

> use admin

> db.createUser({ user: "rootUser", pwd: "rootUserPwd", roles: ["root"]})

#### Agora saia do mongo db

> exit

#### Para ativar a autenticação, abra o arquivo de configuração /etc/mongod.conf e adicione no final do arquivo:

> security:

>   authorization: enabled

#### Agora reinicie o serviço

> sudo service mongod restart

#### Agora será necessário autenticar no usuário root para ter acesso

> mongo --port 27017 -u "rootUser" -p "rootUserPwd" --authenticationDatabase "admin"

#### Agora vamos criar um usuário e dar a ele os papéis readWrite e dbAdmin em um novo banco de dados chamado teste.

> use teste

> db.createUser({ user: "teste", pwd: "123", roles: [{ role: "dbAdmin", db: "teste" }, { role: "readWrite", db: "teste" } ]})

> exit

#### Faz a autenticação com o usuário criado

> mongo --port 27017 -u "teste" -p "123" --authenticationDatabase "teste"

> use teste


## Configurações para rodar a aplicação e teste:
 
### No arquivo src/config.py do projeto da api configure os seguintes itens:

#### Tipos de lojas aceitos:
` Caso for necessário adicione o nome da plataforma que deseja integrar ` 

> __sales_types = {1: 'magento1', 2: 'magento2'}

#### Tipos de algorítmos implementados
` Caso for necessário adicione o nome do algoritmo novo que implementar `

> __algorithms = {

> 1:'als'

> }

#### Configuração para acesso ao banco MongoDB
` Informe as configurações que informou para criar o usuário e o banco `

> __mongo_db = {

>      'domain':'localhost:27017',

>      'user':'teste', 

>      'password':'123',

>      'database':'teste', 

>  }

#### Configurações dos grupos das lojas(multi-stores)
` Aqui é configurado os dados gerais da loja, como usuário de acesso, tipo da loja, etc `

>__sales_groups_conf = {

>    1 [ group id sale ]:{

>        'id': 1, [ group id sale ]

>        'sale_type': 2,

>        'username':'teste',

>        'password':'123',

>        'secret_key': 'dasdad@$&%#@1514',

>        'hours_exp_token': 30,

>        'ip': '127.0.0.1'

>    },

>}

#### Configurações para cada loja independente(store_id)
` O magento possui a opção de criar várias lojas ou seja, é possível definir um algoritmo diferente para cada tipo de loja`
> __sales = {

>        1: {

>            'name_store': 'teste', [name sale]

>            'increment_id': 1, [id sale]

>            'sale_group': 1, [id group sale]

>            ` Configurações especificas que variam para cada tipo de loja `

>            'settings':{

>                'store_id': 1, [store_id magento sale]

>                'website_id': 1, [website_id magento sale]

>                'group_id': 1 [group_id magento sale]

>            }

>        },

>    }

#### Configurações dos parâmetros dos algoritmos de cada loja
`A configuração dos parâmetros são para adicionar informações adicionais para setar no algoritmo de recomendação.`

>__params = {

>   1:{

>      'algorithm': 1,

>      'train': 0.8,

>      'test': 0.2,

>      'random_state': 200,

>      'factors': 20,

>      'regularization': 0.1,

>      'iterations': 20,

>      'alpha_val': 15,

>      'n_similar': 10,

>      'num_items': 10

>  },

>}

#### Rodar Api:

> export FLASK_APP=main.py

> python3 -m flask run
