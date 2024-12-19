import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:frontend/widgets/counter_box.dart';
import 'package:frontend/widgets/text_box.dart';
import 'package:frontend/widgets/date_box.dart';
import 'package:frontend/widgets/stars_rating.dart';
import 'package:google_fonts/google_fonts.dart';
import "package:frontend/services/api.dart";

void main() {
  runApp(MyApp());
}

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

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  HomeScreenState createState() => HomeScreenState();
}

//---------- HOME SCREEN ----------//
class HomeScreenState extends State<HomeScreen> {
  final TextEditingController startDate = TextEditingController();
  final TextEditingController endDate = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  final _controller = TextEditingController();

  final ApiService apiService = ApiService(
    baseUrl: 'http://127.0.0.1:5000',
    proxyUrl: 'http://198.44.255.5:80',
  );

  int _estaticCounter = 0;
  int _sidecarCounter = 0;
  int _reelCounter = 0;
  int _stars = 0;
  List<dynamic> _capturedPosts = [];
  bool _isLoading = false;

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Scaffold(
        backgroundColor: const Color(0xFFE2E2E2),
        appBar: PreferredSize(
          preferredSize: const Size.fromHeight(90),
          child: Container(
            color: const Color(0xFF0F4655),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Image.asset('assets/images/logo_drfisiologia.png'),
                Image.asset('assets/images/lupa_drfisiologia.png'),
              ],
            ),
          ),
        ),

        // BODY //
        body: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 48.0),
          child: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [

                // CLIENTE //
                const SizedBox(height: 36),
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

                // DATAS INICIAL E FINAL //
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

                // BUSCAR POSTS //
                const SizedBox(height: 12),
                ElevatedButton(
                  onPressed: _isLoading
                    ? null
                    : () {
                      if (_formKey.currentState?.validate() ?? false) {
                        fetchPosts();
                      }
                    },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF0F4655),
                    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                  ),
                  child: _isLoading
                    ? const CircularProgressIndicator(color: Colors.white)
                    : const Text('Buscar Posts',
                      style: TextStyle(color: Colors.white, fontSize: 18),
                    ),
                ),

                // COUNTER BOXES + CATEGORIAS //
                const SizedBox(height: 12),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    CounterBox(label: 'Educação em saúde:', counter: _estaticCounter),
                    const SizedBox(width: 18),
                    CounterBox(label: 'Data comemorativa:', counter: _sidecarCounter),
                    const SizedBox(width: 18),
                    CounterBox(label: 'Publicidade:', counter: _reelCounter),
                  ],
                ),

                // COUNTER BOXES + FORMATOS //
                const SizedBox(height: 24),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    CounterBox(label: 'Estático:', counter: _estaticCounter),
                    const SizedBox(width: 18),
                    CounterBox(label: 'Carrossel:', counter: _sidecarCounter),
                    const SizedBox(width: 18),
                    CounterBox(label: 'Reels:', counter: _reelCounter),
                  ],
                ),

                // CLASSIFICAÇÃO POR ESTRELAS //
                const SizedBox(height: 24),
                StarsRating(
                  labelText: 'Classificação por estrelas:',
                  starSpacing: 6,
                  index: _stars,
                ),

                // POSTS CAPTURADOS //
                const SizedBox(height: 48),
                Center(
                  child: Text('Posts Capturados',
                    style: TextStyle(
                      fontFamily: GoogleFonts.workSans().fontFamily,
                      fontWeight: FontWeight.bold,
                      fontSize: 30,
                      letterSpacing: 0.5,
                      color: const Color(0xFF0F4655),
                      decoration: TextDecoration.underline,
                      decorationColor: const Color(0xFF0F4655),
                      decorationThickness: 1,
                    ),
                  ),
                ),

            // GRID DE POSTS CAPTURADOS //
            const SizedBox(height: 36),
            _capturedPosts.isNotEmpty
                ? GridView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: MediaQuery.of(context).size.width > 1200 ? 6 : 3,
                      crossAxisSpacing: 18,
                      mainAxisSpacing: 18,
                    ),
                    itemCount: _capturedPosts.length,
                    itemBuilder: (context, index) {
                      return Container(
                        decoration: BoxDecoration(
                          color: const Color(0xFF0F4655),
                          borderRadius: BorderRadius.circular(6),
                          image: DecorationImage(
                            image: NetworkImage(_capturedPosts[index]['imageUrl'] ?? ''),
                            fit: BoxFit.cover,
                          ),
                        ),
                      );
                    },
                  )
                : const Text('Nenhum post capturado.'),
              ],
            ),
          ),
        ),
      ),
    );
  }

  // FUNÇÃO PARA BUSCAR OS POSTS //
  Future<void> fetchPosts() async {
    setState(() => _isLoading = true);
    try {
      final data = await apiService.fetchPosts(
        username: _controller.text,
        dataInicial: startDate.text,
        dataFinal: endDate.text,
      );

      setState(() {
        _estaticCounter = data['estatico'] ?? 0;
        _sidecarCounter = data['carrossel'] ?? 0;
        _reelCounter = data['reel'] ?? 0;
        _stars = data['estrela'] ?? 0;
        _capturedPosts = data['posts'] ?? [];
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Erro ao buscar posts: $e")),
      );
    } finally {
      setState(() => _isLoading = false);
    }
  }

  void selectDate(BuildContext context, TextEditingController controller) async {
    final pickedDate = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime(2000),
      lastDate: DateTime.now(),
    );
    if (pickedDate != null) {
      controller.text = '${pickedDate.day}/${pickedDate.month}/${pickedDate.year}';
    }
  }
}
