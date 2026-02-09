import graphviz
import os
from config import OUTPUTS_DIR

def create_mind_map(edges: list, file_name: str) -> str:
    """
    Создает картинку графа и возвращает путь к ней.
    edges: [['Понятие А', 'Понятие Б'], ...]
    """
    dot = graphviz.Digraph(comment='Mind Map', format='png')
    dot.attr(rankdir='LR') # Слева направо
    
    # Настройка узлов (красивые коробочки)
    dot.attr('node', shape='box', style='filled', fillcolor='lightblue', fontname='Arial')

    for start, end in edges:
        dot.edge(str(start), str(end))

    output_path = os.path.join(OUTPUTS_DIR, f"map_{file_name}")
    
    try:
        # render создает файл map_file_name.png
        file_path = dot.render(output_path, cleanup=True)
        return file_path
    except Exception as e:
        print(f"Ошибка Graphviz: {e}")
        return None