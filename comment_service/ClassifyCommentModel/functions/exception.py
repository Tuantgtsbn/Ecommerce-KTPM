from ClassifyCommentModel.functions.model_tfidf import Dict_Tfidf
import joblib
PATH = "ClassifyCommentModel/data/train.crash"

def exist_nhung(text):
	text_list = text.split(" ")
	for i in range(len(text_list)):
		if (text_list[i] == "nhưng" or text_list[i] == "nhung"):
			break
	text_list = text_list[i+1:]
	text_final = [" ".join(text_list)]

	dict_tfidf = Dict_Tfidf(PATH)
	vectorizer = dict_tfidf.create_dict_tfidf()
	vector_tfidf = vectorizer.transform(text_final)
	model= joblib.load('../models/finalmodel.pkl')
	label = model.predict(vector_tfidf)
	if(label[0] == 1):
		print("Day la binh luan tieu cuc!")
	else:
		print("Day la binh luan tich cuc!")

