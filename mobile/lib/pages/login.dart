import 'package:flutter/material.dart';
import '../services/autenticacao_service.dart';


class Login extends StatelessWidget {
  Login({super.key});
  final TextEditingController email = TextEditingController();
  final TextEditingController senha = TextEditingController();
  final AutenticacaoService  _autenticacaoService = AutenticacaoService();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Login', style: Theme.of(context).textTheme.headlineMedium),
            const SizedBox(height: 24),
            TextField(
              controller: email,
              keyboardType: TextInputType.emailAddress,// cria a caixa pra poder digitar
              decoration: const InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: senha,
              obscureText: true,//pra nao conseguir ver a senha
              decoration: const InputDecoration(
                labelText: 'Senha',
                border: OutlineInputBorder(),
              ),
            ),
           const SizedBox(height: 24),
           SizedBox(
            width:double.infinity,
            height: 48,
            child: ElevatedButton(onPressed:() async{
              print('BOTÃO CLICADO');//debug com print
              final erro= await _autenticacaoService.cadastrar(email.text, senha.text);
              if (erro==null){
                ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Usuario cadastrado com sucesso')));
                //Navigator.pop(context);
              }
              else {
                 ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(erro)));
              }

            },
            child: const Text('Entrar'),),
           ),
          ],
        ),
      ),
    );
  }
}
