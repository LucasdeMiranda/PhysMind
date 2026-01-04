import 'package:google_sign_in/google_sign_in.dart';

class Googlelogin{
  final GoogleSignIn _googleSignIn=GoogleSignIn();//_ significa que so pode ser usado dentro desse arquivo
  Future<GoogleSignInAccount?>  signIn() async{
    return await _googleSignIn.signIn();
  }
}