# 1. Síntese

A transparência de falha é, na minha opinião, a mais difícil de implementar corretamente em sistemas distribuídos. Isso ocorre porque detectar e mascarar falhas de componentes remotos exige mecanismos sofisticados de retry, timeout e consistência de estado, como visto no arquivo t7_falha/transparencia_falha.py. Muitas vezes, é impossível garantir que uma operação remota foi concluída com sucesso ou que o sistema está em um estado consistente após uma falha, tornando a implementação robusta desse tipo de transparência um grande desafio técnico.

# 2. Trade-offs

Um exemplo bom é o WhatsApp Web. Se o sistema escondesse completamente a distribuição e mascarasse toda instabilidade de rede, o usuário poderia continuar enviando mensagens localmente sem perceber que está offline, levando à perda de contexto e possíveis inconsistências. Ao expor parte da distribuição, o sistema permite que o usuário tome decisões informadas, aumentando a resiliência percebida, pois ele sabe quando suas ações não estão sendo propagadas.

# 3. Conexão com Labs anteriores

O uso de async/await no Lab 02 permite lidar explicitamente com operações assíncronas e atrasos de rede, tornando o fluxo de execução mais transparente para o desenvolvedor. Na Tarefa 7, ao quebrar a transparência de falha, o código pode optar por informar o usuário sobre problemas de comunicação, em vez de mascará-los. Assim, async/await facilita a implementação de lógicas que tratam falhas de forma explícita, conectando-se diretamente à decisão de não esconder todos os detalhes da distribuição.

# 4. GIL e multiprocessing

A Tarefa 6 utiliza multiprocessing em vez de threading porque o GIL do Python impede que múltiplas threads executem bytecodes Python simultaneamente em um mesmo processo. Isso limita a ocorrência real de condições de corrida race conditions em programas multithreaded. Com multiprocessing, cada processo tem seu próprio interpretador Python e GIL, permitindo concorrência real e tornando possível demonstrar problemas clássicos de concorrência, como visto em t6_concorrencia/com_concorrencia.py.

# 5. Desafio técnico

Durante o laboratório, um desafio comum foi o provisionamento do Redis Cloud, especialmente ao configurar as permissões de acesso e obter as credenciais corretas. O diagnóstico envolveu analisar mensagens de erro de conexão no teste_conexao_redis.py e revisar a configuração do arquivo t1_acesso/config.json. A solução foi garantir que o IP local estava autorizado no painel do Redis Cloud e que a string de conexão estava corretamente formatada, permitindo o acesso remoto ao banco de dados.
