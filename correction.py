class correction:
    def __init__(self, candidate_correction, correct_letter, error_letter, x_given_w, x_given_word, prob_word,
                 final_val,error_type,error_position):
        self.candidate_correction = candidate_correction
        self.correct_letter = correct_letter
        self.error_letter = error_letter
        self.x_given_w = x_given_w
        self.x_given_word = x_given_word
        self.prob_word = prob_word
        self.final_val = final_val
        self.error_type = error_type
        self.error_position = error_position