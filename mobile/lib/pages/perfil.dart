import 'package:flutter/material.dart';
import 'package:mobile/models/dieta.dart';
import 'package:mobile/models/alimento.dart';
import 'package:mobile/models/perfil.dart';
import 'package:mobile/models/refeicao.dart';
import 'package:mobile/models/consumoalimento.dart';
import '../services/perfil_service.dart';
import '../services/dieta_service.dart';
import '../services/refeicao_service.dart';
import '../services/alimento_service.dart';
import '../pages/detalhealimento.dart';

class PerfilPage extends StatefulWidget {
  const PerfilPage({super.key});

  @override
  State<PerfilPage> createState() => _PerfilState();
}

// perfil state recebe a herança de state e coloca e monta um objeteo perfil
class _PerfilState extends State<PerfilPage> {
  PerfilService _perfilService = PerfilService();
  Perfil? perfil;

  @override
  initState() {
    super.initState();
    carregarPerfil();
  }

  Future<void> carregarPerfil() async {
    final resposta = await _perfilService.buscarPerfil();
    setState(() {
      perfil = resposta;
    });
  }

  Widget InformacoesBasicas() {
    return ExpansionTile(
      title: Text("Perfil"),
      children: [
        //! garante que o perfil nao é nulo se cair aqui porque já foi esperado verificar se ele existia mesmo
        TextFormField(initialValue: perfil!.nome),
        
        TextFormField(initialValue: perfil!.idade.toString()),
        TextFormField(initialValue: perfil!.sexo),

        Row(
          //botao de deletar refeições do lado de cada refeição
          mainAxisSize: MainAxisSize.min,
          children: [
            IconButton(
              icon: const Icon(Icons.edit),
              onPressed: () async {
                await _perfilService.atualizarPerfil(perfil.toJson());
                await carregarPerfil();
              },
            ),
          ],
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    if (perfil == null) {
      return const Center(child: CircularProgressIndicator());
    }

    return Scaffold(body: InformacoesBasicas());
  }
}
