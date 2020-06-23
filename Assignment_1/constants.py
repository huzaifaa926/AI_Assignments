NODES_NAME = {'Arad': 0, 'Mehadia': 1, 'Bucharest': 2, 'Neamt': 3, 'Craiova': 4,
                'Oradea': 5, 'Drobeta': 6, 'Pitesti': 7, 'Eforie': 8, 'Rimnicu_Vilcea': 9,
                'Fagaras': 10, 'Sibiu': 11, 'Giurgiu': 12,'Timisoara': 13, 'Hirsova': 14,
                'Urziceni': 15, 'Iasi': 16, 'Vaslui': 17, 'Lugoj': 18, 'Zerind': 19
            }

GRAPH = {
            'Arad': [('Sibiu', 140), ('Timisoara', 118), ('Zerind', 75)],
            'Mehadia': [('Drobeta', 75), ('Lugoj', 70)],
            'Bucharest': [('Fagaras', 211), ('Giurgiu', 90), ('Pitesti', 101), ('Urziceni', 85)],
            'Neamt': [('Iasi', 87)],
            'Craiova': [('Drobeta', 120), ('Pitesti', 138), ('Rimnicu_Vilcea', 146)],
            'Oradea': [('Sibiu', 151), ('Zerind', 71)],
            'Drobeta': [('Craiova', 120), ('Mehadia', 75)],
            'Pitesti': [('Bucharest', 101), ('Craiova', 138), ('Rimnicu_Vilcea', 97)],
            'Eforie': [('Hirsova', 86)],
            'Rimnicu_Vilcea': [('Craiova', 146), ('Pitesti', 97), ('Sibiu', 80)],
            'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
            'Sibiu': [('Arad', 140), ('Fagaras', 99), ('Oradea', 151), ('Rimnicu_Vilcea', 80)],
            'Giurgiu': [('Bucharest', 90)],
            'Timisoara': [('Arad', 118), ('Lugoj', 111)],
            'Hirsova': [('Eforie', 86), ('Urziceni', 98)],
            'Urziceni': [('Bucharest', 85), ('Hirsova', 98), ('Vaslui', 142)],
            'Iasi': [('Neamt', 87), ('Vaslui', 92)],
            'Vaslui': [('Iasi', 92), ('Urziceni', 142)],
            'Lugoj': [('Mehadia', 70), ('Timisoara', 111)],
            'Zerind': [('Arad', 75), ('Oradea', 71)]
        }
        
HEURISTIC = {
               'Arad': 366, 'Mehadia': 241, 'Bucharest': 0, 'Neamt': 234,
                'Craiova': 160, 'Oradea': 380, 'Drobeta': 242, 'Pitesti': 100,
                'Eforie': 161, 'Rimnicu_Vilcea': 193, 'Fagaras': 176, 'Sibiu': 253, 
                'Giurgiu': 77, 'Timisoara': 329, 'Hirsova': 151,'Urziceni': 80,
                'Iasi': 226, 'Vaslui': 199, 'Lugoj': 244, 'Zerind': 374
            }
