
document.addEventListener('DOMContentLoaded', (event) => {
    tippy('.tooltip', {
        content(reference) {
            const id = reference.id;
            switch (id) {case 'revision0':
    return 'Consider rephrasing to sound more objective.';
case 'revision1':
    return 'Specify which surveys are being referred to for better credibility.';
case 'revision2':
    return 'This self-reference seems unnecessary; consider removing it.';
case 'revision3':
    return 'Clarify that this refers to \'some people\' or \'certain individuals\' to avoid generalizations.';
case 'revision4':
    return 'Mention who is using this term to provide context.';
case 'revision5':
    return 'Reword to maintain a formal tone.';
case 'revision6':
    return 'Reword as a paraphrased statement for a more formal presentation.';
case 'revision7':
    return 'Add the unit (%, points, etc.) for clarity.';
case 'revision8':
    return 'Clarify that these percentages refer to Americans naming inflation as the most important problem.';
case 'revision9':
    return 'Update this information if more recent data is available.';
case 'revision10':
    return 'Replace with a more formal term.';
case 'revision11':
    return 'Reword to maintain a formal tone.';
case 'revision12':
    return 'Clarify if Zandi is being quoted directly or if his views are being paraphrased.';
case 'revision13':
    return 'Reword these sentences to maintain a neutral and objective tone.';
case 'revision14':
    return 'Clarify what it \'says\' to make your point clearer.';}
            
        }
    });
});
