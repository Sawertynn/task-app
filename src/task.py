class Task:
    def __init__(self, text):
        self.text = text
        self.is_finished = False
    
    def __str__(self):
        mark = 'X' if self.is_finished else ' '
        return f'[{mark}] {self.text}'
    
    def finish(self):
        self.is_finished = True