// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables
import 'package:flutter/material.dart';
import 'package:frontend/widgets/counter_box.dart';
import 'package:frontend/widgets/text_box.dart';
import 'package:frontend/widgets/date_box.dart';
import 'package:frontend/widgets/stars_rating.dart';
import 'package:google_fonts/google_fonts.dart';
import "package:frontend/services/api_service.dart";

void main() {
  runApp(MyApp());
}

// CLASS MY-APP
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Análise de Posts',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        fontFamily: GoogleFonts.workSans().fontFamily,
      ),
      home: const HomeScreen(),
    );
  }
}

// CLASS HOME-SCREEN
class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  HomeScreenState createState() => HomeScreenState();
}

// CLASS HOME-SCREEN-STATE
class HomeScreenState extends State<HomeScreen> {
  final TextEditingController startDate = TextEditingController();
  final TextEditingController endDate = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  final _controller = TextEditingController();
  final ApiService apiService = ApiService(baseUrl: 'http://198.44.255.5:80');

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Scaffold(
        backgroundColor: Color(0xFFE2E2E2),

        // HEADER
        appBar: PreferredSize(
          preferredSize: Size.fromHeight(90), 
          child: Container(
            color: Color(0xFF0F4655),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Image.asset('assets/images/logo_drfisiologia.png'),
                Image.asset('assets/images/lupa_drfisiologia.png'),
              ],
            ),
          ),
        ),
        
        // BODY
        body: Padding(
          padding: const EdgeInsets.only(top: 0, bottom: 48.0, right: 24.0, left: 24.0),
          child: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [

                // CLIENTE
                SizedBox(height: 36),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    CustomTextBox(
                      labelText: 'Nome ou Link do Perfil:', 
                      hintText: '', 
                      height: 60, 
                      width: 400,
                      controller: _controller,
                      formKey: _formKey,
                    ),
                  ],
                ),

                // DATAS INICIAL E FINAL
                const SizedBox(height: 12),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    IconButton(
                      onPressed: () => selectDate(context, startDate), 
                      icon: const Icon(Icons.today, size: 32, color: Color(0xFF0F4655)),
                    ),

                    CustomDateBox(
                      labelText: 'Data Inicial:', 
                      hintText: 'DD/MM/AAAA', 
                      height: 60, 
                      width: 194,
                      controller: startDate,
                      onClickIcon: () => selectDate(context, startDate),
                    ),

                    const SizedBox(width: 12),
                    CustomDateBox(
                      labelText: 'Data Final:', 
                      hintText: 'DD/MM/AAAA', 
                      height: 60, 
                      width: 194,
                      controller: endDate,
                      onClickIcon: () => selectDate(context, endDate),
                    ),

                    IconButton(
                      onPressed: () => selectDate(context, endDate),
                      icon: const Icon(Icons.event, size: 32, color: Color(0xFF0F4655)),
                    ),
                  ],
                ),

                // BUSCAR POSTS
                SizedBox(height: 12),
                ElevatedButton(
                  onPressed: fetchPosts, 
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Color(0xFF0F4655),
                    padding: EdgeInsets.symmetric(horizontal: 24, vertical: 12)),
                  child: 
                  Text('Buscar Posts',
                    style: TextStyle(color: Colors.white, fontSize: 18),
                  ),
                ),
                
                // COUNTER BOXES + CATEGORIAS
                const SizedBox(height: 12),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    CounterBox(label: 'Educação em saúde:', counter: _estaticCounter),
                    SizedBox(width: 18),
                    CounterBox(label: 'Data comemorativa:', counter: _sidecarCounter),
                    SizedBox(width: 18),
                    CounterBox(label:'Publicidade:', counter: _reelCounter),
                  ],
                ),

                // COUNTER BOXES + FORMATOS
                const SizedBox(height: 24),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    CounterBox(label: 'Estático:', counter: _estaticCounter),
                    SizedBox(width: 24),
                    CounterBox(label: 'Carrossel:', counter: _sidecarCounter),
                    SizedBox(width: 24),
                    CounterBox(label: 'Estático:', counter: _reelCounter),
                  ],
                ),

                // CLASSIFICAÇÃO POR ESTRELAS
                const SizedBox(height: 24),
                StarsRating(labelText: 'Classificação por estrelas:', starSpacing: 6, index: _stars),

                // POSTS CAPTURADOS
                const SizedBox(height: 48),
                Center(
                  child: Text("Posts Capturados",
                    style: TextStyle(
                      fontFamily: GoogleFonts.workSans().fontFamily,
                      fontWeight: FontWeight.bold,
                      fontSize: 30,
                      letterSpacing: 0.5,
                      color: Color(0xFF0F4655),
                      decoration: TextDecoration.underline,
                      decorationColor: Color(0xFF0F4655),
                      decorationThickness: 1,
                    ),
                  ),
                ),

                // GRID DE POSTS CAPTURADOS
                /*const SizedBox(height: 36),
                GridView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: MediaQuery.of(context).size.width > 1200 ? 6 : 3,
                    crossAxisSpacing: 18,
                    mainAxisSpacing: 18,
                  ),
                  itemCount: 6,
                  itemBuilder: (context, index) {
                    return Container(
                      height: 600,
                      width: 200,
                      decoration: BoxDecoration(
                        color: (Color(0xFF0F4655)),
                        borderRadius: BorderRadius.circular(6),
                        image: DecorationImage(
                          image: NetworkImage(_capturedPosts[index]['imageUrl']),
                          fit: BoxFit.cover,
                        )
                      ),
                    );
                  },
                ),*/
              ],
            ),
          ),
        ),
      ),
    );
  }

  // FUNÇÃO PARA BUSCAR OS POSTS
  int _estaticCounter = 0;
  int _sidecarCounter = 0;
  int _reelCounter = 0;
  int _stars = 0;
  List<dynamic> _capturedPosts = [];

  Future<void> fetchPosts() async {
    try {
      final data = await apiService.fetchPosts(
        username: _controller.text,
        dataInicial: startDate.text,
        dataFinal: endDate.text,
      );

      setState(() {
        //_healthEducationCounter
        //_celebrationCounter
        //_publicityCounter

        _estaticCounter = data['estatico'];
        _sidecarCounter = data['carrossel'];
        _reelCounter = data['reel'];

        _stars = data['estrela'];
        _capturedPosts = data['posts'];
      });
    } catch (e) {
      print("Erro ao buscar posts: $e");
    }
  }
}

