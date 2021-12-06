import time
import math
import re
import pandas as pd
from ast import literal_eval
import nltk
from nltk.corpus import stopwords
from string import punctuation

from constants import *


nltk.download('punkt')
nltk.download('stopwords')


# Set to True to evaluate the current cropper parameters
IS_EVALUATION = False

WINDOW_SIZE = 5
STOP_WORDS = set(stopwords.words("english") + ["in", ",", "(", ")", "'", "-", "pew", "research", "center", "%", ":", ".", "’"])


def crop_captions():
	global start_time
	start_time = time.time()

	# Retrieve meta df
	no_data_meta_df = pd.read_csv(NO_DATA_DIR + ("for_evaluation/" if IS_EVALUATION else "") + META_FILTERED_PATH, converters={"columns": literal_eval, "caption": literal_eval})

	# Crop charts
	cropped_caption, paras_with_scores, sentence_with_scores = crop_meta_df(no_data_meta_df, IS_EVALUATION)

	# Format: [(para, relevance_score, proximity, is_confirmed), ...] (only cropped paragraphs)
	no_data_meta_df["croppedCaption"] = cropped_caption
	# Format: [(para, relevance_score, proximity, is_confirmed), ...] (all paragraphs)
	no_data_meta_df["parasWithScores"] = paras_with_scores
	# Format: [(sentence, sentence_score, unknown_data, known_words, known_data), ...]
	no_data_meta_df["sentencesWithScores"] = sentence_with_scores

	# Save df
	no_data_meta_df.to_csv(index=False, path_or_buf=NO_DATA_DIR + ("for_evaluation/" + CROPPED_META_PATH if IS_EVALUATION else CROPPED_META_FILTERED_PATH))

	print("complete", time.time() - start_time)


def crop_meta_df(meta_df, IS_EVALUATION):
	meta_df["title"] = meta_df["title"].astype("str")

	output = meta_df.apply(func=lambda chart: crop_chart(chart, IS_EVALUATION), axis=1)

	cropped_caption = output.apply(func=lambda row: row[0])
	paras_with_scores = output.apply(func=lambda row: row[1])
	sentence_with_scores = output.apply(func=lambda row: row[2])

	return cropped_caption, paras_with_scores, sentence_with_scores


def crop_chart(chart, IS_EVALUATION):
	global start_time
	chart_id = chart["id"]

	if chart_id % 100 == 0:
		print(chart_id, time.time() - start_time)

	# Title tokens
	title = chart["title"]
	title_tokens = remove_stop_words(title) if title is not None else []

	# Data tokens
	data_path = NO_DATA_DIR + "data_for_cropping/" + str(chart_id) + ".txt"

	try:
		with open(data_path, "r") as f:
			data = f.read()
	except:
		data = ""

	lines = data.split("\n")
	data_values = [token for line in lines for token in remove_stop_words(line)]
	data_tokens = []
	number_tokens = set()

	for value in data_values:
		try:
			number_tokens.add(abs(float(value.replace(",", ""))))
		except:
			data_tokens.append(value)

	# Tokens to look for
	tokens_to_look_for = set(title_tokens + data_tokens)

	additional_number_tokens = set()

	for number_token in number_tokens:
		# In case of thousands, millions, K, M scale
		if number_token < 1000:
			additional_number_tokens.add(number_token * 1000)
			additional_number_tokens.add(number_token * 1000000)
		# Thousand
		elif number_token < 1000000:
			additional_number_tokens.add(number_token / 1000)
		# Million
		elif number_token < 1000000000:
			additional_number_tokens.add(number_token / 1000)
			additional_number_tokens.add(number_token / 1000000)
		# Billion
		elif number_token < 1000000000000:
			additional_number_tokens.add(number_token / 1000)
			additional_number_tokens.add(number_token / 1000000)
			additional_number_tokens.add(number_token / 1000000000)

	number_tokens = number_tokens.union(additional_number_tokens)

	# Crop caption
	caption_paras = chart["caption"]

	combined_sentences_with_scores = []
	paras_with_scores = []

	for para, proximity in caption_paras:
		# Window size
		if abs(proximity) > WINDOW_SIZE:
			continue


		# Sentence score
		sentences_with_scores = score_sentences(para, tokens_to_look_for, number_tokens)
		combined_sentences_with_scores.append(sentences_with_scores)

		max_sentence_score = max([score for sentence, score, unknown_data, known_words, known_data in sentences_with_scores])

		# for sentence, score, unknown_data, known_words, known_data in sentences_with_scores:
		# 	 print(sentence)
		# 	 print("Score:", score)
		# 	 if len(unknown_data) != 0:
		# 		 print("Unknown:", unknown_data)
		#
		# 	 if len(known_words + known_data) != 0:
		# 		 print("Known:", known_words + known_data)


		# Relevance score
		proximity_factor = 0.4 * math.exp(-0.1 * (proximity ** 2)) + 0.6
		sentence_factor = 1 / (1 + math.exp(0.3 * (-max_sentence_score + 1.7)))

		relevance_score = proximity_factor * sentence_factor  # 2 / ((1 / proximity_factor) + (1/ sentence_factor))


		# Confirmed paragraphs
		total_unknown_data = sum([len(unknown_data) for sentence, score, unknown_data, known_words, known_data in sentences_with_scores])
		total_known_words = sum([len(known_words) for sentence, score, unknown_data, known_words, known_data in sentences_with_scores])
		total_known_data = sum([len(known_data) for sentence, score, unknown_data, known_words, known_data in sentences_with_scores])

		if total_unknown_data == 0 and total_known_words > 3 and total_known_data > 0 and relevance_score > 0.72 and len(sentences_with_scores) > 1:
			is_confirmed = True
		else:
			is_confirmed = False

		# print(para)
		# print("Proximity Score:", proximity_factor, proximity)
		# print("Sentence Score:", sentence_factor, max_sentence_score)
		# print([score for sentence, score, unknown_data, known_words, known_data in sentences_with_scores])
		# print("✅" if relevance_score > 0.5 else "❌", "Score:", relevance_score)
		# print()

		paras_with_scores.append((para, relevance_score, proximity, is_confirmed))


	# Cropped caption
	cropped_chunk = [i for i in paras_with_scores if i[1] > 0.5]
	cropped_paras = [i[0] for i in cropped_chunk]
	cropped_caption = "\n".join(cropped_paras)

	# Confirmed caption
	confirmed_chunk = [i for i in paras_with_scores if i[3]]
	confirmed_paras = [i[0] for i in confirmed_chunk]
	confirmed_caption = "\n".join(confirmed_paras)

	# Save captions
	if not IS_EVALUATION:
		captionPath = NO_DATA_DIR + CROPPED_CAPTIONS_DIR + str(chart_id) + ".txt"
		with open(captionPath, "w") as f:
			f.write(cropped_caption)

		confirmedPath = NO_DATA_DIR + CONFIRMED_CAPTIONS_DIR + str(chart_id) + ".txt"
		with open(confirmedPath, "w") as f:
			f.write(confirmed_caption)

	return cropped_chunk, paras_with_scores, combined_sentences_with_scores


def score_sentences(para, tokens_to_look_for, number_tokens):
	# Tokenise paragraph
	sentences = nltk.sent_tokenize(para)
	sentences_with_scores = []

	for sentence in sentences:
		unknown_data = []
		known_words = []
		known_data = []

		sentence_tokens = set(remove_stop_words(sentence))
		sentence_score = 0

		# Lexical token matches
		for token in tokens_to_look_for:
			if token in sentence_tokens:
				sentence_score += 0.58
				known_words.append(token)

		
		for token in sentence_tokens:
			if re.fullmatch('\d[,\.\d]*', token) is not None:
				try:
					num = float(token.replace(",", ""))

					# Numerical token matches
					for number_token in number_tokens:
						if abs(num - number_token) < 1:
							# Year numerical tokens
							if 1950 < number_token < 2050:
								pass
							# Non-year numerical tokens
							else:
								sentence_score += 1.4

							known_data.append(num)
							break

					# Numerical token mismatches
					else:
						unknown_data.append(token)
						sentence_score -= 0.5
				except:
					pass

		sentences_with_scores.append((sentence, sentence_score, unknown_data, known_words, known_data))

	return sentences_with_scores


def remove_stop_words(text):
	text = " ".join(text.split("-"))
	text = " ".join(text.split("—"))
	words = [word.lower().strip(punctuation) for word in nltk.word_tokenize(text)]
	return [word for word in words if word not in STOP_WORDS and len(word) != 0]


def run_evaluation():
	cropped_meta_df = pd.read_csv(NO_DATA_DIR + "for_evaluation/" + CROPPED_META_PATH, converters={
		"caption": literal_eval,
		"croppedCaption": literal_eval,
		"parasWithScores": literal_eval
	})
	ground_truth_df = pd.read_csv(NO_DATA_DIR + "for_evaluation/ground_truth.csv").set_index("id")


	output = []

	for _, item in cropped_meta_df.iterrows():
		item_id = item["id"]
		title = item["title"]
		imgPath = item["imgPath"]
		url = item["URL"]
		paras_with_scores = item["parasWithScores"]

		for para, score, proximity, is_confirmed in paras_with_scores:
			is_included = score > 0.5

			output.append({
				"id": item_id,
				"title": title,
				"imgPath": imgPath,
				"url": url,
				"proximity": proximity,
				"score": score,
				"caption": para,
				"is_included": is_included,
				"is_confirmed": is_confirmed,
			})
	
	output_df = pd.DataFrame(output).set_index("id")
	output_df = pd.concat([output_df, ground_truth_df[["is_relevant", "chart_type"]]], axis=1)

	chart_types = ground_truth_df.reset_index()[["id", "chart_type"]].drop_duplicates()["chart_type"].value_counts()

	print("For all images:")
	print(chart_types)
	print("Total no. of images:", sum(chart_types))
	print()
	print("Paragraphs for Annotation:")
	evaluate_df(output_df)
	print()
	print("Confirmed Paragraphs:")
	evaluate_df(output_df, use_confirmed=True)
	print()
	print()
	print("=" * 30)

	print("For only charts:")
	print(chart_types.drop(["table", "photo", "icon", "table,photo"]))
	print("Total no. of charts:", sum(chart_types.drop(["table", "photo", "icon", "table,photo"])))
	print()

	print("Paragraphs for Annotation:")
	evaluate_df(output_df, all_images=False)
	print()

	print("Confirmed Paragraphs:")
	evaluate_df(output_df, all_images=False, use_confirmed=True)


def evaluate_df(evaluate_cropped_captions_df, all_images=True, use_confirmed=False):
	"""
	Args:
		evaluate_cropped_captions_df (pandas.DataFrame)): DataFrame to evaluate with.
		all_images (bool): Use all images if true. Otherwise, only use chart images.
		use_confirmed (bool): Use only confirmed paragraphs if true. Otherwise, use all cropped paragraphs.
	"""

	tp = 0
	tn = 0
	fp = 0
	fn = 0

	for _, item in evaluate_cropped_captions_df.iterrows():
		prediction = item["is_confirmed" if use_confirmed else "is_included"]
		is_relevant = item["is_relevant"]

		chart_type = item["chart_type"]

		if is_relevant not in [True, False] or (not all_images and chart_type in ["table", "photo", "icon", "table,photo"]):
			continue

		is_true = prediction == is_relevant
		is_positive = prediction

		if (prediction != True and prediction != False):
			print(prediction)

		if (is_relevant != True and is_relevant != False):
			print(is_relevant)

		if is_true:
			if is_positive:
				tp += 1
			else:
				tn += 1
		else:
			if is_positive:
				fp += 1
			else:
				fn += 1

	print("True Positives:", tp)
	print("True Negatives:", tn)
	print("False Positives:", fp)
	print("False Negatives:", fn)
	print()

	# Precision & recall
	recall = tp / (tp + fn)
	precision = tp / (tp + fp)

	print("Recall:", recall)
	print("Precision:", precision)

	# F Score & accuracy
	print("F Score:", 2 / ((1 / recall) + (1 / precision)))
	print("Accuracy:", (tp + tn) / (tp + tn + fp + fn))

	# Objective function (prioritises recall over precision)
	obj_func = recall * 3 + precision
	print("Objective Function:", obj_func)


if __name__ == '__main__':
	crop_captions()

	if IS_EVALUATION:
		print()
		run_evaluation()
