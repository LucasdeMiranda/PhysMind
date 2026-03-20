import 'package:flutter/material.dart';
import '../services/autenticacao_service.dart';
import 'homeusuariocomum.dart';
import '../pages/informacoesbasicas.dart';
import '../pages/homeprofissional.dart';

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
              try{
              final autenticacao= await _autenticacaoService.cadastrar(email.text, senha.text);
              if (autenticacao.status=='novo'){
                 Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) =>Informacoesbasicas()),);//perfil novo precisa cadastrar
              }
              else if (autenticacao.status=='existente' &&autenticacao.tipoUsuario=='aluno' || autenticacao.status=='existente' &&autenticacao.tipoUsuario=='usuario_comum'){
                 Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => Homeusuariocomum()),);//usuário comum 
              }
              else if (autenticacao.status=='existente' &&autenticacao.tipoUsuario=='profissional'){
                 Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) =>Homeprofissional()),);//profissional 
              }
              }
               catch(e){
                ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.toString())),);
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
