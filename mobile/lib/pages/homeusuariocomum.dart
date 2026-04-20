import 'package:flutter/material.dart';
import 'package:mobile/models/dieta.dart';
import '../services/perfil_service.dart';
import '../services/dieta_service.dart';
import '../services/refeicao_service.dart';
import '../services/alimento_service.dart';

class Homeusuariocomum extends StatefulWidget {
  const Homeusuariocomum({super.key});

  @override
  State<Homeusuariocomum> createState() => _HomeusuariocomumState();
}

class _HomeusuariocomumState extends State<Homeusuariocomum> {
  DietaService _dietaService = DietaService();
  Dieta ? dieta;
  int consumido=0;
  Future<void> carregarDieta() async {
    final resposta= await _dietaService.buscarDietaAtiva();
    setState(() {
      dieta=resposta;
    });
  }

  @override
  void initState() {
    super.initState();
    carregarDieta();
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
          Text("$consumido / ${dieta?.calorias ?? 0}")
          
          
        ],
      ),
    );
  }

  Widget _Refeicao(BuildContext context){
    final cor=Theme.of(context).colorScheme;
    return Container(
      
    )
    
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold();
  }
}