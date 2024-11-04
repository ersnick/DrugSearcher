import 'package:flutter/material.dart';
import 'drug_page.dart';

class SearchBarDrug extends StatefulWidget {
  const SearchBarDrug({super.key});

  @override
  State<SearchBarDrug> createState() => _SearchBarDrugState();
}

class _SearchBarDrugState extends State<SearchBarDrug> {
  String _searchQuery = ''; // Переменная для хранения текста

  @override
  Widget build(BuildContext context) {
    return SearchAnchor(
      builder: (BuildContext context, SearchController controller) {
        return SearchBar(
          backgroundColor: WidgetStateProperty.all<Color>(
              Theme.of(context).colorScheme.primary),
          controller: controller,
          padding: const WidgetStatePropertyAll<EdgeInsets>(
              EdgeInsets.symmetric(horizontal: 16.0)),
          onTap: () {
            controller.openView();
          },
          onChanged: (value) {
            setState(() {
              _searchQuery = value; // Обновляем значение при изменении текста
            });
            controller.openView();
          },

          onSubmitted: (_){
            controller.closeView(_searchQuery); // Закрываем представление поиска
            // // Отправляем запрос

            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => DrugPage(medicineName: _searchQuery),
              ),
            );
          },
          leading: const Icon(Icons.search),


        );
      },
      viewOnSubmitted : (_searchQuery) {
        //await getDrugInfo(_searchQuery);
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => DrugPage(medicineName: _searchQuery),
          ),
        );
      },
      suggestionsBuilder: (BuildContext context, SearchController controller) {
        return List<ListTile>.generate(5, (int index) {
          final String item = 'Лекарство ${index + 1}';
          return ListTile(
            title: Text(item),
            onTap: () {
              setState(() {
                controller.closeView(item);
                // Переход на второй экран с передачей названия лекарства
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => DrugPage(medicineName: item),
                  ),
                );
              });
            },
          );
        });
      },

    );
  }
}