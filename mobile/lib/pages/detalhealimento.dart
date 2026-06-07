import 'package:flutter/material.dart';
import '../models/alimento.dart';
import 'package:fl_chart/fl_chart.dart'; //biblioteca externa adicionada no pubspec.yaml
import '../models/consumoalimento.dart';

class DetalheAlimento extends StatefulWidget {
  final Alimento alimento;

  const DetalheAlimento({required this.alimento});

  @override
  State<DetalheAlimento> createState() => _DetalheAlimentoState();
}

class _DetalheAlimentoState extends State<DetalheAlimento> {
  int quantidade = 100;

  final TextEditingController _quantidadeController = TextEditingController(
    text: "100",
  );

  @override
  Widget build(BuildContext context) {
    final calorias = (widget.alimento.calorias ?? 0) * quantidade / 100;

    final carbo = (widget.alimento.carboidratos ?? 0) * quantidade / 100;

    final prote = (widget.alimento.proteinas ?? 0) * quantidade / 100;

    final gordura = (widget.alimento.gordura ?? 0) * quantidade / 100;

    return Scaffold(
      appBar: AppBar(title: Text(widget.alimento.nome)),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const SizedBox(height: 20),

            SizedBox(
              height: 200,
              child: PieChart(
                PieChartData(
                  sections: [
                    PieChartSectionData(
                      value: widget.alimento.carboidratos ?? 0,
                      color: Colors.yellow,
                      title: "Carb",
                    ),
                    PieChartSectionData(
                      value: widget.alimento.proteinas ?? 0,
                      color: Colors.green,
                      title: "Prot",
                    ),
                    PieChartSectionData(
                      value: widget.alimento.gordura ?? 0,
                      color: const Color.fromARGB(255, 25, 28, 186),
                      title: "Gord",
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 20),

            TextField(
              controller: _quantidadeController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: "Quantidade (g)",
                border: OutlineInputBorder(),
              ),
              onChanged: (value) {
                setState(() {
                  quantidade = int.tryParse(value) ?? 100;
                });
              },
            ),

            const SizedBox(height: 20),

            //informações do alimento
            Text(
              "${calorias.toStringAsFixed(1)} kcal",
              style: const TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 10),

            Text("Carb: ${carbo.toStringAsFixed(1)} g"),
            Text("Prot: ${prote.toStringAsFixed(1)} g"),
            Text("Gord: ${gordura.toStringAsFixed(1)} g"),

            const SizedBox(height: 8),

            Text(
              "Baseado em $quantidade g",
              style: TextStyle(color: Colors.grey[600]),
            ),

            const Spacer(),

            ElevatedButton(
              onPressed: () {
                Navigator.pop(
                  context,
                  ConsumoAlimento(
                    id: widget.alimento.id,
                    nome: widget.alimento.nome,
                    quantidade: quantidade,
                    calorias: calorias,
                    proteinas: prote,
                    carboidratos: carbo,
                    gordura: gordura,
                  ),
                );
              },
              child: const Text("Adicionar à refeição"),
            ),
          ],
        ),
      ),
    );
  }
}