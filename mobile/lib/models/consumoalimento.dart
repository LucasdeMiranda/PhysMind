import '../models/alimento.dart';

class ConsumoAlimento {
  int id, quantidade;

  int? alimentoBaseId;
  int? alimentoCustomizadoId;
  int ?refeicaoId;

  String nome;

  double calorias, proteinas, carboidratos, gordura;

  ConsumoAlimento({
    required this.id,
    required this.quantidade,
    this.alimentoBaseId,
    this.refeicaoId,
    this.alimentoCustomizadoId,
    required this.nome,
    required this.calorias,
    required this.proteinas,
    required this.carboidratos,
    required this.gordura,
  });

  factory ConsumoAlimento.fromJson(Map<String, dynamic> json) {
    return ConsumoAlimento(
      id: json['id'],
      alimentoBaseId: json['alimentobase'],
      refeicaoId: json['refeicao'],
      alimentoCustomizadoId: json['alimentocustomizado'],
      nome: json['nome'],
      quantidade: json['quantidade'],
      calorias: (json['calorias'] ?? 0).toDouble(),
      proteinas: (json['proteinas'] ?? 0).toDouble(),
      carboidratos: (json['carboidratos'] ?? 0).toDouble(),
      gordura: (json['gordura'] ?? 0).toDouble(),
    );
  }

  factory ConsumoAlimento.fromAlimento(Alimento a) {
    return ConsumoAlimento(
      id: 0, // ainda não existe consumo salvo
      alimentoBaseId: a.id,
      nome: a.nome,
      quantidade: 100,
      calorias: a.calorias ?? 0,
      carboidratos: a.carboidratos ?? 0,
      proteinas: a.proteinas ?? 0,
      gordura: a.gordura ?? 0,
    );
  }
  Map<String, dynamic> toJsonCriacao() {
  return {
    'refeicao': refeicaoId,
    'alimentobase': alimentoBaseId,
    'alimentocustomizado': alimentoCustomizadoId,
    'quantidade': quantidade,
  };
}
}