// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables
import 'package:flutter/material.dart';
import 'package:frontend/widgets/check_box.dart';
import 'package:frontend/widgets/counter_box.dart';
import 'package:frontend/widgets/text_box.dart';
import 'package:frontend/widgets/date_box.dart';
import 'package:frontend/widgets/stars_rating.dart';
import 'package:google_fonts/google_fonts.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Instagram Scraper',
      home: HomeScreen(),
    );
  }
}

class HomeScreen extends StatelessWidget {
  HomeScreen({super.key});
  final TextEditingController startDate = TextEditingController();
  final TextEditingController endDate = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  final _controller = TextEditingController();

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

                // COUNTER BOXES + CATEGORIAS
                const SizedBox(height: 24),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    CounterBox(label: 'Educação em saúde:', counter: 000),
                    SizedBox(width: 18),
                    CounterBox(label: 'Data comemorativa:', counter: 000),
                    SizedBox(width: 18),
                    CounterBox(label:'Publicidade:', counter: 000),
                  ],
                ),

                // CHECK BOXES + FORMATOS
                const SizedBox(height: 24),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    CheckBox(label: 'Reels', enable: true),
                    const SizedBox(width: 24),
                    CheckBox(label: 'Carrossel', enable: false),
                    const SizedBox(width: 24),
                    CheckBox(label: 'Estático', enable: true),
                  ],
                ),

                // CLASSIFICAÇÃO POR ESTRELAS
                const SizedBox(height: 24),
                StarsRating(labelText: 'Classificação por estrelas:', index: 2, starSpacing: 6),

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
                const SizedBox(height: 36),
                GridView.builder(
                  shrinkWrap: true, // Ajusta o tamanho da lista para ocupar apenas o espaço necessário, sem expandir
                  physics: const NeverScrollableScrollPhysics(),
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 6, // Define o número de colunas (ou linhas) em uma grade
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
                      ),
                    );
                  },
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}