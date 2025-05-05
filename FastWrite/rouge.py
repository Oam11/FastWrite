from rouge_metric import PyRouge

# Load summary results
#hypotheses = [
#    'how are you\ni am fine',  # document 1: hypothesis
#    'it is fine today\nwe won the football game',  # document 2: hypothesis
#]
#references = [[
#    'how do you do\nfine thanks',  # document 1: reference 1
#    'how old are you\ni am three',  # document 1: reference 2
#], [
 #   'it is sunny today\nlet us go for a walk',  # document 2: reference 1
 #   'it is a terrible day\nwe lost the game',  # document 2: reference 2
#]]

# Evaluate document-wise ROUGE scores


def calculate_rouge(candidate_doc: str, reference_doc: str) -> float:
    
    rouge = PyRouge(rouge_n=(1, 2), rouge_l=True, rouge_w=False, rouge_s=False, rouge_su=False)
    
    
    score = rouge.evaluate(candidate_doc, reference_doc)
    
    rouge1_f = score["rouge-1"]['f']
    return rouge1_f #done are there circumstances where people would need the entire dictionary tho ? not really but im gona maybe add it, or do you wanna make this part custom