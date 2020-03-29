import os
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
from datetime import datetime
from google.cloud import videointelligence

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

paragraph = "In an attempt to build an AI-ready workforce, Microsoft announced Intelligent Cloud Hub which has been launched to empower the next generation of students with AI-ready skills. Envisioned as a three-year collaborative program, Intelligent Cloud Hub will support around 100 institutions with AI infrastructure, course content and curriculum, developer support, development tools and give students access to cloud and AI services. As part of the program, the Redmond giant which wants to expand its reach and is planning to build a strong developer ecosystem in India with the program will set up the core AI infrastructure and IoT Hub for the selected campuses. The company will provide AI development tools and Azure AI services such as Microsoft Cognitive Services, Bot Services and Azure Machine Learning.According to Manish Prakash, Country General Manager-PS, Health and Education, Microsoft India, said, With AI being the defining technology of our time, it is transforming lives and industry and the jobs of tomorrow will require a different skillset. This will require more collaborations and training and working with AI. That’s why it has become more critical than ever for educational institutions to integrate new cloud and AI technologies. The program is an attempt to ramp up the institutional set-up and build capabilities among the educators to educate the workforce of tomorrow. The program aims to build up the cognitive skills and in-depth understanding of developing intelligent cloud connected solutions for applications across industry. Earlier in April this year, the company announced Microsoft Professional Program In AI as a learning track open to the public. The program was developed to provide job ready skills to programmers who wanted to hone their skills in AI and data science with a series of online courses which featured hands-on labs and expert instructors as well. This program also included developer-focused AI school that provided a bunch of assets to help build AI skills. "
print("\nParagraph: \n" + paragraph + "\n")

# user journey -> submit url -> download video from url -> transcribe video -> use text rank to build summary

def transcribe_video(url):
    startTime = datetime.now()
    """Transcribe speech from a video stored on GCS."""
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.SPEECH_TRANSCRIPTION]

    config = videointelligence.types.SpeechTranscriptionConfig(
        language_code="en-US", enable_automatic_punctuation=True
    )
    video_context = videointelligence.types.VideoContext(
        speech_transcription_config=config
    )

    operation = video_client.annotate_video(
        "gs://videos12491/health_officials.mp4", features=features, video_context=video_context
    )

    print("\nProcessing video for speech transcription.")

    result = operation.result(timeout=600)

    # There is only one annotation_result since only
    # one video is processed.
    annotation_results = result.annotation_results[0]
    wallOfText = ""
    for speech_transcription in annotation_results.speech_transcriptions:
        # print(speech_transcription)

        # The number of alternatives for each transcription is limited by
        # SpeechTranscriptionConfig.max_alternatives.
        # Each alternative is a different possible transcription
        # and has its own confidence score.
        for alternative in speech_transcription.alternatives:
            wallOfText += alternative.transcript
            # print("Alternative level information:")

            # print("Transcript: {}".format(alternative.transcript))
            # print("Confidence: {}\n".format(alternative.confidence))

            # print("Word level information:")
            # for word_info in alternative.words:
            #     word = word_info.word
            #     start_time = word_info.start_time
            #     end_time = word_info.end_time
            #     print(
            #         "\t{}s - {}s: {}".format(
            #             start_time.seconds + start_time.nanos * 1e-9,
            #             end_time.seconds + end_time.nanos * 1e-9,
            #             word,
            #         )
            #     )
    print(wallOfText)
    # print(f"""Execution Time: {datetime.now() - startTime}""")

'''
paragraph = f.read()
'''

def transcribe_get_all(url):
    startTime = datetime.now()
    """Transcribe speech from a video stored on GCS."""
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.SPEECH_TRANSCRIPTION]

    config = videointelligence.types.SpeechTranscriptionConfig(
        language_code="en-US", enable_automatic_punctuation=True
    )
    video_context = videointelligence.types.VideoContext(
        speech_transcription_config=config
    )

    operation = video_client.annotate_video(
        "gs://videos12491/trimmed.mp4", features=features, video_context=video_context
    )

    print("\nProcessing video for speech transcription.")

    result = operation.result(timeout=600)

    # There is only one annotation_result since only
    # one video is processed.
    annotation_results = result.annotation_results[0]
    for speech_transcription in annotation_results.speech_transcriptions:
        # print(speech_transcription)

        # The number of alternatives for each transcription is limited by
        # SpeechTranscriptionConfig.max_alternatives.
        # Each alternative is a different possible transcription
        # and has its own confidence score.
        for alternative in speech_transcription.alternatives:
            print("Alternative level information:")

            print("Transcript: {}".format(alternative.transcript))
            print("Confidence: {}\n".format(alternative.confidence))

            print("Word level information:")
            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time
                end_time = word_info.end_time
                print(
                    "\t{}s - {}s: {}".format(
                        start_time.seconds + start_time.nanos * 1e-9,
                        end_time.seconds + end_time.nanos * 1e-9,
                        word,
                    )
                )
    # print(f"""Execution Time: {datetime.now() - startTime}""")

def split_text_into_sentences():
    sentences = paragraph.split(".")
    return text_preprocessing(sentences)

def text_preprocessing(sentences):
    clean_sentences = []
    for sentence in sentences:
        clean_sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    clean_sentences.pop() # getting rid of the empty list at the end

    return clean_sentences

def compare_sentences(sentence1, sentence2):
    # make a list of all the unique words between the two sentences
    # make a vector holds how each word has a specific entity in the list
    # from the vector, use cosine_distance to find how different these vectors are

    sentence1 = [sentence.lower() for sentence in sentence1]
    sentence2 = [sentence.lower() for sentence in sentence2]

    all_unique_words = list(set(sentence1+sentence2)) # get a list of all unique words

    vector1 = [0]*len(all_unique_words)
    vector2 = [0]*len(all_unique_words)

    for i in sentence1: # each time there is a non-stop word, count its occurence
        if i in stop_words: # skip if it is a stopword
            continue
        vector1[all_unique_words.index(i)] += 1

    for i in sentence2:
        if i in stop_words: # skip if it is a stopword
            continue
        vector2[all_unique_words.index(i)] += 1

    # https://kite.com/python/docs/nltk.cluster.cosine_distance
    # cosine similarity is a mathematical term used to compute the angle between two documents where each word is on it's own dimension
    # cosine distance is 1-cosine_similarity, below we are calculating cosine similarity
    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences):
    # go through and a build a matrix that is sentences.length by sentences.length
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    
    for counter1, sentence1 in enumerate(sentences):
        for counter2, sentence2 in enumerate(sentences):
            if sentence1 == sentence2:
                continue
            similarity_matrix[counter1][counter2] = compare_sentences(sentence1, sentence2)
    
    return similarity_matrix

def generate_summary():
    # generate the sentences from the existing paragraph
    sentences = split_text_into_sentences()

    # generate a similarity matrix
    similarity_matrix = build_similarity_matrix(sentences)

    # rank the sentences in the similarity matrix
    sentence_similarity_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)

    # organize the scores from top to bottom
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
    #print("Indexes of top ranked_sentence order are ", ranked_sentence)     

    summarize_text = []

    for i in range(5):
      summarize_text.append(" ".join(ranked_sentence[i][1]))

    # Step 5 - Offcourse, output the summarize text
    summary = ". ".join(summarize_text)+"."
    print("Summarize Text: \n", summary)
    return summary

if __name__ == "__main__":
    url = ""
    transcribe_get_all(url)
    # generate_summary()
    # print("Paragraph summarized: " + paragraph)