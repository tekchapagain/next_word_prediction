class Message:
    def __init__(self, query, content):
        self.query = query
        self.content = content

class Predict:
    def __init__(self, predictedword):
        self.predictedword = predictedword