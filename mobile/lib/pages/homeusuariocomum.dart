import 'package:flutter/material.dart';
import 'package:mobile/models/dieta.dart';
import 'package:mobile/models/alimento.dart';
import 'package:mobile/models/refeicao.dart';
import 'package:mobile/models/consumoalimento.dart';
import '../services/perfil_service.dart';
import '../services/dieta_service.dart';
import '../services/refeicao_service.dart';
import '../services/alimento_service.dart';
import '../pages/detalhealimento.dart';

class Homeusuariocomum extends StatefulWidget {
  //dois tipos de windget stateful que muda com o tempo e stateless que não muda
  const Homeusuariocomum({super.key});

  @override
  State<Homeusuariocomum> createState() => _HomeusuariocomumState(); //basicamente quando mudar usa o state e acessa a logica de homeusuarioestate
}

class _HomeusuariocomumState extends State<Homeusuariocomum> {
  //home usuario state recebe herança de state
  DietaService _dietaService = DietaService();
  Dieta? dieta;
  RefeicaoService _refeicaoService = RefeicaoService();
  AlimentoService _alimentoService = AlimentoService();
  Refeicao? refeicao;
  bool criandoRefeicao = false;
  final TextEditingController nomeController = TextEditingController();

  int consumido = 0;
  Future<void> carregarDieta() async {
    final resposta = await _dietaService.buscarDietaAtiva();
    setState(() {
      dieta = resposta;
    });
  }

  List<Refeicao> refeicoes = [];
  Future<void> carregarRefeicoes() async {
    final resposta = await _refeicaoService.buscarRefeicao();
    setState(() {
      refeicoes = resposta;
    });
  }

  @override
  void initState() {
    super.initState();
    carregarDieta();
    carregarRefeicoes();
  }

  Widget _Meta(BuildContext context) {
    final cor = Theme.of(context).colorScheme;
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: cor.surface,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            "Calorias",
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          Text("$consumido / ${dieta?.calorias ?? 0}"),
        ],
      ),
    );
  }

  Widget _AdicionarRefeicao() {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color.fromARGB(255, 139, 138, 138),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        children: [
          Row(
            children: [
              const Text("Adicionar Refeição"),
              IconButton(
                icon: const Icon(Icons.add),
                onPressed: () {
                  setState(() {
                    criandoRefeicao = !criandoRefeicao;
                  });
                },
              ),
            ],
          ),
          if (criandoRefeicao) ...[
            const SizedBox(height: 12),
            TextField(
              controller: nomeController,
              decoration: InputDecoration(
                hintText: "Nome da refeição",
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
            ),
               const SizedBox(height: 12),
              ElevatedButton(
                onPressed: () async {
                  final nome = nomeController.text;
                  if (nome.isNotEmpty) {
                    final novaRefeicao = await _refeicaoService.criaRefeicao({
                      'nome': nome,
                    });
                    setState(() {
                      refeicoes.add(novaRefeicao);
                      criandoRefeicao = false;
                      nomeController.clear();
                    });
                  }
                },
                child: const Text("Criar Refeição"),
            ),
          ],
        ],
      ),
    );
  }

  // a partir daqui tem que ver
  double totalCarb(Refeicao ref) {
    return ref.itens.fold(0, (soma, item) => soma + (item.carboidratos ?? 0));
  }

  double totalProt(Refeicao ref) {
    return ref.itens.fold(0, (soma, item) => soma + (item.proteinas ?? 0));
  }

  double totalGord(Refeicao ref) {
    return ref.itens.fold(0, (soma, item) => soma + (item.gordura ?? 0));
  }

  Widget _Refeicao({
    required int id,
    required String titulo,
    required double carb,
    required double prot,
    required double gord,
    required List<ConsumoAlimento> alimentos,
  }) {
    bool expandido = false;
    List<Alimento> resultados = [];
    return StatefulBuilder(
      builder: (context, setLocalState) {
        //setlocal redesenha apenas aquele pedaço da tela muito util
        return Container(
          margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: const Color.fromARGB(255, 139, 138, 138),
            borderRadius: BorderRadius.circular(16),
          ),
          child: Column(
            children: [
              GestureDetector(
                //captura o toque
                onTap: () {
                  setLocalState(() {
                    expandido = !expandido;
                  });
                },

                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(titulo, style: const TextStyle(fontSize: 16)),
                        Text("Carb: $carb  Prot: $prot  Gor: $gord"),
                      ],
                    ),
                    const Icon(Icons.expand_more),
                  ],
                ),
              ),
              if (expandido) ...[
                const SizedBox(height: 12),
                Column(
                  children: [
                    TextField(
                      onChanged: (value) async {
                        final resultado = await _alimentoService
                            .buscarAlimentos(value);
                        setLocalState(() {
                          resultados = resultado;
                        });
                      },
                      decoration: InputDecoration(
                        hintText: "Buscar alimento...",
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                    ),

                    const SizedBox(height: 10),
                    //exibe os resultados mas a pessoa não consegue esclorar como aquelas listas mesmo auto complete
                    ListView.builder(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      itemCount: resultados.length,
                      itemBuilder: (context, index) {
                        final a = resultados[index];

                        return ListTile(
                          title: Text(a.nome),
                          onTap: () async {
                            final ConsumoAlimento? resultado =
                                await Navigator.push<ConsumoAlimento>(
                                  context,
                                  MaterialPageRoute(
                                    builder: (context) =>
                                        DetalheAlimento(alimento: a),
                                  ),
                                );
                            if (resultado != null) {
                              resultado.refeicaoId = id;
                               await _refeicaoService.adicionarAlimento(resultado);
                              await carregarRefeicoes();
                            }
                          },
                        );
                      },
                    ),

                    const SizedBox(height: 10),

                    //ALIMENTOS DA REFEIÇÃO
                    Column(
                      children: alimentos.map<Widget>((a) {
                        return ListTile(
                          title: Text(a.nome),
                          subtitle: Text(
                            "${a.quantidade}g • ${a.calorias} kcal\nC:${a.carboidratos} P:${a.proteinas} G:${a.gordura}",
                          ),
                        );
                      }).toList(),
                    ),
                  ],
                ),
              ],
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          _Meta(context),
          _AdicionarRefeicao(),

          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  "Refeições",
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),

                IconButton(
                  icon: const Icon(Icons.add),
                  onPressed: () {
                    // chamar API para criar refeição
                  },
                ),
              ],
            ),
          ),

          Expanded(
            child: ListView.builder(
              itemCount: refeicoes.length,
              itemBuilder: (context, index) {
                final ref = refeicoes[index];

                return _Refeicao(
                  id: ref.id,
                  titulo: ref.nome,
                  carb: totalCarb(ref),
                  prot: totalProt(ref),
                  gord: totalGord(ref),
                  alimentos: ref.itens,
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
