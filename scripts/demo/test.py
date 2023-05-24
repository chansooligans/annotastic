# %%
from annotastic import config
import openai
import json
import html

secrets = config.setup()
openai.api_key = secrets["openai"]["api_key"]

# %% [markdown]
"""
# open AI
"""

# %%
def get_annotations(passage):

    messages = [
        {"role": "user", "content": f"Passage: {passage}"},
        {
            "role": "user",
            "content": """
            Please provide 20 critiques of the essay, as if you were an editor at NYT or WSJ. 

            Use color to label importance of the text: 'red' for very important, 'orange' for 
            somewhat important, and 'grey' for neutral.
            """,
        },
        {
            "role": "user",
            "content": """
            Return translations in json format.

            example:

            {
                "0":{
                    "text":[text to be critiqued],
                    "output":[critique],
                    "color":"red", "orange", "grey"
                }
            }

            json object:
            """,
        },
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4", 
        # model="gpt-3.5-turbo",
        messages=messages, temperature=0.9, max_tokens=2000
    )

    return response

# %% [markdown]
"""
# HTML
"""

# %%
passage = """
Almost a year has passed since the Bureau of Economic Analysis announced that the U.S. economy had contracted for two quarters in a row. Some people believe, wrongly, that two quarters of falling G.D.P. is the official definition of a recession. Economic negativity ran rampant, especially but not only on the political right.

The interesting question now is why, at least according to some surveys, the public remains very negative on the economy — as negative as it has been in the past amid severe economic downturns — even though those recession calls were clearly a false alarm, and the economy is actually looking remarkably strong. Or maybe the question should be why people say that they’re very negative on the economy.

This is a touchy subject, albeit one I’ve commented on before. You don’t want to say that Americans are stupid; you certainly don’t want to sound like that John McCain adviser who insisted that America was a “nation of whiners” who were experiencing only a “mental recession.”

On the other hand, there are now huge gaps between what people say about the economy and both what the data says and what they say about their own experience. And we have some new information on what lies behind these gaps.

First, about that much-hyped “Biden recession.” The actual definition of a recession involves several economic indicators, and aside from those G.D.P. numbers, nothing that has happened to the economy looks remotely like a recession.

Since December 2021 the U.S. economy has added almost six million jobs while the unemployment rate has fallen from 3.9 percent to 3.4 percent, a level not seen since the 1960s. And no, unemployment isn’t low because Americans have dropped out of the labor force: The percentage of adults either working or looking for a job has declined, but that’s almost entirely a result of an aging population, and labor force participation is right back in line with prepandemic projections.

And these are good jobs, according to workers themselves. According to the Conference Board, which has been surveying job satisfaction since 1987, “U.S. workers have never been more content.”

To be sure, the return of serious inflation after decades of quiescence rattled everyone, and not just because it reduced real incomes. (Real wages fell during Ronald Reagan’s second term, but people felt pretty good about the economy anyway.) One benefit of low inflation is that it gives people one less thing to worry about; according to the American Psychological Association, inflation was a major source of stress during 2022.

But inflation, while still elevated, has come way down. The inflation rate over the past six months was 3.3 percent, compared with 9.6 percent last June. The price of gasoline, a major political talking point last year, is now more or less normal compared with average earnings.

And people have noticed. In October, 20 percent of Americans named inflation as the most important problem facing the nation; that’s now down to 9 percent.

So what’s going on? The general rule seems to be that Americans are feeling good about their personal situation but believe that bad things are happening to other people. A Federal Reserve study found that in late 2021 a record-high percentage of Americans were positive about their own finances while a record low were positive about the economy. We don’t have results for 2022 yet, but my guess is that they’ll look similar.

Partisanship surely explains much of this divergence. A newly published study shows that who holds the White House has huge effects on views of the economy; this is true for supporters of both parties, although the effect appears to be about twice as strong for Republicans. The study also finds, however, that these changes in reported views don’t appear to have any effect on actual spending — that they reflect “cheerleading,” as opposed to “actual expectations.”

Beyond that, there’s good reason to believe that media reports about the economy have had a strongly negative bias. One thing that has gone really, really right in America lately is job creation, yet the public consistently reports having heard more negative than positive news about employment.

And let’s not let economists off the hook. As Mark Zandi of Moody’s Analytics points out, many economists have been predicting recession month after month for the past year. Sooner or later, a recession will no doubt happen, but as he says, “In my 30-plus years as a professional economist, I’ve never seen such recession pessimism,” even as the economy has remained resilient. And this pessimism has surely filtered through to the public.

So where does all this leave us? America hasn’t yet brought inflation back to prepandemic levels, and we may yet have an economic hard landing. But so far, at least, we’ve had a stunningly successful recovery from the Covid shock.

While many Americans tell surveys that things are terrible — which says something about how people respond to surveys and where they get their information — this doesn’t contradict that positive assessment.
"""

passage = passage.replace("’","'")
passage = passage.replace("  "," ")

# %%
response = get_annotations(passage)
revisions = json.loads(response["choices"][0]["message"]["content"])
print("gpt4 cost: ",.001 * (response["usage"]["prompt_tokens"] * .03 + response["usage"]["completion_tokens"] * .06)) 
print("gpt3.5 cost: ",.001 * 0.002 * response["usage"]["total_tokens"]) 


# %% [markdown]
"""
# analyze
"""

# %%
def apply_revision(passage, revision, i):
    revision_id = f'revision{i}'
    revision['text'] = revision['text'].strip(',.')
    revised_text = html.escape(revision['text'])
    revised_text = f'<span id="{revision_id}" class="tooltip">{revised_text}</span>'
    
    return passage.replace(revision['text'], revised_text, 1)

def get_notation_type(text):
    ntk = len(text.split(" "))
    if ntk > 30:
        return "box"
    elif ntk > 5:
        return "bracket"
    elif ntk > 1:
        return "underline"
    else:
        return "circle"


def get_rough_notation(passage, revisions):
    base_js = """
    import {{ annotate, annotationGroup }} from 'https://unpkg.com/rough-notation?module';

    {elements}

    {annotations}

    const animation = annotationGroup([{annotation_names}]);
    animation.show();
    """

    elements = []
    annotations = []
    annotation_names = []

    # Loop through the JSON data and create JavaScript lines for each item
    for i, item in revisions.items():
        if f"revision{i}" in passage:
            elements.append(f"const e{i} = document.querySelector('span#revision{i}');")
            annotations.append(f"const a{i} = annotate(e{i}, {{ type: '{get_notation_type(item['text'])}', color: '{item['color']}' }});")
            annotation_names.append(f"a{i}")

    # Format the base JavaScript with the created lines
    js_code = base_js.format(
        elements='\n'.join(elements),
        annotations='\n'.join(annotations),
        annotation_names=', '.join(annotation_names),
    )

    # with open('script.js', 'w') as f:
    #     f.write(js_code)

    return js_code

def get_tippy(revisions):
    # Define the base JavaScript structure
    base_js = """
    document.addEventListener('DOMContentLoaded', (event) => {{
        tippy('.tooltip', {{
            content(reference) {{
                const id = reference.id;
                switch (id) {{{switch_cases}}}
                
            }}
        }});
    }});
    """

    # Loop through the JSON data and create JavaScript lines for each item
    switch_cases = []
    for i, item in revisions.items():
        output = item['output'].replace("'", "\\'")
        switch_cases.append(f"""case 'revision{i}':\n    return '{output}';""")

    # Format the base JavaScript with the created lines
    js_code = base_js.format(
        switch_cases='\n'.join(switch_cases)
    )

    # with open('tippy.js', 'w') as f:
    #     f.write(js_code)

    return js_code

# %%
for i, revision in enumerate(revisions.values()):
    passage = apply_revision(passage, revision, i)

# %%
with open('revised_passage.html', 'w') as f:
    passage = passage.replace('\n', '<br>')
    f.write(f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <link rel="stylesheet" href="styles.css">
            <script type="module" src="https://unpkg.com/rough-notation?module"></script>
            
            <!-- Development -->
            <script src="https://unpkg.com/@popperjs/core@2/dist/umd/popper.min.js"></script>
            <script src="https://unpkg.com/tippy.js@6/dist/tippy-bundle.umd.js"></script>
            <!-- Production -->
            <!-- <script src="https://unpkg.com/@popperjs/core@2"></script>
            <script src="https://unpkg.com/tippy.js@6"></script> -->
        </head>
        <body>
        <div>
        <h1>Sample Document</h1>
        <br><br>
        {passage}
        <br><br>
        </div>
        </body>
        <script type="module">
        {get_rough_notation(revisions=revisions, passage=passage)}
        </script>
        <script>
        {get_tippy(revisions=revisions)}
        </script>
        </html>
    ''')

# %%
