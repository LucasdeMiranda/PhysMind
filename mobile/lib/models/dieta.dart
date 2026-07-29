class Dieta {
  String nome;
  int calorias;
  double proteinas;
  double carboidratos;
  double gordura;

  Dieta({
    required this.nome,
    required this.calorias,
    required this.proteinas,
    required this.carboidratos,
    required this.gordura,
  });

  factory Dieta.fromJson(Map<String, dynamic> json) {
    return Dieta(
      nome: json['nome'] ?? '',
      calorias: json['calorias'] ?? 0,
      proteinas: (json['proteinas'] ?? 0).toDouble(),
      carboidratos: (json['carboidratos'] ?? 0).toDouble(),
      gordura: (json['gordura'] ?? 0).toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'calorias': calorias,
      'proteinas': proteinas,
      'carboidratos': carboidratos,
      'gordura': gordura,
    };
  }
}