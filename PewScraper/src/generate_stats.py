import pandas as pd
import nltk
import matplotlib.pyplot as plt


# Uncomment for first time running
nltk.download('punkt')


def get_stats(base_dir, has_data=True):
	meta_df = pd.read_csv("../final_out/" + base_dir + "metadata.csv")
	output_str = ""


	def print_to_str(*args):
		nonlocal output_str
		output_str += " ".join([str(i) for i in args]) + "\n"


	# General
	num_charts = len(meta_df)
	titles = meta_df.pop('title')
	title_count = titles.notnull().sum()

	print_to_str("Total charts:", num_charts)
	print_to_str("Total charts with titles:", title_count)
	print_to_str()


	# Chart Types
	chart_types = meta_df.pop('chartType')
	chart_types_value_counts = chart_types.value_counts()

	print_to_str("=== Chart Type Information ===")
	print_to_str("Number of charts of each chart type")
	for index, value in chart_types_value_counts.iteritems():
		print_to_str(f"{index}: {value}")
	print_to_str()

	chart_types.value_counts().plot.pie(figsize=(8, 5), autopct="%.1f%%", fontsize=10, colormap="Set3")
	plt.ylabel("")
	plt.savefig("../final_out/" + base_dir + "chart_type_distribution.png")
	plt.close()


	# Topics
	chart_topics = meta_df.pop('topic')
	chart_topics_value_counts = chart_topics.value_counts()

	print_to_str("=== Topic Information ===")
	print_to_str("Number of charts of each topic")
	for index, value in chart_topics_value_counts.iteritems():
		print_to_str(f"{index}: {value}")
	print_to_str()

	chart_topics.value_counts().plot.pie(figsize=(8, 5), autopct="%.1f%%", fontsize=10, colormap="Set3")
	plt.ylabel("")
	plt.savefig("../final_out/" + base_dir + "topic_distribution.png")
	plt.close()


	# Captions
	captions_text = meta_df.pop('caption')
	captions_text = captions_text[captions_text != ""]

	tokens = captions_text.apply(lambda x: nltk.word_tokenize(x))
	num_tokens = tokens.apply(lambda x: len(x))
	avg_token_count = num_tokens.mean()
	total_num_tokens = sum(num_tokens)
	total_num_types = len(set(tokens.explode()))

	num_chars = captions_text.apply(lambda x: len(x))
	avg_char_count = num_chars.mean()
	total_num_chars = sum(num_chars)

	num_sentences = captions_text.apply(lambda x: len(nltk.sent_tokenize(x)))
	avg_sentence_count = num_sentences.mean()
	total_num_sentences = sum(num_sentences)

	num_paras = captions_text.apply(lambda x: len(x.split("\n")))
	avg_para_count = num_paras[num_paras > 0].mean()
	total_num_paras = sum(num_paras)

	avg_sentence_in_para_count = total_num_sentences / total_num_paras

	print_to_str("=== Token Information ===")
	print_to_str("Number of non-empty captions:", len(captions_text))
	print_to_str("Average token count per summary:", avg_token_count)
	print_to_str("Average character count per summary:", avg_char_count)
	print_to_str("Total character count:", total_num_chars)
	print_to_str("Average sentence count per summary:", avg_sentence_count)
	print_to_str("Total sentence count:", total_num_sentences)
	print_to_str("Average paragraph count per summary:", avg_para_count)
	print_to_str("Total paragraph count:", total_num_paras)
	print_to_str("Average sentence count per paragraph:", avg_sentence_in_para_count)
	print_to_str("Total tokens:", total_num_tokens)
	print_to_str("Total types (unique tokens):", total_num_types)


	if not has_data:
		print_to_str()

		# Data
		data_paths = meta_df.pop('dataPath')
		data_shape = data_paths.apply(lambda x: pd.read_csv(x.replace("out/", "../final_out/"), header=0).shape)
		num_rows = data_shape.apply(lambda x: x[0])
		num_cols = data_shape.apply(lambda x: x[1])
		avg_row_count = num_rows.mean()
		avg_col_count = num_cols.mean()

		print_to_str("=== Data Shape Information ===")
		print_to_str("Average number of rows:", avg_row_count)
		print_to_str("Average number of columns:", avg_col_count)


	with open("../final_out/" + base_dir + "stats.txt", "w+") as f:
		f.write(output_str)


if __name__ == '__main__':
	for base_dir in ["two_col/", "multi_col/"]:
		get_stats(base_dir)

	get_stats("no_data/", has_data=False)
