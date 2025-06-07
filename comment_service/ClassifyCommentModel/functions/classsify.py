from ClassifyCommentModel.functions.model_tfidf import Dict_Tfidf
import joblib
from ClassifyCommentModel.functions.utils import util
import os
from ClassifyCommentModel.functions.exception import exist_nhung
PATH = "ClassifyCommentModel/data/train.crash"

def classify(arrText):
    result = []
    if not os.path.exists(PATH):
        print(f"Lỗi: Tệp {PATH} không tồn tại.")
        exit(1)
    
    dict_tfidf = Dict_Tfidf(PATH)
    vectorizer = dict_tfidf.create_dict_tfidf()
    model = joblib.load('ClassifyCommentModel/models/finalmodel.pkl')
    Util = util()
    for text in arrText:
        if "nhưng" in text or "nhung" in text:
            result.append(exist_nhung(text))  # Assuming `exception.exist_nhung` returns -1
            break
        if "được mỗi" in text or "được cái" in text:
            result.append(-1)
            break
        
        textTrans = [Util.text_util_final(text)]
        vector_tfidf = vectorizer.transform(textTrans)
        label = model.predict(vector_tfidf)
        
        if label[0] == 1:
            result.append(-1)
        else:
            result.append(1)
    
    return result

if __name__ == '__main__':
    sample_texts = ["Sản phẩm xấu", "Sản phẩm tốt"]  # Replace with actual input
    print(classify(sample_texts))