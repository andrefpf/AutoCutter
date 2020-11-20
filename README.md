# AutoCutter
Bot do telegram para remover pausas desnecessárias em áudios e vídeos.
Mais uma versão do [jumpcutter](https://github.com/carykh/jumpcutter), só que dessa vez no telegram e usando biblioteca de alto nível.

## Instalando
- Clone ou baixe esse repositório. 
- Instale os requisitos com ```pip install -r requirements.txt```.
- Estou supondo que você tenha uma mínima noção de como python funciona e tenha ele instalado.

## Executando
- crie um arquivo na raiz do projeto chamado ```config.json``` semelhante a isso:
    ```
    {
      "token" : "0123456789:QWERTYUIOPASDFGHJKLÇZXCVBNM_abcdefg",
      "db_path" : "home/andre/documents"
    }
    ```
- "token" é o token do seu bot gerado pelo [@BotFather](https://telegram.me/BotFather) do telegram.
- "db_path" trata-se de um diretório de sua escolha para a criação do banco de dados que será usado
  para armazenar as configurações de cada usuário. Se nada for especificado vai ser criado um arquivo 
  na raiz do projeto chamado ```database.db```.
- para iniciar o bot basta usar o comando ```python autocutter/``` dentro da pasta.

## Utilizando
- Se estiver muito confuso pra configurar seu próprio bot, 
  ou se não estiver com saco pra isso manda uma mensagem pro [@auto_cutter_bot](https://telegram.me/auto_cutter_bot).
- Em geral ele não fica rodando, porque não tenho um servidor dando sopa por aqui, mas se você for muito sortudo talvez encontre ele online.

## Requerimentos
- [moviepy](https://github.com/Zulko/moviepy)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
