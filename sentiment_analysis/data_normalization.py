import re


def read_line_from_file(file_name):
    with open(file_name) as f:
        for line in f:
            yield line.lower()

def replace_pattern(generator, regex, s):
    for string in generator:
        Id, Class, source, tweet = string.split(',', 3)
        tweet = re.sub(regex, s, tweet)
        yield ','.join((Id, Class, source, tweet))

def replace(generator, pattern, s):
    for string in generator:
        yield string.replace(pattern, s)

def remove_punctuation(generator, punc_list):
    for string in generator:
        for punct in punc_list:
            string = string.replace(punct, "")
        yield string

def remove_comma(generator):
    #removes sentmentsource column too
    for string in generator:
        Id, Class, source, tweet = string.split(',', 3)
        tweet = tweet.replace(',', '')
        yield ','.join((Id, Class, tweet))


if __name__ == '__main__':
    file_generator = read_line_from_file('sentiment_analysis_dataset.csv')
    replace_urls = replace_pattern(file_generator, r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", "")
    replace_mentions = replace_pattern(replace_urls, r"\S*@(?:\[[^\]]+\]|\S+)", "")
    remove_hash = replace(replace_mentions, "#", "")
    remove_punct = remove_punctuation(remove_hash, ['!', '.', '?', ':', ';', '=', '(', ')', '[', ']', '`', '|', '-', '*', '"', '/', '\\', '_'])
    generator = remove_comma(remove_punct)
    with open('normalized_sentiment_analisys_dataset.csv', 'w') as f:
        for line in generator:
            f.write(line)
    print "Done!"
