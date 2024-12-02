import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class CounterBox extends StatelessWidget {
  final String label;
  final int counter;

  const CounterBox({
    super.key,
    required this.label,
    required this.counter,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Text(
          label,
          style: GoogleFonts.workSans(
            fontSize: 18,
            fontWeight: FontWeight.w600,
            letterSpacing: .5,
            color: Color(0xFF0F4655),
          ),
        ),
        const SizedBox(width: 8),
        Container(
          padding: const EdgeInsets.symmetric(vertical: 3, horizontal: 18),
          decoration: BoxDecoration(
            color: Colors.transparent,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: (Color(0xFF0F4655))),
          ),
          child: Text(
            counter.toString().padLeft(3, '0'),
            style: const TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 18,
            ),
          ),
        ),
      ],
    );
  }
}