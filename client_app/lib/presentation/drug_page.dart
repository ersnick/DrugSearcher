import 'package:flutter/material.dart';
import '../service/drug_service.dart';

class DrugPage extends StatefulWidget {
  final String medicineName;

  const DrugPage({super.key, required this.medicineName});

  @override
  State<DrugPage> createState() => _DrugPageState();
}

class _DrugPageState extends State<DrugPage> {
  Map<String, dynamic>? drugData;

  @override
  void initState() {
    super.initState();
    _fetchDrugInfo();
  }

  Future<void> _fetchDrugInfo() async {
    final data = await getDrugInfo(widget.medicineName);
    setState(() {
      drugData = data;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.medicineName),
        backgroundColor: Theme.of(context).colorScheme.primary,
      ),
      body: drugData == null
          ? Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
        child: Column(
          children: [
            ExpansionTile(
              title: Text("Описание"),
              children: [
                ListTile(title: Text(drugData?['description'] ?? 'Нет данных')),
              ],
            ),
            ExpansionTile(
              title: Text("Характеристики"),
              children: [
                ListTile(
                  title: Text(drugData?['influence'] ?? 'Нет данных'),
                ),
                ListTile(
                  title: Text("ATX код: ${drugData?['atx_code'] ?? 'Нет данных'}"),
                ),
              ],
            ),
            ExpansionTile(
              title: Text("Инструкция"),
              children: [
                ListTile(
                  title: Text(drugData?['dosage'] ?? 'Нет данных'),
                ),
                ListTile(
                  title: Text("Показания: ${drugData?['indication'] ?? 'Нет данных'}"),
                ),
                ListTile(
                  title: Text("Побочные эффекты: ${drugData?['side_effects'] ?? 'Нет данных'}"),
                ),
              ],
            ),
            ExpansionTile(
              title: Text("Активные вещества"),
              children: [
                for (var ingredient in drugData?['active_ingredients'] ?? [])
                  ListTile(
                    title: Text("${ingredient['name']}, дозировка: ${ingredient['dosage']}"),
                  ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}