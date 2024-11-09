# Json File Explanation

We develop two GUI tools to conduct data annotation, `GUI1.py` for the failure type annotation, `GUI2.py` for the pairwise model comparision.

## Failure File Description

`failure/failure_prompt_model.json`: key represents the interaction, the value represents the results of human evaluation.

The value before "/" represents the failure type:

"0": **No failure**

"1": **Interactive element missing**

"2": **No interaction**

"3": **Wrong interactive element**

"4": **Wrong type of interactive element**

"5": **Wrong position of interactive element**

"6": **Wrong position after interaction**

"7": **Wrong type of interaction effects**

"8": **Effect on wrong element**

"9": **Partial Implementation**

"10": **Wrong function**


The value after "/" represent the usability:

"0": **Usable**

"1": **Unusable**



## Compare File Description
`compare/compare_prompt_model.json`: key represents the interaction, the value represents the results of pairwise model comparision.

"0" represents win, "1" represents tie, "2" represents lose. The baseline is Gemini-1.5 under the direct prompt.
