import 'package:flutter/material.dart';
import '../models/perfil.dart';   
import '../services/perfil_service.dart';
import '../pages/homeusuariocomum.dart';
import './homeprofissional.dart';


/**
  SET STAGE:Finalidade: Atualizar a interface do usuário dinamicamente. Sem chamar o setState, o 
 Flutter não saberá que deve renderizar novamente o widget, 
 mesmo que a variável tenha sido alterada.
 */
class Informacoesbasicas extends StatefulWidget {
  const Informacoesbasicas({super.key});

@override//sobrescrever um metódo de uma classe 
  State<Informacoesbasicas> createState() => _InformacoesbasicasState(); 
}
 
 class _InformacoesbasicasState extends State<Informacoesbasicas>{
    final PageController _pageController=PageController();
    final PerfilService _perfilService=PerfilService();
    final Perfil _perfil=Perfil();
    int pagatual=0;
    int totalpaginas=9;


    Future<void>  proximaPagina() async{
      if(pagatual<totalpaginas-1){
        _pageController.nextPage(duration: const Duration(milliseconds: 300), curve: Curves.easeInOut,);

      }
      //else{
        //await _perfilService.atualizarPerfil(_perfil.toJson());
         //Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => Homeusuariocomum()),);
         //tenho que direcionar pra home certa aqui TENHO QUE VER SE PRECISO DISSO DEPOIS 
      //}
    }

    void  paginaAnterior(){
      if(pagatual>0){
        _pageController.previousPage(duration:const Duration(milliseconds: 300), curve: Curves.easeInOut,);//o jeito que ocorre a animação de troca de pagina é o curve
      }
    }

    Future<void> finalizar() async{// pra redirecionar pra home depois eu olho como faz 
     try{
      await _perfilService.atualizarPerfil(_perfil.toJson());
      if (!mounted) return;//caso a pessoa feche a tela ou algo errado aconteça 
      if(_perfil.tipousuario=='aluno'){
        Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => Homeusuariocomum()),);
      }
      else if(_perfil.tipousuario=='profissional'){
        Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) =>Homeprofissional()),);
      }
     }
     catch(e){
      print('erro ao atualizar perfil');
     }

    }

    Widget _barraProgresso(){
      return Padding(padding: const EdgeInsets.symmetric(horizontal:24),//define o tamanho da barra sem mexer em cima
      child:Column(
        crossAxisAlignment: CrossAxisAlignment.start,//centralizar tudo a esquerda colum tem dois eixos vertical e horizontal
        children: [
          LinearProgressIndicator(//mostra uma barra na horizontal
            value:(pagatual+1)/totalpaginas,
            minHeight: 8,//altura minima da barra
            borderRadius:BorderRadius.circular(10),//borda
          ),
          const SizedBox(height: 8,),
          Text(
            '${pagatual+1} de $totalpaginas', //mostra a pagina que ta e quantas falta
             style: const TextStyle(color: Colors.grey),
          ),
        ],
      ));

    }

    Widget _conteudo(){
      return Expanded(child: PageView(
        controller: _pageController,
        physics: const NeverScrollableScrollPhysics(),//nao deixa o usuário deslizar com o dedo
        onPageChanged: (index) {
          setState(() => pagatual=index);//set stage serve pra atualizar a pagina e reconstuir e chamar o build nisso 
        },
        children: [
          _paginaNome(),
          _paginaIdade(),
          _paginatipoUsuario(),
          _paginaSexo(),
          _paginaAltura(),
          _paginaPescoco(),
          _paginaCintura(),
          _paginaObjetivo(),
          _paginaNivelatividadefisica(),
        ],
      ));
    }
     
     Widget _paginaNome(){
      return Padding(padding: const EdgeInsets.all(24),
      child: Column(//colum organiza tudo verticalmente
        crossAxisAlignment: CrossAxisAlignment.start,//alinha tudo na esquerda
        children: [//const serve sempre que um valor não muda ajuda na memória
          const Text('Qual o seu nome?', style: TextStyle(fontSize: 24,fontWeight: FontWeight.bold),),
          const SizedBox( height:24),
          TextField(
            onChanged: (v) {
              setState(() {//para reconstuir a tela e ver o valor atual e nao dar bug com a função de paginaprenchida
                _perfil.nome=v;
              });
            },//executa toda vez que o usuario digita 
            decoration: const InputDecoration(
              labelText: 'Nome',
              border:OutlineInputBorder(),
            ),
          )
        ],
      ),);
     }

     Widget _paginaIdade(){
      return Padding(
        padding: const EdgeInsets.all(24),//espacamento borda em todos os lados da pra fazer lado a lado
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Qual sua idade?',
              style: TextStyle(fontSize: 24,fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 24),
            TextField(
              keyboardType: TextInputType.number,//pra abrir o teclado  numerico
              onChanged: (v){
                setState(() {
                  _perfil.idade = int.tryParse(v) ?? 0;
                });

              },// se for algo invalido retorna null
              decoration: const InputDecoration(
                labelText: 'Idade',
                border: OutlineInputBorder(),
              ),
            ),
          ],
        ),
      );
     }

     Widget _paginatipoUsuario(){
      return Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Você é?',
              style: TextStyle(fontSize: 24,fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 24),

            _botaoSelecaoTipo('Usuário comum','usuario_comum'),
            const SizedBox(height: 12),
            _botaoSelecaoTipo('Profissional','profissional'),
            const SizedBox(height: 12),
             _botaoSelecaoTipo('Aluno','aluno'),
            const SizedBox(height: 12),
             
          ],
        ),
      );
     }

     Widget _paginaAltura(){
      return Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Qual sua altura?',
              style: TextStyle(fontSize: 24,fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 24),
            Center(
              child: Text(
                '${_perfil.altura == 0 ? 170 : _perfil.altura} cm',
                style: const TextStyle(fontSize: 32,fontWeight: FontWeight.bold),
              ),
            ),
            Slider(// é o que faz aquele negocio que vc desliza e mexe na altura 
              min: 120,
              max: 220,
              divisions: 100,//divide em 100 partes 
              value: (_perfil.altura == 0 ? 170 : _perfil.altura).toDouble(),//faz com que no inicio aparecça marcado 1.70 e tambem ta convertando de double pra int
              onChanged: (v){
                setState(() {//reconstoi os widgets filhos toda vez que muda com onchaged
                  _perfil.altura = v.toInt();
                });
              },
            ),
          ],
        ),
      );
     }

     Widget _paginaSexo(){
      return Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Qual seu sexo?',
              style: TextStyle(fontSize: 24,fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 24),

            _botaoSelecaosexo('Masculino','m'),
            const SizedBox(height: 12),
            _botaoSelecaosexo('Feminino','f'),
          ],
        ),
      );
     }

     Widget _paginaObjetivo(){
      return Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Qual seu objetivo?',
              style: TextStyle(fontSize: 24,fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 24),

            _botaoSelecaoObjetivo('💪 Ganhar Massa','bulking'),
            const SizedBox(height: 12),
            _botaoSelecaoObjetivo('🔥 Perder Gordura','cutting'),
            const SizedBox(height: 12),
            _botaoSelecaoObjetivo('⚖️ Manter Peso','manutenção'),
          ],
        ),
      );
     }

     Widget _paginaNivelatividadefisica(){
      return Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Qual seu nível de atividade?',
              style: TextStyle(fontSize: 24,fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 24),

            _botaoSelecaoAtividade('🛋 Sedentário','sedentario'),
            const SizedBox(height: 12),
            _botaoSelecaoAtividade('🚶 Leve','leve'),
            const SizedBox(height: 12),
            _botaoSelecaoAtividade('🏃 Moderado','moderado'),
            const SizedBox(height: 12),
            _botaoSelecaoAtividade('🏋️ Intenso','intenso'),
          ],
        ),
      );
     }

     Widget _paginaCintura(){
      return Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Circunferência da cintura',
              style: TextStyle(fontSize: 24,fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 24),
            Row(
              children: [
                Expanded(
                  child: TextField(
                    keyboardType: TextInputType.number,
                    onChanged: (v){
                      setState(() {
                        _perfil.cintura = double.tryParse(v) ?? 0.0;
                      });
                    },
                    decoration: const InputDecoration(
                      border: OutlineInputBorder(),
                      labelText: 'Cintura',
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                const Text('cm', style: TextStyle(fontSize: 18)),
              ],
            ),
          ],
        ),
      );
     }

     Widget _paginaPescoco(){
      return Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Circunferência do pescoço',
              style: TextStyle(fontSize: 24,fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 24),
            Row(
              children: [
                Expanded(
                  child: TextField(
                    keyboardType: TextInputType.number,
                    onChanged: (v){
                      setState(() {
                         _perfil.pescoco = double.tryParse(v) ?? 0.0;
                      });
                    },
                    decoration: const InputDecoration(
                      border: OutlineInputBorder(),
                      labelText: 'Pescoço',
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                const Text('cm', style: TextStyle(fontSize: 18)),
              ],
            ),
          ],
        ),
      );
     }

     Widget _botaoSelecaosexo(String textovisto, String textosalvo){
      final selecionado = _perfil.sexo == textosalvo; /**
      controi o widget como nada foi selecionado ainda faz a 
      comparação e da false pros dois a pessoa clica e ai recontroi 
      com o build e compara denovo com os dois 
      porque chama duas vezes e ai retorna true?  essa é a logica disso muito bom 
      basicamente verifica qual botão foi clicado*/
      
      return GestureDetector(//detextar arrastar segurar deslizar duplo clique e etc  se ele detecta o ontap ai que setstage é chamado(setstage)
        onTap: (){
          setState(() {
            _perfil.sexo = textosalvo;
          });
        },
        child: Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(12),
            color: selecionado ? Colors.blue : Colors.grey[200],
          ),
          child: Center(
            child: Text(
              textovisto,
              style: TextStyle(
                color: selecionado ? Colors.white : Colors.black,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
      );
     }

     Widget _botaoSelecaoTipo(String textovisto,String textosalvo ){
      final selecionado= _perfil.tipousuario==textosalvo;
      return GestureDetector(
        onTap: (){
          setState(() {
            _perfil.tipousuario = textosalvo;
          });
        },
        child: Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(12),
            color: selecionado ? Colors.blue : Colors.grey[200],
          ),
          child: Center(
            child: Text(
              textovisto,
              style: TextStyle(
                color: selecionado ? Colors.white : Colors.black,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
      );
     }

     Widget _botaoSelecaoObjetivo(String textovisto,String textosalvo){
      final selecionado = _perfil.objetivo == textosalvo;

      return GestureDetector(
        onTap: (){
          setState(() {
            _perfil.objetivo = textosalvo;
          });
        },
        child: Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(12),
            color: selecionado ? Colors.blue : Colors.grey[200],
          ),
          child: Center(
            child: Text(
              textovisto,
              style: TextStyle(
                color: selecionado ? Colors.white : Colors.black,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
      );
     }

     Widget _botaoSelecaoAtividade(String textovisto, String textosalvo){
      final selecionado = _perfil.nivelatividadefisica == textosalvo;

      return GestureDetector(
        onTap: (){
          setState(() {
            _perfil.nivelatividadefisica = textosalvo;
          });
        },
        child: Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(12),
            color: selecionado ? Colors.blue : Colors.grey[200],
          ),
          child: Center(
            child: Text(
              textovisto,
              style: TextStyle(
                color: selecionado ? Colors.white : Colors.black,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
      );
     }

int _contadorPaginasPreenchidas(){
  int contador = 0;

  if(_perfil.nome.isNotEmpty) contador++;//empty=vazio se nao está vazio
  if(_perfil.idade > 0) contador++;
  if(_perfil.tipousuario.isNotEmpty) contador++;
  if(_perfil.sexo.isNotEmpty) contador++;
  if(_perfil.altura > 0) contador++;
  if(_perfil.pescoco > 0) contador++;
  if(_perfil.cintura > 0) contador++;
  if(_perfil.objetivo.isNotEmpty) contador++;
  if(_perfil.nivelatividadefisica.isNotEmpty) contador++;

  return contador;
}

bool _paginaAtualPreenchida() {
  switch (pagatual) {
    case 0:
      return _perfil.nome.isNotEmpty;

    case 1:
      return _perfil.idade > 0;

    case 2:
      return _perfil.tipousuario.isNotEmpty;

    case 3:
      return _perfil.sexo.isNotEmpty;

    case 4:
      return _perfil.altura > 0;

    case 5:
      return _perfil.pescoco > 0;

    case 6:
      return _perfil.cintura > 0;

    case 7:
      return _perfil.objetivo.isNotEmpty;

    case 8:
      return _perfil.nivelatividadefisica.isNotEmpty;

    default:
      return false;
  }
}
@override
Widget build(BuildContext context) {
  return Scaffold(
    body: SafeArea(
      child: Column(
        children: [
          const SizedBox(height: 20),

          _barraProgresso(),

          const SizedBox(height: 20),

          _conteudo(),

          const SizedBox(height: 20),

          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [

                if (pagatual > 0)
                  TextButton(
                    onPressed: paginaAnterior,
                    child: const Text('Voltar'),
                  ),

                 if (_contadorPaginasPreenchidas() > 3)
                 TextButton(onPressed:finalizar, child: const Text('Finalizar'),),
                 TextButton(onPressed:_paginaAtualPreenchida()?proximaPagina : null, child: const Text('Proximo')),

              ],
            ),
          ),

          const SizedBox(height: 20),
        ],
      ),
    ),
  );
} 
}
