import 'package:mobile/models/consumoalimento.dart';

class Refeicao{
  int id;
  String nome;
  List <ConsumoAlimento> itens;
   Refeicao({
    required this.id,required this.nome, required this.itens
   });
   factory Refeicao.fromJson(Map<String, dynamic> json){
    return Refeicao(
      id: json['id'],
      nome: json['nome'],
      itens: (json['itens'] as List).map((item)=>ConsumoAlimento.fromJson(item)).toList()
    );
   }
}