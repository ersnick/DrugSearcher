import 'package:flutter/material.dart';
import 'drugPage.dart';

void main() {
  runApp(const MyApp());
}
class MyApp extends StatefulWidget { // Делаем MyApp StatefulWidget
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  ThemeMode _themeMode = ThemeMode.system; // Состояние для themeMode

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      locale: const Locale('ru', 'RU'),
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: const ColorScheme.light(
          brightness:  Brightness.light,
          primary: Color(0xff33568A),
          // secondary: Color(0xff6200EE),
        ),
      ),
      darkTheme: ThemeData(
        useMaterial3: true,
        colorScheme: const ColorScheme.dark(
          brightness:  Brightness.dark,
          primary: Color(0xff33568A),
          // secondary: Color(0xff6200EE),
        ),
      ),
      themeMode: _themeMode, // Используем _themeMode
      //home: MedicinePage(medicineName: 'Парацетамол'),
      home: MyHomePage(onThemeChange: _changeTheme), // Передаем функцию изменения темы
    );
  }

  void _changeTheme(ThemeMode newThemeMode) {
    setState(() { // Обновляем состояние
      _themeMode = newThemeMode;
    });
  }
}

class MyHomePage extends StatelessWidget {
  final Function(ThemeMode) onThemeChange; // Функция изменения темы

  const MyHomePage({super.key, required this.onThemeChange});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: const Text('ЧЕ ЗЫРИШЬ'),
        backgroundColor: Theme.of(context).colorScheme.primary,
        actions: [
          ThemeButton(onThemeChange: onThemeChange), // Передаем функцию изменения темы
        ],
      ),
      body: const App(),
      drawer: const MyDrawer(),
    );
  }
}

class ThemeButton extends StatefulWidget {
  final Function(ThemeMode) onThemeChange; // Функция изменения темы

  const ThemeButton({super.key, required this.onThemeChange});

  @override
  State<ThemeButton> createState() => _ThemeButtonState();
}

class _ThemeButtonState extends State<ThemeButton> {
  bool isDark = false; // Переменная для отслеживания режима

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: 'Change brightness mode',
      child: IconButton(
        onPressed: () {
          setState(() {
            isDark = !isDark;
            widget.onThemeChange(isDark ? ThemeMode.dark : ThemeMode.light); // Изменяем themeMode в MyApp
          });
        },
        icon: Icon(
          isDark ? Icons.light_mode : Icons.dark_mode,
        ),
      ),
    );
  }
}

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return const Padding(
      padding: const EdgeInsets.all(8.0),
      child: SearchBarDrug(),
    );
  }
}


class MyDrawer extends StatelessWidget {
  const MyDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        children: <Widget>[
          DrawerHeader(
            margin: EdgeInsets.zero,
            padding: EdgeInsets.zero,
            child: UserAccountsDrawerHeader (
              decoration: BoxDecoration(color: Theme.of(context).colorScheme.primary),
              accountName: const Text('Кися'),
              accountEmail: const Text("home@dartflutter.ru"),
              currentAccountPicture: Container(
                  decoration: const BoxDecoration(
                      shape: BoxShape.circle,
                      image : DecorationImage(
                        image: AssetImage('assets/images/avataaar.jpg'),
                        fit: BoxFit.fill,
                      )
                  )
              ),
            ),
          ),
          ListTile(
              title: const Text("О себе"),
              leading: const Icon(Icons.account_box),
              onTap: (){}
          ),
          ListTile(
              title: const Text("Настройки"),
              leading: const Icon(Icons.settings),
              onTap: (){}
          )
        ],
      ),
    );
  }
}

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

          },
          leading: const Icon(Icons.search),


        );
      },
      viewOnSubmitted : (_searchQuery) {
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

