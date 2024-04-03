import requests
import tiktoken

tokens_per_word=1.5
token_margin=10

debug = True

def count_tokens_tiktoken(input_string, encoding_name="cl100k_base"):
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(input_string))
    return num_tokens

def count_tokens_ooba(input_string, api_port=5000):
    # For local streaming, the websockets are hosted without ssl - http://
    #
    # Not currently working--not sure this is actually implemented, or maybe internals aren't accessible
    #
    HOST = 'localhost:'+str(api_port)
    URI = f'http://{HOST}/v1/internal/token_count'
    request = {'text':input_string}
    response = requests.post(URI, json=request)
    if response.status_code == 200:
        result = response.json()['length'][0]
        return result
    else:
        print(response.status_code)


def token_length(input_string):
    words = input_string.split()  # Splits the string into a list of words
    tlength=int(tokens_per_word * len(words))   # Approximates token count from word count
    return tlength

def whitespace_positions(input_string):
    return [index for index, char in enumerate(input_string) if char.isspace()]


def token_split(input_string, tokens): # Splits input string into two pieces; the later part of the string has less than "tokens" tokens and is split on a token boudary.  Returns rightmost, leftmost strings
    token_boundaries=whitespace_positions(input_string) # These are word boundaries, not token boundaries, but acceptable approximation
    words = int (tokens / tokens_per_word)
    right_string=''
    left_string=''
    if len(token_boundaries)<words:
        right_string=input_string
        left_string=''
    else:
        split_index=token_boundaries[-words]
        right_string=input_string[split_index:]
        left_string=input_string[:split_index]
    return right_string, left_string

def token_crop(input_string, tokens): # Returns the portion of the input string that fits in token count
    words = input_string.split()  # Splits the string into a list of words to ensure we split on a word boundary
    tcrop=''
    if (tokens_per_word * len(words)) < tokens:
        tcrop=input_string
    else:
        tcrop=' '.join(words[-int(tokens / tokens_per_word):])
    tcrop, t_cropped = token_split(input_string, tokens)
    return tcrop

def token_cropped(input_string, tokens): # Returns the portion of the input string that does not fit in token count
    words = input_string.split()  # Splits the string into a list of words
    t_cropped=''
    if (tokens_per_word * len( words )) < tokens:
        t_cropped=''
    else:
        tcropped=' '.join(words[: - int( tokens / tokens_per_word )])
    tcrop, t_cropped = token_split(input_string, tokens)
    return t_cropped


def script_length(context="A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.\n\n",user="USER:",bot="ASSISTANT:"):
    buffer = token_margin # Account for newlines that have to get added, etc
    context_length = token_length(context) + token_length(user) + token_length(bot) + buffer
    return context_length


def search_backwards(input_string, string_1, string_2):
    index_1 = input_string.rfind(string_1)
    index_2 = input_string.rfind(string_2)

    if index_1 == -1 and index_2 == -1:
        return ""
    elif index_1 > index_2:
        return string_1
    else:
        return string_2


def formulate_query(history, prompt, context_size=4096, context="A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.\n\n",user="USER: ",bot="ASSISTANT: "):
#
#   Returns a query string that contains as much of the prompt and history as is possible.
#   Query string does not include context, but DOES account for it to be added
#   (This is because for history-keeping it generally makes sense to hold the context out separately)
#   Note that this will stuff the context to the gills with history if there's space, leaving no room for new tokens to generate.  
#   Make sure the "context_size" you pass makes sense with reserve for token generation.
#
    raw_history_string = ''.join(history)
    history_string = raw_history_string
    header_length = script_length(context, user, bot)
    if header_length + token_length(prompt) > context_size:
        if header_length > context_size:
            prompt=''
            raise ValueError("** CONTEXT HEADER TOO LARGE FOR CONTEXT SIZE**")
        else:
            # Crop the prompt (but not the context!)
            prompt = token_crop(prompt, context_size - header_length)
    if header_length + token_length(prompt) < context_size:
        # There is room for history
        history_toadd = token_crop(history_string, context_size - header_length - token_length(prompt))
        # The best thing to do here is to recognize if you've cropped the user or assistant header in the history, and then put it back at the beginning.
        history_cropped_string = token_cropped(history_string, context_size - header_length - token_length(prompt))
        missing_header = search_backwards(history_cropped_string, user, bot)
        history_string = missing_header + history_toadd
    else:
        history_string=''
    query_string = history_string + user + prompt + "\n" + bot
    #   The Yi models are very sensitive to the \n.  Will need \n to be part of the bot string, generically
    #   query_string = history_string + user + prompt + bot
    #
    # Query_string does NOT include context, but DOES ensure there's room to add it
    return query_string


def formulate_query_and_call(history, prompt, context_size=4096, context="A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.\n\n",user="USER:",bot="ASSISTANT:", api_port = 5000):
#
#   Formulates a query that fits in the context length, adds the system message ("context"), then calls the model.
#
#   If you directly use formulate_query note that it won't add the system message!
#
#   Reserve at least 25% of context, or 200 tokens, whichever is larger
#
    minimum_tokens=200
    generation_reserve=max(minimum_tokens, int(0.25*context_size))
    query_string=formulate_query(history, prompt, context_size-generation_reserve, context, user, bot)
    call_prompt = context + "\n" + query_string
    response = llm_ooba(call_prompt, context_size, api_port=api_port)
    return response

def llm_ooba(prompt, context_size=None, preset='Divine Intellect', repetition_penalty=1.17, temperature = 1.31, top_p = 0.14, api_port=5000, guidance_scale = 1, negative_prompt = ""):

    if (debug):
        print("Ooba prompt:" + prompt)

    # For local streaming, the websockets are hosted without ssl - http://
    HOST = 'localhost:'+str(api_port)
    URI = f'http://{HOST}/v1/completions'

    # For reverse-proxied streaming, the remote will likely host with ssl - https://
    # URI = 'https://your-uri-here.trycloudflare.com/api/v1/generate'

    if context_size==None:
        context_max=4096
    else:
        context_max=context_size

    max_new_tokens=context_max-token_length(prompt)
    if (debug):
        print(max_new_tokens)

    request = {
        'prompt': prompt,
        'max_tokens': max_new_tokens,
        'auto_max_new_tokens': False,
        'max_tokens_second': 0,
        # Generation params. If 'preset' is set to different than 'None', the values
        # in presets/preset-name.yaml are used instead of the individual numbers.
        'preset': preset,
        'do_sample': True,
        'temperature': temperature,
        'top_p': top_p,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': repetition_penalty,
        'repetition_penalty_range': 0,
        'top_k': 49,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,
        'grammar_string': '',
        'guidance_scale': 1,
        'negative_prompt': '',
        'seed': -1,
        'add_bos_token': True,
        'truncation_length': context_max,
        'ban_eos_token': False,
        'custom_token_bans': '',
        'skip_special_tokens': True,
        'stop': ["</s>"]
    }

    response = requests.post(URI, json=request)

    if (debug):
        print(response)

    if response.status_code == 200:
        result = response.json()['choices'][0]['text']
        return result
    else:
        print(response.status_code)
