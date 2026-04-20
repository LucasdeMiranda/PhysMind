class Alimento {
  int id;
  String nome;
  String tipo;
  double calorias;
  double? proteinas;
  double? carboidratos;
  double? fibra;
  double? gordura;
  double? sodio;
  double? colesterol;
  double? gordurasaturada;

  Alimento({
    required this.id,
    required this.nome,
    required this.tipo,
    required this.calorias,
    this.proteinas,
    this.carboidratos,
    this.fibra,
    this.gordura,
    this.sodio,
    this.colesterol,
    this.gordurasaturada,
  });

  factory Alimento.fromJson(Map<String, dynamic> json) {
    return Alimento(
      id: json['id'],
      nome: json['nome'],
      tipo: json['tipo'],
      calorias: (json['calorias'] as num).toDouble(),

      proteinas: json['proteinas'] != null
          ? (json['proteinas'] as num).toDouble()
          : null,

      carboidratos: json['carboidratos'] != null
          ? (json['carboidratos'] as num).toDouble()
          : null,

      fibra: json['fibra'] != null
          ? (json['fibra'] as num).toDouble()
          : null,

      gordura: json['gordura'] != null
          ? (json['gordura'] as num).toDouble()
          : null,

      sodio: json['sodio'] != null
          ? (json['sodio'] as num).toDouble()
          : null,

      colesterol: json['colesterol'] != null
          ? (json['colesterol'] as num).toDouble()
          : null,

      gordurasaturada: json['gordurasaturada'] != null
          ? (json['gordurasaturada'] as num).toDouble()
          : null,
    );
  }
}