import os
def app_path(path):
    bundle_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(bundle_dir, path)

class Score:

    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.bronze_medal = 0
        self.silver_medal = 0
        self.gold_medal = 0
        self.diamond_medal = 0

        self.filename = 'data/scores.txt'

        with open(self.filename, "r") as f:
            lines = f.readlines()
            self.high_score = int(lines[0].rstrip('\n'))
            self.bronze_medal = int(lines[1].rstrip('\n'))
            self.silver_medal = int(lines[2].rstrip('\n'))
            self.gold_medal = int(lines[3].rstrip('\n'))
            self.diamond_medal = int(lines[4].rstrip('\n'))

    def scored(self):
        self.score += 1

    def reset(self):
        self.score = 0
    
    def end(self):
        self.high_score = max(self.score, self.high_score)

        if self.score >= 40:
            self.diamond_medal += 1
        elif self.score >= 30:
            self.gold_medal += 1
        elif self.score >= 20:
            self.silver_medal += 1
        elif self.score >= 10:
            self.bronze_medal += 1

        with open(self.filename, 'w') as f:
            f.write("%s\n" % self.high_score)
            f.write("%s\n" % self.bronze_medal)
            f.write("%s\n" % self.silver_medal)
            f.write("%s\n" % self.gold_medal)
            f.write("%s\n" % self.diamond_medal)