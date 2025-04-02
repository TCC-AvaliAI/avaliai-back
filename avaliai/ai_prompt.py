class AIPrompt:
    def __init__(self, type: str, description: str, discipline: str, theme: str, difficulty: str):
        self.ai_prompt = f"""
        Crie uma {type} com as seguintes informações:
        Breve descrição da prova {description}.
        A matéria é {discipline}.
        O tema da prova é {theme}.
        A dificuldade da prova é {difficulty}.
        Para as questões de múltipla escolha, forneça as respostas em posições aleatórias. no array de opções."""
    def __str__(self):
        return self.ai_prompt