class Top_Score():
    def __init__(self, pos, score_input, font, color):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.color = color
        self.score_input = score_input
        self.text = self.font.render(self.score_input, True, self.color)
        self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.text, self.rect)
